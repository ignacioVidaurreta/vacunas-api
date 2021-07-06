wget https://sisa.msal.gov.ar/datos/descargas/covid-19/files/datos_nomivac_covid19.zip
unzip -p datos_nomivac_covid19.zip | awk -F "," 'NR>1{ print $11" "$12 }' | sort | uniq -c | sort -bnr | awk -F " " '{ print $2","$3","$1 }' > dates_vaccines_qty.csv
sed -i '1s/^/fecha_aplicacion,vacuna,cantidad\n/' dates_vaccines_qty.csv
