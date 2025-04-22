# **🌤 Weather Monitoring App — Frontend**

## 🧭 Overview

This is the **frontend** of the Weather Monitoring App. It provides a simple and interactive interface built with [Streamlit](https://streamlit.io/) and includes the following screens:

- 🔐 Sign In

- 🌤 Weather Dashboard

- 🔔 Notification Settings

- 📈 Weather History

## 🚀 Getting Started

### 📦 Requirements

- Python **3.12**
- Poetry **≥ 2.0.0**

**Or** use Docker if you prefer running in a containerized environment.

### ▶️ Run Locally (without Docker)

1. Install dependencies:

    ```bash
    poetry install
    ```

2. Start the app:

    ```bash
    poetry run streamlit run app.py
    ```

### 🐳 Run with Docker

```bash
docker run -d --name weather-frontend -p 8080:8501 ebob/weather-frontend:latest
```

Then open `http://localhost:8080` in your browser.
