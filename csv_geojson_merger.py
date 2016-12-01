#!/usr/bin/python
# -*- coding: utf-8 -*-

# Augusto Bott - augusto@bott.com.br - 2016-11-26

# reads GeoJSON from a specific column on a CSV file and merges them
# written to be used with https://github.com/GAUP/GAUPsurvey

# based on
# https://gist.github.com/themiurgo/8687883
# https://gist.github.com/migurski/3759608/
# https://github.com/shawnbot/py-geojoin
# https://github.com/batpad/merge-geojson
# https://github.com/andrewjdyck/csvToGeoJSON

import csv
import json
from argparse import ArgumentParser, FileType
import sys
from re import compile

float_pat = compile(r'^-?\d+\.\d+(e-?\d+)?$')
charfloat_pat = compile(r'^[\[,\,]-?\d+\.\d+(e-?\d+)?$')

parser = ArgumentParser(description="Group (merge) multiple GeoJSON features/groups from CSV.")
defaults = dict(precision=-1, outfile=sys.stdout, column=0)
parser.set_defaults(**defaults)

parser.add_argument('file',
                  type=FileType('r'), help='CSV file to be read/merged')
parser.add_argument('-c', '--column', dest='column', required=True,
                  type=int, help='Column to be read/merged')
parser.add_argument('-p', '--precision', dest='precision',
                  type=int, help='Digits of precision')
parser.add_argument('-o', '--outfile', dest='outfile',
                  type=FileType('wb', 0), help='Outfile')

if __name__ == '__main__':
  args = parser.parse_args()
  infile = args.file
  outfile = args.outfile
  rawData = csv.reader(infile, delimiter=',', quotechar='"')

  outjson = dict(type='FeatureCollection', features=[])

  iter = 0

  for row in rawData:
    iter += 1
    if iter >= 2:
      try:
        dados = row[args.column]
        if dados != '':
          injson = json.loads(dados)

          if injson.get('type', None) != 'FeatureCollection':
              raise Exception('Sorry, "%s" does not look like GeoJSON' % infile)

          if type(injson.get('features', None)) != list:
              raise Exception('Sorry, "%s" does not look like GeoJSON' % infile)
          try:    
              outjson['features'] += injson['features']
          except:
              outjson['features'] += injson
      except IndexError:
        pass
      except AttributeError:
        print ('Sorry, "%s" does not look like GeoJSON' % infile)

  infile.close()

  encoder = json.JSONEncoder(separators=(',', ':'))
  encoded = encoder.iterencode(outjson)

  precision = args.precision
  format = '%.' + str(precision) + 'f'
  output = outfile

  for token in encoded:
    if precision >= 0:
      if charfloat_pat.match(token):
        # in python 2.7, we see a character followed by a float literal
        output.write(token[0] + format % float(token[1:]))

      elif float_pat.match(token):
        # in python 2.6, we see a simple float literal
        output.write(format % float(token))

      else:
        output.write(token)
    else:
      output.write(token)

  output.write("\n")


