Explicitly tell your server to only watch your actual code folder
uvicorn main:app --reload --reload-dir app