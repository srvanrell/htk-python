#!/usr/bin/python
# Convierte un hmm prototipo en un archivo que contiene un hmm para cada fonema

import sys, argparse, os

parser = argparse.ArgumentParser(description='Convierte un hmm prototipo en un archivo que contiene un hmm para cada fonema (hmmdefs). Crea el archivo macros junto a hmmdefs')

parser.add_argument('-i',help="Input file: HMM prototipe",required=True)
parser.add_argument('-o',help="Output file: HMM for each phone",required=True)
parser.add_argument('-p',help="phones list",required=True)    

args = parser.parse_args()

# el archivo macros se guarda en la misma carpeta que hmmdefs (output file)
hmmdefsName = str(args.o)
barra = hmmdefsName.rfind('/')
if barra > 0:
    outputFolder = hmmdefsName[0:barra+1]
else:
    outputFolder = ''
macrosName = outputFolder + 'macros'
vfloorsName = outputFolder + 'vFloors'

# aviso por pantalla
print ("\nEntrada: %s, %s\n" % (str(args.i), vfloorsName) )
print ("Salida: %s, %s\n" % (hmmdefsName, macrosName))
print ("Fonemas: %s\n" % str(args.p))

# Abro los archivos de lectura y creo los archivo de salida
protoFile   = open(args.i, 'r')
hmmdefsFile = open(args.o, 'w')
phones      = open(args.p, 'r')
macrosFile  = open(macrosName,'w')
vfloorsFile = open(vfloorsName,'r')

# busqueda del header y contenido
protoFileContent = protoFile.read()
endHeader = protoFileContent.find('~h')

header = protoFileContent[0:endHeader]
proto  = protoFileContent[endHeader:]

comilla1  = proto.find('"')
comilla2 = proto.find('"',comilla1+1)
name = proto[comilla1+1:comilla2]

#Escribo el archivo de salida
hmmdefsFile.write(header)

for line in phones:
    hmmdefsFile.write(proto.replace(name,line[:-1]))


# Agrego el header a vfloors y guardo en macros
vfloorsContent = vfloorsFile.read()
macrosFile.write(header)
macrosFile.write(vfloorsContent)

# Cierro todos los archivos
protoFile.close()
hmmdefsFile.close()
phones.close()
macrosFile.close()
vfloorsFile.close()
