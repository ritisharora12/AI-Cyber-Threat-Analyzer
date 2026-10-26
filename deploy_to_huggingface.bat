@echo off
title Deploy AI Cyber Threat Analyzer to Hugging Face Spaces (24/7 Free)
cd /d "%~dp0"
echo ===============================================================
echo   Deploying to Hugging Face Spaces (24/7 Permanent Cloud)
echo ===============================================================
py deploy_to_huggingface.py
pause
