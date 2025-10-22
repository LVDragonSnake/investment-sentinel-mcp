from flask import Flask, jsonify, request
import requests

API_BASE = "https://investment-sentinel-api-new.onrender.com"

app = Flask(__name__)

def forward(path, params=None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params or {}, timeout=15)
        r.raise_for_status()
        return jsonify(r.json()), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"ok": False, "error": str(e), "path": path}), 502

@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "investment-sentinel-mcp"})

# Endpoints tool del tuo MCP
@app.get("/tools/finanzamille_digest")
def finanzamille_digest():
    limit = request.args.get("limit", 8)
    return forward("/finanzamille/digest", {"limit": limit})

@app.get("/tools/global_news_scan")
def global_news_scan():
    region = request.args.get("region", "us")
    window = request.args.get("window", "6h")
    return forward("/news/scan", {"region": region, "window": window})

@app.get("/tools/portfolio_csv_import")
def portfolio_csv_import():
    # per ora usa la GET che hai già attiva
    return forward("/portfolio/csv/import")

@app.get("/tools/alpaca_bridge")
def alpaca_bridge():
    return forward("/alpaca/health")

# Manifest MCP servito da qui
@app.get("/mcp/manifest")
def manifest():
    return jsonify({
        "name": "investment-sentinel-mcp",
        "tools": [
            {
                "name": "finanzamille_digest",
                "description": "Restituisce gli articoli del giorno da Finanzamille in JSON",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "default": 8}
                    }
                }
            },
            {
                "name": "global_news_scan",
                "description": "Scan macro e mercati. Parametri: region, window",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "region": {"type": "string", "default": "us"},
                        "window": {"type": "string", "default": "6h"}
                    }
                }
            },
            {
                "name": "portfolio_csv_import",
                "description": "Importa posizioni da CSV o Drive e calcola PnL",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "alpaca_bridge",
                "description": "Verifica stato collegamento Alpaca",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
    })
