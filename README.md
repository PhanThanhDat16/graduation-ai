# AI Chatbot (Chainlit)

A simple AI chatbot project built with **Chainlit** for experimenting and developing LLM/AI features.

---

## Requirements

- Python **3.11+**
- [Poetry](https://python-poetry.org/)
- Git

---

## Installation

Clone this repository and enter the `ai` directory:

```bash
cd ai
```

Install dependencies:

```bash
poetry install
```

---

## Run the Chatbot API

Start the FastAPI server:

```bash
poetry run uvicorn main:app --host 0.0.0.0 --reload --port 8003
```

---

## Run Chainlit Chat UI

To start the Chainlit chat UI:

```bash
chainlit run app.py
```

Or, if you don't want to activate the poetry shell:

```bash
poetry run chainlit run app.py
```

---

## Access the Chat UI

After starting Chainlit, open your browser at:

```
http://localhost:8000
```

You'll see a chat interface similar to ChatGPT.

---

## Development

Install additional dependencies:

```bash
poetry add <package-name>
```

Run linting (Ruff):

```bash
poetry run ruff check .
```

Run type checking (MyPy):

```bash
poetry run mypy .
```

---

## Notes

- Dependency management by **Poetry**.
- Chatbot UI built on **Chainlit**.
- You can integrate **LangChain** or **OpenAI API** for real AI responses.

---

## License

MIT
