from .BaseController import BaseController
from models.db_schemes import Project
from models.db_schemes import DataChunk
from typing import List
from stores.llm.LLMEnums import DocumentTypeEnum
import json

class NLPController(BaseController):
    def __init__(self,vectordb_client,embedding_client,generation_client,template_parser):
        super().__init__()
        self.vectordb_client = vectordb_client
        self.embedding_client = embedding_client
        self.generation_client = generation_client
        self.template_parser = template_parser
    
    def create_collection_nmae(self,project_id: str):
        return f"collection_{self.vectordb_client.default_vector_size}_{project_id}".strip()
    
    async def reset_vector_db_collection(self,project: Project):
        collection_nmae = self.create_collection_nmae(project_id=project.project_id)
        return await self.vectordb_client.delete_collection(collection_nmae=collection_nmae)
    
    async def get_vector_db_collection_info(self,project: Project):
        collection_name = self.create_collection_nmae(project_id=project.project_id)
        collection_info =  await self.vectordb_client.get_collection_info(collection_name=collection_name)
        return json.loads(
            json.dumps(collection_info,default=lambda x: x.__dict__)
        )
    
    async def insert_into_vector_db(self,project: Project,
                              chunks: List[DataChunk], chunk_ids: List[int], do_reset:bool = False):
        # get collection name
        collection_name = self.create_collection_nmae(project_id=project.project_id)
        
        # get texts, metadatas, vectors
        texts = [chunk.chunk_text for chunk in chunks]
        metadatas = [metadata.chunk_metadata for metadata in chunks]
        vectors = self.embedding_client.embed_text(text=texts,document_type=DocumentTypeEnum.DOCUMENT.value)
        
        #create collection if not exist
        _ = await self.vectordb_client.create_collection(collection_name=collection_name,
                                                   collection_size=self.embedding_client.embedding_size,
                                                   do_reset = do_reset)
        
        # insert data
        _ = await self.vectordb_client.insert_many(collection_name = collection_name,
                                                    texts = texts,
                                                    vectors = vectors,
                                                    metadata= metadatas,
                                                    record_ids= chunk_ids)
        
        return True
    
    async def search_vector_db_collection(self,project:Project,text:str,limit:int = 5):
        
        collection_name = self.create_collection_nmae(project_id=project.project_id)
        query_vector = None
        
        vectors = self.embedding_client.embed_text(
            text=text,document_type=DocumentTypeEnum.QUERY.value
        )
        
        if not vectors or len(vectors) == 0:
            return False
        
        if isinstance(vectors,list) and len(vectors)>0:
            query_vector = vectors[0]
        
        if query_vector == None:
            return False
        
        results = await self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector = query_vector,
            limit = limit
        )
        if not results:
            return False
        
        return results
    
    async def answer_rag_question(self,project:Project,query:str,limit:int = 5):
        
        retreived_documents = await self.search_vector_db_collection(
            project=project,
            text=query,
            limit=limit
        )
        if not retreived_documents or len(retreived_documents) == 0:
            return None
        
        system_prompt = self.template_parser.get("rag","system_prompt")
        
        document_prompt = "\n".join([
            self.template_parser.get("rag","document_prompt",
                                     {"doc_num":idx+1,
                                      "chunk_text":str( self.generation_client.process_text(doc.text))})
            for idx,doc in enumerate(retreived_documents)
        ])
        
        footer_prompt = self.template_parser.get("rag","footer_prompt",{"query":query})
        
        chat_history = [
            self.generation_client.construct_prompt(
                prompt = system_prompt,
                role = self.generation_client.enums.SYSTEM.value
            )
        ]
        
        full_prompt = "\n\n".join(
            [document_prompt,footer_prompt]
        )
        
        answer = self.generation_client.generate_text(
            prompt = full_prompt,
            chat_history = chat_history
        )
        
        return answer,full_prompt,chat_history