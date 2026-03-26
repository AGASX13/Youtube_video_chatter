# Common Issues & Solutions

## Connection Issues

### Ollama Connection Refused

**Error**: `ConnectionError: Failed to connect to http://localhost:11434`

**Causes**: Ollama not running

**Solutions**:
```bash
# Check if running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Or use nohup (background)
nohup ollama serve > ollama.log 2>&1 &
```

---

### Model Not Found

**Error**: `Error: model not found: llama3`

**Causes**: Model not downloaded

**Solutions**:
```bash
# List available
ollama list

# Download missing model
ollama pull llama3
ollama pull nomic-embed-text

# Wait for download to complete (~2-10GB each)
```

---

### Wrong Base URL

**Error**: Multiple timeouts or no connection

**Solution**: Check `.env`
```env
OLLAMA_BASE_URL=http://localhost:11434  # Default (local)
# OR if Ollama is on another machine:
OLLAMA_BASE_URL=http://192.168.1.100:11434
```

---

## Import Issues

### Module Not Found Error

**Error**: `ModuleNotFoundError: No module named 'langchain'`

**Causes**: Dependencies not installed or wrong virtual env

**Solutions**:
```bash
# Check virtual environment is active
# Windows: Should see (venv) in prompt
# If not:
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Check installed packages
pip list | grep langchain

# Reinstall all
pip install -r requirements.txt --force-reinstall
```

---

### Conflicting Versions

**Error**: `ERROR: pip's dependency resolver does not currently take into account all the packages that are installed`

**Solution**: Same as above, force reinstall

```bash
pip install -r requirements.txt --force-reinstall --no-cache-dir
```

---

## Vector Store Issues

### FAISS Index Corrupted

**Error**: `Error loading faiss index. Corrupt index.`

**Solutions**:
```bash
# Delete corrupted index
rm -r data/vectorstore_store
# Windows: rmdir /s data\vectorstore_store

# Reload video to recreate
# In Streamlit: Click "Clear Index" button
```

---

### Out of Memory Loading Index

**Error**: `MemoryError: Unable to allocate memory for index`

**Causes**: Large video transcript or low RAM

**Solutions**:
1. **Delete old indices**:
   ```bash
   rm -r data/vectorstore_store/*
   ```

2. **Reduce chunk size** in `.env`:
   ```env
   CHUNK_SIZE=300  # Down from 500
   ```

3. **Use smaller video**: Try shorter video

4. **Increase system RAM**: Add more physical memory

---

## Performance Issues

### Slow Responses

**Causes**: 
- Model still loading
- Large retrieval set
- System resource issues

**Solutions**:
1. **Wait on first query**: 30-60 seconds normal
2. **Reduce TOP_K** in `.env`:
   ```env
   TOP_K=2  # Down from 3
   ```
3. **Switch to faster model**:
   ```env
   LLM_MODEL=mistral  # 2x faster than llama3
   ```
4. **Check system resources**:
   - Windows: Task Manager → Performance
   - Linux: `top` or `htop`
   - Mac: Activity Monitor

---

### High CPU Usage

**Causes**: Model inference

**Solutions**:
- This is normal during generation
- Use lighter model (mistral)
- Run fewer parallel processes
- Close other applications

---

### Streamlit Very Slow on Load

**Error**: Takes 30+ seconds to start

**Solutions**:
```bash
# Use multiple workers
streamlit run --logger.level=error ui/streamlit_app.py

# Cache settings
streamlit run --client.showErrorDetails=false ui/streamlit_app.py
```

---

## YouTube Issues

### Transcript Not Found

**Error**: `I don't have information about that in the provided context`

**Causes**:
- Video doesn't have captions
- Captions disabled by uploader
- YouTube API issues

**Solutions**:
1. **Check if video has captions**: Open in YouTube
2. **Try different video**: Test with known-caption video
3. **Check internet**: YouTube API needs internet

---

### Invalid URL Format

**Error**: `❌ Invalid YouTube URL. Please provide a valid URL or video ID`

**Valid Formats**:
```
✅ https://www.youtube.com/watch?v=dQw4w9WgXcQ
✅ https://youtu.be/dQw4w9WgXcQ
✅ dQw4w9WgXcQ (just ID)

❌ https://youtube.com/video/...  (wrong format)
❌ https://www.youtube.com (no ID)
```

---

### Rate Limited

**Error**: `quotaExceeded` or repeated failures

**Causes**: Too many requests to YouTube

