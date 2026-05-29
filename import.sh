#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
# SEED — Import n8n Workflow
# Usage: ./import.sh [N8N_URL] [API_KEY]
# ─────────────────────────────────────────────

N8N_URL="${1:-http://localhost:5678}"
API_KEY="${2:-${N8N_API_KEY:-}}"
WORKFLOW_FILE="$(dirname "$0")/seed-evolution-workflow.json"

# ── Validate ──────────────────────────────────
if [[ ! -f "$WORKFLOW_FILE" ]]; then
  echo "❌ File not found: $WORKFLOW_FILE"
  exit 1
fi

if [[ -z "$API_KEY" ]]; then
  echo "❌ API key required."
  echo "   Usage : ./import.sh http://localhost:5678 eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwYmNhZGMzZC0zZmRjLTQ4YjEtYWRhNi1jZGVkYzAwMzYxZGYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiOGE5NzJkYjAtYjQyYi00NWU1LTliYzMtOTQ3YzMyZjlhNGI3IiwiaWF0IjoxNzc5ODUwMjY3fQ.YT-9dmmdBNKFuAPX6pmLR1u5fFCYQuUb5jSoWTJmmGE"
  echo "   Or set: export N8N_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwYmNhZGMzZC0zZmRjLTQ4YjEtYWRhNi1jZGVkYzAwMzYxZGYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiOGE5NzJkYjAtYjQyYi00NWU1LTliYzMtOTQ3YzMyZjlhNGI3IiwiaWF0IjoxNzc5ODUwMjY3fQ.YT-9dmmdBNKFuAPX6pmLR1u5fFCYQuUb5jSoWTJmmGE"
  exit 1
fi

# ── Import ────────────────────────────────────
echo "→ Importing SEED workflow to $N8N_URL ..."

RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X POST "$N8N_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d @"$WORKFLOW_FILE")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n -1)

if [[ "$HTTP_CODE" == "200" || "$HTTP_CODE" == "201" ]]; then
  WORKFLOW_ID=$(echo "$BODY" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
  echo "✅ Workflow imported successfully!"
  echo "   ID  : $WORKFLOW_ID"
  echo "   URL : $N8N_URL/workflow/$WORKFLOW_ID"
else
  echo "❌ Import failed (HTTP $HTTP_CODE)"
  echo "$BODY"
  exit 1
fi
