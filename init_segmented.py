# -*- coding: utf-8 -*-
# ===================================================
# sinc(i) - sinc.unl.edu.ar
# Leandro A. Bugnon
# Created: 11 Sep 2014
# Modified: 08 Apr 2014
# ===================================================
import sys, os
def segmentedStart(clsDir,confFile,trainList,hmmlist,segmentedLabels,prototype):
    "Initialize all hmm in clsDir with a hmm-segmented dataset using HInit. "

    modelDir=clsDir+"/hmm000"
    if not os.path.exists(modelDir):
        os.mkdir(modelDir)
    fhmmdefs=open("%s/hmmdefs.mmf" %modelDir,"w")
    
    # Initialize each HMM with HInit and append to the MMF.
    for hmm in open(hmmlist):
        command="HInit -C %s -S %s -M %s -l %s -I %s -T 1 %s >  log/HInit.log" %(confFile,trainList,clsDir,hmm.strip(),segmentedLabels,prototype)
        os.system(command)
        # TODO: consider later to add "-H vFloor.mmf" to control variance floors

        fproto=open("%s/prototype" %clsDir)          # Prototype initialized with subemotion hmm           

        if fhmmdefs.tell() is 0:                     # Copy header
            for n,line in enumerate(fproto):
                # write MMF heading
                if n<3:                    
                    fhmmdefs.write(line)
                else:
                    break
            fproto.seek(0)
        
        for n,line in enumerate(fproto):             # Append prototype to hmmdefs
            if n is 2:
                fhmmdefs.write("~h \"%s\"\n" %hmm.strip())
            if n>3:
                fhmmdefs.write(line)

    fproto.close()
    fhmmdefs.close()
    # ==========================================================================================
