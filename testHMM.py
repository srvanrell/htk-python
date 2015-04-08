#!/usr/bin/python
# Test a given trained HMM 

import argparse, os

parser = argparse.ArgumentParser(description='Test a given trained HMM.')

#==============================================================================
#    HVite -T 1 -C defs/config -H "models/trainedWithList${i}/hmm${j}/hmmdefs" 
#    -H "models/trainedWithList${i}/hmm${j}/macros" -S "lists/subject${i}.scp" -l '*' 
#    -i "results/trainedWithList${i}/rawresults" -w defs/activityNet -p 0.0 
#    -s 5.0 dicts/activityDictFull dicts/subactivityListFull > "results/trainedWithList${i}/log"
#    # TODO completar descripción HVite
#    # -t 250.0
#    #    Es la opción para hacer pruning durante el reconocimiento, desechando bajas probabilidades. 
#    #    Como no necesito ahorrar tiempo la saco por el momento. 
#    #    Más información en la página 187 del htkbook (section 13.4)
#==============================================================================

parser.add_argument('-T',help="Trace flag: numeric value ti define logging detail [0:4]. -A -V -D options are added by default",required=True)
parser.add_argument('-C',help="Config file: relative path to config file",required=True)
parser.add_argument('-H',help="trained HMMs folder: relative path to folder that contain hmmdefs and macros files",required=True)
parser.add_argument('-S',help="Script file: relative path to scp file (list of test records)",required=True)
parser.add_argument('-w',help="wordnet file",required=True)
parser.add_argument('-dict',help="Dictionary: relative path to dictionary",required=True)
parser.add_argument('-hl',help="HMM list file: relative path to list of HMM's names",required=True)

#parser.add_argument('-l',help="......",required=True)
# TODO complete description or add as an argument if necessary

parser.add_argument('-I',help="Master label file: mlf",required=True)



parser.add_argument('-tol',help="tolerance: to stop training HMMs",required=True)
#parser.add_argument('-maxIt',help="Maximum training iterations to stop training HMMs",required=True)

args = parser.parse_args()

# Trace argument string
trace = int(args.T);
trace_str = " -A -V -D -T %d" % trace

# Config argument string
config = str(args.C)
config_str = " -C %s" % config

# trained HMM folder argument string
hmmfolder = str(args.H) # trained hmm folder */*/hmm##
hmm_str = " -H %s/hmmdefs -H %s/macros" % hmmfolder

# Script argument string
scp = str(args.S)
scp_str = " -S %s" % scp

# results argument string
trainedwith = hmmfolder.find('trainedWith')
slash = hmmfolder.find('/',trainedwith)
resultsfolder = 'results/' + hmmfolder[trainedwith:slash]
rawresults_str = resultsfolder + "/rawresults"

# Wordnet argument string
wordnet = str(args.w)
wordnet_str = " -w %s" % wordnet

# Dictionary argument string
dictionary = str(args.dict)
dict_str = " %s" % dictionary

# HMM list argument string
hmmlist = str(args.hl)
hmmlist_str = " %s" % hmmlist

# log filename string
logfilename = resultsfolder + '/log'
log_str = ' > ' + logfilename

# miscelaneous configuration
ele_str = " -l '*'"
misc_str = " -p 0.0 -s 5.0"

# comando completo para realizar el testeo
HVite_str = "HVite" + trace_str + config_str + hmm_str + scp_str + ele_str + rawresults_str + wordnet_str + misc_str + dict_str + hmmlist_str + log_str
os.system(HVite_str)
    # TODO completar descripción HVite
    # -t 250.0
    #    Es la opción para hacer pruning durante el reconocimiento, desechando bajas probabilidades. 
    #    Como no necesito ahorrar tiempo la saco por el momento. 
    #    Más información en la página 187 del htkbook (section 13.4)










#==============================================================================
# # MLF argument string
# mlf = str(args.I)
# mlf_str = " -I %s" % mlf
# 
# 
# 
# 
# 
# 
# 
# # Tolerance for log likehood 
# tolerance = float(args.tol)
# 
# # Maximum Training iterations
# maxIter = int(args.maxIt)
# 
# loglike = 1.0 # initial log-likelihood
# 
# for it in range(maxIter):
#     # number of new model to train
#     newhmmNumber = oldhmmNumber + 1
#     
#     print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
#     print "Training of hmm%d in progress..." % newhmmNumber
#     print "-------------------------------------------------------------------"
#     
#     # update folder's names of old and new model
#     oldhmmFolder = hmmfolder + str(oldhmmNumber)
#     newhmmFolder = hmmfolder + str(newhmmNumber)
#     
#     # actualizo los argumentos de HERest que utilizan los nombres de las carpetas
#     hmm_str = " -H %s/hmmdefs -H %s/macros -M %s" % (oldhmmFolder, oldhmmFolder, newhmmFolder)
#     logfilename = newhmmFolder + '/log'
#     log_str = ' > ' + logfilename
#     
#     # creo la carpeta del modelo nuevo si no existe
#     if not os.path.exists(newhmmFolder):
#         os.mkdir(newhmmFolder)
#         print newhmmFolder + " was created"
#     
#     # comando completo para realizar la reestimacion
#     HERest_str = "HERest" + trace_str + config_str + mlf_str + scp_str + hmm_str + hmmlist_str + log_str
#     os.system(HERest_str)
#     print "Trained model was stored at " + newhmmFolder
#     # TODO completar descripcion HERest
#     # -t 250.0 150.0 1000.0
#     #    Es la opcion para hacer pruning durante el entrenamiento, desechando bajas probabilidades. 
#     #    Como no necesito ahorrar tiempo la saco por el momento. 
#     #    Mas informacion en la pagina 128 del htkbook (section 8.5)
#     
#     # si encuentra warnings o errores en el log los saca por pantalla
#     grep_str = 'grep -i "WARNING\|ERROR" %s' % logfilename
#     os.system(grep_str)
#           
#     # Busqueda de log-likehood en el archivo de log
#     logfile = open(logfilename)
#     logcontent = logfile.read()
#     loglikeStart = logcontent.find('log prob per frame = ') + 21
#     loglikeEnd = logcontent.find("\n",loglikeStart)
#     loglike = float(logcontent[loglikeStart:loglikeEnd])
#     print "average log prob per frame: %f" % loglike
#     
#     # si no es la primera iteracion calculo la mejora del log-likelihood
#     if it == 0:
#         loglikediff = 1.0
#     else:
#         loglikediff = abs( (oldloglike - loglike) / oldloglike ) 
#     print "loglikediff: %f (tolerance: %f)" % (loglikediff, tolerance)
#         
#     # guardo algunos valores para la siguiente iteracion
#     oldhmmNumber = newhmmNumber
#     oldloglike = loglike
#     
#     print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
#     
#     # si la variacion esta por debajo de la tolerancia dejo de entrenar
#     if loglikediff < tolerance:
#         break
# 
# print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"    
#==============================================================================
print "Training finished after %d iterations" % (it+1)    
print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"          
