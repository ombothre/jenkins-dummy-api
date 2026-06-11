from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from common import (
    simulate_image_to_url_pipeline,
    simulate_import_db_beauty_pipeline,
    simulate_image_varnish_purge_pipeline,
    simulate_image_cloudflare_purge_pipeline,
)


app = FastAPI(
    title="Jenkins Dummy APIs",
    description="Dummy endpoints that simulate NOC Jenkins pipeline responses.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> HTMLResponse:
    return HTMLResponse("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Jenkins Dummy APIs</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 10px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 900px;
                width: 100%;
                padding: 50px 40px;
            }
            h1 {
                color: #333;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .subtitle {
                color: #666;
                font-size: 1.1em;
                margin-bottom: 40px;
                font-weight: 300;
            }
            .section {
                margin-bottom: 40px;
            }
            .section h2 {
                color: #667eea;
                font-size: 1.5em;
                margin-bottom: 20px;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
            }
            .endpoints-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .endpoint-card {
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 20px;
                border-radius: 5px;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .endpoint-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }
            .endpoint-method {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.85em;
                font-weight: bold;
                margin-right: 10px;
            }
            .method-post {
                background: #ff6b6b;
                color: white;
            }
            .method-get {
                background: #51cf66;
                color: white;
            }
            .endpoint-path {
                font-family: 'Courier New', monospace;
                color: #333;
                font-size: 1.1em;
                margin-top: 5px;
            }
            .endpoint-desc {
                color: #666;
                font-size: 0.95em;
                margin-top: 8px;
            }
            .docs-links {
                background: #f0f4ff;
                padding: 20px;
                border-radius: 5px;
                margin-top: 30px;
            }
            .docs-links h3 {
                color: #667eea;
                margin-bottom: 15px;
            }
            .docs-links a {
                display: inline-block;
                margin-right: 15px;
                margin-bottom: 10px;
                color: #667eea;
                text-decoration: none;
                font-weight: 500;
                padding: 8px 16px;
                border: 2px solid #667eea;
                border-radius: 5px;
                transition: all 0.2s;
            }
            .docs-links a:hover {
                background: #667eea;
                color: white;
            }
            .version {
                color: #999;
                font-size: 0.9em;
                margin-top: 40px;
                text-align: center;
                border-top: 1px solid #eee;
                padding-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Jenkins Dummy APIs</h1>
            <p class="subtitle">Dummy endpoints that simulate NOC Jenkins pipeline responses</p>
            
            <div class="section">
                <h2>Available Endpoints</h2>
                <div class="endpoints-grid">
                    <div class="endpoint-card">
                        <span class="endpoint-method method-post">POST</span>
                        <div class="endpoint-path">/image-to-url</div>
                        <div class="endpoint-desc">Convert images to static URLs</div>
                    </div>
                    <div class="endpoint-card">
                        <span class="endpoint-method method-post">POST</span>
                        <div class="endpoint-path">/import-db-beauty</div>
                        <div class="endpoint-desc">Import database beauty data</div>
                    </div>
                    <div class="endpoint-card">
                        <span class="endpoint-method method-post">POST</span>
                        <div class="endpoint-path">/image-varnish-purge</div>
                        <div class="endpoint-desc">Purge image Varnish cache</div>
                    </div>
                    <div class="endpoint-card">
                        <span class="endpoint-method method-post">POST</span>
                        <div class="endpoint-path">/image-cloudflare-purge</div>
                        <div class="endpoint-desc">Purge image Cloudflare cache</div>
                    </div>
                    <div class="endpoint-card">
                        <span class="endpoint-method method-get">GET</span>
                        <div class="endpoint-path">/health</div>
                        <div class="endpoint-desc">Health check endpoint</div>
                    </div>
                </div>
            </div>
            
            <div class="docs-links">
                <h3>📚 Interactive Documentation</h3>
                <a href="/docs">Swagger UI</a>
                <a href="/redoc">ReDoc</a>
                <a href="/openapi.json">OpenAPI Schema</a>
            </div>
            
            <div class="version">
                <strong>Jenkins Dummy APIs v0.1.0</strong>
            </div>
        </div>
    </body>
    </html>
    """)



@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/image-to-url")
def image_to_url(payload: dict[str, Any]) -> dict[str, Any]:
    return simulate_image_to_url_pipeline(payload)


@app.post("/import-db-beauty")
def import_db_beauty(payload: dict[str, Any]) -> dict[str, Any]:
    return simulate_import_db_beauty_pipeline(payload)


@app.post("/image-varnish-purge")
def image_varnish_purge(payload: dict[str, Any]) -> dict[str, Any]:
    return simulate_image_varnish_purge_pipeline(payload)


@app.post("/image-cloudflare-purge")
def image_cloudflare_purge(payload: dict[str, Any]) -> dict[str, Any]:
    return simulate_image_cloudflare_purge_pipeline(payload)
