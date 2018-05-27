from __future__ import division
import utils
import lwlr
import TDEstimation
import math

def predict_vm(ecs_infor_array,input_file_array):

    #Get the CPU information
    CPU_kernal,CPU_memory,N_Pvm,condition,Pvm,Predict_time,Predict_Start=utils.splitEscData(ecs_infor_array)
    '''
    CPU_kernal: The number of CPU kernal
    CPU_memory: The size of memory
    N_Pvm: The number of Vms which need to predict
    condition
    Pvm: The Vms which need to predict
    Predict_time: The period of prediction 
    '''
    
    #Get the History Data information
    length,Hvm,History_Start=utils.splitInputData(input_file_array)
    #History Data

    #Statistic and Split
    lenD,S_Data=utils.Statistic_Split(length,Hvm,N_Pvm,Pvm)
    #print S_Data
    
    result = []
    if ecs_infor_array is None:
        print 'ecs information is none'
        return result
    if input_file_array is None:
        print 'input file information is none'
        return result
    #---------------------method one----------------------
    #NEPvm=lwlr.Prob_predict(N_Pvm,lenD,S_Data,Predict_time)
    
    #---------------------method two----------------------
    #NEPvm=lwlr.lwlr_predict(N_Pvm,lenD,S_Data,Predict_time)

    #---------------------method Three--------------------
    #NEPvm=lwlr.Simp_regress(N_Pvm,lenD,S_Data,Predict_time)
    #print NEPvm

    #---------------------method Four--------------------
    #NEPvm=lwlr.EachD_predict()
    #print NEPvm

    #--------------------method five estimate--------------
    NEPvm=TDEstimation.EstTD(History_Start,Predict_Start,lenD,N_Pvm,S_Data,Predict_time)
    print NEPvm

    
    #write result
    result.append(int(sum(NEPvm)))
    for i in range(N_Pvm):
        result.append((str(Pvm[i][0])+" "+str(int(NEPvm[i]))))
    result.append("")
    
    # the numbor of predicted vms
    total_kernal=0
    total_memory=0
    for i in range(N_Pvm):
        total_kernal=total_kernal+NEPvm[i]*Pvm[i][1]
        total_memory=total_memory+NEPvm[i]*Pvm[i][2]
    if (math.ceil(total_kernal/CPU_kernal)>=math.ceil(total_memory/CPU_memory)):
        N_PCPU=int(math.ceil(total_kernal/CPU_kernal))
    else:
        N_PCPU=int(math.ceil(total_momery/CPU_kernal))

    # allocation
    CPU,N_PCPU=Boxing(N_PCPU,NEPvm,Pvm,N_Pvm,CPU_kernal,CPU_memory)
    result=utils.results_expression(result,CPU,N_PCPU)
    return result


def Boxing(N_PCPU,NEPvm,Pvm,N_Pvm,CPU_kernal,CPU_memory):
    VMs=[]
    # all Predicted vms
    for i in range(N_Pvm):
        for j in range(int(NEPvm[i])):
            VMs.append(Pvm[i])
    lenVMs=len(VMs)
    # The number of all predicted VMs
    CPU=[]
    for i in range(N_PCPU):
        CPU.append([])
    # intialize the cpu list
    VMs_info=[[0 for i in range(2)]for j in range(lenVMs)]
    for i in range(lenVMs):
        VMs_info[i]=utils.SelectVM(VMs[i][0],Pvm,N_Pvm)
    # get each cpu information
    index=[0 for i in range(lenVMs)]
    for j in range(lenVMs):
        index[j]=VMs_info[j][1]-VMs_info[j][0]
    idx=utils.argsort(index)
    # get the index (ascend)

    temp_vms=[]
    temp_vminfo=[]
    for i in range(lenVMs):
        temp_vms.append(VMs[idx[i]])
        temp_vminfo.append(VMs_info[idx[i]])
    VMs=temp_vms
    VMs_info=temp_vminfo
    # get the sorted array
    CPU_index=[(CPU_memory-CPU_kernal) for i in range(N_PCPU)]
    CPU_limit=[[CPU_kernal,CPU_memory] for i in range(N_PCPU)]
    for j in range(lenVMs):
        count=0
        idx=utils.argsort(CPU_index)
        for z in range(N_PCPU):
            if(CPU_limit[idx[z]][0]>=VMs_info[j][0]and CPU_limit[idx[z]][1]>=VMs_info[j][1]):
                CPU[idx[z]].append(VMs[j][0])
                CPU_limit[idx[z]][0]=CPU_limit[idx[z]][0]-VMs_info[j][0]
                CPU_limit[idx[z]][1]=CPU_limit[idx[z]][1]-VMs_info[j][1]
                CPU_index[idx[z]]=CPU_index[idx[z]]-VMs_info[j][1]+VMs_info[j][0]
                break
            else:    
                count=count+1
        if (count==len(CPU)):
            N_PCPU=N_PCPU+1
            CPU.append([])
            CPU_limit.append([CPU_kernal,CPU_memory])
            CPU_index.append((CPU_memory-CPU_kernal))
            CPU[(N_PCPU-1)].append(VMs[j][0])
            CPU_limit[(N_PCPU-1)][0]=CPU_limit[(N_PCPU-1)][0]-VMs_info[j][0]
            CPU_limit[(N_PCPU-1)][1]=CPU_limit[(N_PCPU-1)][1]-VMs_info[j][1]
            CPU_index[(N_PCPU-1)]=CPU_index[(N_PCPU-1)]-VMs_info[j][1]+VMs_info[j][0]
            
    return CPU,N_PCPU
        
                                    
         
        
    
    




















