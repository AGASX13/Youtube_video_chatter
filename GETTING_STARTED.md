# 🎬 Getting Started - Visual Guide

## Your YouTube Video Chatter is Ready! 🎉

Follow this visual guide to get up and running in 10 minutes.

---

## ⏱️ 10-Minute Quick Start

### Step 1: Install Ollama (2 min)
```
Download: https://ollama.ai
Install and complete setup
```

### Step 2: Get Models (5 min)
```
Open Terminal/PowerShell

ollama pull llama3
ollama pull nomic-embed-text

Wait for downloads (~2GB total)
```

### Step 3: Start Ollama (30 sec)
```
ollama serve

Keep this terminal open
```

### Step 4: Setup Project (2 min)
```
Open NEW Terminal/PowerShell
Navigate to: youtube-video-chatter

Windows:    setup.bat
Linux/Mac:  ./setup.sh
```

### Step 5: Launch UI (1 min)
```
streamlit run ui/streamlit_app.py

Opens automatically at http://localhost:8501
```

---

## 🖥️ Web UI Tour

### Tab 1: Load Video

```
┌─────────────────────────────────────────┐
│ 📹 Load YouTube Video               [X] │
├─────────────────────────────────────────┤
│                                         │
│ YouTube URL or Video ID                 │
│ ┌───────────────────────────────────┐   │
│ │ https://www.youtube.com/watch...  │   │
│ └───────────────────────────────────┘   │
│                                 [Load]   │
│                                         │
│ ✅ Successfully loaded transcript!     │
│ (250 chunks created)                   │
│                                         │
└─────────────────────────────────────────┘
```

✅ **What to enter:**
- Full URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- Short URL: `https://youtu.be/dQw4w9WgXcQ`
- Just ID: `dQw4w9WgXcQ`

---

### Tab 2: Ask Questions

```
┌─────────────────────────────────────────┐
│ ❓ Ask Questions                   [X]  │
├─────────────────────────────────────────┤
│ ✅ Ready to answer...                  │
│                                         │
│ Your Question                           │
│ ┌───────────────────────────────────┐   │
│ │ What is this video about?         │   │
│ │ (Enter your question here...)     │ │
│ └───────────────────────────────────┘   │
│                                 [Ask]   │
│                                         │
│ >>> ANSWER APPEARS HERE <<<            │
│                                         │
│ 📚 Source Documents (3)                │
│ ├─ Document 1: "The content..."       │
│ ├─ Document 2: "The topic..."         │
│ └─ Document 3: "This includes..."     │
│                                         │
│ 💬 Chat History (expandable)           │
│                                         │
└─────────────────────────────────────────┘
```

✅ **How it works:**
1. Type your question
2. Click "Ask"
3. See answer in seconds
4. View source documents
5. Repeat for more questions

---

### Tab 3: Configuration (Sidebar)

```
┌──────────────────────┐
│ ⚙️ Configuration     │
├──────────────────────┤
│                      │
│ [🔄 Clear Index]     │
│ [💾 Save Index]      │
│                      │
│ Model Settings       │
│                      │
│ Top-K Retrieved:     │
│ ▬▬▬●▬▬▬▬ (3)         │
│ [Help: Number of...] │
│                      │
│ Temperature:         │
│ ▬▬▬●▬▬▬▬ (0.7)       │
│ [Help: Controls...]  │
│                      │
│ 📊 Status            │
│ ✅ Video Loaded      │
│ 📚 4 Documents       │
│                      │
└──────────────────────┘
```

✅ **Options:**
- **Top-K**: How many results (1-10)
- **Temperature**: Randomness (0=fixed, 1=creative)
- **Clear/Save**: Index management

---

## 💻 Command Line Usage

### Interactive Mode (Recommended)
```bash
python app/main.py --interactive

Output:
🎥 YouTube Video Chatter - Interactive Mode
============================================================

Enter YouTube URL or video ID (or 'quit' to exit):
> https://www.youtube.com/watch?v=...

⏳ Loading video...
✅ Video loaded successfully!

Enter your questions (type 'quit' to exit):

You: What is this about?
🤔 Thinking...
Assistant: [Answer appears here]
📚 Used 3 source documents

You: Ask another question
...
```

