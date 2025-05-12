# Safety-First Triage Assistant

This project provides a simple web interface to assess patient statements for risk level and suggest next steps, potentially using similar past cases for context.

It consists of:
*   A FastAPI backend (`app/`) handling risk assessment, RAG, and advice generation.
*   A Streamlit frontend (`streamlit_app.py`) providing the user interface.

## Configuration

### Streamlit Secrets (for Login)

This application uses a simple username/password authentication mechanism configured via Streamlit secrets.

1.  Create a directory named `.streamlit` in the root of your project if it doesn't already exist:
    ```bash
    mkdir .streamlit
    ```
2.  Inside the `.streamlit` directory, create a file named `secrets.toml`.
3.  Add the following content to `secrets.toml`, replacing `"your_username"` and `"your_password"` with your desired credentials:
    ```toml
    [auth]
    username = "your_username"
    password = "your_password"

    [api]
    OPENAI_API_KEY = "your api key"
    ```
    If this file is not present, or the `auth` section is missing, the application will default to `username: admin` and `password: changeme`.
    
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

3. **Setup api and credentials:**
    Create .env from .env_template and update the paths accordingly

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
