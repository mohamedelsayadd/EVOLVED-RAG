from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import base, data,nlp
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates_folder.template_parser import TempelateParser
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker
from utils.metrics import setup_metrics



@asynccontextmanager
async def lifespan(app:FastAPI):
    
    settings = get_settings()
    
                            #postgresql+asyncpg://username:password@host:port/database
    postgres_connection = f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}"
    app.db_engine = create_async_engine(url=postgres_connection)
    app.db_client = sessionmaker(
        app.db_engine,class_=AsyncSession,expire_on_commit=False
    )
    

    llm_provider_factory = LLMProviderFactory(settings)
    vectordb_provider_factory = VectorDBProviderFactory(settings,db_client=app.db_client)

    # generation client
    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id = settings.GENERATION_MODEL_ID)

    # embedding client
    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,
                                             embedding_size=settings.EMBEDDING_MODEL_SIZE)
    # vectordb client 
    app.vectordb_client = vectordb_provider_factory.create(provider=settings.VECTOR_DB_BACKEND)
    await app.vectordb_client.connect()
    
    app.template_parser = TempelateParser(language=settings.PRIMARY_LANG,default_language=settings.DEFAULT_LANG)
    
    yield 
    await app.db_engine.dispose()
    await app.vectordb_client.disconnect()


app = FastAPI(lifespan=lifespan)
setup_metrics(app=app)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)

