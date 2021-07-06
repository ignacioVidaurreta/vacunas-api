echo -e "\033[92m Descargando y transformando dataset\033[0m"
#./desagregated_shorterer.sh
echo -e "\033[92m Iniciando front y back\033[0m"
uvicorn main:app --reload & > uvicorn_log && cd dash; python3 app.py
