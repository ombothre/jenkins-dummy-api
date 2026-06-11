# Jenkins Dummy APIs - Quick Reference

## Base URL
```
http://127.0.0.1:8000
```

## Endpoints Summary

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/image-to-url` | Image-to-URL pipeline |
| POST | `/import-db-beauty` | Import-DB-Beauty pipeline |
| POST | `/image-varnish-purge` | Image Varnish cache purge (recovery) |
| POST | `/image-cloudflare-purge` | Image Cloudflare cache purge (recovery) |

---

## Quick Examples

### 1. Check API Health
```bash
curl http://127.0.0.1:8000/health
```

### 2. Image to URL Pipeline
```bash
curl -X POST http://127.0.0.1:8000/image-to-url \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "IMG-001",
    "pipeline_type": "IMAGE_TO_URL",
    "brand": "nykaaman",
    "source": {
      "email_subject": "Images",
      "drive_link": "https://drive.google.com/drive/folders/xyz",
      "zip_file_name": "images.zip"
    },
    "jenkins_job": "upload_file_to_create_static_url",
    "parameters": {
      "DirName": "",
      "File.zip": "images.zip",
      "Useremail": "user@nykaa.com"
    },
    "files": ["img1.jpg", "img2.jpg"]
  }'
```

### 3. Import DB Beauty Pipeline
```bash
curl -X POST http://127.0.0.1:8000/import-db-beauty \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "DB-001",
    "pipeline_type": "IMPORT_DB_BEAUTY",
    "brand": "nykaa-beauty",
    "source": {
      "email_subject": "DB Import",
      "requested_by": "user@nykaa.com"
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

### 4. Image Varnish Purge
```bash
curl -X POST http://127.0.0.1:8000/image-varnish-purge \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "VARNISH-001",
    "brand": "nykaaman",
    "image_urls": [
      "https://images-static.nykaa.com/media/img1.jpg",
      "https://images-static.nykaa.com/media/img2.jpg"
    ],
    "jenkins_job": "Nykaaman-varnish-url-flush"
  }'
```

### 5. Image Cloudflare Purge
```bash
curl -X POST http://127.0.0.1:8000/image-cloudflare-purge \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "CF-001",
    "brand": "nykaaman",
    "image_urls": [
      "https://images-static.nykaa.com/media/img1.jpg",
      "https://images-static.nykaa.com/media/img2.jpg"
    ],
    "jenkins_job": "cloudflare-url-cache-purge-man"
  }'
```

---

## Response Status Codes

- **200 OK** - Request processed (check `status` field)
- **422 Unprocessable Entity** - Invalid request
- **500 Internal Server Error** - Server error

---

## Key Notes

✓ Responses always return 200, check the `status` field ("SUCCESS" or "FAILURE")  
✓ Builds numbers and pipeline results are **randomized** per request  
✓ All timestamps are in ISO 8601 UTC format  
✓ CORS is enabled for all origins  
✓ `/image-varnish-purge` and `/image-cloudflare-purge` are recovery endpoints only (called independently, not automatically)

---

## Interactive Documentation

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **OpenAPI JSON**: http://127.0.0.1:8000/openapi.json

---

## Running the API

```bash
# Activate virtual environment
source .venv/bin/activate

# Start API with auto-reload
uvicorn app:app --reload

# Or start both API + Streamlit UI
./run-both.sh
```

---

## Response Field Reference

### Image-to-URL Success Response
```json
{
  "request_id": "string",
  "pipeline_type": "IMAGE_TO_URL",
  "status": "SUCCESS",
  "jenkins": {
    "job_name": "string",
    "build_number": 0,
    "build_url": "string",
    "duration_seconds": 0
  },
  "output": {
    "static_urls": ["string"],
    "notified_email": "string",
    "slack_channel": "string"
  },
  "completed_at": "2024-06-11T10:30:45Z"
}
```

### Image-to-URL Failure Response
```json
{
  "request_id": "string",
  "pipeline_type": "IMAGE_TO_URL",
  "status": "FAILURE",
  "jenkins": { ... },
  "output": {
    "static_urls": [],
    "notified_email": "string",
    "slack_channel": "string"
  },
  "error": {
    "code": "ZIP_EXTRACTION_FAILED|STATIC_UPLOAD_FAILED|JENKINS_BUILD_FAILED",
    "message": "string"
  },
  "completed_at": "2024-06-11T10:30:45Z"
}
```

### Import-DB-Beauty Success Response
```json
{
  "request_id": "string",
  "pipeline_type": "IMPORT_DB_BEAUTY",
  "status": "SUCCESS",
  "stages": [
    {
      "job_name": "string",
      "build_number": 0,
      "status": "SUCCESS",
      "duration_seconds": 0,
      "build_url": "string"
    }
  ],
  "output": {
    "imported_category_ids": ["string"],
    "purged_category_ids": ["string"],
    "product_ids": ["string"],
    "message": "string"
  },
  "completed_at": "2024-06-11T11:15:30Z"
}
```

### Import-DB-Beauty Failure Response
```json
{
  "request_id": "string",
  "pipeline_type": "IMPORT_DB_BEAUTY",
  "status": "FAILURE",
  "stages": [ ... ],
  "output": {
    "imported_category_ids": [],
    "purged_category_ids": [],
    "product_ids": ["string"],
    "message": "string"
  },
  "error": {
    "code": "CATEGORY_IMPORT_FAILED|VARNISH_PURGE_FAILED|JENKINS_BUILD_FAILED",
    "message": "string"
  },
  "completed_at": "2024-06-11T11:15:30Z"
}
```

### Image Varnish Purge Success Response
```json
{
  "request_id": "string",
  "pipeline_type": "IMAGE_VARNISH_PURGE",
  "status": "SUCCESS",
  "jenkins": {
    "job_name": "string",
    "build_number": 0,
    "build_url": "string",
    "duration_seconds": 0
  },
  "output": {
    "purged_urls": ["string"],
    "message": "string"
  },
  "completed_at": "2026-06-11T10:30:45Z"
}
```

### Image Varnish Purge Failure Response
```json
{
  "request_id": "string",
  "pipeline_type": "IMAGE_VARNISH_PURGE",
  "status": "FAILURE",
  "jenkins": { ... },
  "output": {
    "purged_urls": [],
    "message": "string"
  },
  "error": {
    "code": "IMAGE_VARNISH_PURGE_FAILED",
    "message": "string"
  },
  "completed_at": "2026-06-11T10:30:45Z"
}
```

### Image Cloudflare Purge Success Response
```json
{
  "request_id": "string",
  "pipeline_type": "IMAGE_CLOUDFLARE_PURGE",
  "status": "SUCCESS",
  "jenkins": {
    "job_name": "string",
    "build_number": 0,
    "build_url": "string",
    "duration_seconds": 0
  },
  "output": {
    "purged_urls": ["string"],
    "message": "string"
  },
  "completed_at": "2026-06-11T10:35:45Z"
}
```

### Image Cloudflare Purge Failure Response
```json
{
  "request_id": "string",
  "pipeline_type": "IMAGE_CLOUDFLARE_PURGE",
  "status": "FAILURE",
  "jenkins": { ... },
  "output": {
    "purged_urls": [],
    "message": "string"
  },
  "error": {
    "code": "IMAGE_CLOUDFLARE_PURGE_FAILED",
    "message": "string"
  },
  "completed_at": "2026-06-11T10:35:45Z"
}
```

---

## Common Error Codes

### Image-to-URL
- `ZIP_EXTRACTION_FAILED` - Failed to extract ZIP
- `STATIC_UPLOAD_FAILED` - Failed to upload static files
- `JENKINS_BUILD_FAILED` - Generic failure

### Import-DB-Beauty
- `CATEGORY_IMPORT_FAILED` - Category import failed
- `VARNISH_PURGE_FAILED` - Cache purge failed
- `JENKINS_BUILD_FAILED` - Generic failure

### Image Varnish Purge
- `IMAGE_VARNISH_PURGE_FAILED` - Varnish cache purge failed

### Image Cloudflare Purge
- `IMAGE_CLOUDFLARE_PURGE_FAILED` - Cloudflare cache purge failed

---

For complete documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
