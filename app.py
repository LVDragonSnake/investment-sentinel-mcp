from flask import Flask, jsonify
import requests

API_BASE = "https://investment-sentinel-api-new.onrender.com"  # il tuo API già live

app = Flask(__name__)

def forward(path, params=None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params or {}, timeout=12)
        r.raise_for_status()
        return jsonify(r.json()), r.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"ok": False, "error": str(e), "path": path}), 502

@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "investment-sentinel-mcp"})

# ---- ROUTE USATE DALL’AGENTE (MCP) ----
@app.get("/tools/finanzamille")
def finanzamille():
    return forward("/finanzamille/digest", {"limit": 8})

@app.get("/tools/news")
def news():
    return forward("/news/scan", {"region": "us", "window": "6h"})

@app.get("/tools/portfolio")
def portfolio():
    return forward("/portfolio/csv/import")

@app.get("/tools/alpaca")
def alpaca():
    return forward("/alpaca/health")
