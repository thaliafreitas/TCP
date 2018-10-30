#!/usr/bin/env python
# -*- coding: utf-8 -*-
import select
import sys
import utils 
import socket
import numpy as np
import struct
import time
import collections
import os
from bitstring import BitArray
from bitstring import BitStream
from bitstring import BitString

def reEnvio():
    #print "Reenvio"
    reEnvio = janela.copy()          
    while(len(reEnvio) != 0 ):                                                
        seqNum = np.int32(reEnvio.keys()[0])                                                              
        ackNum = np.int32(0) 
        oRestoBin = BitStream(32)              
        del oRestoBin[1:17] 
        idNum = format(idNumRecv, '#018b')

        idBitArray = BitStream(idNum)                               

        oRestoBin = idBitArray + oRestoBin 
        
        idNumTest = oRestoBin.read('uint:16')          
        notUsedTest = oRestoBin.read('uint:13')           
        ackTest = oRestoBin.read('uint:1')            
        synTest = oRestoBin.read('uint:1')      
        fimTest = oRestoBin.read('uint:1')  
        #print "ackNumREnvEnv" + str(ackNum)      
        print "seqREnvEnv" + str(seqNum) 
        ##print "idEnv" + str(idNumTest)
        ##print "ackEnv" + str(ackTest)
        ##print "synEnv" + str(synTest)
        ##print "fimEnv" + str(fimTest) 
        ##print "------------------FIM------------" 
          

        inteiro = oRestoBin.uint
        oResto = np.int32(inteiro)  
        dadosReEnv = reEnvio.values()[0]                          
        struct_fmt = "{}s".format(len(dadosReEnv))                
        struct_fmt = "i i i " + struct_fmt
        s = struct.Struct(struct_fmt)
        pct = s.pack(seqNum, ackNum, oResto, reEnvio.values()[0])  
        cliente_socket.sendto(pct, (host, port))                                                   
        ##print str(reEnvio)                                                      
        del reEnvio[reEnvio.keys()[0]]  
            




