# Setup & Installation Guide

Complete step-by-step guide to get YouTube Video Chatter running on your system.

## System Requirements

- Windows 10+, macOS 11+, or Linux (Ubuntu 20.04+)
- Python 3.8 or higher
- 4GB RAM minimum (6GB+ recommended)
- 10GB disk space for models
- Stable internet connection (for YouTube API and initial model download)

## Step 1: Install Ollama

### Windows
1. Download from [ollama.ai](https://ollama.ai)
2. Run the installer
3. Follow on-screen instructions
4. Ollama will start automatically

### macOS
```bash
# Using Homebrew
brew install ollama

# Or download DMG from ollama.ai
```

### Linux
```bash
curl https://ollama.ai/install.sh | sh
```

## Step 2: Download Required Models

Open terminal/PowerShell and run:

```bash
# Start Ollama server
ollama serve

# In a new terminal/PowerShell window:

# Download LLM model (11GB)
ollama pull llama3

# Download embedding model (274MB)
ollama pull nomic-embed-text

# (Optional) Faster alternative LLM
ollama pull mistral
```

**Expected Output:**
```
pulling manifest
pulling 6a0746a1ec1a
pulling 4fa551d4061f
pulling d078f7f024e9
pulling 887433b89a90
pulling c4dcd51bc6d7
...
success
```

Verify:
```bash
ollama list
```

Should show:
```
NAME                    ID              SIZE    MODIFIED
llama3:latest          ...             4.7GB   2 hours ago
nomic-embed-text:latest ...            274MB   3 minutes ago
```

## Step 3: Clone Project

```bash
# Navigate to your Projects directory
cd "C:\Users\YourUsername\Desktop\Main Projects"

# The directory should already exist. Verify:
cd youtube-video-chatter
ls  # or dir on Windows
```

## Step 4: Setup Python Environment

### Windows (PowerShell)

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again:
.\venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate
```

## Step 5: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

**This may take 5-10 minutes.** You should see:
```
Successfully installed langchain-0.1.11 langchain-community-0.0.24 faiss-cpu-1.7.4 ...
```

## Step 6: Configure Environment

```bash
# Copy template
cp .env.example .env
# On Windows: copy .env.example .env

# Edit .env with your settings (optional)
# Most defaults work fine
```

## Step 7: Create Directories

```bash
# Create logs directory (if not exists)
mkdir logs
mkdir data\vectorstore_store
# On Linux/Mac: mkdir -p data/vectorstore_store
```

## Step 8: Verify Installation

```bash
# Test imports
python -c "from langchain_community.chat_models import ChatOllama; print('✅ LangChain imports OK')"

# Test Ollama connection
python -c "from embeddings.embedding_model import EmbeddingModel; EmbeddingModel(); print('✅ Ollama connection OK')"
```

## Step 9: Run the Application

### Option A: Web UI (Recommended)

```bash
# Make sure virtual environment is active
streamlit run ui/streamlit_app.py
```

Opens automatically at `http://localhost:8501`

UI Features:
- Clean interface for loading videos
- Interactive Q&A
- View source documents
- Configure settings
- Chat history

### Option B: Command Line

```bash
# Interactive mode
python app/main.py --interactive

# Single query (no UI)
python app/main.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
                   --question "What is this video?"

# Get help
python app/main.py --help
```

### Option C: VS Code

1. Open VS Code
2. Open folder: `youtube-video-chatter`
3. Select Python interpreter: `.\venv\Scripts\python.exe`
4. Terminal → New Terminal
5. Run: `streamlit run ui/streamlit_app.py`

## Troubleshooting Installation

### Problem: "Python not found"

```bash
# Windows: Use py instead
py -m venv venv
py -m pip install -r requirements.txt

# Check installation
python --version
```

### Problem: "Module not found" errors

```bash
# Ensure virtual environment is active
# Windows indicator: `(venv)` before your prompt
# Linux/Mac indicator: `(venv)` before your prompt

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Problem: "Can't connect to Ollama"

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Should return model list in JSON
# If error: Start Ollama (ollama serve) in another terminal
```

### Problem: Import errors for LangChain

```bash
# Clear and reinstall
pip uninstall -y langchain langchain-community
pip install -r requirements.txt
```

### Problem: FAISS errors

```bash
# On Windows, if FAISS fails:
pip install --upgrade faiss-cpu

# On Mac with Apple Silicon:
pip install faiss-cpu --no-cache-dir
```

### Problem: Slow performance

1. **Check Ollama is running**: `ollama list`
2. **Check system resources**: Task Manager / Activity Monitor
3. **Use mistral instead**: `LLM_MODEL=mistral` in `.env`
4. **Reduce chunk size**: `CHUNK_SIZE=300` in `.env`

## First Run Checklist

- [ ] Ollama installed and running (`ollama serve`)
- [ ] Models downloaded (`ollama list` shows llama3 and nomic-embed-text)
- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file copied from `.env.example`
- [ ] `/data` and `/logs` directories exist
- [ ] Can run: `streamlit run ui/streamlit_app.py`

## Quick Test

```bash
# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Run test
python -c "
from ingestion.youtube_loader import YouTubeLoader
from embeddings.embedding_model import EmbeddingModel
loader = YouTubeLoader()
model = EmbeddingModel()
print('✅ All systems operational!')
"
```

## Performance Tips

1. **First Start**: May take 30-60 seconds while Ollama loads model
2. **Subsequent Runs**: 5-10 seconds after model warmup
3. **Video Processing**: Depends on transcript length (2-5 min average)
4. **Response Generation**: 5-15 seconds per question

## Using Alternative Models

### Switch to Mistral (Faster)

```bash
ollama pull mistral

# In .env:
LLM_MODEL=mistral
```

### Other Available Models

```bash
ollama pull neural-chat
ollama pull openchat
ollama pull dolphin-mixtral
```

## Advanced: Docker Setup (Optional)

```bash
# Build Docker image
docker build -t youtube-chatter .

# Run with Ollama service
docker run -p 8501:8501 \
           -e OLLAMA_BASE_URL=http://ollama:11434 \
           youtube-chatter
```

## Update/Upgrade

```bash
# Activate virtual environment

# Update dependencies
pip install -r requirements.txt --upgrade

# Update Ollama models
ollama pull llama3
ollama pull nomic-embed-text
```

## Uninstall

```bash
# Remove virtual environment
rm -r venv
# Windows: rmdir /s venv

# Clean up Ollama models (optional)
ollama rm llama3
ollama rm nomic-embed-text
```

## Next Steps

1. ✅ Complete setup above
2. ✅ Run `streamlit run ui/streamlit_app.py`
3. ✅ Paste a YouTube URL (or try: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
4. ✅ Click "Load"
5. ✅ Ask a question
6. ✅ Enjoy! 🎉

## Support

- **Logs**: Check `logs/app.log` for errors
- **Enable Debug**: `LOG_LEVEL=DEBUG` in `.env`
- **Ollama Status**: `ollama list`
- **Check Connection**: `curl http://localhost:11434/api/tags`

Good luck! 🚀
