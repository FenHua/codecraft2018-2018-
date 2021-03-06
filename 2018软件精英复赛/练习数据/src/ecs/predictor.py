import utils
import Allocation
import ES
import copy
import math
import Score

def predict_vm(ecs_infor_array,input_file_array):

    #Get the CPU information
    N_Stype,Servers,N_Pvm,Pvm,Predict_time,Predict_Start=utils.splitEscData(ecs_infor_array)

    #Get the History Data information
    length,Hvm,History_End=utils.splitInputData(input_file_array)
    #History Data
    #Statistic and Split
    lenD,S_Data=utils.Statistic_Split(length,Hvm,N_Pvm,Pvm)

    # deal with gaps
    gaps=int(round((utils.getTimeDiff(Predict_Start,History_End))/86400))
    for i in range(N_Pvm):
        for j in range(gaps):
            S_Data[i].append((S_Data[i][-gaps]))

    
    result = []
    if ecs_infor_array is None:
        print 'ecs information is none'
        return result
    if input_file_array is None:
        print 'input file information is none'
        return result

    if(N_Pvm>5):
        T=2
        V=0
        #return
        NEPvm=ES.ES(lenD,N_Pvm,S_Data,Predict_time,T,V)
        for i in range(N_Pvm):
            if(Pvm[i][0]=="flavor3")and(int(History_End[6])>6):
                NEPvm[i]=int(NEPvm[i]*34)
    else:
        #return
        T=0.85
        V=6
        NEPvm=ES.ES(lenD,N_Pvm,S_Data,Predict_time,T,V)
    for i in range(N_Pvm):
        if(Pvm[i][0]=="flavor8"):
            NEPvm[i]=int(NEPvm[i]*1.7)
    # allocation
    Servers_N,P_Servers=Allocation.Allocate(NEPvm,Pvm,N_Stype,Servers)
    
    result=utils.results_expression(P_Servers,Servers_N,Servers,Pvm)
    return result


            
            
        
        
    
    




















