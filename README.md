# ∂ QUANT MEMORIA

> **Advanced Quantitative Finance Learning Platform**  
> Adaptive spaced repetition for BCRP Financial Engineering Program

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/streamlit-1.32+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 What This Is

Quant Memoria is a **professional learning engineering platform** — not a basic flashcard app. It combines:

- **Modified SM-2 algorithm** with Ebbinghaus forgetting curve modeling
- **Active recall & retrieval practice** with 6-level rating system
- **Error-driven learning** with persistent error tracking
- **Formula breakdowns** with LaTeX, derivations, intuition, and Python code
- **Document ingestion** from PDF/TXT/DOCX → auto-generated cards
- **Analytics dashboard** with mastery heatmaps and retention curves

### Domains Covered

| Domain | Topics |
|--------|--------|
| Financial Engineering | Black-Scholes, Itô's Lemma, PDEs, Martingales, Monte Carlo |
| Portfolio Management | Mean-Variance, CAPM, Factor Models, Robust Optimization |
| Interest Rate Models | Vasicek, CIR, Hull-White, HJM, Yield Curves |
| Financial Econometrics | ARCH/GARCH, ARIMA, Cointegration, VAR, High-Frequency |
| Financial Stability | Systemic Risk, CoVaR, Macroprudential Policy, Basel III |

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/quant-memoria.git
cd quant-memoria

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app auto-seeds a starter library of curated flashcards on first run.

---

## 📁 Project Structure

```
quant_memoria/
├── app.py                    # Main Streamlit application
├── requirements.txt
├── .streamlit/
│   └── config.toml           # Dark theme configuration
│
├── core/
│   ├── srs_engine.py         # Spaced repetition algorithm (SM-2)
│   ├── card_model.py         # Card schema & topic taxonomy
│   └── store.py              # Persistence layer (JSON → SQLite ready)
│
├── data/
│   ├── seed_cards.py         # Curated starter flashcard deck
│   ├── cards/library.json    # Card database (auto-created)
│   └── sessions/             # SRS states & analytics (auto-created)
│
└── utils/
    ├── analytics.py          # Learning metrics & visualizations
    └── ingestion.py          # PDF/TXT/DOCX → flashcard pipeline
```

---

## 🧠 Cognitive Science Foundation

### Spaced Repetition (SM-2)
Modified SuperMemo SM-2 with:
- Adaptive ease factor (1.3 to 5.0 range)
- Error penalty on ease factor
- Ebbinghaus retention estimation: `R = e^(-t/S)`

### Active Recall Hierarchy
Cards are typed by cognitive load:
1. **Concept** — definitional understanding
2. **Formula** — mathematical expression
3. **Derivation** — step-by-step proof
4. **Coding** — implementation
5. **Application** — real-world use case
6. **Interview** — synthesis under pressure
7. **Central Bank** — policy reasoning

### Mastery Score
`mastery = 0.5 × retention + 0.5 × (reps/10) − 0.05 × errors`

---

## 📥 Importing Your BCRP Documents

1. Go to **Import Docs** in the sidebar
2. Upload individual files (PDF, TXT, DOCX) via the upload tab
3. Or point to your local folder:  
   `C:\Users\usuario\OneDrive\Desktop\FRANCO\CURSOS DE EXTENSION\BCRP`
4. Cards are automatically extracted and added to the library

**Tip:** Convert Word documents to TXT for best text extraction quality.

---

## ☁️ Streamlit Cloud Deployment

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo → set main file: `app.py`
4. Deploy 🚀

Note: On Streamlit Cloud, local folder ingestion is disabled. Use file upload instead.

---

## 🔭 Roadmap

### Phase 1 (Current) ✅
- SM-2 spaced repetition engine
- Rich flashcard schema (LaTeX, code, derivations)
- Analytics dashboard
- Document ingestion

### Phase 2 (Planned)
- [ ] LLM-powered auto card generation (Claude API)
- [ ] Semantic search across card library
- [ ] Quiz mode (MCQ, fill-in-the-blank)
- [ ] MATLAB snippet support

### Phase 3 (Future)
- [ ] Vector database for semantic similarity
- [ ] AI tutor mode (Socratic questioning)
- [ ] Speech-to-text for hands-free review
- [ ] Collaborative decks

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit + Plotly |
| SRS Engine | Custom Python (SM-2) |
| Persistence | JSON (→ SQLite ready) |
| Math | LaTeX via Streamlit native |
| PDF | PyPDF2 |
| DOCX | python-docx |
| Analytics | Plotly + custom metrics |

---

## 📄 License

MIT License — free for personal and academic use.

---

*Built for the BCRP Financial Engineering intensive program.*  
*Quant Memoria — because forgetting is the enemy of expertise.*