if __name__ == "__main__":

    args = sys.argv
    if len(args) != 4:
        print utils.CLIENT_USAGE
        sys.exit()

    host = args[1]
    port = int(args[2])
    fileName = args[3]
    
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cliente_socket.setblocking(0)
    cliente_socket.settimeout(0.5)
    arq = open(fileName, 'r') 
    
    if os.path.getsize ( "/home/paloma/Documentos/Redes" + "/" + fileName ) > 100000000:
         print "Apenas arquivos de ate 100MB são suportados "
         sys.exit()
        
             
    seqNum = np.int32(12345)
    ackNum = np.int32(0) 
    oRestoBin = BitStream(32)
    oRestoBin[30] = 1 
    inteiro = oRestoBin.uint
    oResto = np.int32(inteiro)  
    s = struct.Struct('i i i')
    head = s.pack(seqNum, ackNum, oResto)               
    cliente_socket.sendto(head, (host, port))
    cwnd = 512
    ss_thresh = 10000
    lastDadosTam = 0
    janela = dict()
    auxJan = 512 
    continuarSeq = 0      
    print "seqEnv" + str(seqNum) 
   

    print 'Start the transfer'
    
   
                       
    dados = arq.read(512)
    lastDadosTam = len(dados)
    

    while 1: 
       
            try:
                data, addr = cliente_socket.recvfrom(12)   
                if data: 
                     s = struct.Struct('i i i')
                     seqNumRecv, ackNumRecv, oResto= s.unpack(data) 
                     oRestoStr = format(oResto, '#034b')
                     bitstring = BitStream(oRestoStr)                                                                                 
                     idNumRecv = bitstring.read('uint:16') 
                     notUsedRecv = bitstring.read('uint:13')           
                     ackRecv = bitstring.read('uint:1')            
                     synRecv = bitstring.read('uint:1')      
                     fimRecv = bitstring.read('uint:1')           
                                                                              
                     if synRecv == 1 and ackRecv == 1:
                     
                        seqNum = np.int32(ackNumRecv)

                        ackNum = np.int32(seqNumRecv + 1) 
                        oRestoBin = BitArray(32)
                        oRestoBin[29] = 1 
                        idNum = format(idNumRecv, '#018b')                           
                        idBitArray = BitString(idNum)               
                        del oRestoBin[1:17]                        
                        oRestoBin = idBitArray + oRestoBin  
                        
                        idNumTest = oRestoBin.read('uint:16')          
                        notUsedTest = oRestoBin.read('uint:13')           
                        ackTest = oRestoBin.read('uint:1')            
                        synTest = oRestoBin.read('uint:1')      
                        fimTest = oRestoBin.read('uint:1')              
                        print "seqEnv" + str(seqNum) 
                        
                                                                                            
                        inteiro = oRestoBin.uint
                        oResto = np.int32(inteiro)  
                        struct_fmt = "{}s".format(len(dados))                
                        struct_fmt = "i i i " + struct_fmt
                        s = struct.Struct(struct_fmt)
                        pct = s.pack(seqNum, ackNum, oResto, dados)  
                        cliente_socket.sendto(pct, (host, port))
                        janela [seqNum] = dados                                                
                        dados = arq.read(512) 
                                                               
                                        
                     if synRecv == 0 and ackRecv == 1:
                        print  "synRecv == 0 and ackRecv == 1"                 
                        if cwnd < ss_thresh :                            
                           cwnd += 512
                        else:                            
                            cwnd += (512*512)/cwnd                    
                        aux = len(janela.values()[0]) + janela.keys()[0]                                               
                        if ackNumRecv == aux:                           
                            del janela[janela.keys()[0]]
                            
                            if len(janela) == 0 and dados == "":                              
                                break
                                 
                                                       
                            if len(janela) == 0 and dados != "":                                 
                                auxCwnd = cwnd       
                                while(auxCwnd > 0):                                       
                                    if dados != "":
                                    
                                        #if seqNum + lastDadosTam  > 102400:
                                            #continuarSeq = seqNum + lastDadosTam
                                            #seqNum = np.int32(0)
                                        
                                        #else: 
                                        seqNum = np.int32(seqNum + lastDadosTam ) 
                                           
                          
                                        ackNum = np.int32(0) 
                                        oRestoBin = BitStream(32)              
                                        del oRestoBin[1:17] 
                                        idNum = format(idNumRecv, '#018b')
                                        idBitArray = BitStream(idNum)                               

                                        oRestoBin = idBitArray + oRestoBin 
                                        
                                        idNumTest = oRestoBin.read('uint:16')          
                                        notUsedTest = oRestoBin.read('uint:13')           
                                        ackTest = oRestoBin.read('uint:1')            
                                        synTest = oRestoBin.read('uint:1')      
                                        fimTest = oRestoBin.read('uint:1')  
                                        #print "ackNumEnv" + str(ackNum)                                                                   
                                        print "seqEnv" + str(seqNum)                                            
                                        ##print "idEnv" + str(idNumTest)
                                        ##print "ackEnv" + str(ackTest)
                                        ##print "synEnv" + str(synTest)
                                        ##print "fimEnv" + str(fimTest) 
                                        #print "------------------FIM------------" 
                                          
                                        inteiro = oRestoBin.uint
                                        oResto = np.int32(inteiro)                              
                                        struct_fmt = "{}s".format(len(dados))                
                                        struct_fmt = "i i i " + struct_fmt
                                        s = struct.Struct(struct_fmt)
                                        pct = s.pack(seqNum, ackNum, oResto, dados)                                  
                                        cliente_socket.sendto(pct, (host, port))                                      
                                        auxCwnd = auxCwnd - 512                                        
                                        janela [seqNum] = dados
                                        janelaOrder = collections.OrderedDict(sorted(janela.items())) 
                                        janela.clear()
                                        janela = janelaOrder                                                                      
                                        lastDadosTam = len(dados)                               
                                        dados = arq.read(512)  
                                  
                                    
                                    else:                                                                          
                                        break    
                                
                                
                        else:                           
                            reEnvio()          
                            
                            
            except socket.timeout:              
                reEnvio()
               
                                                       

   
    arq.close()
    print 'transfer concluded'
   
    seqNum = np.int32(ackNumRecv + 1)
    ackNum = np.int32(0) 
    oRestoBin = BitStream(32)
    oRestoBin[31] = 1 
    del oRestoBin[1:17] 
    idNum = format(idNumRecv, '#018b')
    idBitArray = BitStream(idNum)                               
    oRestoBin = idBitArray + oRestoBin 
                    
    idNumTest = oRestoBin.read('uint:16')          
    notUsedTest = oRestoBin.read('uint:13')           
    ackTest = oRestoBin.read('uint:1')            
    synTest = oRestoBin.read('uint:1')      
    fimTest = oRestoBin.read('uint:1')  

    #print "ackNumEnv" + str(ackNum)      
    #print "seqEnv" + str(seqNum) 
    #print "idEnv" + str(idNumTest)
    #print "ackEnv" + str(ackTest)
    #print "synEnv" + str(synTest)
    #print "fimEnv" + str(fimTest) 
    #print "------------------FIM------------" 
      
    inteiro = oRestoBin.uint
    oResto = np.int32(inteiro)                                            
    struct_fmt = "i i i "
    s = struct.Struct(struct_fmt)
    pct = s.pack(seqNum, ackNum, oResto)  
    cliente_socket.sendto(pct, (host, port)) 
     
    data, addr = cliente_socket.recvfrom(12)      
    if data: 
             s = struct.Struct('i i i')
             seqNumRecv, ackNumRecv, oResto= s.unpack(data) 
             oRestoStr = format(oResto, '#034b')
             bitstring = BitStream(oRestoStr)                                                                                 

             idNumRecv = bitstring.read('uint:16') 
             notUsedRecv = bitstring.read('uint:13')           
             ackRecv = bitstring.read('uint:1')            
             synRecv = bitstring.read('uint:1')      
             fimRecv = bitstring.read('uint:1') 
             #print "------------------INICIO------------"                         
             #print "ackNumRevc" + str(ackNumRecv)      
             #print "seqRevc" + str(seqNumRecv) 
             #print "idRevc" + str(idNumRecv)  
             #print "ackRevc" + str(ackRecv)
             #print "synRevc" + str(synRecv)
             #print "fimRevc" + str(fimRecv)                       
             if ackRecv == 1:   
                cliente_socket.settimeout(2)                
                end_time = time.time() + 2             
                countTimer = 0
                sleepTime = 0.500                 
                while time.time() < end_time:                    
                    try:
                        data, addr = cliente_socket.recvfrom(12)      
                        if data: 
                             s = struct.Struct('i i i')
                             seqNumRecv, ackNumRecv, oResto= s.unpack(data) 
                             oRestoStr = format(oResto, '#034b')
                             bitstring = BitStream(oRestoStr)                                                                          
                             idNumRecv = bitstring.read('uint:16') 
                             notUsedRecv = bitstring.read('uint:13')           
                             ackRecv = bitstring.read('uint:1')            
                             synRecv = bitstring.read('uint:1')      
                             fimRecv = bitstring.read('uint:1') 
                             #print "------------------INICIO------------"                         
                             #print "ackNumRevc" + str(ackNumRecv)      
                             #print "seqRevc" + str(seqNumRecv) 
                             #print "idRevc" + str(idNumRecv)  
                             #print "ackRevc" + str(ackRecv)
                             #print "synRevc" + str(synRecv)
                             #print "fimRevc" + str(fimRecv)                                                    
                             if fimRecv == 1:
                                seqNum = np.int32(seqNum + 1 )
                                ackNum = np.int32(seqNumRecv + 1) 
                                oRestoBin = BitArray(32)
                                oRestoBin[29] = 1 
                                idNum = format(idNumRecv, '#018b')                           
                                idBitArray = BitString(idNum)               
                                del oRestoBin[1:17]                        
                                oRestoBin = idBitArray + oRestoBin  
                                
                                idNumTest = oRestoBin.read('uint:16')          
                                notUsedTest = oRestoBin.read('uint:13')           
                                ackTest = oRestoBin.read('uint:1')            
                                synTest = oRestoBin.read('uint:1')      
                                fimTest = oRestoBin.read('uint:1')  
                                #print "ackNumEnv" + str(ackNum)      
                                #print "seqEnv" + str(seqNum) 
                                #print "idEnv" + str(idNumTest)
                                #print "ackEnv" + str(ackTest)
                                #print "synEnv" + str(synTest)
                                #print "fimEnv" + str(fimTest) 
                                                                                                    
                                inteiro = oRestoBin.uint
                                oResto = np.int32(inteiro)  
                                s = struct.Struct('i i i')
                                head = s.pack(seqNum, ackNum, oResto)               
                                cliente_socket.sendto(head, (host, port)) 


                    except socket.timeout:
                        cliente_socket.close()
