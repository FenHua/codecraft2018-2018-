import utils
import Box
import mirror
import copy
import math

def predict_vm(ecs_infor_array,input_file_array):

    #Get the CPU information
    CPU_kernel,CPU_memory,N_Pvm,condition,Pvm,Predict_time,Predict_Start=utils.splitEscData(ecs_infor_array)
    #Get the History Data information
    length,Hvm,History_Start=utils.splitInputData(input_file_array)
    #History Data

    #Statistic and Split
    #lenD,S_Data=utils.Statistic_Split(length,Hvm,N_Pvm,Pvm)
    lenD,S_Data=utils.Denoise_Split(length,Hvm,N_Pvm,Pvm)

    #print S_Data
    
    result = []
    if ecs_infor_array is None:
        print 'ecs information is none'
        return result
    if input_file_array is None:
        print 'input file information is none'
        return result

    #-----------------------Mirror-------------------------
    NEPvm=mirror.Mirror(lenD,N_Pvm,S_Data,Predict_time)
    #-----------------------Smirror-------------------------
    #NEPvm=mirror.Smirror(lenD,N_Pvm,S_Data,Predict_time)
    #-----------------------Smirror-------------------------
    #NEPvm=mirror.Commirror(lenD,N_Pvm,S_Data,Predict_time)

    #print NEPvm


    
    # allocation
    CPU,N_PCPU=Box.Boxing(NEPvm,Pvm,N_Pvm,CPU_kernel,CPU_memory,condition)
    print N_PCPU
    result=utils.results_expression(CPU,N_PCPU,N_Pvm,Pvm)
    return result


            
            
        
        
    
    




















