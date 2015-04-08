#!/usr/bin/python
# Train HMM until log likelihood variation reach given tolerance

import argparse, os, sys

parser = argparse.ArgumentParser(description='Train a HMM until log '
'likelihood variation reach given tolerance or maximum iterations. Also plot '
'the distributions of the last trained models.')

parser.add_argument('-T', help="Trace flag: numeric value ti define logging detail [0:4]. -A -V -D options are added by default", required=True)
parser.add_argument('-C', help="Config file: relative path to config file", required=True)
parser.add_argument('-I', help="Master label file: mlf", required=True)
parser.add_argument('-S', help="Script file: relative path to scp file (list of records)", required=True)
parser.add_argument('-H', help="old HMMs folder: relative path to folder that contain hmmdefs and macros files", required=True)
parser.add_argument('-hl', help="HMM list file: relative path to list of HMM's names", required=True)
parser.add_argument('-tol', help="tolerance: to stop training HMMs", required=True)
parser.add_argument('-maxIt', help="Maximum training iterations to stop training HMMs", required=True)

args = parser.parse_args()

# Trace argument string
trace = int(args.T);
trace_str = " -A -V -D -T %d" % trace

# Config argument string
config = str(args.C)
config_str = " -C %s" % config

# MLF argument string
mlf = str(args.I)
mlf_str = " -I %s" % mlf

# Script argument string
scp = str(args.S)
scp_str = " -S %s" % scp

# HMM initial folder
auxhmm = str(args.H)                     # initial hmm folder */*/hmm##
slashhmm = auxhmm.find('/hmm')           # /hmm position
hmmfolder = auxhmm[:slashhmm+4]          # hmm folder "*/*/hmm"
oldhmmNumber = int(auxhmm[slashhmm+4:])  # initial hmm number

# HMM list argument string
hmmlist = str(args.hl)
hmmlist_str = " %s" % hmmlist

# Tolerance for log likehood
tolerance = float(args.tol)

# Maximum Training iterations
maxIter = int(args.maxIt)

loglike = 1.0 # initial log-likelihood

for it in range(maxIter):
    # number of new model to train
    newhmmNumber = oldhmmNumber + 1

    print "-------------------------------------------------------------------"
    print "Training of hmm%d in progress..." % newhmmNumber
    

    # update folder's names of old and new model
    oldhmmFolder = hmmfolder + str(oldhmmNumber)
    newhmmFolder = hmmfolder + str(newhmmNumber)

    # actualizo los argumentos de HERest que utilizan los nombres de las carpetas
    hmm_str = " -H %s/hmmdefs -H %s/macros -M %s" % (oldhmmFolder, oldhmmFolder, newhmmFolder)
    logfilename = newhmmFolder + '/log'
    log_str = ' > ' + logfilename
    
    # creo la carpeta del modelo nuevo si no existe
    if not os.path.exists(newhmmFolder):
        os.mkdir(newhmmFolder)
        print newhmmFolder + " was created"
    
    # comando completo para realizar la reestimacion
    HERest_str = "HERest" + trace_str + config_str + mlf_str + scp_str + hmm_str + hmmlist_str + log_str
    os.system(HERest_str)
    print "Trained model was stored at " + newhmmFolder
    # TODO completar descripcion HERest
    # -t 250.0 150.0 1000.0
    #    Es la opcion para hacer pruning durante el entrenamiento, desechando bajas probabilidades. 
    #    Como no necesito ahorrar tiempo la saco por el momento. 
    #    Mas informacion en la pagina 128 del htkbook (section 8.5)
    
    # si encuentra warnings o errores en el log los saca por pantalla
    grep_str = 'grep -i "WARNING\|ERROR" %s' % logfilename
    os.system(grep_str)
          
    # Busqueda de log-likehood en el archivo de log
    logfile = open(logfilename)
    logcontent = logfile.read()
    loglikeStart = logcontent.find('log prob per frame = ') + 21
    loglikeEnd = logcontent.find("\n",loglikeStart)
    loglike = float(logcontent[loglikeStart:loglikeEnd])
    print "average log prob per frame: %f" % loglike
    
    # si no es la primera iteracion calculo la mejora del log-likelihood
    if it == 0:
        loglikediff = 1.0
    else:
        loglikediff = abs( (oldloglike - loglike) / oldloglike ) 
    print "loglikediff: %f (tolerance: %f)" % (loglikediff, tolerance)
        
    # guardo algunos valores para la siguiente iteracion
    oldhmmNumber = newhmmNumber
    oldloglike = loglike
       
    # si la variacion esta por debajo de la tolerancia dejo de entrenar
    if loglikediff < tolerance:
        break

print "-------------------------------------------------------------------"
print "Training finished after %d iterations" % (it+1)
print "Last trained model saved at %s" % (newhmmFolder)    
print "-------------------------------------------------------------------"        

# Guardar el ultimo modelo entrenado
lastModelFile = open(hmmfolder[:-3]+"lastTrained.txt", 'w')
lastModelFile.write(str(newhmmNumber))
lastModelFile.close()


# Grafica la distribuciones de los modelos entrenados
#sys.stdout.flush()
#os.system("./htkModelParser/hmm_plotter.py %s" %(newhmmFolder + "/hmmdefs"))
#sys.stdout.flush()
