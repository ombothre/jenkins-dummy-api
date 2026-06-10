# Jenkins Dummy APIs

Dummy HTTP endpoints that simulate NOC Jenkins pipeline responses.

## Run the Streamlit UI

```bash
streamlit run ui.py --server.port 8501
```

This also starts the FastAPI API server automatically on `http://127.0.0.1:8000` if it is not already running.

Then open the browser URL shown in the terminal.

## Run as HTTP API

```bash
uvicorn app:app --reload
```

Open FastAPI docs at:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

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
