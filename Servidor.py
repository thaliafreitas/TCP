#!/usr/bin/env python
# -*- coding: utf-8 -*-
import select
import socket
import sys
import utils 
import numpy as np
import struct
from bitstring import BitArray
from bitstring import BitStream
from bitstring import BitString



if __name__ == "__main__":

  
    args = sys.argv
    if len(args) != 3: #Verifica se os argumentos foram passados corretamente
        print utils.SERVER_PORT
        sys.exit()
        
    port = int(args[1]) 
    fileDir = args[2] 
    conectId = 0  
    gerenConect = dict() 
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #serverSocket.setblocking(0)
    #serverSocket.settimeout(10) 
    serverSocket.bind(("", port))
    bodyData = ""
    tamBody = 0
    lastseqNum = 0
    ackEnvi = 0 
 
    

    print utils.SERVER_START.format(port)  
   
    while 1:             
            try:           
                data, addr = serverSocket.recvfrom(524)                                                                 
                if data:  
                     if len(data) == 12:
                         s = struct.Struct('i i i')
                         seqNumRecv, ackNumRecv, oResto= s.unpack(data) 
                     else:  
                        tamBody = len(data[12:525])         
                        struct_fmt = "{}s".format(tamBody)
                        struct_fmt = "i i i " + struct_fmt 
                        s = struct.Struct(struct_fmt)
                        seqNumRecv, ackNumRecv, oResto, bodyData = s.unpack(data) 
                           
                     oRestoStr = format(oResto, '032b')
                     oRestoStr = "0b" + oRestoStr
                     bitstringHead = BitStream(oRestoStr)                                                                                 
                     idNumRecv = bitstringHead.read('uint:16')          
                     notUsedRecv = bitstringHead.read('uint:13')           
                     ackRecv = bitstringHead.read('uint:1')            
                     synRecv = bitstringHead.read('uint:1')      
                     fimRecv = bitstringHead.read('uint:1')                                                        
                     
                     if synRecv == 1:  
                        print "synRecv == 1"
                        conectId = conectId + 1                         
                        seqNum = np.int32(4321)   
                        lastseqNum = seqNum             
                        ackNum = np.int32(seqNumRecv + 1) 
                        ackEnvi = ackNum
                        oRestoBin = BitStream(32)
                        oRestoBin[30] = 1 
                        oRestoBin[29] = 1 
                        del oRestoBin[1:17]   
                        idNum = format(conectId, '#018b')                           
                        idBitArray = BitString(idNum)                                                       
                        oRestoBin = idBitArray + oRestoBin   
                                    
                        idNumTest = oRestoBin.read('uint:16')          
                        notUsedTest = oRestoBin.read('uint:13')           
                        ackTest = oRestoBin.read('uint:1')            
                        synTest = oRestoBin.read('uint:1')      
                        fimTest = oRestoBin.read('uint:1')  
                        print "ackNumEnv" + str(ackNum)      
                        #print "seqEnv" + str(seqNum) 
                        ##print "idEnv" + str(idNumTest)
                        ##print "ackEnv" + str(ackTest)
                        ##print "synEnv" + str(synTest)
                        ##print "fimEnv" + str(fimTest)
                        #print "------------------FIM------------" 
                                                        
                        inteiro = oRestoBin.uint
                        oResto = np.int32(inteiro)  
                        s = struct.Struct('i i i')
                        gerenConect[conectId] = [seqNum, ackNum, ackEnvi, conectId, lastseqNum]
                        head = s.pack(seqNum, ackNum, oResto)               
                        serverSocket.sendto(head, addr)
                        
                        
                     elif fimRecv == 1: 
                        con = gerenConect[idNumRecv] 
                        print "fimRecv == 1" 
                        print seqNumRecv                
                        con[0] = np.int32(4322)
                        con[1] = np.int32(seqNumRecv + 1) 
                        oRestoBin = BitStream(32)
                        oRestoBin[29] = 1 
                        del oRestoBin[1:17]   
                        idNum = format(con[3], '#018b')                           
                        idBitArray = BitString(idNum)                                                       
                        oRestoBin = idBitArray + oRestoBin   
                                    
                        idNumTest = oRestoBin.read('uint:16')          
                        notUsedTest = oRestoBin.read('uint:13')           
                        ackTest = oRestoBin.read('uint:1')            
                        synTest = oRestoBin.read('uint:1')      
                        fimTest = oRestoBin.read('uint:1')  
                        print "ackNumEnv" + str(con[1])      
                        #print "seqEnv" + str(seqNum) 
                        ##print "idEnv" + str(idNumTest)
                        ##print "ackEnv" + str(ackTest)
                        ##print "synEnv" + str(synTest)
                        ##print "fimEnv" + str(fimTest)
                        #print "------------------FIM------------" 
                                                        
                        inteiro = oRestoBin.uint
                        oResto = np.int32(inteiro)  
                        s = struct.Struct('i i i')
                        head = s.pack(con[0], con[1], oResto)               
                        serverSocket.sendto(head, addr)                       
                        con[0] = np.int32(4322)
                        con[1] = np.int32(0) 
                        oRestoBin = BitStream(32)
                        oRestoBin[31] = 1 
                        del oRestoBin[1:17]   
                        idNum = format(con[3], '#018b')                           
                        idBitArray = BitString(idNum)                                                       
                        oRestoBin = idBitArray + oRestoBin   
                                    
                        idNumTest = oRestoBin.read('uint:16')          
                        notUsedTest = oRestoBin.read('uint:13')           
                        ackTest = oRestoBin.read('uint:1')            
                        synTest = oRestoBin.read('uint:1')      
                        fimTest = oRestoBin.read('uint:1')  
                        #print "ackNumEnv" + str(ackNum)      
                        #print "seqEnv" + str(seqNum) 
                        ##print "idEnv" + str(idNumTest)
                        ##print "ackEnv" + str(ackTest)
                        ##print "synEnv" + str(synTest)
                        ##print "fimEnv" + str(fimTest)                     
                                                        
                        inteiro = oRestoBin.uint
                        oResto = np.int32(inteiro)  
                        s = struct.Struct('i i i')
                        head = s.pack(con[0], con[1], oResto) 
                        gerenConect[idNumRecv] = con               
                        serverSocket.sendto(head, addr)                
                        
                        
                        
                     elif ackRecv == 1 and ackNumRecv == 4322:
                     
                        con = gerenConect[idNumRecv]        
                        if seqNumRecv == con[2]:
                            fileName= "/home/paloma/Documentos/Redes" + fileDir + "/" + str(idNumRecv) + ".file"
                            arqi = open( fileName, 'a')        
                            con[0] = np.int32(4322)         
                            con[1] = np.int32(seqNumRecv + tamBody)                     
                            con[2] = con[1]                                                 
                            oRestoBin = BitStream(32)    
                            oRestoBin[29] = 1 
                            del oRestoBin[1:17]
                            idNum = format(con[3], '#018b')  
                            idBitArray = BitString(idNum)
                            oRestoBin = idBitArray + oRestoBin  
                            
                            idNumTest = oRestoBin.read('uint:16')          
                            notUsedTest = oRestoBin.read('uint:13')           
                            ackTest = oRestoBin.read('uint:1')            
                            synTest = oRestoBin.read('uint:1')      
                            fimTest = oRestoBin.read('uint:1')  
                            print "ackNumEnv" + str(con[1])      
                            #print "seqEnv" + str(seqNum) 
                            ##print "idEnv" + str(idNumTest)
                            ##print "ackEnv" + str(ackTest)
                            ##print "synEnv" + str(synTest)
                            ##print "fimEnv" + str(fimTest) 
                            #print "------------------FIM------------"             
                             
                                            
                            inteiro = oRestoBin.uint
                            oResto = np.int32(inteiro)  
                            s = struct.Struct('i i i')
                            
                            con[4] = con[0]
                            head = s.pack(con[0], con[1], oResto) 
                            gerenConect[idNumRecv] = con              
                            serverSocket.sendto(head, addr)                                                                         
                            arqi.write(bodyData) 
                                            
                     elif ackRecv == 1 and ackNumRecv == 4323:
                        print "ackRecv == 1 and ackNumRecv == 4323"
                        fileName= "/home/paloma/Documentos/Redes" + fileDir + "/" + str(idNumRecv) + ".file"
                        arqi = open( fileName, 'a')     
                        arqi.close()
                        print "concluido"
                        
                     
                                                           
                     else:                       
                            con = gerenConect[idNumRecv]                       
                            if seqNumRecv == con[2]:
                                print "seqNumRecv " + str(seqNumRecv) + " ackEnvi" + str(con[2])
                                print "Rcebendo o pacote com o seqNum = " + str(seqNumRecv)
                                fileName= "/home/paloma/Documentos/Redes" + fileDir + "/" + str(idNumRecv) + ".file"
                                arqi = open( fileName, 'a')                                                              
                                con[0] = np.int32(4322)
                                
                                #if seqNumRecv + tamBody > 102400:
                                 #   ackNum = np.int32(0)
                                #else: 
                                con[1] = np.int32(seqNumRecv + tamBody)     
                                
                                con[2] = con[1]                                                 
                                oRestoBin = BitStream(32)    
                                oRestoBin[29] = 1 
                                del oRestoBin[1:17]
                                idNum = format(idNumRecv, '#018b')  
                                idBitArray = BitString(idNum)
                                oRestoBin = idBitArray + oRestoBin  
                                
                                idNumTest = oRestoBin.read('uint:16')          
                                notUsedTest = oRestoBin.read('uint:13')           
                                ackTest = oRestoBin.read('uint:1')            
                                synTest = oRestoBin.read('uint:1')      
                                fimTest = oRestoBin.read('uint:1')  
                                print "ackNumEnv" + str(con[1])      
                                #print "seqEnv" + str(seqNum) 
                                ##print "idEnv" + str(idNumTest)
                                ##print "ackEnv" + str(ackTest)
                                ##print "synEnv" + str(synTest)
                                ##print "fimEnv" + str(fimTest) 
                                #print "------------------FIM------------"   
                         
                                inteiro = oRestoBin.uint
                                oResto = np.int32(inteiro)  
                                s = struct.Struct('i i i')
                                
                                head = s.pack(con[0], con[1], oResto) 
                                gerenConect[idNumRecv] = con              
                                serverSocket.sendto(head, addr)                                                 
                                arqi.write(bodyData)      
                     
                            elif seqNumRecv < con[4]:
                                con = gerenConect[idNumRecv] 
                                print "pacote duplicado "
                                con[0] = np.int32(4322)
                                        
                                #if seqNumRecv + tamBody > 102400:
                                 #   ackNum = np.int32(0)
                                #else: 
                                con[1] = np.int32(con[2])     
                                                                                       
                                oRestoBin = BitStream(32)    
                                oRestoBin[29] = 1 
                                del oRestoBin[1:17]
                                idNum = format(idNumRecv, '#018b')  
                                idBitArray = BitString(idNum)
                                oRestoBin = idBitArray + oRestoBin  
                                
                                idNumTest = oRestoBin.read('uint:16')          
                                notUsedTest = oRestoBin.read('uint:13')           
                                ackTest = oRestoBin.read('uint:1')            
                                synTest = oRestoBin.read('uint:1')      
                                fimTest = oRestoBin.read('uint:1')  
                                print "ackNumEnv" + str(con[1])      
                                #print "seqEnv" + str(seqNum) 
                                ##print "idEnv" + str(idNumTest)
                                ##print "ackEnv" + str(ackTest)
                                ##print "synEnv" + str(synTest)
                                ##print "fimEnv" + str(fimTest) 
                                #print "------------------FIM------------"   
                         
                                inteiro = oRestoBin.uint
                                oResto = np.int32(inteiro)  
                                s = struct.Struct('i i i')
                                
                                head = s.pack(con[0], con[1], oResto)
                                gerenConect[idNumRecv] = con               
                                serverSocket.sendto(head, addr)    
                            else:
                                #print "Recebeu fora de orde"                                                              
                            con[4] = con[0]
                                
                    
                    

            except socket.timeout:
                #print "Deu timeout"
                con = gerenConect[idNumRecv] 
                if con[1] == 0:             
                    con[0] = np.int32(4322)
                    con[1] = np.int32(0) 
                    oRestoBin = BitStream(32)
                    oRestoBin[31] = 1 
                    del oRestoBin[1:17]   
                    idNum = format(con[3], '#018b')                           
                    idBitArray = BitString(idNum)                                                       
                    oRestoBin = idBitArray + oRestoBin   
                                
                    idNumTest = oRestoBin.read('uint:16')          
                    notUsedTest = oRestoBin.read('uint:13')           
                    ackTest = oRestoBin.read('uint:1')            
                    synTest = oRestoBin.read('uint:1')      
                    fimTest = oRestoBin.read('uint:1')  
                    #print "ackNumRenvEnv" + str(ackNum)      
                    #print "seqEnv" + str(seqNum) 
                    ##print "idEnv" + str(idNumTest)
                    ##print "ackEnv" + str(ackTest)
                    ##print "synEnv" + str(synTest)
                    ##print "fimEnv" + str(fimTest)
                    #print "------------------FIM------------" 
                                                    
                    inteiro = oRestoBin.uint
                    oResto = np.int32(inteiro)  
                    s = struct.Struct('i i i')
                    
                    head = s.pack(con[0], con[1], oResto) 
                    gerenConect[idNumRecv] = con              
                    serverSocket.sendto(head, addr)         
                     
            
          
            
        
            
                                    
    
                
    
    
    serverSocket.close()
    
