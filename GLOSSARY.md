# Glossary & Key Concepts

## Core Concepts

### RAG (Retrieval Augmented Generation)

A system that:
1. **Retrieves** relevant documents based on a query
2. **Augments** the LLM prompt with retrieved context
3. **Generates** an answer from the context

Benefits:
- Answers use current/specific information
- Reduces hallucinations (LLM confabulations)
- Works without fine-tuning

### LLM (Large Language Model)

An AI model trained on vast amounts of text to understand and generate language.

Examples:
- `llama3`: Meta's model, very capable, larger (~7B parameters)
- `mistral`: Open source, faster, smaller (~7B parameters)
- `gpt-3.5`: Proprietary, fastest, but requires API

### Embeddings

Numerical representations (vectors) of text that capture semantic meaning.

Example:
```
"cat" → [0.1, -0.5, 0.3, 0.8, ...]  # 384 values for nomic-embed-text
"dog" → [0.09, -0.51, 0.32, 0.79, ...]  # Similar to "cat"
"pizza" → [-0.8, 0.2, -0.4, -0.1, ...]  # Different from "cat"
```

Similarity measured by cosine distance:
```
similarity("cat", "dog") = 0.95  # Very similar
similarity("cat", "pizza") = 0.10  # Not similar
```

### Vector Store (FAISS)

A database that:
- Stores embeddings efficiently
- Finds similar vectors via fast algorithms
- Returns top-K nearest neighbors

FAISS = Facebook AI Similarity Search

### Tokenization

Breaking text into tokens (words/subwords):
```
"Hello world" → ["Hello", "world"] or ["Hel", "lo", "world"]
```

Token limits:
- llama3: ~8192 tokens
- mistral: ~32000 tokens
- 1 token ≈ 4 characters

### Context Window

The maximum length of text the model can process at once.

Typical: 4K-32K tokens

### Temperature

Controls randomness in model output:
- `0.0` = Deterministic, repeatable answers
- `0.5` = Balanced
- `1.0` = Creative, varied answers

### Top-K Retrieval

Returns the K most similar documents.

Examples:
- TOP_K=3: Return 3 most relevant chunks
- TOP_K=1: Return only the best match
- TOP_K=10: Return 10 options

## Architecture Terms

### LCEL (LangChain Expression Language)

A way to chain LLM operations together:

```python
retriever → formatter → prompt → llm → parser
```

Benefits:
- Declarative
- Easy streaming
- Built-in parallelization

### Prompt Template

A template for constructing LLM prompts:

```
"Question: {question}\nContext: {context}\nAnswer:"
```

Variables filled in at runtime.

### Chain

A sequence of operations:
```
input → process1 → process2 → ... → processN → output
```

### Retriever

A component that finds relevant documents for a query.

Responsible for the "R" in RAG.

### Runnable

In LangChain, any component that accepts input and produces output.

Examples:
- `retriever` (input: query, output: documents)
- `llm` (input: prompt, output: text)
- `parser` (input: text, output: structured)

## Technical Terms

### FAISS Index

A data structure for fast similarity search.

Types:
- `IndexFlatL2`: Exact search (slower, more accurate)
- `IndexIVFFlat`: Approximate (faster, approximate)

We use flat (exact) for simplicity.

### Vector Dimension

The size of embedding vectors.

`nomic-embed-text`: 384 dimensions
`OpenAI ada`: 1536 dimensions

More dimensions = more expressive but slower.

### Semantic Similarity

How "close" two pieces of text are in meaning:

```
"John is a programmer" vs "John codes" = High similarity
"John is a programmer" vs "The sky is blue" = Low similarity
```

Measured using cosine similarity (0-1 range).

### Chunking

Breaking long documents into smaller pieces.

Reasons:
- Embedding models have token limits
- Retrieval needs smaller units
- Context windows are limited

### Overlap

When chunks share text:

```
Text: "ABCDEFGHIJ" (10 chars)
Chunk1: "ABCDE" (5 chars)
Chunk2: "DEFI" (4 chars, 2 char overlap "DE")
```

Prevents losing meaning at chunk boundaries.

### Hallucination

When an LLM makes up facts not in training data.

RAG reduces this by providing context.

## LangChain-Specific Terms

### Document

A LangChain object with `page_content` and `metadata`:

```python
doc.page_content  # "actual text"
doc.metadata      # {"source": "youtube", "timestamp": 120}
```

### Runnable Parallel

Execute multiple chains in parallel:

```python
RunnableParallel(
    context=retriever,
    question=RunnablePassthrough()
)
```

### StrOutputParser

Extracts string output from LLM responses.

Handles raw model output → clean string.

### ChatPromptTemplate

Template for chat-style prompts:

```python
ChatPromptTemplate.from_messages([
    ("system", "You are helpful"),
    ("human", "{question}")
])
```

## Project-Specific Terms

### "Video ID"

YouTube unique identifier:
- Full URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- Video ID: `dQw4w9WgXcQ`

11 alphanumeric characters.

### "Transcript"

Full closed-caption text from YouTube video.

Usually accurate but may contain:
- Typos
- Stutters
- "[Music]" markers

### "Chunk"

A piece of text (≈500 characters by default).

Multiple chunks = index

### "Index"

Stored vector representation of all chunks.

Persisted in `./data/vectorstore_store/`.

### "Memory Buffer"

Conversation history storage.

Keeps last 5 exchanges by default.

## Data Flow Terms

### Ingestion

Process of:
1. Fetching youtube transcript
2. Cleaning text
3. Splitting into chunks
4. Generating embeddings
5. Storing in vector database

### Retrieval

Finding relevant chunks for a query.

Returns top-K most similar chunks.

### Generation

LLM creating an answer from context.

Takes format:
```
Context: [retrieved chunks]
Question: [user question]
Answer: [LLM generates]
```

### Augmentation

Adding retrieved context to the prompt.

This is what makes it "Augmented".

## Model Names

### LLM Models

| Model | Size | Speed | Quality | Context |
|-------|------|-------|---------|---------|
| mistral | 7B | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 32K |
| llama3 | 8B | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 8K |
| neural-chat | 7B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 8K |

### Embedding Models

| Model | Dimension | Size |
|-------|-----------|------|
| nomic-embed-text | 384 | 274MB |
| all-minilm:l6-v2 | 384 | 44MB |
| snowflake-arctic | 768 | 1.5GB |

## Common Commands Reference

```bash
# Ollama operations
ollama serve                # Start server
ollama list                 # List installed models
ollama pull llama3          # Download model
ollama rm llama3            # Delete model
ollama run llama3 "prompt"  # Run directly

# Python operations
streamlit run ui/streamlit_app.py   # Web UI
python app/main.py --interactive    # CLI
python -m pytest tests/             # Run tests

# Debugging
tail -f logs/app.log        # View logs
python app/config.py        # Check config
python embeddings/embedding_model.py  # Test embeddings
```

## Quick Reference

- **RAG**: Retrieval + Augmented + Generation
- **LLM**: Large Language Model
- **FAISS**: Vector similarity search
- **Embedding**: Vector representation of text
- **Chunk**: Small piece of document
- **Token**: ~4 characters
- **Context**: Information provided to LLM
- **Temperature**: Randomness level (0-1)
- **LCEL**: LangChain Expression Language
- **Runnable**: Any component with input/output
- **Memory Buffer**: Conversation history
- **Vector Dimension**: Size of embedding vectors (384 for nomic)

Think of RAG as:
```
Question → Search for relevant info → Add to prompt → Ask LLM → Answer
```
