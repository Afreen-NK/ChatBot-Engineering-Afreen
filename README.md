# CareerCompass — Engineering Student FAQ Chatbot

> **An NLP-Powered Career Guidance Assistant for Engineering Students**  
> Built with Python, Flask, NLTK, Scikit-Learn (TF-IDF & Cosine Similarity), and Vanilla Web Technologies.

---

## 1. Project Overview

**CareerCompass** is an intelligent, domain-specialized FAQ retrieval chatbot designed specifically for engineering undergraduates. It delivers fast, verified, and student-friendly answers to common questions about career paths, programming languages, campus placements, internships, resume preparation, projects, certifications, higher studies, AI/ML, and electronics engineering (ECE).

Unlike applications that query external third-party generative AI APIs (such as OpenAI or Gemini), CareerCompass is built from the ground up to demonstrate **fundamental Natural Language Processing (NLP)** concepts. It showcases an explainable, deterministic information retrieval pipeline using text normalization, tokenization, stop-word elimination, WordNet lemmatization, TF-IDF vector space modeling, and cosine similarity scoring.

---

## 2. Problem Statement

Engineering students face an overwhelming volume of conflicting advice across social media, forums, and senior advice regarding:
- Which programming language or tech stack to learn first.
- How to structure resumes and prepare for campus placement coding tests vs. HR interviews.
- When and how to apply for summer internships and off-campus opportunities.
- Whether to pursue higher studies (GATE / MS abroad) or accept job offers.
- How non-CS engineering students (such as ECE) can break into tech roles.

Generic search engines often surface sponsored bootcamps or lengthy, unstructured articles. Generative models can hallucinate or produce generic platitudes. Engineering students need a **concise, direct, and factual reference assistant** tailored to their academic journey.

---

## 3. Proposed Solution

CareerCompass provides a lightweight, local web-based assistant that maps a student's natural language question to a curated repository of 95 high-yield engineering career FAQs. By applying classical NLP and mathematical vector similarity:
- The system understands semantically equivalent questions phrased in different ways.
- It guarantees accurate, curated answers without risk of hallucination.
- It operates completely offline/locally without requiring API keys or paid credits.
- It maintains transparency by scoring similarity and applying a strict confidence threshold with helpful fallback guidance.

---

## 4. Key Features

- **Extensive FAQ Knowledge Base**: 95 curated questions covering 10 engineering domains:
  1. 🎯 Career Paths (Software Engineer, AI/ML, Data Science, Embedded, VLSI, DevOps, Cybersecurity, Cloud)
  2. 💻 Programming (Python vs C++, Java, DSA importance, OOP pillars, Git, SQL)
  3. 🤖 AI / ML (Roadmaps, ML vs DL, NLP, Computer Vision, math prerequisites, beginner projects)
  4. 💼 Internships (Application timeline, cold emailing, LinkedIn outreach, interview prep, PPOs)
  5. 🏢 Placements (Aptitude tests, coding rounds, technical interviews, HR STAR method, tier-3 tips)
  6. 📄 Resume (1-page format, ATS optimization, project bullet points, GitHub links, skill categorization)
  7. 🛠️ Projects (Choosing topics, README documentation, avoiding cliché projects, free deployment)
  8. 📜 Certifications (Cloud credentials, AWS/GCP, NPTEL, Coursera/Udemy vs. practical projects)
  9. 🎓 Higher Studies (GATE preparation, MS abroad vs. job, GRE/TOEFL, research papers, funding)
  10. ⚡ ECE Careers (Core VLSI, Embedded C/RTOS, IoT, Robotics, switching from ECE to Software)
- **Classical NLP Preprocessing Pipeline**:
  - Domain-aware token preservation (e.g. `C++` $\rightarrow$ `cpp`, `C#` $\rightarrow$ `csharp`, `AI/ML` $\rightarrow$ `ai ml`).
  - Regex-based punctuation removal.
  - NLTK word tokenization.
  - English stop-word filtering.
  - NLTK `WordNetLemmatizer` with dual verb and noun normalization (`preparing` $\rightarrow$ `prepare`, `internships` $\rightarrow$ `internship`).
- **Mathematical FAQ Retrieval**:
  - `TfidfVectorizer` utilizing unigrams and bigrams (`ngram_range=(1, 2)`) with sublinear term-frequency scaling.
  - Cosine similarity matrix computation over the FAQ vector space.
  - Configurable similarity threshold (`SIMILARITY_THRESHOLD = 0.25`).
  - Graceful fallback guidance when queries fall below the threshold or are off-topic.
- **Explainable Console Logs**: Displays raw user query, preprocessed lemma tokens, matched FAQ, similarity score, and threshold decision for live viva/demonstrations.
- **Modern Responsive Web UI**:
  - Clean card-based chat layout built with semantic HTML5 and vanilla CSS.
  - Interactive clickable suggestion chips.
  - Horizontal quick-access category pills bar with dynamic questions drawer.
  - Slide-out off-canvas category directory.
  - Animated typing indicator.
  - Session-based conversation persistence (`sessionStorage`).
  - Clear chat control.