### Single Query Mode
```bash
python app/main.py \
  --url "https://www.youtube.com/watch?v=..." \
  --question "What is the main topic?"

Output:
Loading video...
✅ Video loaded!

Asking: What is the main topic?

[Answer appears here]

Source documents used: 3
```

### Get Help
```bash
python app/main.py --help

Options:
  --url URL              YouTube URL to load
  --question QUESTION    Question to ask (requires --url)
  --interactive          Run in interactive mode
  --streamlit           Run Streamlit web interface
```

---

## 📊 What Happens Behind the Scenes

```
You: "What is the video about?"
        ↓
[YouTube Transcript API]
        ↓
Raw transcript (1000s of characters)
        ↓
[Text Splitter - 500 char chunks]
        ↓
250 chunks (approx)
        ↓
[Ollama: nomic-embed-text]
        ↓
250 vectors (384 dimensions each)
        ↓
[FAISS: Similarity Search]
        ↓
Top 3 most similar chunks
        ↓
[ChatOllama: llama3]
Input: "Context: [top 3 chunks] Question: [your question]"
        ↓
Answer generation
        ↓
"Here's what the video is about..."
```

---

## 🎯 Common Tasks

### Load a Different Video
1. Click "Load Video" tab
2. Paste new URL
3. Click "Load"
4. Previous answers cleared
5. New Q&A session starts

### Clear Chat History
1. Go to "Ask Questions" tab
2. Click "Clear Chat" button
3. History removed
4. Vector index stays

### Delete Vector Index
1. Sidebar → "Clear Index" button
2. Frees up disk space
3. Next video will be re-indexed

### Change Model Speed
1. Sidebar → "Top-K Retrieved"
2. Lower value = faster (fewer results)
3. Higher value = slower (more results)

### Make Answers More Creative
1. Sidebar → "Temperature"
2. Increase value (0.5 → 0.8)
3. Answers more varied
4. May be less accurate

---

## ❌ Troubleshooting Quick Fix

### Problem: "Can't connect to Ollama"
```bash
# Check if running
curl http://localhost:11434/api/tags

# If fails: Start Ollama
ollama serve
```

### Problem: "Model not found"
```bash
# Download
ollama pull llama3
ollama pull nomic-embed-text

# Verify
ollama list
```

### Problem: "Just spinning, no answer"
1. Wait longer (first query can take 60+ seconds)
2. Check system resources (Task Manager)
3. Reduce TOP_K in sidebar
4. Try shorter question

### Problem: "Module not found"
```bash
# Reinstall
pip install -r requirements.txt

# Better: Force reinstall
pip install -r requirements.txt --force-reinstall
```

See **TROUBLESHOOTING.md** for more solutions.

---

## 📱 Example Queries

### Good Questions ✅
```
"What is the main topic of this video?"
"Explain the key points about machine learning"
"What are the technical details mentioned?"
"Who are the speakers and what are their roles?"
"What problem does this video address?"
```

### Less Effective ❌
```
"Great video!" (Not a question)
"What do you think?" (Not in transcript)
"Tell me everything" (Too vague)
"Compare this to another video" (No context)
```

### Why Context Matters
```
Good:    "When was Python released?"
Better:  "According to the video, when was Python released?"

If question not in video → "I don't have information about that"
```

---

## 💡 Pro Tips

### Tip 1: Test with Known Video
```
URL: https://youtu.be/dQw4w9WgXcQ
Question: "What song is this?"
Answer: "This is Never Gonna Give You Up by Rick Astley"
```

### Tip 2: Save Indices for Reuse
```bash
# Indices auto-save to: ./data/vectorstore_store/
# Next time you load same video = instant (no re-indexing)
```

### Tip 3: Control Quality
```
Better answers:
- Higher temperature = More creative (0.8)
- Specific questions = Better answers
- Longer transcripts = More context
```

### Tip 4: Extend the Codebase
```python
# Easy to add features:
# - Custom retrievers
# - Different LLM models
# - Batch processing
# - API endpoints
# See ARCHITECTURE.md
```

