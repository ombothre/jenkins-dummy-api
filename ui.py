import json
import os
import time
import urllib.error
import urllib.request
from typing import Any
from urllib.parse import urljoin

from dotenv import load_dotenv

from common import (
    IMAGE_TO_URL_INPUT,
    IMPORT_DB_BEAUTY_INPUT,
    simulate_image_to_url_pipeline,
    simulate_import_db_beauty_pipeline,
)

load_dotenv()

FASTAPI_BASE_URL = os.environ.get("FASTAPI_BASE_URL", "https://jenkins-dummy-api.onrender.com").strip().rstrip("/")
FASTAPI_DOCS_URL = os.environ.get("FASTAPI_DOCS_URL", "/docs").strip()

API_ENDPOINTS: dict[str, dict[str, Any]] = {
    "/image-to-url": {
        "method": "POST",
        "title": "Image Upload / Image to URL",
        "description": "Convert images to static URLs",
        "sample": IMAGE_TO_URL_INPUT,
    },
    "/import-db-beauty": {
        "method": "POST",
        "title": "Import DB Pipeline (Beauty)",
        "description": "Import database beauty data",
        "sample": IMPORT_DB_BEAUTY_INPUT,
    },
    "/image-varnish-purge": {
        "method": "POST",
        "title": "Image Varnish Purge",
        "description": "Purge image Varnish cache",
        "sample": {
            "request_id": "IMG-POC-0002",
            "pipeline_type": "IMAGE_VARNISH_PURGE",
            "brand": "nykaaman",
            "image_urls": [
                "https://images-static.nykaa.com/media/1stOrder-HP-App.jpg",
                "https://images-static.nykaa.com/media/2ndOrder-HP-App.jpg",
            ],
            "jenkins_job": "Nykaaman-varnish-url-flush",
        },
    },
    "/image-cloudflare-purge": {
        "method": "POST",
        "title": "Image Cloudflare Purge",
        "description": "Purge image Cloudflare cache",
        "sample": {
            "request_id": "IMG-POC-0003",
            "pipeline_type": "IMAGE_CLOUDFLARE_PURGE",
            "brand": "nykaaman",
            "image_urls": [
                "https://images-static.nykaa.com/media/1stOrder-HP-App.jpg",
                "https://images-static.nykaa.com/media/2ndOrder-HP-App.jpg",
            ],
            "jenkins_job": "cloudflare-url-cache-purge-man",
        },
    },
    "/health": {
        "method": "GET",
        "title": "Health Check",
        "description": "Check that the API is reachable",
        "sample": None,
    },
}


