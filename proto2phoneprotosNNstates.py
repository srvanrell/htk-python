#!/usr/bin/python
# Convierte un hmm prototipo en un archivo que contiene un hmm para cada fonema, con la cantidad de estados indicada en la lista de fonemas

import sys, argparse, os

parser = argparse.ArgumentParser(description='Convierte un hmm prototipo en un archivo que contiene un hmm para cada fonema (hmmdefs). Crea el archivo macros junto a hmmdefs')

parser.add_argument('-i',help="Input file: HMM prototipe",required=True)
parser.add_argument('-o',help="Output file: HMM for each phone",required=True)
parser.add_argument('-p',help="phonesFile list, with number of states desired separated by a tab space",required=True)    

args = parser.parse_args()

# el archivo macros se guarda en la misma carpeta que hmmdefs (output file)
hmmdefsPath = str(args.o)
barra = hmmdefsPath.rfind('/')
if barra > 0:
    outputFolder = hmmdefsPath[0:barra+1]
else:
    outputFolder = ''
macrosPath = outputFolder + 'macros'

# el archivo vFloors se lee del mismo lugar que el prototipo
protoPath = str(args.i)
barra2 = protoPath.rfind('/')
if barra2 > 0:
    inputFolder = protoPath[0:barra2+1]
else:
    inputFolder = ''
vfloorsPath = inputFolder + 'vFloors'

phonesListPath = str(args.p)

# aviso por pantalla los archivos que estoy leyendo o escribiendo
print ("\nEntrada: %s, %s\n" % (protoPath, vfloorsPath) )
print ("Salida: %s, %s\n" % (hmmdefsPath, macrosPath))
print ("Fonemas: %s\n" % phonesListPath)

# Abro los archivos de lectura y creo los archivo de salida
protoFile   = open(protoPath, 'r')
hmmdefsFile = open(hmmdefsPath, 'w')
phonesFile  = open(phonesListPath, 'r')
macrosFile  = open(macrosPath,'w')
vfloorsFile = open(vfloorsPath,'r')


# Busqueda del header y contenido
protoFileContent = protoFile.read()
endHeader = protoFileContent.find('~h')
startTransMatrix = protoFileContent.find('<TRANSP>')

header = protoFileContent[0:endHeader]
states = protoFileContent[endHeader:startTransMatrix]
transMatrix = protoFileContent[startTransMatrix:]

# Busco el nombre del prototipo
comilla1  = states.find('"')
comilla2 = states.find('"',comilla1+1)
protoName = states[comilla1+1:comilla2]

# Busco todos los comienzos de los estados del prototipo (y de <MEAN>)
posSTATE = -1
startState = [] # lista de posiciones de <STATE>
startMean = []  # lista de posiciones de <MEAN>
while posSTATE < len(states):
    posSTATE = states.find('<STATE>',posSTATE+1)
    posMEAN = states.find('<',posSTATE+1)
    # si llega al final deja de buscar
    if posSTATE < 0:
        break
    startState.append(posSTATE)
    startMean.append(posMEAN)

# Busco la cantidad de estados definidos en el prototipo
posNUMSTATES = states.find('<NUMSTATES> ')
protoNumStates = int(states[posNUMSTATES+12:startState[0]-1])
protoNumStates -= 2 # descuento los estados inicial y final no emisores
print  'En el prototipo hay', protoNumStates, 'estados emisores\n'

# Comienzo a escribir el archivo de salida
hmmdefsFile.write(header)

# Recorro la lista de fonemas
for line in phonesFile:
    # Primero busco el nombre y cuantos estados deseo que tenga
    splitted = line.split('\t')
    phoneName = splitted[0]
    phoneNumStates = int(splitted[1][:-1])
    
    # inicio el HMM con su nombre segun la lista de fonemas
    hmmdefsFile.write(states[:posNUMSTATES].replace(protoName,phoneName))
        
    # defino la cantidad de estados solicitada
    hmmdefsFile.write('<NUMSTATES> %d\n' % (phoneNumStates+2)  )
    
    #==========================================================================
    # Decido si tengo que quitar o agregar estados del prototipo  
    #==========================================================================
    # - si tengo que quitar me quedo con los primeros
    # - si son de igual tamanio lo copio tal cual
    # - si tengo que agregar empiezo a repetir los primeros y completo con los 
    #   ultimos

    print 'El modelo "%s" tiene %d estados emisores, creado a partir de:' % (phoneName,phoneNumStates)
    
    # Cantidad de repeticiones de los estados que deben ser repetidos        
    repeats = 1 + phoneNumStates // protoNumStates
    
    # Busco hasta cual estado debo repetir el maximo de veces 
    repeatUntil  = phoneNumStates % protoNumStates
    
    # si la cantidad de estados del fonema es multiplo de la cantidad de 
    # estados del prototipo repito todos los estado igual cantidad de veces
    if repeatUntil == 0:
        repeatUntil = protoNumStates
        repeats -= 1 # ajusto las repeticiones si es multiplo
        
    stateCount = 0

    # Recorro cada estado del prototipo y lo repito de ser necesario
    for pstate in range(1,protoNumStates+1):
        
        # distingo entre el ultimo estado y el resto
        if pstate == protoNumStates:
            endState = startTransMatrix
        else:
            endState = startState[pstate]
            
        # repito las veces que sea necesario
        if pstate <= repeatUntil:
            pstateRepeats = repeats
        else:
            pstateRepeats = repeats - 1
            
        for r in range(pstateRepeats):
            stateCount += 1
            print 'estado', pstate+1, 'del prototipo => estado', stateCount+1
            hmmdefsFile.write(' <State> %d\n' % (stateCount+1))
            hmmdefsFile.write(states[startMean[pstate-1]:endState])
            
    # separo por una linea vacia la salida
    print ''
            
    #==========================================================================
    # Completo el modelo con la matriz de transicion
    #==========================================================================
    if phoneNumStates != protoNumStates:
        # Agrego la matriz de transiciones para la nueva cantidad de estados
        transpline = (' <TransP> %d\n' % (phoneNumStates+2))
        hmmdefsFile.write(transpline)

        for ii in range(phoneNumStates+2):
            hmmdefsFile.write('   ')
            for jj in range(phoneNumStates+2):
                if (jj == 1) and (ii==0):
                    hmmdefsFile.write('1.0 ')
                elif (jj >= ii) and (ii>0) and (ii<phoneNumStates+1):
                    prob = 1.0/(phoneNumStates+2-ii)
                    hmmdefsFile.write("%s " % prob)
                else:
                    hmmdefsFile.write('0.0 ')
            hmmdefsFile.write('\n')

        # Ultima linea donde avisa del fin del HMM
        endline = '<EndHMM>\n'
        hmmdefsFile.write(endline)
    else:
        # copio la matriz de transicion del prototipo
        hmmdefsFile.write(transMatrix)



# Agrego el header a vFloors y guardo en macros
vfloorsContent = vfloorsFile.read()
macrosFile.write(header)
macrosFile.write(vfloorsContent)

# Cierro todos los archivos
protoFile.close()
hmmdefsFile.close()
phonesFile.close()
macrosFile.close()
vfloorsFile.close()