---

## 🎓 Understanding the Tech

### What's RAG?
```
RAG = Retrieval + Augmented + Generation

1. Retrieval: Search for relevant text chunks
2. Augmented: Add them to the prompt
3. Generation: LLM creates an answer

Result: Accurate, context-grounded answers
```

### Why Ollama?
```
✅ Free and open source
✅ Runs completely locally
✅ No API keys needed
✅ No internet required (after setup)
✅ Privacy-preserving
✅ 100% free
```

### Why FAISS?
```
✅ Fast similarity search
✅ Stores embeddings efficiently
✅ Exact results (not approximate)
✅ Works offline
✅ Lightweight
```

---

## 📚 Documentation Map

**Start Here:**
1. This file (you are here)
2. README.md (full guide)
3. SETUP.md (installation details)

**Deep Dive:**
1. ARCHITECTURE.md (technical details)
2. GLOSSARY.md (terminology)
3. Source code (well-documented)

**Troubleshooting:**
1. TROUBLESHOOTING.md (25+ solutions)
2. logs/app.log (error details)

**Configuration:**
1. .env.example (all settings)
2. app/config.py (code reference)

---

## 🚀 Next Steps

1. ✅ Install Ollama
2. ✅ Download models (`ollama pull llama3`)
3. ✅ Run `setup.bat` or `./setup.sh`
4. ✅ `streamlit run ui/streamlit_app.py`
5. ✅ Load your first video
6. ✅ Ask your first question
7. ✅ Enjoy! 🎉

---

## 🤝 Need Help?

| Issue | Where to Look |
|-------|----------------|
| Installation problems | SETUP.md |
| How does it work? | GLOSSARY.md + ARCHITECTURE.md |
| Common errors | TROUBLESHOOTING.md |
| Configuration options | .env.example + README.md |
| Code reference | Module docstrings |
| Getting started | README.md + This guide |

---

## 🎓 Learning Path

```
Beginner (Day 1)
  ├─ Read README.md
  ├─ Follow SETUP.md
  ├─ Run Streamlit
  ├─ Load a video
  └─ Ask questions

Intermediate (Day 2)
  ├─ Read GLOSSARY.md
  ├─ Try CLI mode
  ├─ Modify .env
  ├─ Change models
  └─ Explore settings

Advanced (Day 3+)
  ├─ Read ARCHITECTURE.md
  ├─ Examine source code
  ├─ Add custom features
  ├─ Modify chains
  └─ Deploy production
```

---

## 📊 Performance Expectations

| Task | Time | Notes |
|------|------|-------|
| Load video (5 min transcript) | 15-30 sec | First time only |
| Reload (already indexed) | 1 sec | From disk |
| First question | 30-60 sec | Model warmup |
| Subsequent questions | 5-15 sec | Model in memory |
| Embedding generation | ~100ms per chunk | Happens once |
| Retrieval search | ~1-5ms | FAISS is fast |

---

## ✨ Features Summary

| Feature | Included | Location |
|---------|----------|----------|
| YouTube integration | ✅ | `ingestion/` |
| Text processing | ✅ | `ingestion/` |
| Embeddings | ✅ | `embeddings/` |
| Vector storage | ✅ | `vectorstore/` |
| Similarity search | ✅ | `retrieval/` |
| RAG pipeline | ✅ | `chains/` |
| Web UI | ✅ | `ui/` |
| CLI | ✅ | `app/` |
| Chat history | ✅ | `utils/` |
| Config management | ✅ | `app/` |
| Logging | ✅ | `utils/` |
| Error handling | ✅ | All modules |
| Type hints | ✅ | All modules |
| Documentation | ✅ | 5 files |

---

## 🎉 You're All Set!

Your production-grade RAG application is ready to:

- Answer questions about YouTube videos
- Run completely locally
- Provide source document citations
- Maintain conversation history
- Handle errors gracefully
- Scale to multiple videos

**Ready?** → `streamlit run ui/streamlit_app.py`

**Questions?** → Check TROUBLESHOOTING.md

**Want to extend?** → Read ARCHITECTURE.md

---

**Happy learning! 🚀**
