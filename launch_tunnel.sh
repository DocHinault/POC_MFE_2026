#!/bin/bash
# Script pour lancer localtunnel (plus simple que ngrok)

echo "📦 Installation de localtunnel..."
npm install -g localtunnel > /dev/null 2>&1

echo "✅ localtunnel installé"
echo ""
echo "🌐 Lancement du tunnel pour localhost:8503..."
echo ""

lt --port 8503 --print-requests