**Solution**: 
- Wait 30 minutes before retrying
- Don't reload same video repeatedly
- Use official captions only

---

## Data Issues

### Chunks Look Incomplete

**Cause**: TextSplitter broke at wrong place

**Solution**: Adjust overlap in `.env`:
```env
CHUNK_OVERLAP=150  # Up from 100
```

---

### Low Relevance Scores

**Cause**: Semantic mismatch between question and content

**Solutions**:
1. **Ask clearer questions**: More specific phrasing
2. **Increase TOP_K**: Get more results
3. **Lower threshold** (if implemented)
4. **Rephrase question**: Try different words

---

## Configuration Issues

### Wrong Model Settings

**Error**: `Invalid temperature value` or similar

**Checks**:
```env
CHUNK_SIZE=500        # Must be > 0
TOP_K=3              # Must be > 0
TEMPERATURE=0.7      # Must be 0.0-1.0
RETRIEVAL_THRESHOLD=0.5  # Must be 0.0-1.0
```

---

### Log File Permission Error

**Error**: `PermissionError: [Errno 13] Permission denied: 'logs/app.log'`

**Solutions**:
```bash
# Create logs directory
mkdir logs

# Change permissions  
chmod 755 logs

# Or disable logging
# In .env: LOG_FILE=/dev/null (Linux/Mac)
```

---

## Streamlit UI Issues

### "SessionState deprecated" warnings

**Cause**: Old Streamlit API

**Solution**:
```bash
pip install streamlit --upgrade
```

---

### Cached Functions Error

**Error**: `CachedObjectMutationWarning`

**Cause**: Modifying cached object

**Solution**: This is just a warning, safe to ignore

---

### Button Not Responding

**Cause**: Long operation blocking UI

**Solution**:
- Streamlit is single-threaded
- Will respond when query finishes
- Lower TOP_K for faster responses

---

## Logging & Debugging

### Enable Debug Logging

Edit `.env`:
```env
LOG_LEVEL=DEBUG  # See everything
LOG_FILE=logs/app.log
```

Then check logs:
```bash
tail -f logs/app.log
```

---

### Verbose Error Messages

**View full traceback**:
```bash
# In terminal/PowerShell where you run streamlit
# Error will appear in terminal, not just in app
```

---

### Test Individual Modules

```bash
# Test YouTube loader
python -c "from ingestion.youtube_loader import YouTubeLoader; YouTubeLoader().fetch_transcript('dQw4w9WgXcQ')"

# Test embeddings
python -c "from embeddings.embedding_model import EmbeddingModel; EmbeddingModel().embed_query('test')"

# Test FAISS
python -c "from vectorstore.faiss_store import FAISSVectorStore; FAISSVectorStore()"

# Test full chain
python app/main.py
```

---

## GPU Issues

### "No CUDA" but want GPU

**Status**: Currently using `faiss-cpu`

**To use GPU** (advanced):
```bash
pip uninstall faiss-cpu
pip install faiss-gpu

# Also requires NVIDIA CUDA toolkit installed
```

**Note**: Not required for good performance in most cases

---

## Emergency Troubleshooting

### Complete Fresh Start

```bash
# Remove everything
rm -r venv data/vectorstore_store logs/*.log

# Start over
python -m venv venv
.\venv\Scripts\Activate.ps1  # or source venv/bin/activate
pip install -r requirements.txt

# Check Ollama
ollama list

# Run
streamlit run ui/streamlit_app.py
```

---

## Getting Help

1. **Check logs**: `logs/app.log`
2. **Enable debug**: `LOG_LEVEL=DEBUG` 
3. **Test connections**: 
   ```bash
   curl http://localhost:11434/api/tags
   python -c "from app.config import validate_config; validate_config()"
   ```
4. **Search error message** in console
5. **Check YouTube**: Does it have captions?
6. **Restart everything**: Ollama, Python, terminal

---

## Performance Tuning

### Too Slow / High Latency

```env
LLM_MODEL=mistral      # Faster
CHUNK_SIZE=300         # Faster retrieval
TOP_K=2                # Fewer documents
TEMPERATURE=0.5        # Could be faster
```

### Hallucinating Too Much

```env
TEMPERATURE=0.3        # More deterministic
TOP_K=5                # More context
CHUNK_SIZE=700         # Larger chunks
```

### Running Out of Memory

```env
CHUNK_SIZE=300         # Smaller chunks
TOP_K=1                # One document
LLM_MODEL=mistral      # Smaller model
```
