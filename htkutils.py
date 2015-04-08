#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Collection of functions to use and interact with htk.

@author: sebastian
@organization: sinc(i) - UNL-CONICET
@contact: srvanrell*gmail.com

Created on Thu Feb 19 16:13:26 2015
"""

import sys, os
import textwrap

def makeproto(filename, nStates, nFeatures, nMixtures=0, streams=[]):
    """Create a prototype with given numbers of states and features. Covariance
    matrix created is diagonal.

    Inputs:
    - filename: HMM protoype filename (absolute or relative path)
    - nStates: number of emitive states (internally will add first and last)
    - nFeatures: number of features
    - nMixtures: number of mixtures for each state
    - streams: list of number of features by streams

    Usage:
    >>> makeproto("proto", 5, 30)
    """

    # Abro los archivos de lectura y creo el archivo de salida
    protoFile = open(filename, 'w')
    print "\nPrototype file saved: %s\n" % filename

    # Me quedo con el nombre del archivo para que sea el nombre del prototipo
    barra = filename.find('/')
    if barra > 0:
        protoName = filename[barra+1:]
    else:
        protoName = filename

    # Comienzo a escribir el archivo de prototipo
    oline = ('~o <VecSize> %d <USER>\n' % nFeatures)
    protoFile.write(oline)

    if streams:
        nStreams = len(streams)
        auxStreams = ' '.join('%d'%n for n in streams)
        streaminfo = ('   <StreamInfo> %d %s\n' % (nStreams, auxStreams))
        protoFile.write(streaminfo)

    if streams and nMixtures > 0:
        print "ERROR: prototype cannot have streams and mixtures at the same time.\n"
    # TODO protoype should work with mixtures and streams, both at the same time

    hline = ('~h "%s"\n<BeginHMM>\n <NumStates> %d\n' % (protoName, nStates+2))
    protoFile.write(hline)

    # Defino los vectores de medias y varianzas para cada estado
    for st in range(nStates):
        numMixes_str = ""
        if nMixtures > 0:
            numMixes_str = "<NumMixes> %d" % nMixtures

        stline = (' <State> %d %s\n' % (st+2, numMixes_str))
        protoFile.write(stline)

        ceros = '0.0 '*nFeatures
        meanline = ('   <Mean> %d\n     %s\n' % (nFeatures, ceros))
        varline = ('   <Variance> %d\n     %s\n' % (nFeatures, ceros))

        for nm in range(nMixtures):
            mixture_line = ('  <Mixture> %d %f\n' % (nm+1, 1.0/nMixtures))
            protoFile.write(mixture_line)
            protoFile.write(meanline)
            protoFile.write(varline)

        if nMixtures == 0 and not streams:
            protoFile.write(meanline)
            protoFile.write(varline)

        if streams:
           for n in range(nStreams):
               streamline = ('  <Stream> %d\n' %(n+1))
               protoFile.write(streamline)

               nStream = streams[n]
               ceros = '0.0 '*nStream
               meanline = ('   <Mean> %d\n     %s\n' % (nStream, ceros))
               varline = ('   <Variance> %d\n     %s\n' % (nStream, ceros))
               protoFile.write(meanline)
               protoFile.write(varline)

    # Matriz de posibles transiciones entre estados
    transpline = (' <TransP> %d\n' % (nStates+2))
    protoFile.write(transpline)

    for ii in range(nStates+2):
        protoFile.write('   ')
        for jj in range(nStates+2):
            if (jj == 1) and (ii == 0):
                protoFile.write('1.0 ')
            elif (jj >= ii) and (ii > 0) and (ii < nStates+1):
                prob = 1.0/(nStates+2-ii)
                protoFile.write("%s " % prob)
    #        elif (jj == ii) and (ii>0) and (ii<nStates+1):
    #            protoFile.write('0.5 ')
    #        elif (jj == ii + 1) and (ii>0) and (ii<nStates+1):
    #            protoFile.write('0.5 ')
            else:
                protoFile.write('0.0 ')
        protoFile.write('\n')

    # Ultima linea donde avisa del fin del HMM
    endline = '<EndHMM>\n'
    protoFile.write(endline)

    protoFile.close()
    sys.stdout.flush()


def write_textfile(filename, content):
    "Dedent and save content in filename. Print name of saved file."
    txtfile = open(filename, 'w')
    txtfile.write(textwrap.dedent(content))
    txtfile.close()
    print "Archivo creado:", filename
    sys.stdout.flush()

def print_stdout(content):
    "dedent, print to stdout and flush it"
    print textwrap.dedent(content)
    sys.stdout.flush()

def get_num_features(htk_filename):
    "get number of features from an htk_file"
    flag = os.system("HList -A -V -D -T 3 -h -e 0 %s > temp.log" %htk_filename)
    if flag > 0:
        print "ERROR: failed to get number of features from htk file"
        return -1
    else:
        logfile = open('temp.log', 'r')
        logfile_content = logfile.read()
        logfile.close()
        os.system('rm temp.log')
        print logfile_content
        # parsing number of features
        numcomps = logfile_content.find('Num Comps:')
        sampleperiod = logfile_content.find('Sample Period:')
        num_features = int(logfile_content[numcomps+10:sampleperiod])
        return num_features

def set_features_function(a2features_filename, features, signals):
    """Creates a2features.m file in the specified location, with features and
    signals given. List of extracted features and list of streams are returned."""
    a2features_content = textwrap.dedent("""\
    % This file was created automatically by runall.py
    function features = a2features( a )
    %convierte un registro en las caracteristicas para pasarselas al htk
    features = [];
    """)
    if 'mag' in signals:
        a2features_content += "amag = sqrt(a.x.^2 + a.y.^2 + a.z.^2);\n"
    if 'x' in signals:
        a2features_content += "ax = a.x;\n"
    if 'y' in signals:
        a2features_content += "ay = a.y;\n"
    if 'z' in signals:
        a2features_content += "az = a.z;\n"

    extracted_features = []
    streams = [[None, None, None, None, None],
               [0, 0, 0, 0, 0]] # primera lista para nombres, segunda lista para cantidad por stream

    for feature in features:
        feature_index = features.index(feature)

        for signal in signals:
            exist_cep = False

            if 'fft' in feature:
                endnum = feature.find('fft')
                num = int(feature[:endnum])
                a2features_content += "fft%s = spectrogram(a%s, 512, 256, 512, 100);\n" %(signal, signal)
                a2features_content += "fft%s = abs(fft%s(2:%d,:)); " %(signal, signal, num+1)
                a2features_content += "%% Me quedo con %d muestras, para no considerar c0\n" % num
                a2features_content += "features = [features fft%s'];\n" % signal
                extracted_features += ["fft%s%d"%(signal, n) for n in range(1,num+1)]
                streams[0][feature_index] = 'fft'
                streams[1][feature_index] += num
            if ('cep' in feature) or ('f0' == feature) and not exist_cep:
                a2features_content += "[cep%s, qf0%s] = cepstrogram(a%s, 512, 256, 100);\n" %(signal, signal, signal)
                exist_cep = True
            if 'cep' in feature:
                endnum = feature.find('cep')
                num = int(feature[:endnum])
                a2features_content += "features = [features cep%s(1:%d,:)'];\n" % (signal, num)
                extracted_features += ["cep%s%d"%(signal, n) for n in range(1,num+1)]
                streams[0][feature_index] = 'cep'
                streams[1][feature_index] += num
            if 'f0' == feature:
                a2features_content += "features = [features qf0%s'];\n" % signal
                extracted_features += ["qf0%s"%(signal)]
                streams[0][feature_index] = 'f0'
                streams[1][feature_index] += 1
            if 'feat' == feature:
                a2features_content += "feat%s = featuresgram(a%s, 512, 256, 100);\n" %(signal, signal)
                a2features_content += "features = [features feat%s'];\n" % signal
                extracted_features += ["%s%s"%(feat,signal) for feat in ['ene', 'amp', 'max', 'min', 'std']]
                streams[0][feature_index] = 'feat'
                streams[1][feature_index] += 5

    if 'featxyz' in features:
        for axis in ['x', 'y', 'z']:
            a2features_content += "feataxis%s = featuresgram(a.%s, 512, 256, 100);\n" %(axis, axis)
            a2features_content += "features = [features feataxis%s'];\n" % axis
            extracted_features += ["%saxis%s"%(feat,axis) for feat in ['ene', 'amp', 'max', 'min', 'std']]
        streams[0].append('featxyz')
        streams[1].append(15)
    a2features_content += "end\n"

    write_textfile(a2features_filename, a2features_content)

    # remove zeros from streams
    for useless in range(streams[0].count(None)):
        streams[0].remove(None)
        streams[1].remove(0)

    return extracted_features, streams

def tie_sil2relax(old_hmm_folder, hmm_list_file, hed_file):
    "tie silence state to relax central state"

    # HMM initial folder
    auxhmm = old_hmm_folder                  # initial hmm folder */*/hmm##
    slashhmm = auxhmm.find('/hmm')           # /hmm position
    hmmfolder = auxhmm[:slashhmm+4]          # hmm folder "*/*/hmm"
    oldhmmNumber = int(auxhmm[slashhmm+4:])  # initial hmm number

    # number of new model to train
    newhmmNumber = oldhmmNumber + 1

    # HMM list argument string
    hmmlist = hmm_list_file

    print_stdout("-------------------------------------------------------------------")
    print_stdout("Tying sil and relax in hmm%d..." % newhmmNumber)

    # update folder's names of old and new model
    oldhmmFolder = hmmfolder + str(oldhmmNumber)
    newhmmFolder = hmmfolder + str(newhmmNumber)

    # creo la carpeta del modelo nuevo si no existe
    if not os.path.exists(newhmmFolder):
        os.mkdir(newhmmFolder)
        print_stdout(newhmmFolder + " was created")

    tieSilRelaxFileName = hed_file

    os.system("HHEd -A -V -D -T 3 -H %s/macros -H %s/hmmdefs -M %s %s %s"
              %(oldhmmFolder, oldhmmFolder, newhmmFolder, tieSilRelaxFileName,
                hmmlist))
    sys.stdout.flush()

    print_stdout("Tying sil and relax has finished")
    print_stdout("-------------------------------------------------------------------")

