@echo off
title DermaVision RAG Clinical Chatbot Server
echo =====================================================================
echo Launching DermaVision Standalone RAG Clinical Chatbot
echo Port: 8502 (Separate from Main Screening App on 8501)
echo Model: Meta Llama 3.2 (1B) + mxbai-embed-large (1024-dim)
echo =====================================================================
cd /d "%~dp0\.."
python -m streamlit run rag_chatbot/chatbot_app.py --server.port 8502 --server.headless false
pause
