# geoconvert
Reads GeoJSON features from a specific column on a CSV file and merges them

Written to be used with https://github.com/GAUP/GAUPsurvey

usage: csv_geojson_merger.py [-h] -c COLUMN [-p PRECISION] [-o OUTFILE] file

Group (merge) multiple GeoJSON features/groups from CSV.

positional arguments:
  file                  CSV file to be read/merged

optional arguments:
  -h, --help            show this help message and exit
  -c COLUMN, --column COLUMN
                        Column to be read/merged
  -p PRECISION, --precision PRECISION
                        Digits of precision
  -o OUTFILE, --outfile OUTFILE
                        Outfile
