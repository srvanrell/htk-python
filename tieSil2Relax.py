#!/usr/bin/python
# tie silence state to relax central state

import argparse, os, sys

parser = argparse.ArgumentParser(description='Tie silence state to relax central state.')

parser.add_argument('-H', help="old HMMs folder: relative path to folder that contain hmmdefs and macros files", required=True)
parser.add_argument('-hl', help="HMM list file: relative path to list of HMM's names", required=True)

args = parser.parse_args()

# HMM initial folder
auxhmm = str(args.H)                     # initial hmm folder */*/hmm##
slashhmm = auxhmm.find('/hmm')           # /hmm position
hmmfolder = auxhmm[:slashhmm+4]          # hmm folder "*/*/hmm"
oldhmmNumber = int(auxhmm[slashhmm+4:])  # initial hmm number

# number of new model to train
newhmmNumber = oldhmmNumber + 1

# HMM list argument string
hmmlist = str(args.hl)

print "-------------------------------------------------------------------"
print "Tying sil and relax in hmm%d..." % newhmmNumber

# update folder's names of old and new model
oldhmmFolder = hmmfolder + str(oldhmmNumber)
newhmmFolder = hmmfolder + str(newhmmNumber)
    
# creo la carpeta del modelo nuevo si no existe
if not os.path.exists(newhmmFolder):
    os.mkdir(newhmmFolder)
    print newhmmFolder + " was created"

tieSilRelaxFileName = 'defs/tieSilRelax.hed'
tieSilRelaxFile = open(tieSilRelaxFileName, 'w')
#tieSilRelaxFile.write("""
#AT 1 3 0.3 {sil.transP}
#TI silrelax {sil.state[2],relax.state[3]}
#""")
tieSilRelaxFile.write("TI silrelax {sil.state[2],relax.state[3]}\n")
tieSilRelaxFile.close()

sys.stdout.flush()
os.system("HHEd -A -V -D -T 3 -H %s/macros -H %s/hmmdefs -M %s %s %s" 
          %(oldhmmFolder, oldhmmFolder, newhmmFolder, tieSilRelaxFileName,
            hmmlist))
sys.stdout.flush()

print "Tying sil and relax has finished"
print "-------------------------------------------------------------------"
