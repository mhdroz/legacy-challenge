# Safety-First Triage Assistant

This project provides a simple web interface to assess patient statements for risk level and suggest next steps, potentially using similar past cases for context.

It consists of:
*   A FastAPI backend (`app/`) handling risk assessment, RAG, and advice generation.
*   A Streamlit frontend (`streamlit_app.py`) providing the user interface.

## Setup and Running Locally

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Install dependencies:**
    *Ensure you have a `requirements.txt` file.*
    ```bash
    pip install -r requirements.txt
    ```
    *(If you don't have `requirements.txt`, you can generate one using `pip freeze > requirements.txt` after installing necessary packages like `fastapi`, `uvicorn`, `streamlit`, `requests`, etc.)*

3.  **Run the backend API:**
    From the project root directory:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```

4.  **Run the Streamlit frontend:**
    Open a *new terminal* in the project root directory and activate the virtual environment again. Then run:
    ```bash
    streamlit run streamlit_app.py
    ```
    The app should open in your browser, likely at `http://localhost:8501`.
