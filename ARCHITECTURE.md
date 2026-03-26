# Architecture & API Documentation

## System Architecture

### Data Flow

```
User Input (YouTube URL)
    ↓
[YouTubeLoader] → Raw Transcript
    ↓
[TextSplitter] → Chunks (500 char, 100 overlap)
    ↓
[OllamaEmbeddings] → Vectors (384 dim)
    ↓
[FAISS VectorStore] → Persisted Index
    ↓
User Question
    ↓
[DocumentRetriever] → Similarity Search (Top-K)
    ↓
[RAG Chain - LCEL]
    ├─ Format Documents
    ├─ Create Prompt  
    ├─ Call ChatOllama
    └─ Parse Output
    ↓
Answer with Sources
```

## Module Reference

### Configuration (`app/config.py`)

Centralized settings management.

**Key Settings**:
- `OLLAMA_BASE_URL`: http://localhost:11434
- `LLM_MODEL`: llama3 or mistral
- `EMBEDDING_MODEL`: nomic-embed-text
- `CHUNK_SIZE`: 500 characters
- `TOP_K`: 3 documents
- `TEMPERATURE`: 0.7

**Usage**:
```python
from app.config import Config
print(Config.LLM_MODEL)
```

### YouTube Loader (`ingestion/youtube_loader.py`)

Fetch YouTube transcripts.

**Methods**:
- `fetch_transcript(url)`: Get raw text
- `fetch_and_clean(url)`: Get cleaned text

### Text Splitter (`ingestion/text_splitter.py`)

Split text into chunks using RecursiveCharacterTextSplitter.

**Separator Strategy**:
1. Double newlines
2. Single newlines  
3. Periods
4. Spaces
5. Characters (fallback)

### Embedding Model (`embeddings/embedding_model.py`)

Ollama embeddings wrapper.

**Dimension**: 384 (nomic-embed-text)

**Methods**:
- `embed_query(query)`: Single embedding
- `embed_documents(docs)`: Batch embeddings

### FAISS Store (`vectorstore/faiss_store.py`)

Persistent vector storage.

**Methods**:
- `create_index(documents)`: New index
- `add_documents(documents)`: Add to index
- `search(query, k)`: Similarity search
- `save_index()`: Persist to disk
- `delete_index()`: Remove index

### Retriever (`retrieval/retriever.py`)

Document search interface.

**Methods**:
- `retrieve(query, top_k)`: Get documents
- `retrieve_with_scores(query)`: Get scores too

### RAG Chain (`chains/rag_chain.py`)

Complete LCEL pipeline.

**Structure**:
```
retriever → format → prompt → ChatOllama → parser
```

**Methods**:
- `invoke(question)`: Get answer string
- `invoke_with_documents(question)`: Get answer + sources

## Type Hints

All modules use complete type hints:

```python
# Function signatures
def retrieve(self, query: str, top_k: Optional[int] = None) -> list[Document]:
    pass

# Class attributes
documents: list[str]
scores: list[float]
```

## Error Handling

Comprehensive error handling at each layer:

```
YouTubeLoader
├─ TranscriptsDisabled
├─ NoTranscriptFound
└─ Network errors

TextSplitter
├─ Empty input
└─ Splitting errors

EmbeddingModel
├─ Ollama connection
└─ Model loading

FAISS
├─ Index creation
└─ Search errors

RAGChain
├─ Retrieval failures
├─ LLM errors
└─ Parse errors
```

All errors logged with full context.

## Logging

Configured in `utils/helpers.py`:

```python
import logging
logger = logging.getLogger(__name__)
logger.info("Event")
logger.error("Error", exc_info=True)
```

Log levels:
- `DEBUG`: Detailed flow
- `INFO`: Normal operation
- `WARNING`: Recoverable issues
- `ERROR`: Failures
- `CRITICAL`: Fatal errors

## Extension Points

### Custom LLM Model

```python
from langchain_community.chat_models import ChatOllama

chain = RAGChain(llm_model="mistral")
```

### Custom Embedding

```python
from embeddings.embedding_model import EmbeddingModel

custom_embedder = EmbeddingModel(model_name="custom-embed")
```

### Custom Prompt

Edit `chains/rag_chain.py` method `_build_chain()`.

### Custom Retrieval

Extend `DocumentRetriever` class.

## Performance Characteristics

- **Embedding**: ~100-500 docs/sec (depends on hardware)
- **Retrieval**: ~1-5ms (local FAISS)
- **LLM Generation**: ~20-100 tokens/sec (depends on model)
- **Memory**: 4-6GB total (base + models + data)

## Security Considerations

- No API keys stored in code
- Environment variables via `.env`
- Local-only processing
- Input validation on URLs
- Logging sanitization

## Testing

Test individual modules:

```bash
python ingestion/youtube_loader.py
python embeddings/embedding_model.py
python chains/rag_chain.py
```

Check logs:
```bash
tail -f logs/app.log
```
