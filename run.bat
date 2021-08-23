@echo off
VENV\scripts\activate && cd speech-commands && python main.py %* & cd .. && deactivate && pause