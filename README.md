# CareerCompass — Engineering Student FAQ Chatbot

> **An NLP-Powered Career Guidance Assistant for Engineering Students**  
> Built with Python, Flask, NLTK, Scikit-Learn (TF-IDF & Cosine Similarity), and Vanilla Web Technologies.

## 1. Project Overview

**CareerCompass** is a domain-specific FAQ retrieval chatbot designed to assist engineering undergraduate students with career-related guidance.

It provides answers to commonly asked questions about career paths, programming, campus placements, internships, resume preparation, projects, certifications, higher studies, AI/ML and Electronics & Communication Engineering (ECE).

Unlike applications that rely on external generative AI APIs, CareerCompass demonstrates fundamental Natural Language Processing (NLP) and information retrieval techniques through a locally hosted web application.

Its retrieval pipeline combines text normalization, tokenization, stop-word removal, WordNet lemmatization, TF-IDF vectorization and cosine similarity to identify relevant questions from a curated FAQ dataset.

---

## 2. Problem Statement

Engineering students often encounter conflicting or overwhelming career advice across social media, online forums and other information sources.

Common challenges include:

* Choosing the right programming language and technical skills to learn.
* Preparing for coding assessments and technical interviews.
* Finding internships and understanding application processes.
* Building effective resumes and project portfolios.
* Exploring higher education options such as GATE and MS abroad.
* Identifying technology career opportunities for non-CS students, particularly those from ECE backgrounds.

CareerCompass addresses this problem by providing a structured, domain-specific reference assistant that retrieves concise answers from a predefined knowledge base.

---

## 3. Proposed Solution

CareerCompass provides a lightweight, locally hosted web-based FAQ assistant that matches natural language queries against a curated dataset of engineering career-related questions and answers.

The application uses classical NLP and machine learning techniques to:

* Normalize and preprocess user queries.
* Represent questions using TF-IDF features.
* Calculate cosine similarity between user queries and stored FAQ entries.
* Rank matching questions based on similarity scores.
* Apply a configurable similarity threshold to determine whether to return an answer or a fallback response.

The system does not depend on external generative AI APIs or require API keys. Missing NLTK resources may need to be downloaded during initial setup.

---

## 4. Key Features

### 4.1 Domain-Specific FAQ Knowledge Base

A curated FAQ dataset covering 10 engineering-related categories:

1. Career Paths
2. Programming
3. AI / ML
4. Internships
5. Placements
6. Resume Preparation
7. Projects
8. Certifications
9. Higher Studies
10. ECE Careers

### 4.2 NLP Preprocessing Pipeline

* Domain-aware normalization of technical terms such as `C++`, `C#` and `.NET`.
* Lowercase conversion and punctuation normalization.
* NLTK-based word tokenization.
* English stop-word removal.
* WordNet-based lemmatization using verb and noun normalization.

### 4.3 TF-IDF-Based FAQ Retrieval

* TF-IDF vectorization using unigrams and bigrams.
* Sublinear term-frequency scaling.
* Cosine similarity-based query matching.
* Ranking of the most relevant FAQ entries.
* Configurable similarity threshold.
* Fallback responses for empty, irrelevant or low-similarity queries.

### 4.4 Explainable Matching Process

The backend provides console output containing information such as:

* Original user query.
* Preprocessed query.
* Best-matching FAQ.
* Similarity score.
* Threshold-based retrieval decision.

### 4.5 Responsive Web Interface

* HTML5-based chat interface.
* CSS-based responsive styling.
* JavaScript-powered asynchronous communication with the Flask backend.
* Interactive question suggestions.
* Category-based FAQ navigation.
* Typing indicator.
* Session storage for conversation persistence.
* Clear chat functionality.

---

## 5. Technologies Used

| Layer                | Technology       | Purpose                                           |
| -------------------- | ---------------- | ------------------------------------------------- |
| Programming Language | Python 3.10+     | Backend development and NLP processing            |
| NLP Toolkit          | NLTK             | Tokenization, stop-word removal and lemmatization |
| Machine Learning     | Scikit-learn     | TF-IDF vectorization and cosine similarity        |
| Web Framework        | Flask            | Application routing and backend endpoints         |
| Frontend             | HTML5            | Web interface structure                           |
| Styling              | CSS3             | Responsive interface design                       |
| Client-side Logic    | JavaScript (ES6) | User interactions and asynchronous requests       |
| Testing              | Python unittest  | Automated unit testing                            |

---

## 6. NLP Processing & Matching Pipeline

CareerCompass processes user queries through a sequence of NLP and information retrieval operations.

### Query Processing Workflow

```text
             User Submits a Question
                       |
                       v
              Text Normalization
          (Lowercase, technical terms,
             punctuation handling)
                       |
                       v
                  Tokenization
                 (NLTK)
                       |
                       v
               Stop-Word Removal
                       |
                       v
              WordNet Lemmatization
                       |
                       v
               TF-IDF Vectorization
                       |
                       v
              Cosine Similarity
                       |
                       v
               Rank FAQ Matches
                       |
                       v
              Similarity Threshold
                  Evaluation
                  /       \
                YES        NO
                 |          |
                 v          v
           Return Best    Return
           FAQ Answer    Fallback
```

### Technical Explanation

**1. Text Normalization:** Converts text into a consistent format and handles selected technical terms.

**2. Tokenization:** Splits the processed query into individual tokens using NLTK.

**3. Stop-Word Removal:** Filters common English words that contribute limited information to the retrieval process.

**4. Lemmatization:** Converts words into their dictionary forms using WordNet.

**5. TF-IDF Vectorization:** Represents the processed query and FAQ entries as numerical feature vectors using unigrams and bigrams.

**6. Cosine Similarity:** Calculates similarity between the user query vector and the stored FAQ vectors.

**7. Threshold Evaluation:** Compares the highest similarity score against the configured threshold (0.25 by default).

**8. Response Generation:** Returns the corresponding FAQ answer when the threshold is met; otherwise, provides a fallback response.


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