---

## 5. Technologies Used

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core backend and NLP logic |
| **NLP Toolkit** | NLTK 3.8+ | Tokenization, stop-words corpus, WordNet lemmatization |
| **Machine Learning** | Scikit-Learn 1.4+ | TF-IDF vectorization, n-grams, cosine similarity calculation |
| **Web Framework** | Flask 3.0+ | REST API endpoints, routing, static asset serving |
| **Frontend UI** | HTML5 / CSS3 / ES6 JS | Responsive interface, async fetch calls, category drawer |
| **Testing** | Python `unittest` | Automated test suite for NLP preprocessing and matching accuracy |

---

## 6. NLP Processing & Matching Pipeline

The matching engine processes user queries through the following pipeline:

```
                  ┌────────────────────────────────────────┐
                  │       User Asks a Question             │
                  │ "How can I prepare for AI/ML careers?" │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │          Text Normalization            │
                  │   - Convert to lowercase               │
                  │   - Domain terms (C++ -> cpp, etc.)    │
                  │   - Strip punctuation & special chars  │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │              Tokenization              │
                  │     NLTK word_tokenize(clean_text)     │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │           Stop-Word Removal            │
                  │ Filter words in nltk.corpus.stopwords   │
                  │ (removes: 'how', 'can', 'i', 'for')    │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │       WordNet Lemmatization            │
                  │ Reduce to base dictionary form:        │
                  │ 'careers' -> 'career', 'preparing'     │
                  │ Output: "prepare ai ml career"         │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │         TF-IDF Vectorization           │
                  │ Transform via pre-fit TfidfVectorizer  │
                  │ (produces sparse high-dimensional vec) │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │       Cosine Similarity Matrix         │
                  │  cos_sim(User_Vec, FAQ_Matrix)         │
                  │  Rank scores descending: S1 >= S2 >= S3│
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │       Threshold Evaluation Check       │
                  │      Is Best_Score >= 0.25 ?           │
                  └──────────┬──────────────────┬──────────┘
                             │                  │
                           YES                  NO
                             │                  │
                             ▼                  ▼
               ┌───────────────────────┐  ┌───────────────────────┐
               │ Return Top FAQ Answer │  │ Return Friendly       │
               │ + Confidence & Badges │  │ Fallback Prompt       │
               └───────────────────────┘  └───────────────────────┘
```

---

## Project Structure

```text
CareerCompass/
│
├── app.py                  # Flask application and API endpoints
├── chatbot.py              # TF-IDF-based FAQ matching and cosine similarity
├── nlp_processor.py        # Text normalization and NLP preprocessing
├── faq_data.json           # FAQ dataset containing questions, answers and keywords
├── requirements.txt        # Python project dependencies
├── .gitignore              # Files and directories excluded from version control
├── README.md               # Project documentation
│
├── templates/
│   └── index.html          # Chat interface
│
├── static/
│   ├── style.css           # Interface styling and responsive layout
│   └── script.js           # Client-side interactions and API communication
│
└── tests/
    └── test_chatbot.py     # Automated unit tests using unittest
```

**Note:** The virtual environment (`.venv/`) is excluded from version control and is created locally during installation.


---

## Installation & Setup

### Prerequisites

* Python 3.10 or higher.
* Git (for cloning the repository).
* pip (Python package installer).

### Step 1: Clone the Repository

```bash
git clone https://github.com/Afreen-NK/ChatBot-Engineering-Afreen.git
cd ChatBot-Engineering-Afreen
```

Alternatively, navigate to the project directory if you have already downloaded the repository.

### Step 2: Create a Virtual Environment

A virtual environment keeps project dependencies isolated from other Python projects.

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

With the virtual environment activated, run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: NLTK Resource Setup

On execution, `nlp_processor.py` checks for the required NLTK resources and attempts to download any missing ones.

These include:

* `punkt`
* `punkt_tab`
* `stopwords`
* `wordnet`
* `omw-1.4`

An active internet connection may be required when these resources are not already available locally.


## 9. Running the Application

### Start the Flask Server
```bash
python app.py
```
*(Or `py app.py` on Windows)*

### Open the Web Interface
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

You can immediately ask questions in natural language, click any of the suggestion chips, or click on category pills (such as **Placements** or **AI/ML**) to inspect specific questions.

---

## 10. Running the Test Suite

## 10. Running the Test Suite

CareerCompass includes an automated unit testing suite built using Python's `unittest` framework.

The tests cover:

* NLP preprocessing and text normalization.
* Domain-specific terminology preservation.
* Tokenization, stop-word removal and lemmatization.
* Exact and paraphrased FAQ matching.
* Case and punctuation variations.
* Empty input and unrelated query handling.
* Similarity threshold behaviour.
* FAQ category availability.

