#kill uvicorn
kill -9 `lsof -nti :8000` 2>/dev/null
#kill dash
kill -9 `lsof -nti :8050` 2>/dev/null

