# Jenkins Dummy APIs

Dummy HTTP endpoints that simulate NOC Jenkins pipeline responses.

## Run the Streamlit UI

1. Copy the example env file:

```bash
cp .env.example .env
```

2. Edit `.env` if needed.

3. Start Streamlit:

```bash
streamlit run ui.py --server.port 8501
```

This starts only the Streamlit UI. Run the FastAPI server separately with `uvicorn app:app --reload`.

Then open the browser URL shown in the terminal.

## Run as HTTP API

```bash
uvicorn app:app --reload
```

Open FastAPI docs at `/docs` or `/redoc` on the API host.

If the API is hosted separately, set `FASTAPI_DOCS_URL` in `.env` before running Streamlit.

## Run both together

```bash
./run-both.sh
```

This starts:

- FastAPI on `http://127.0.0.1:8000`
- Streamlit UI on `http://127.0.0.1:8501`

Available endpoints:

- `POST /image-to-url`
- `POST /import-db-beauty`
- `GET /health`
- `GET /`

## Example curl

```bash
curl -X POST http://127.0.0.1:8000/image-to-url \
  -H 'Content-Type: application/json' \
  -d '{"request_id":"IMG-POC-0001","pipeline_type":"IMAGE_TO_URL","brand":"nykaaman","jenkins_job":"upload_file_to_create_static_url","files":["1stOrder-HP-App.jpg"]}'
```