### Execute Tests

Run the following command from the project root:

```bash
python -m unittest discover -s tests -v
```

### Verified Test Results

| Metric         |        Result |
| -------------- | ------------: |
| Total Tests    |            16 |
| Passed         |            16 |
| Failed         |             0 |
| Errors         |             0 |
| Execution Time | 1.555 seconds |
| Status         |          PASS |

*Test results verified locally using Python 3.11 in a virtual environment.*


## 11. How the Algorithm Works (Viva / Exam Guide)

### 1. Term Frequency-Inverse Document Frequency (TF-IDF)
TF-IDF reflects how important a word is to a document within a collection:

$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

- **Term Frequency (TF)**: How frequently term $t$ appears in document $d$:
  $$\text{TF}(t, d) = \frac{\text{Count of } t \text{ in } d}{\text{Total terms in } d}$$
- **Inverse Document Frequency (IDF)**: Penalizes words that appear across all documents (such as 'computer' or 'student') and boosts rare, informative terms (such as 'VLSI' or 'PPO'):
  $$\text{IDF}(t, D) = \log\left(\frac{1 + |D|}{1 + \text{count}(d \in D : t \in d)}\right) + 1$$

### 2. Cosine Similarity
Cosine similarity measures the cosine of the angle between two multi-dimensional vectors in the vector space:

$$\text{Cosine Similarity}(u, v) = \frac{u \cdot v}{\|u\|_2 \|v\|_2} = \frac{\sum_{i=1}^{n} u_i v_i}{\sqrt{\sum_{i=1}^{n} u_i^2} \sqrt{\sum_{i=1}^{n} v_i^2}}$$

- **1.0**: Vectors point in the exact same direction (identical vocabulary distributions).
- **0.0**: Vectors are orthogonal (no shared terms).
- In CareerCompass, the user's vector is compared against all 95 pre-calculated FAQ vectors. The question with the highest cosine score above `SIMILARITY_THRESHOLD = 0.25` is selected.

---

## 12. Example Queries and Expected Matches

| Student Query | Processed Tokens | Matched FAQ | Category | Score |
| :--- | :--- | :--- | :--- | :--- |
| *"How can I prepare for placements?"* | `prepare placement` | *How should I prepare for campus placements?* | Placements | ~0.54 |
| *"What should I do to get ready for campus recruitment?"* | `get ready campus recruitment` | *How should I prepare for campus placements?* | Placements | ~0.50 |
| *"I want to become an AI engineer. What should I learn?"* | `want become ai engineer learn` | *What should I learn to become an AI engineer?* | AI/ML | ~0.66 |
| *"How do I get an internship?"* | `get internship` | *How do I find internships as an engineering student?* | Internships | ~0.48 |
| *"How do I make a resume?"* | `make resume` | *How do I create a good engineering resume?* | Resume | ~0.43 |
| *"Should an ECE student learn Python?"* | `ece student learn python` | *Should an ECE student learn Python?* | ECE Careers | ~0.84 |
| *"What is deep learning?"* | `deep learn` | *What is deep learning?* | AI/ML | ~0.63 |
| *"What is the recipe for chocolate cake?"* | `recipe bake chocolate cake` | None (Score < 0.25) | Fallback | 0.00 |

---

## 13. System Limitations

1. **Vocabulary Invariance (Out-Of-Vocabulary - OOV)**: TF-IDF relies on exact term overlap. If a user uses slang or rare synonyms not present in the FAQ question or keywords, the cosine similarity may drop.
2. **Grammar & Word Order Insensitivity**: TF-IDF treats texts primarily as bag-of-words (mitigated partially in CareerCompass by using bigrams `(1, 2)`).
3. **Domain Scope**: The chatbot answers questions within its 95 curated engineering career FAQs and is intentionally prevented from hallucinating answers to out-of-scope queries.

---

## 14. Future Improvements

- **Dense Sentence Transformers**: Upgrade from sparse TF-IDF vectors to dense sentence embeddings (such as `all-MiniLM-L6-v2`) for deeper semantic capture.
- **Retrieval-Augmented Generation (RAG)**: Connect the top matched FAQ documents to a small local open-source LLM (such as Llama 3 8B or Gemma 2 2B) to summarize and personalize answers dynamically.
- **Voice Input & Speech-to-Text**: Integrate the Web Speech API in the frontend for hands-free queries.
- **Multilingual Support**: Add Hindi and regional Indian language support for wider student accessibility.
- **User Analytics & Feedback**: Store student upvotes/downvotes in an SQLite/PostgreSQL database to automatically identify missing FAQs.

---

## 15. License & Academic Attribution

Developed as an academic demonstration of Natural Language Processing and Information Retrieval principles for engineering students. Free to use, adapt, and extend for educational projects and presentations.
