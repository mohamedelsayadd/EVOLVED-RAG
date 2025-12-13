from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "file_validate_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    PROCESSING_SUCCESS = "processing_success"
    PROCESSING_FAILED = "processing_failed"
    NO_FILES_ERROR = "not_found_files"
    FILE_ID_ERROR = "no_file_found_with_this_id"
    PROJECT_NOT_FOUND_ERROR = "project not found"
    CHUNKS_NOT_INSERTED_ERROR = "chunk didn't inserted"
    CHUNKS_INSERTED_SUCCESS = "chunks inserted successfully!"
    VECTORDB_COLLECTION_RETRIEVD = "collection retrived successfully"
    VECTORDB_SEARCH_ERROR = "vectordb search error"
    VECTORDB_SEARCH_SUCCESS = "vectordb search success"
    RAG_ANSWER_ERROR = "LLM Can't Generate Answer"
    RAG_ANSWER_SUCCESS = "LLM Generation Success"
