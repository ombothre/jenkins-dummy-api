import json
import os
import time
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


def build_fastapi_url(path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if FASTAPI_BASE_URL:
        return urljoin(f"{FASTAPI_BASE_URL}/", path.lstrip("/"))
    return path



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
        "Local simulator for NOC automation pipeline responses. "
        "Edit the request JSON, trigger the pipeline, and review the dummy output."
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

    image_tab, db_tab = st.tabs([
        "Image Upload / Image to URL",
        "Import DB Pipeline (Beauty)",
    ])

    with image_tab:
        render_pipeline_tab(
            title="Image Upload / Image to URL Pipeline",
            default_payload=IMAGE_TO_URL_INPUT,
            text_area_key="image_payload",
            run_button_key="run_image_pipeline",
            response_key="image_response",
            simulator=simulate_image_to_url_pipeline,
            api_endpoint="/image-to-url",
        )

    with db_tab:
        render_pipeline_tab(
            title="Import DB Pipeline (Beauty)",
            default_payload=IMPORT_DB_BEAUTY_INPUT,
            text_area_key="db_payload",
            run_button_key="run_db_pipeline",
            response_key="db_response",
            simulator=simulate_import_db_beauty_pipeline,
            api_endpoint="/import-db-beauty",
        )


if __name__ == "__main__":
    main()
