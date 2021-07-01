unzip datos_nomivac_covid19.zip
cat datos_nomivac_covid19.csv | awk -F "," '{ print $11" "$12 }' | sort | uniq -c | sort -bnr | awk -F " " '{ print $2","$3","$1 }' > dates_vaccines_qty.csv
