#!/usr/bin/python
# Convierte un hmm prototipo en un archivo que contiene un hmm para cada fonema

import sys, argparse, os

parser = argparse.ArgumentParser(description='Genera un archivo .hed con las instrucciones para enlazar los parametros del modelo')

parser.add_argument('-p',help="phones list",required=True)    
parser.add_argument('-o',help="Output file: hed",required=True)

args = parser.parse_args()

print ("\nFonemas: %s\n" % str(args.p))
print ("\nSalida: %s\n" % str(args.o))

# Abro los archivos de lectura y creo el archivo de salida
hedFile = open(args.o, 'w')
phones  = open(args.p, 'r')

# contenido a replicar para cada fonema
header    = "JO 8 2.0\n" 
plantilla = "TI mix_FONEMA {FONEMA.state[2-4].mix}\n"
footer    = "HK TIEDHS"

#Escribo el archivo de salida
hedFile.write(header)
for line in phones:
    hedFile.write(plantilla.replace('FONEMA',line[:-1]))
hedFile.write(footer)

