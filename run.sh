echo -e "\033[92m Descargando y transformando dataset\033[0m"
./desagregated_shorterer.sh
echo -e "\033[92m Descargando informacion de recepcion de vacunas\033[0m"
./download_vac_reception.sh
echo -e "\033[92m Iniciando back\033[0m"
uvicorn main:app --reload & > uvicorn_log
echo -e "\033[92m Iniciando front\033[0m"
sleep 2
cd dash; python3 app.py