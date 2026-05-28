**Insurance Policy RAG Chatbot**



AI-Powered Insurance Policy Question Answering System using \*\*RAG (Retrieval Augmented Generation)\*\*, \*\*FAISS\*\*, \*\*Groq LLM\*\*, and \*\*Flask\*\*.



This project allows users to select either:



&#x20;- Health Insurance Chatbot

&#x20;- Car Insurance Chatbot



and ask natural language questions related to insurance policy documents.



The chatbot retrieves relevant clauses from policy documents and generates contextual answers using AI.



\---



**Features**



&#x20;- Health Insurance Question Answering

&#x20;- Car Insurance Question Answering

&#x20;- RAG-based architecture

&#x20;- Semantic document retrieval

&#x20;- Multi-page reasoning

&#x20;- Fast vector search using FAISS

&#x20;- Groq LLM integration

&#x20;- Modern Flask-based chatbot UI

&#x20;- Handles:



&#x20;  - Two-column PDFs

&#x20;  - Table-heavy PDFs

&#x20;  - Complex insurance clauses

&#x20;- Context-aware answers

&#x20;- Page reference support



\---



**Tech Stack**



**Backend**



&#x20;- Python

&#x20;- Flask



**AI / NLP**



&#x20;- Sentence Transformers

&#x20;- FAISS

&#x20;- Groq API (Llama 3.3 70B)



**PDF Processing**



&#x20;- PyMuPDF (fitz)



**Frontend**



&#x20;- HTML

&#x20;- CSS

&#x20;- JavaScript



\---



**System Architecture**



User Question

↓

Frontend (HTML/CSS/JS)

↓

Flask Backend

↓

Retriever

↓

FAISS Semantic Search

↓

Top Relevant Chunks

↓

Groq LLM

↓

Generated Answer

↓

Frontend Response



\---



**Project Workflow**



**Step 1 — PDF Extraction**



Insurance PDFs are processed using **PyMuPDF**.



The system handles:



&#x20;- Single-column pages

&#x20;- Two-column pages

&#x20;- Table-heavy pages



Text blocks are extracted using coordinates to preserve proper reading order.



\---



**Step 2 — Layout Detection**



Each page is classified as:



&#x20;- Single-column

&#x20;- Two-column

&#x20;- Table-heavy



This allows different extraction strategies for different page structures.



\---



**Step 3 — Section Detection**



Extracted content is grouped into:



&#x20;- Headings

&#x20;- Subheadings

&#x20;- Content blocks



This improves semantic understanding and chunk quality.



\---



**Step 4 — Chunking**



Large documents are divided into smaller semantic chunks.



Example:



&#x20;- Chunk 1 → Grace Period

&#x20;- Chunk 2 → Waiting Period

&#x20;- Chunk 3 → Exclusions



Chunking improves retrieval accuracy.



\---



**Step 5 — Embeddings**



Each chunk is converted into vector embeddings using:



all-MiniLM-L6-v2



These embeddings capture semantic meaning instead of keyword matching.



\---



**Step 6 — FAISS Indexing**



Embeddings are stored inside:



&#x20;- health.index

&#x20;- car.index



FAISS enables extremely fast semantic similarity search.



\---



**Step 7 — Retrieval**



When a user asks a question:



Question → Embedding → FAISS Search



The system retrieves the most relevant chunks from the policy document.



\---



**Step 8 — Answer Generation**



Retrieved chunks are sent to:



Groq Llama 3.3 70B



The LLM generates final answers using only retrieved policy content.



\---



**Understanding Important Files**



**`.index` File**



Example:



health.index



Purpose:



&#x20;- Stores vector embeddings using FAISS

&#x20;- Used for fast semantic similarity search



When user asks a question:



&#x20;- Question is converted into vector embedding

&#x20;- FAISS finds nearest matching chunks



\---



**`.pkl` File**



Example:



health\_metadata.pkl



Purpose:



\* Stores chunk metadata

\* Stores actual text content

\* Stores titles and page references



Used after FAISS retrieval to fetch real chunk data.



\---



**Installation**



**1. Clone Repository**



```bash

git clone <your-repository-url>

cd insurance\_chatbot

```



**2. Create Virtual Environment**



```bash

python -m venv venv

```



Activate environment:



**Windows**



```bash

venv\\Scripts\\activate

```



**Linux / Mac**



```bash

source venv/bin/activate

```



\---



**3. Install Dependencies**



```bash

pip install flask

pip install sentence-transformers

pip install faiss-cpu

pip install groq

pip install pymupdf

pip install torch

```



\---



**Groq API Setup**



Get your free API key from:



https://console.groq.com



Open:



app.py



Replace:



```python

API\_KEY = "YOUR\_GROQ\_API\_KEY"

```



with your actual Groq API key.



\---



**Running the Project**



**Start Flask Server**



```bash

python app.py

```



Open browser:



http://127.0.0.1:5000



\---



**Example Questions**



**Health Insurance**



&#x20;- What is grace period?

&#x20;- What is waiting period?

&#x20;- Does policy cover ambulance charges?

&#x20;- What happens if premium payment is delayed?

&#x20;- Is diabetes covered?



\---



**Car Insurance**



&#x20;- What is depreciation?

&#x20;- Does policy cover theft?

&#x20;- What happens if someone without valid license crashes my car?

&#x20;- How is IDV calculated?

&#x20;- Is tire damage covered?



\---



**Why RAG Instead of Direct PDF + LLM?**



Instead of sending full PDFs to the LLM every time:



Search First → Answer Later



Benefits:



&#x20;- Faster responses

&#x20;- Lower cost

&#x20;- Better scalability

&#x20;- Handles large PDFs

&#x20;- Reduces hallucinations

&#x20;- Improves contextual accuracy



\---



**Challenges Solved**



**Complex PDF Layouts**



Handled:



&#x20;- Two-column documents

&#x20;- Tables

&#x20;- Mixed layouts



\---



**Multi-page Reasoning**



The chatbot combines information from:



&#x20;- Multiple chunks

&#x20;- Multiple pages

&#x20;- Multiple clauses



\---



**Semantic Understanding**



The system understands meaning instead of exact keywords.



Example:



User Question:

“What happens if I pay premium late?”



Document Clause:

“Grace period...”



The system still retrieves correct results.







