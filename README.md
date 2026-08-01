# BLOOM AI – Real-Time Floral Shop Voice Assistant

BLOOM AI is a warm, real-time voice assistant for a floral shop. Customers can search flowers, get bouquet recommendations, track orders, and ask about delivery, refunds, returns, or flower care.

## Architecture

The existing LiveKit voice pipeline remains unchanged:

`Customer voice → LiveKit → existing STT → existing LLM → Cartesia TTS → Customer`

The business layer adds four local tools:

- `search_flowers()` searches `data/products.json` by flower type, color, occasion, keywords, and budget.
- `recommend_bouquet()` recommends a bouquet or basket for an occasion and budget.
- `track_order()` reads `data/orders.json` and returns status, delivery estimate, items, price, and tracking ID.
- `lookup_policy()` retrieves the top three relevant chunks from the local policy index using MMR.

The RAG index uses LangChain, recursive chunking with overlap, Sentence Transformers `all-MiniLM-L6-v2`, and persistent local ChromaDB. It does not use a cloud vector database. If no relevant policy is found, the assistant says: “I'm sorry, I couldn't find that information in our flower shop policies.”

## Folder structure

```text
agent.py                 LiveKit agent, BLOOM AI instructions, and tools
api.py                   Flask JWT token server
index.html               Existing LiveKit UI with floral branding and transcript
data/products.json       40 flower and bouquet products
data/orders.json         Sample floral orders
knowledge/*.txt          Delivery, returns, refund, care, and FAQ policies
rag/policy_rag.py        Persistent local Chroma RAG
tools/*.py               Flower, bouquet, order, policy, and memory tools
```

## Installation

Use Python 3.10 or newer:

```bash
pip install -r requirements.txt
pip install -r requirements-agent.txt
```

Configure the existing project credentials in `.env`:

```env
LIVEKIT_URL=your-livekit-url
LIVEKIT_API_KEY=your-livekit-api-key
LIVEKIT_API_SECRET=your-livekit-api-secret
GOOGLE_API_KEY=your-google-api-key
CARTESIA_API_KEY=your-cartesia-api-key
```

The first policy question downloads the local embedding model and creates `rag/chroma_db/`.

## Run

Terminal 1:

```bash
python api.py
```

Terminal 2:

```bash
python agent.py dev
```

Terminal 3, for the frontend:

```bash
python -m http.server 8080
```

Open `http://localhost:8080/index.html`, allow microphone access, and click **Join**. The assistant welcomes the customer with: “Welcome to BLOOM AI Floral Shop! How can I help you today?”

## Vercel deployment

This repository is configured for Vercel to host:

- `public/index.html` and `public/assets/*`
- the Flask token endpoint at `/api/getToken`
- a health endpoint at `/api/health`

Set these environment variables in the Vercel project settings:

```env
LIVEKIT_URL=wss://your-livekit-url.livekit.cloud
LIVEKIT_API_KEY=your-livekit-api-key
LIVEKIT_API_SECRET=your-livekit-api-secret
```

Vercel uses the lightweight root `requirements.txt` for the serverless token API. The full LiveKit voice agent and local RAG dependencies live in `requirements-agent.txt` because the agent is a long-running worker and should run separately from Vercel, for example locally, on a VM, or on a worker/container host:

```bash
python agent.py dev
```

## Sample voice commands

- “I need flowers under ₹1,000.”
- “Suggest flowers for a wedding.”
- “Track my order ORD1002.”
- “Which flowers last the longest?”
- “Can I return flowers?”
- “How should I care for orchids?”
- “Recommend a birthday bouquet.”
- “Suggest flowers for my wife.”
- “Do you have white lilies?”

## Scope

This capstone intentionally has no checkout, payment gateway, admin panel, analytics, or external database. Customer details and preferences are held only in conversation memory.
