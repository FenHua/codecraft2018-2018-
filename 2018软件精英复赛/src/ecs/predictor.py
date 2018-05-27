import utils
import Allocation
import mirror
import copy
import math
import datetime

def predict_vm(ecs_infor_array,input_file_array):

    #Get the CPU information
    N_Stype,Servers,N_Pvm,Pvm,Predict_time,Predict_Start=utils.splitEscData(ecs_infor_array)

    #Get the History Data information
    length,Hvm,History_End=utils.splitInputData(input_file_array)
    #History Data
    Hdate=datetime.datetime.strptime(History_End,"%Y-%m-%d %H:%M:%S").date()

    #Statistic and Split
    #lenD,S_Data=utils.Statistic_Split(length,Hvm,N_Pvm,Pvm)
    lenD,S_Data=utils.Denoise_Split(length,Hvm,N_Pvm,Pvm)

    # deal with gaps
    gaps=int(round((utils.getTimeDiff(Predict_Start,History_End))/86400))
    for i in range(N_Pvm):
        for j in range(gaps):
            S_Data[i].append(S_Data[i][(-7)])
    
    result = []
    if ecs_infor_array is None:
        print 'ecs information is none'
        return result
    if input_file_array is None:
        print 'input file information is none'
        return result
    
    if(N_Pvm>5):
        return
        V=3.3
        NEPvm=mirror.Commirror(lenD,N_Pvm,S_Data,Predict_time,V)
        for i in range(N_Pvm):
            if((Pvm[i][0]=="flavor3")and(Hdate.month>6)):
                NEPvm[i]=int(NEPvm[i]*19)
    else:
        #add value
        #V=4
        V=0
        NEPvm=mirror.Smirror(lenD,N_Pvm,S_Data,Predict_time,V)
    for i in range(N_Pvm):
        if(Pvm[i][0]=="flavor8"):
            NEPvm[i]=int(NEPvm[i]*1.2)
    
    # allocation
    Servers_N,P_Servers=Allocation.Allocate(NEPvm,Pvm,N_Stype,Servers)

    
    result=utils.results_expression(P_Servers,Servers_N,Servers,Pvm)
    return result


            
            
        
        
    
    




















