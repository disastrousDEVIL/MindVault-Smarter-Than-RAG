MindVault 🧠

A Knowledge-Graph Memory Layer for LLMs

MindVault is a backend service that converts documents into a structured knowledge graph and allows Large Language Models (LLMs) to answer questions using only stored knowledge.

This project focuses on memory correctness, traceability, and structure, not chat history or vector-only retrieval.

⸻

What MindVault Is
	•	A memory service, not a chatbot
	•	Stores knowledge as atomic facts
	•	Uses a knowledge graph, not raw text chunks
	•	Answers are grounded strictly in stored memory
	•	Supports multiple documents with shared entities
	•	Provides graph visualization for inspection
⸻
Core Idea

Instead of retrieving text chunks and hoping the model reasons correctly, MindVault:
	1.	Extracts atomic facts from documents
	2.	Stores them as entities and relationships
	3.	Builds a knowledge graph
	4.	Retrieves structured facts
	5.	Uses an LLM only to compose answers from memory

If a fact is not stored, it cannot appear in the answer.

⸻

Architecture Overview

Document
   ↓
LLM (fact extraction)
   ↓
Validated atomic facts
   ↓
Knowledge Graph (Cognee)
   ↓
Fact retrieval
   ↓
LLM (answer generation)

LLMs never bypass memory.

⸻

Memory Model

Atomic Fact

The fundamental unit of memory:

Entity → Relation → Entity / Value

Example:
	•	LangGraph → supports → cycles
	•	LangChain → provides → linear chains

Each fact stores:
	•	subject
	•	relation
	•	object
	•	confidence
	•	source document ID

⸻

Tech Stack
	•	Python: 3.11 (required)
	•	API: FastAPI
	•	LLM: OpenAI API
	•	Memory Engine: Cognee
	•	Visualization: Cognee graph visualizer (HTML)

⸻

Prerequisites
	•	Python 3.11
	•	OpenAI API key
	•	pip and virtualenv

⚠️ Python 3.12+ is not recommended due to dependency constraints.

⸻

Installation

git clone https://github.com/your-username/mindvault.git
cd mindvault

python3.11 -m venv venv
source venv/bin/activate

pip install -r requirements.txt


⸻

Environment Variables

Create a .env file in the project root:

OPENAI_API_KEY=sk-your-openai-key
OPENAI_MODEL=gpt-4.1-mini
DEBUG=false

OPENAI_MODEL defaults to gpt-4.1-mini if not set.


⸻

Running the Server

uvicorn app.main:app --reload

Open Swagger UI:

http://127.0.0.1:8000/docs


⸻

API Endpoints

1. Ingest a Document

POST /ingest

{
  "document_id": "doc_langgraph",
  "title": "LangGraph Overview",
  "content": "LangGraph supports stateful workflows and allows cycles."
}

Response:

{
  "status": "success",
  "facts_stored": 2
}


⸻

2. Ask a Question

POST /query

{
  "question": "How does LangGraph differ from LangChain?"
}

Response:

{
  "answer": "LangGraph supports stateful workflows and cycles, while LangChain focuses on linear chains.",
  "sources": ["doc_langgraph", "doc_langchain"]
}


⸻

3. Visualize the Knowledge Graph

GET /graph
	•	Generates an HTML file
	•	If output_path is provided, returns the HTML file directly
	•	If output_path is omitted, writes to Cognee's default location (usually your home directory)
	•	Displays entities and relationships visually

Optional query params:
	•	output_path: where to write the HTML file
	•	dataset_name: Cognee dataset to visualize

Example response (no output_path):

{
  "status": "success",
  "message": "Graph written to Cognee's default location (home directory)."
}

Open the file in a browser to inspect memory.

⸻

Expected Behavior

Correct Answers
	•	Answers combine facts from multiple documents
	•	Sources are always listed
	•	No hallucinations

Failure Case

If memory lacks information:

{
  "answer": "Not enough information in memory to answer this question.",
  "sources": []
}

This is a successful outcome, not an error.

⸻

Folder Structure

MindVault/
├── app/
│   ├── main.py        # FastAPI wiring
│   ├── settings.py    # env loading
│   ├── llm.py         # OpenAI client
│   ├── ingest.py      # document → facts
│   ├── memory.py      # Cognee integration
│   └── retrieve.py    # fact retrieval
│
├── examples/
│   ├── sample_doc.md
│   └── sample_query.txt
│
├── README.md
└── requirements.txt


⸻

Why This Project Matters

Most RAG systems:
	•	Retrieve text chunks
	•	Depend on probabilistic reasoning
	•	Hallucinate silently

MindVault:
	•	Stores knowledge, not text
	•	Makes memory inspectable
	•	Guarantees answer grounding
	•	Scales across documents naturally

This is how LLM memory should actually be built.

⸻

Status

✅ Multi-document ingestion
✅ Knowledge graph memory
✅ Grounded question answering
✅ Graph visualization
✅ Production-ready v1

⸻

License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this software with attribution.
See the LICENSE file for full details.

