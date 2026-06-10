import json
import random
import time
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

import streamlit as st


IMAGE_TO_URL_INPUT = {
    "request_id": "IMG-POC-0001",
    "pipeline_type": "IMAGE_TO_URL",
    "brand": "nykaaman",
    "source": {
        "email_subject": "Image to URL",
        "drive_link": "https://drive.google.com/drive/folders/dummy-folder-id",
        "zip_file_name": "welcome-banners.zip",
    },
    "jenkins_job": "upload_file_to_create_static_url",
    "parameters": {
        "DirName": "",
        "File.zip": "welcome-banners.zip",
        "Useremail": "noc@nykaa.com",
    },
    "files": [
        "1stOrder-HP-App.jpg",
        "2ndOrder-HP-App.jpg",
        "3rdOrder-HP-App.jpg",
    ],
}

IMPORT_DB_BEAUTY_INPUT = {
    "request_id": "DB-POC-0001",
    "pipeline_type": "IMPORT_DB_BEAUTY",
    "brand": "nykaa-beauty",
    "source": {
        "email_subject": "Import DB pipeline for the below IDs",
        "requested_by": "keyur.rana@nykaa.com",
    },
    "category_ids": [
        "58308",
        "58312",
        "58309",
        "58310",
        "58324",
    ],
    "product_ids": [],
    "jenkins_jobs": [
        {
            "sequence": 1,
            "job_name": "edna_category_importer",
            "parameters": {},
        },
        {
            "sequence": 2,
            "job_name": "prod-pdp-plp-varnish-purge",
            "parameters": {
                "category_ids": "58308,58312,58309,58310,58324",
                "product_ids": "",
            },
        },
    ],
}


def main() -> None:
    st.set_page_config(
        page_title="Dummy Jenkins APIs",
        page_icon=":material/account_tree:",
        layout="wide",
    )

    st.title("Dummy Jenkins APIs")
    st.caption("Local Streamlit simulator for NOC automation pipeline responses.")

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
        )

    with db_tab:
        render_pipeline_tab(
            title="Import DB Pipeline (Beauty)",
            default_payload=IMPORT_DB_BEAUTY_INPUT,
            text_area_key="db_payload",
            run_button_key="run_db_pipeline",
            response_key="db_response",
            simulator=simulate_import_db_beauty_pipeline,
        )


def render_pipeline_tab(
    title: str,
    default_payload: dict[str, Any],
    text_area_key: str,
    run_button_key: str,
    response_key: str,
    simulator: Any,
) -> None:
    st.subheader(title)

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("#### Dummy Input")
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
                time.sleep(random.uniform(0.4, 1.2))
                st.session_state[response_key] = simulator(payload)

    with right:
        st.markdown("#### Dummy Output")
        response = st.session_state.get(response_key)
        if response:
            if response.get("status") == "SUCCESS":
                st.success("Pipeline completed successfully")
            else:
                st.error("Pipeline failed")
            st.json(response, expanded=True)
        else:
            st.info("Trigger the pipeline to generate a random dummy response.")


def simulate_image_to_url_pipeline(payload: dict[str, Any]) -> dict[str, Any]:
    success = random.choice([True, False])
    build_number = random.randint(800, 999)
    job_name = payload.get("jenkins_job", "upload_file_to_create_static_url")
    files = payload.get("files") or []
    user_email = (
        payload.get("parameters", {}).get("Useremail")
        or payload.get("source", {}).get("requested_by")
        or "noc@nykaa.com"
    )

    response = {
        "request_id": payload.get("request_id", "IMG-POC-0001"),
        "pipeline_type": payload.get("pipeline_type", "IMAGE_TO_URL"),
        "status": "SUCCESS" if success else "FAILURE",
        "jenkins": {
            "job_name": job_name,
            "build_number": build_number,
            "build_url": (
                "https://prod-jenkins-mumbai.nyk00-int.network/"
                f"job/{job_name}/{build_number}/"
            ),
            "duration_seconds": random.randint(25, 95),
        },
        "output": {
            "static_urls": [
                f"https://images-static.nykaa.com/media/{file_name}"
                for file_name in files
            ],
            "notified_email": user_email,
            "slack_channel": "#noc-nykaa",
        },
        "completed_at": utc_now(),
    }

    if not success:
        response["error"] = {
            "code": random.choice([
                "ZIP_EXTRACTION_FAILED",
                "STATIC_UPLOAD_FAILED",
                "JENKINS_BUILD_FAILED",
            ]),
            "message": "Dummy Jenkins run failed while creating static URLs.",
        }
        response["output"]["static_urls"] = []

    return response


def simulate_import_db_beauty_pipeline(payload: dict[str, Any]) -> dict[str, Any]:
    success = random.choice([True, False])
    category_ids = [str(value) for value in payload.get("category_ids", [])]
    product_ids = [str(value) for value in payload.get("product_ids", [])]
    jobs = payload.get("jenkins_jobs") or deepcopy(IMPORT_DB_BEAUTY_INPUT["jenkins_jobs"])
    failed_stage_index = random.randrange(len(jobs)) if jobs and not success else None

    stages = []
    for index, job in enumerate(jobs):
        job_name = job.get("job_name", f"stage-{index + 1}")
        stage_success = failed_stage_index is None or index < failed_stage_index
        stage_status = "SUCCESS" if stage_success else "FAILURE"
        build_number = random_build_number(job_name)

        stages.append({
            "job_name": job_name,
            "build_number": build_number,
            "status": stage_status,
            "duration_seconds": random.randint(45, 620),
            "build_url": build_url_for_job(job_name, build_number),
        })

        if stage_status == "FAILURE":
            break

    response = {
        "request_id": payload.get("request_id", "DB-POC-0001"),
        "pipeline_type": payload.get("pipeline_type", "IMPORT_DB_BEAUTY"),
        "status": "SUCCESS" if success else "FAILURE",
        "stages": stages,
        "output": {
            "imported_category_ids": category_ids if success else [],
            "purged_category_ids": category_ids if success else [],
            "product_ids": product_ids,
            "message": (
                "Import DB pipeline completed successfully and varnish cache purged."
                if success
                else "Import DB pipeline failed before all stages completed."
            ),
        },
        "completed_at": utc_now(),
    }

    if not success:
        failed_stage = stages[-1]["job_name"] if stages else "unknown"
        response["error"] = {
            "code": random.choice([
                "CATEGORY_IMPORT_FAILED",
                "VARNISH_PURGE_FAILED",
                "JENKINS_BUILD_FAILED",
            ]),
            "message": f"Dummy Jenkins run failed at stage: {failed_stage}.",
        }

    return response


def random_build_number(job_name: str) -> int:
    if job_name == "edna_category_importer":
        return random.randint(390, 460)
    if job_name == "prod-pdp-plp-varnish-purge":
        return random.randint(2800, 2950)
    return random.randint(100, 9999)


def build_url_for_job(job_name: str, build_number: int) -> str:
    if job_name == "edna_category_importer":
        return (
            "https://prod-jenkins-mumbai.nyk00-int.network/view/EDNA/"
            f"job/edna_category_importer/{build_number}/"
        )

    if job_name == "prod-pdp-plp-varnish-purge":
        return (
            "https://prod-jenkins-mumbai.nyk00-int.network/view/Devops/"
            "job/Flush-Varnish-Jobs/"
            f"job/prod-pdp-plp-varnish-purge/{build_number}/"
        )

    return f"https://prod-jenkins-mumbai.nyk00-int.network/job/{job_name}/{build_number}/"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


if __name__ == "__main__":
    main()