def build_fastapi_url(path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if FASTAPI_BASE_URL:
        return urljoin(f"{FASTAPI_BASE_URL}/", path.lstrip("/"))
    return path


def perform_api_request(endpoint: str, payload: dict[str, Any] | None = None) -> tuple[dict[str, Any] | str, int]:
    api_url = build_fastapi_url(endpoint)
    if payload is None:
        request = urllib.request.Request(api_url, method="GET")
    else:
        request = urllib.request.Request(
            api_url,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={"Content-Type": "application/json"},
        )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read().decode("utf-8")
            try:
                return json.loads(body), response.status
            except json.JSONDecodeError:
                return body, response.status

    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            error_body = json.loads(body)
        except json.JSONDecodeError:
            error_body = body or exc.reason
        return {"error": error_body, "reason": exc.reason}, exc.code
    except urllib.error.URLError as exc:
        return {"error": str(exc.reason)}, 0


def render_api_list() -> None:
    import streamlit as st

    st.subheader("Available APIs")
    st.markdown(
        "These sample endpoints are available for the Jenkins dummy APIs. "
        "You can use the API Explorer tab to test any of them with a sample body."
    )

    for path, metadata in API_ENDPOINTS.items():
        method = metadata["method"]
        description = metadata["description"]
        st.markdown(
            f"**{method}** `{build_fastapi_url(path)}`  \n{description}"
        )


def render_api_explorer_tab() -> None:
    import streamlit as st

    st.subheader("API Explorer")
    st.markdown(
        "Use the API Explorer to send sample requests to the configured FastAPI backend. "
        "Edit the payload, then execute the request and inspect the response below."
    )

    endpoint_choices = [f"{data['method']} {path}" for path, data in API_ENDPOINTS.items()]
    selected = st.selectbox("Select endpoint", endpoint_choices, index=0)
    selected_path = selected.split(" ", 1)[1]
    endpoint_data = API_ENDPOINTS[selected_path]

    st.markdown(f"**Description:** {endpoint_data['description']}")
    st.markdown(f"**URL:** `{build_fastapi_url(selected_path)}`")

    payload = endpoint_data["sample"]
    payload_key = f"api_explorer_payload_{selected_path.strip('/').replace('/', '_') or 'root'}"

    if payload is not None:
        payload_text = st.text_area(
            "Request JSON",
            value=json.dumps(payload, indent=2),
            height=320,
            key=payload_key,
        )
    else:
        payload_text = ""
        st.info("This endpoint does not require a request body.")

    if st.button("Send API Request", key=f"api_explorer_send_{selected_path.strip('/').replace('/', '_') or 'root'}"):
        if payload is not None:
            try:
                payload = json.loads(payload_text)
            except json.JSONDecodeError as exc:
                st.error(f"Invalid JSON: {exc.msg} at line {exc.lineno}, column {exc.colno}")
                return
        else:
            payload = None

        with st.spinner("Sending request to API..."):
            response_body, status_code = perform_api_request(selected_path, payload)
            st.markdown(f"**Status code:** {status_code}")
            if isinstance(response_body, dict):
                st.json(response_body, expanded=True)
            else:
                st.code(response_body)


def render_api_documentation_tab() -> None:
    import streamlit as st

    st.subheader("API Documentation")
    st.markdown(
        "This section shows the available API endpoints, request details, and sample payloads "
        "in markdown format. Use it as quick reference documentation for the FastAPI backend."
    )

    for path, metadata in API_ENDPOINTS.items():
        method = metadata["method"]
        description = metadata["description"]
        sample = metadata["sample"]

        st.markdown(f"### `{method} {path}`")
        st.markdown(f"{description}")
        st.markdown(f"**URL:** `{build_fastapi_url(path)}`")

        if sample is not None:
            st.markdown("**Sample request body**")
            st.code(json.dumps(sample, indent=2), language="json")
        else:
            st.markdown("**Sample request body**: None required for this endpoint.")

        curl_payload = "" if sample is None else json.dumps(sample, indent=2)
        if sample is not None:
            escaped_payload = curl_payload.replace("'", "\\'")
            st.markdown("**Sample curl command**")
            st.code(
                "curl -X {} \"{}\" \\\n  -H 'Content-Type: application/json' \\\n  -d '{}'".format(
                    method,
                    build_fastapi_url(path),
                    escaped_payload,
                ),
                language="bash",
            )
        else:
            st.markdown("**Sample curl command**")
            st.code(f"curl -X {method} \"{build_fastapi_url(path)}\"", language="bash")

        st.write("---")


def apply_streamlit_light_theme() -> None:
    # Keep Streamlit's normal light theme styling with default controls.
    # Any custom CSS here can make the UI look less polished, so we keep it minimal.
    return


def render_pipeline_tab(
    title: str,
    default_payload: dict[str, Any],
    text_area_key: str,
    run_button_key: str,
    response_key: str,
    simulator: Any,
    api_endpoint: str,
) -> None:
    import streamlit as st

    st.subheader(title)
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("#### Request payload")
        payload_text = st.text_area(
            "Request JSON",
            value=json.dumps(default_payload, indent=2),
            height=520,
            key=text_area_key,
            label_visibility="collapsed",
        )

        run_clicked = st.button("Trigger Jenkins Pipeline", key=run_button_key)

    if run_clicked:
        try:
            payload = json.loads(payload_text)
        except json.JSONDecodeError as exc:
            st.error(f"Invalid JSON: {exc.msg} at line {exc.lineno}, column {exc.colno}")
        else:
            with st.spinner("Triggering dummy Jenkins job..."):
                time.sleep(0.5)
                st.session_state[response_key] = simulator(payload)

    with right:
        st.markdown("#### Response preview")
        response = st.session_state.get(response_key)
        if response:
            if response.get("status") == "SUCCESS":
                st.success("Pipeline completed successfully")
            else:
                st.error("Pipeline failed")
            st.json(response, expanded=True)
        else:
            st.info("Trigger the pipeline to generate a random dummy response.")

        with st.expander("API usage"):
            api_request_url = build_fastapi_url(api_endpoint)
            st.markdown(f"**POST** `{api_request_url}`")
            st.markdown("Use this payload body for a JSON POST request:")
            st.code(json.dumps(default_payload, indent=2), language="json")
            st.markdown("Content-Type: `application/json` is required for API requests.")


def main() -> None:
    import streamlit as st

    st.set_page_config(
        page_title="Jenkins Dummy APIs",
        page_icon=":gear:",
        layout="wide",
    )
    apply_streamlit_light_theme()

    st.title("Jenkins Dummy APIs")
    st.markdown(
        "Interactive API documentation and explorer for the Jenkins dummy backend. "
        "Use the tabs to view API docs or test requests directly."
    )
    api_docs_url = build_fastapi_url(FASTAPI_DOCS_URL)
    api_root_url = build_fastapi_url("/")

    if FASTAPI_BASE_URL:
        st.markdown(
            f'<div style="display:flex; gap:10px; margin-top:10px;">'
            f'<a href="{api_root_url}" target="_blank" '
            'style="display:inline-block; padding:10px 16px; background-color:#111827; color:#ffffff; '
            'border-radius:8px; text-decoration:none; font-weight:600;">Open FastAPI API</a>'
            f'<a href="{api_docs_url}" target="_blank" '
            'style="display:inline-block; padding:10px 16px; background-color:#4f46e5; color:#ffffff; '
            'border-radius:8px; text-decoration:none; font-weight:600;">Open FastAPI Docs</a>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<a href="{api_docs_url}" target="_blank" '
            'style="display:inline-block; padding:10px 16px; margin-top:10px; '
            'background-color:#4f46e5; color:#ffffff; border-radius:8px; '
            'text-decoration:none; font-weight:600;">Open FastAPI Docs</a>',
            unsafe_allow_html=True,
        )

    api_docs_tab, api_explorer_tab = st.tabs([
        "API Docs",
        "API Explorer",
    ])

    with api_docs_tab:
        render_api_documentation_tab()

    with api_explorer_tab:
        render_api_explorer_tab()


if __name__ == "__main__":
    main()
