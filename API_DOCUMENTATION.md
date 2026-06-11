# Jenkins Dummy APIs Documentation

## Overview

Jenkins Dummy APIs provides mock HTTP endpoints that simulate NOC Jenkins pipeline responses for testing and development purposes. The API is built with [FastAPI](https://fastapi.tiangolo.com/) and includes pipeline simulators for: Image-to-URL, Import-DB-Beauty, Image Varnish Purge, and Image Cloudflare Purge.

- **Base URL**: `http://127.0.0.1:8000` (default local development)
- **Documentation**: Available at `/docs` (Swagger UI) or `/redoc` (ReDoc)
- **Version**: 0.1.0

---

## Endpoints

### 1. Root Endpoint

**GET** `/`

Returns information about available endpoints and the API.

#### Response

```json
{
  "message": "Jenkins Dummy APIs",
  "description": "Dummy endpoints that simulate NOC Jenkins pipeline responses.",
  "endpoints": [
    "/image-to-url",
    "/import-db-beauty",
    "/image-varnish-purge",
    "/image-cloudflare-purge",
    "/health"
  ]
}
```

---

### 2. Health Check

**GET** `/health`

Simple health check endpoint to verify the API is running.

#### Response

```json
{
  "status": "ok"
}
```

---

### 3. Image to URL Pipeline

**POST** `/image-to-url`

Simulates the Jenkins pipeline that converts images to static URLs. This endpoint accepts image details and returns a simulated Jenkins build response with generated static URLs.

#### Request Body

```json
{
  "request_id": "IMG-POC-0001",
  "pipeline_type": "IMAGE_TO_URL",
  "brand": "nykaaman",
  "source": {
    "email_subject": "Image to URL",
    "drive_link": "https://drive.google.com/drive/folders/dummy-folder-id",
    "zip_file_name": "welcome-banners.zip"
  },
  "jenkins_job": "upload_file_to_create_static_url",
  "parameters": {
    "DirName": "",
    "File.zip": "welcome-banners.zip",
    "Useremail": "noc@nykaa.com"
  },
  "files": [
    "1stOrder-HP-App.jpg",
    "2ndOrder-HP-App.jpg",
    "3rdOrder-HP-App.jpg"
  ]
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `request_id` | string | ✓ | Unique identifier for the request |
| `pipeline_type` | string | ✓ | Must be `IMAGE_TO_URL` |
| `brand` | string | ✓ | Brand identifier (e.g., "nykaaman") |
| `source` | object | ✓ | Source information for the image pipeline |
| `source.email_subject` | string | ✓ | Email subject |
| `source.drive_link` | string | ✓ | Google Drive link to source files |
| `source.zip_file_name` | string | ✓ | Name of the ZIP file |
| `jenkins_job` | string | ✓ | Jenkins job name |
| `parameters` | object | ✓ | Jenkins job parameters |
| `parameters.DirName` | string | ✓ | Directory name |
| `parameters.File.zip` | string | ✓ | ZIP file name |
| `parameters.Useremail` | string | ✓ | Email address for notification |
| `files` | array | ✓ | List of image file names |

#### Response (Success - 200 OK)

```json
{
  "request_id": "IMG-POC-0001",
  "pipeline_type": "IMAGE_TO_URL",
  "status": "SUCCESS",
  "jenkins": {
    "job_name": "upload_file_to_create_static_url",
    "build_number": 850,
    "build_url": "https://prod-jenkins-mumbai.nyk00-int.network/job/upload_file_to_create_static_url/850/",
    "duration_seconds": 52
  },
  "output": {
    "static_urls": [
      "https://images-static.nykaa.com/media/1stOrder-HP-App.jpg",
      "https://images-static.nykaa.com/media/2ndOrder-HP-App.jpg",
      "https://images-static.nykaa.com/media/3rdOrder-HP-App.jpg"
    ],
    "notified_email": "noc@nykaa.com",
    "slack_channel": "#noc-nykaa"
  },
  "completed_at": "2024-06-11T10:30:45Z"
}
```

#### Response (Failure - 200 OK)

```json
{
  "request_id": "IMG-POC-0001",
  "pipeline_type": "IMAGE_TO_URL",
  "status": "FAILURE",
  "jenkins": {
    "job_name": "upload_file_to_create_static_url",
    "build_number": 875,
    "build_url": "https://prod-jenkins-mumbai.nyk00-int.network/job/upload_file_to_create_static_url/875/",
    "duration_seconds": 38
  },
  "output": {
    "static_urls": [],
    "notified_email": "noc@nykaa.com",
    "slack_channel": "#noc-nykaa"
  },
  "error": {
    "code": "ZIP_EXTRACTION_FAILED",
    "message": "Dummy Jenkins run failed while creating static URLs."
  },
  "completed_at": "2024-06-11T10:31:15Z"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `request_id` | string | Echo of the request ID |
| `pipeline_type` | string | Echo of the pipeline type |
| `status` | string | Either `SUCCESS` or `FAILURE` (randomly chosen) |
| `jenkins` | object | Jenkins execution details |
| `jenkins.job_name` | string | Name of the executed job |
| `jenkins.build_number` | integer | Randomly generated build number |
| `jenkins.build_url` | string | URL to the Jenkins build |
| `jenkins.duration_seconds` | integer | Simulated execution duration |
| `output` | object | Pipeline output data |
| `output.static_urls` | array | Generated static URLs (empty on failure) |
| `output.notified_email` | string | Email address that will be notified |
| `output.slack_channel` | string | Slack channel for notifications |
| `error` | object | Present only on failure |
| `error.code` | string | Error code (one of: `ZIP_EXTRACTION_FAILED`, `STATIC_UPLOAD_FAILED`, `JENKINS_BUILD_FAILED`) |
| `error.message` | string | Error message |
| `completed_at` | string | ISO 8601 timestamp when the pipeline completed |

---

### 4. Import DB Beauty Pipeline

**POST** `/import-db-beauty`

Simulates the Jenkins pipeline for importing database beauty data and purging Varnish cache. This multi-stage pipeline executes category import and varnish cache purge operations.

#### Request Body

```json
{
  "request_id": "DB-POC-0001",
  "pipeline_type": "IMPORT_DB_BEAUTY",
  "brand": "nykaa-beauty",
  "source": {
    "email_subject": "Import DB pipeline for the below IDs",
    "requested_by": "keyur.rana@nykaa.com"
  },
  "category_ids": [
    "58308",
    "58312",
    "58309",
    "58310",
    "58324"
  ],
  "product_ids": [],
  "jenkins_jobs": [
    {
      "sequence": 1,
      "job_name": "edna_category_importer",
      "parameters": {}
    },
    {
      "sequence": 2,
      "job_name": "prod-pdp-plp-varnish-purge",
      "parameters": {
        "category_ids": "58308,58312,58309,58310,58324",
        "product_ids": ""
      }
    }
  ]
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `request_id` | string | ✓ | Unique identifier for the request |
| `pipeline_type` | string | ✓ | Must be `IMPORT_DB_BEAUTY` |
| `brand` | string | ✓ | Brand identifier (e.g., "nykaa-beauty") |
| `source` | object | ✓ | Source information |
| `source.email_subject` | string | ✓ | Email subject |
| `source.requested_by` | string | ✓ | Email of requester |
| `category_ids` | array | ✓ | List of category IDs to import |
| `product_ids` | array | ✓ | List of product IDs (can be empty) |
| `jenkins_jobs` | array | ✓ | Array of Jenkins jobs to execute in sequence |
| `jenkins_jobs[].sequence` | integer | ✓ | Job execution order |
| `jenkins_jobs[].job_name` | string | ✓ | Name of the Jenkins job |
| `jenkins_jobs[].parameters` | object | ✓ | Job-specific parameters |

#### Response (Success - 200 OK)

```json
{
  "request_id": "DB-POC-0001",
  "pipeline_type": "IMPORT_DB_BEAUTY",
  "status": "SUCCESS",
  "stages": [
    {
      "job_name": "edna_category_importer",
      "build_number": 420,
      "status": "SUCCESS",
      "duration_seconds": 285,
      "build_url": "https://prod-jenkins-mumbai.nyk00-int.network/view/EDNA/job/edna_category_importer/420/"
    },
    {
      "job_name": "prod-pdp-plp-varnish-purge",
      "build_number": 2900,
      "status": "SUCCESS",
      "duration_seconds": 120,
      "build_url": "https://prod-jenkins-mumbai.nyk00-int.network/view/Devops/job/Flush-Varnish-Jobs/job/prod-pdp-plp-varnish-purge/2900/"
    }
  ],
  "output": {
    "imported_category_ids": [
      "58308",
      "58312",
      "58309",
      "58310",
      "58324"
    ],
    "purged_category_ids": [
      "58308",
      "58312",
      "58309",
      "58310",
      "58324"
    ],
    "product_ids": [],
    "message": "Import DB pipeline completed successfully and varnish cache purged."
  },
  "completed_at": "2024-06-11T11:15:30Z"
}
```

#### Response (Failure - 200 OK)

```json
{
  "request_id": "DB-POC-0001",
  "pipeline_type": "IMPORT_DB_BEAUTY",
  "status": "FAILURE",
  "stages": [
    {
      "job_name": "edna_category_importer",
      "build_number": 405,
      "status": "FAILURE",
      "duration_seconds": 95,
      "build_url": "https://prod-jenkins-mumbai.nyk00-int.network/view/EDNA/job/edna_category_importer/405/"
    }
  ],
  "output": {
    "imported_category_ids": [],
    "purged_category_ids": [],
    "product_ids": [],
    "message": "Import DB pipeline failed before all stages completed."
  },
  "error": {
    "code": "CATEGORY_IMPORT_FAILED",
    "message": "Dummy Jenkins run failed at stage: edna_category_importer."
  },
  "completed_at": "2024-06-11T11:16:15Z"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `request_id` | string | Echo of the request ID |
| `pipeline_type` | string | Echo of the pipeline type |
| `status` | string | Either `SUCCESS` or `FAILURE` (randomly chosen) |
| `stages` | array | Array of executed pipeline stages |
| `stages[].job_name` | string | Name of the Jenkins job |
| `stages[].build_number` | integer | Randomly generated build number |
| `stages[].status` | string | Either `SUCCESS` or `FAILURE` |
| `stages[].duration_seconds` | integer | Simulated execution duration |
| `stages[].build_url` | string | URL to the Jenkins build |
| `output` | object | Pipeline output data |
| `output.imported_category_ids` | array | Categories that were imported (empty on failure) |
| `output.purged_category_ids` | array | Categories that were cache-purged (empty on failure) |
| `output.product_ids` | array | Product IDs (from request) |
| `output.message` | string | Human-readable status message |
| `error` | object | Present only on failure |
| `error.code` | string | Error code (one of: `CATEGORY_IMPORT_FAILED`, `VARNISH_PURGE_FAILED`, `JENKINS_BUILD_FAILED`) |
| `error.message` | string | Error message indicating the failed stage |
| `completed_at` | string | ISO 8601 timestamp when the pipeline completed |

---

### 5. Image Varnish Purge

**POST** `/image-varnish-purge`

Simulates the Jenkins pipeline for purging image Varnish cache. This is a recovery endpoint used independently (not automatically called after image-to-url success).

#### Request Body

```json
{
  "request_id": "IMG-POC-0001",
  "brand": "nykaaman",
  "image_urls": [
    "https://images-static.nykaa.com/media/1stOrder-HP-App.jpg",
    "https://images-static.nykaa.com/media/2ndOrder-HP-App.jpg"
  ],
  "jenkins_job": "Nykaaman-varnish-url-flush"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `request_id` | string | ✓ | Unique identifier for the request |
| `brand` | string | ✓ | Brand identifier (e.g., "nykaaman") |
| `image_urls` | array | ✓ | List of image URLs to purge |
| `jenkins_job` | string | ✓ | Jenkins job name |

#### Response (Success - 200 OK)

```json
{
  "request_id": "IMG-POC-0001",
  "pipeline_type": "IMAGE_VARNISH_PURGE",
  "status": "SUCCESS",
  "jenkins": {
    "job_name": "Nykaaman-varnish-url-flush",
    "build_number": 3122,
    "build_url": "https://prod-jenkins-mumbai.nyk00-int.network/job/Flush-Varnish-Jobs/job/Nykaaman-varnish-url-flush/3122/",
    "duration_seconds": 35
  },
  "output": {
    "purged_urls": [
      "https://images-static.nykaa.com/media/1stOrder-HP-App.jpg",
      "https://images-static.nykaa.com/media/2ndOrder-HP-App.jpg"
    ],
    "message": "Image Varnish cache purged successfully."
  },
  "completed_at": "2026-06-11T10:30:45Z"
}
```

#### Response (Failure - 200 OK)

```json
{
  "request_id": "IMG-POC-0001",
  "pipeline_type": "IMAGE_VARNISH_PURGE",
  "status": "FAILURE",
  "jenkins": {
    "job_name": "Nykaaman-varnish-url-flush",
    "build_number": 3123,
    "build_url": "https://prod-jenkins-mumbai.nyk00-int.network/job/Flush-Varnish-Jobs/job/Nykaaman-varnish-url-flush/3123/",
    "duration_seconds": 22
  },
  "output": {
    "purged_urls": [],
    "message": "Image Varnish purge failed."
  },
  "error": {
    "code": "IMAGE_VARNISH_PURGE_FAILED",
    "message": "Dummy Jenkins run failed while purging image Varnish cache."
  },
  "completed_at": "2026-06-11T10:31:10Z"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `request_id` | string | Echo of the request ID |
| `pipeline_type` | string | Always `IMAGE_VARNISH_PURGE` |
| `status` | string | Either `SUCCESS` or `FAILURE` (randomly chosen) |
| `jenkins` | object | Jenkins execution details |
| `jenkins.job_name` | string | Name of the executed job |
| `jenkins.build_number` | integer | Randomly generated build number (3100-3200) |
| `jenkins.build_url` | string | URL to the Jenkins build |
| `jenkins.duration_seconds` | integer | Simulated execution duration (15-45 seconds) |
| `output` | object | Pipeline output data |
| `output.purged_urls` | array | URLs that were purged (empty on failure) |
| `output.message` | string | Status message |
| `error` | object | Present only on failure |
| `error.code` | string | Error code: `IMAGE_VARNISH_PURGE_FAILED` |
| `error.message` | string | Error message |
| `completed_at` | string | ISO 8601 timestamp when the pipeline completed |

---

### 6. Image Cloudflare Purge

**POST** `/image-cloudflare-purge`

Simulates the Jenkins pipeline for purging image Cloudflare cache. This is a recovery endpoint used independently (not automatically called after image-to-url success).

#### Request Body

```json
{
  "request_id": "IMG-POC-0001",
  "brand": "nykaaman",
  "image_urls": [
    "https://images-static.nykaa.com/media/1stOrder-HP-App.jpg",
    "https://images-static.nykaa.com/media/2ndOrder-HP-App.jpg"
  ],
  "jenkins_job": "cloudflare-url-cache-purge-man"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `request_id` | string | ✓ | Unique identifier for the request |
| `brand` | string | ✓ | Brand identifier (e.g., "nykaaman") |
| `image_urls` | array | ✓ | List of image URLs to purge (with https://) |
| `jenkins_job` | string | ✓ | Jenkins job name |

#### Response (Success - 200 OK)

```json
{
  "request_id": "IMG-POC-0001",
  "pipeline_type": "IMAGE_CLOUDFLARE_PURGE",
  "status": "SUCCESS",
  "jenkins": {
    "job_name": "cloudflare-url-cache-purge-man",
    "build_number": 4188,
    "build_url": "https://prod-jenkins-mumbai.nyk00-int.network/job/Flush-Varnish-Jobs/job/cloudflare-url-cache-purge-man/4188/",
    "duration_seconds": 28
  },
  "output": {
    "purged_urls": [
      "images-static.nykaa.com/media/1stOrder-HP-App.jpg",
      "images-static.nykaa.com/media/2ndOrder-HP-App.jpg"
    ],
    "message": "Image Cloudflare cache purged successfully."
  },
  "completed_at": "2026-06-11T10:35:45Z"
}
```

#### Response (Failure - 200 OK)

```json
{
  "request_id": "IMG-POC-0001",
  "pipeline_type": "IMAGE_CLOUDFLARE_PURGE",
  "status": "FAILURE",
  "jenkins": {
    "job_name": "cloudflare-url-cache-purge-man",
    "build_number": 4189,
    "build_url": "https://prod-jenkins-mumbai.nyk00-int.network/job/Flush-Varnish-Jobs/job/cloudflare-url-cache-purge-man/4189/",
    "duration_seconds": 19
  },
  "output": {
    "purged_urls": [],
    "message": "Image Cloudflare purge failed."
  },
  "error": {
    "code": "IMAGE_CLOUDFLARE_PURGE_FAILED",
    "message": "Dummy Jenkins run failed while purging image Cloudflare cache."
  },
  "completed_at": "2026-06-11T10:36:10Z"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `request_id` | string | Echo of the request ID |
| `pipeline_type` | string | Always `IMAGE_CLOUDFLARE_PURGE` |
| `status` | string | Either `SUCCESS` or `FAILURE` (randomly chosen) |
| `jenkins` | object | Jenkins execution details |
| `jenkins.job_name` | string | Name of the executed job |
| `jenkins.build_number` | integer | Randomly generated build number (4150-4250) |
| `jenkins.build_url` | string | URL to the Jenkins build |
| `jenkins.duration_seconds` | integer | Simulated execution duration (10-35 seconds) |
| `output` | object | Pipeline output data |
| `output.purged_urls` | array | URLs that were purged with `https://` prefix removed (empty on failure) |
| `output.message` | string | Status message |
| `error` | object | Present only on failure |
| `error.code` | string | Error code: `IMAGE_CLOUDFLARE_PURGE_FAILED` |
| `error.message` | string | Error message |
| `completed_at` | string | ISO 8601 timestamp when the pipeline completed |

---

## Error Handling

### HTTP Status Codes

- **200 OK** - Request was processed (note: `status` field in response indicates success/failure)
- **422 Unprocessable Entity** - Invalid request payload or missing required fields
- **500 Internal Server Error** - Unexpected server error

### Error Response Structure

All errors include a `status` field set to `"FAILURE"` and an `error` object with:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

### Possible Error Codes

**Image-to-URL Pipeline:**
- `ZIP_EXTRACTION_FAILED` - Failed to extract the ZIP file
- `STATIC_UPLOAD_FAILED` - Failed to upload static files
- `JENKINS_BUILD_FAILED` - Generic Jenkins build failure

**Import-DB-Beauty Pipeline:**
- `CATEGORY_IMPORT_FAILED` - Failed to import categories
- `VARNISH_PURGE_FAILED` - Failed to purge varnish cache
- `JENKINS_BUILD_FAILED` - Generic Jenkins build failure

**Image Varnish Purge Pipeline:**
- `IMAGE_VARNISH_PURGE_FAILED` - Failed to purge image Varnish cache

**Image Cloudflare Purge Pipeline:**
- `IMAGE_CLOUDFLARE_PURGE_FAILED` - Failed to purge image Cloudflare cache

---

## Example Usage

### Using cURL

**Image-to-URL Request:**

```bash
curl -X POST http://127.0.0.1:8000/image-to-url \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "IMG-TEST-001",
    "pipeline_type": "IMAGE_TO_URL",
    "brand": "nykaaman",
    "source": {
      "email_subject": "Test Images",
      "drive_link": "https://drive.google.com/drive/folders/test-id",
      "zip_file_name": "test-images.zip"
    },
    "jenkins_job": "upload_file_to_create_static_url",
    "parameters": {
      "DirName": "",
      "File.zip": "test-images.zip",
      "Useremail": "test@nykaa.com"
    },
    "files": ["image1.jpg", "image2.jpg"]
  }'
```

**Import-DB-Beauty Request:**

```bash
curl -X POST http://127.0.0.1:8000/import-db-beauty \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "DB-TEST-001",
    "pipeline_type": "IMPORT_DB_BEAUTY",
    "brand": "nykaa-beauty",
    "source": {
      "email_subject": "Test Import",
      "requested_by": "test@nykaa.com"
    },
    "category_ids": ["100", "101"],
    "product_ids": [],
    "jenkins_jobs": [
      {
        "sequence": 1,
        "job_name": "edna_category_importer",
        "parameters": {}
      },
      {
        "sequence": 2,
        "job_name": "prod-pdp-plp-varnish-purge",
        "parameters": {
          "category_ids": "100,101",
          "product_ids": ""
        }
      }
    ]
  }'
```

### Using Python

```python
import requests

# Image-to-URL
payload = {
    "request_id": "IMG-TEST-001",
    "pipeline_type": "IMAGE_TO_URL",
    "brand": "nykaaman",
    "source": {
        "email_subject": "Test Images",
        "drive_link": "https://drive.google.com/drive/folders/test-id",
        "zip_file_name": "test-images.zip"
    },
    "jenkins_job": "upload_file_to_create_static_url",
    "parameters": {
        "DirName": "",
        "File.zip": "test-images.zip",
        "Useremail": "test@nykaa.com"
    },
    "files": ["image1.jpg", "image2.jpg"]
}

response = requests.post("http://127.0.0.1:8000/image-to-url", json=payload)
print(response.json())
```

### Using JavaScript/TypeScript

```javascript
const payload = {
  request_id: "IMG-TEST-001",
  pipeline_type: "IMAGE_TO_URL",
  brand: "nykaaman",
  source: {
    email_subject: "Test Images",
    drive_link: "https://drive.google.com/drive/folders/test-id",
    zip_file_name: "test-images.zip"
  },
  jenkins_job: "upload_file_to_create_static_url",
  parameters: {
    DirName: "",
    "File.zip": "test-images.zip",
    Useremail: "test@nykaa.com"
  },
  files: ["image1.jpg", "image2.jpg"]
};

fetch("http://127.0.0.1:8000/image-to-url", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(payload)
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## Running the API

### Development Mode

```bash
# Activate virtual environment (if using venv)
source .venv/bin/activate

# Start the API with auto-reload
uvicorn app:app --reload

# API will be available at: http://127.0.0.1:8000
```

### With Streamlit UI

```bash
# Start both FastAPI and Streamlit UI
./run-both.sh

# FastAPI: http://127.0.0.1:8000
# Streamlit: http://127.0.0.1:8501
# API Docs: http://127.0.0.1:8000/docs
```

---

## API Documentation Tools

The API automatically generates interactive documentation:

- **Swagger UI (Recommended)**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **OpenAPI Schema**: http://127.0.0.1:8000/openapi.json

---

## Notes

- The API **randomly chooses between success and failure** for each request to simulate real pipeline behavior
- Build numbers are **randomly generated** within realistic ranges for each job
- Responses include ISO 8601 timestamps in UTC for completion times
- The API supports **CORS** from all origins (`*`)
- All endpoints return **200 OK** status code; check the `status` field in the response to determine success

---

## Support

For issues or questions about these dummy APIs, refer to the project README or the code comments in `app.py` and `common.py`.
