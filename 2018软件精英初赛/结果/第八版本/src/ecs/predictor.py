from __future__ import division
import utils
import lwlr
import TDEstimation
import mirror
import copy
import math

def predict_vm(ecs_infor_array,input_file_array):

    #Get the CPU information
    CPU_kernal,CPU_memory,N_Pvm,condition,Pvm,Predict_time,Predict_Start=utils.splitEscData(ecs_infor_array)
    
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

    #--------------------method five estimate--------------
    #NEPvm=TDEstimation.EstTD(History_Start,Predict_Start,lenD,N_Pvm,S_Data,Predict_time)

    #-----------------------Mirror-------------------------
    NEPvm=mirror.Mirror(lenD,N_Pvm,S_Data,Predict_time)
    print NEPvm

    #---------------------method Three--------------------
    #NEPvm=lwlr.lwlr_predict(N_Pvm,lenD,S_Data,Predict_time)
    #print NEPvm

    # allocation
    CPU,N_PCPU=Boxing(NEPvm,Pvm,N_Pvm,CPU_kernal,CPU_memory)
    print N_PCPU
    result=utils.results_expression(CPU,N_PCPU,N_Pvm,Pvm)
    return result


def Boxing(NEPvm,Pvm,N_Pvm,CPU_kernal,CPU_memory):
    VMs=[]
    # all Predicted vms
    for i in range(N_Pvm):
        for j in range(int(NEPvm[i])):
            VMs.append(Pvm[i])
    lenVMs=len(VMs) # The number of all predicted VMs
    # Split vms according to M/K
    VM1=[];
    VM2=[];
    VM4=[];
    for i in range(lenVMs):
        VMs_info=[VMs[i][1],VMs[i][2]]
        if (VMs_info[1]/VMs_info[0]==1):
            VM1.append(VMs[i])
        elif(VMs_info[1]/VMs_info[0]==2):
            VM2.append(VMs[i])
        else:
            VM4.append(VMs[i])
    
    Min=min([len(VM1),len(VM2),len(VM4)])

    # maybe zero
    if (Min==0):
        Min=1
        if(len(VM4)==0):
            P4=1
            Min=min([len(VM1),len(VM2)])
            P2=int(math.ceil(len(VM2)/Min))
            P1=int(math.ceil(len(VM1)/Min))
        elif(len(V2)==0):
            P2=1
            Min=min([len(VM1),len(VM4)])
            P4=int(math.ceil(len(VM4)/Min))
            P1=int(math.ceil(len(VM1)/Min))
        else:
            P1=1
            Min=min([len(VM2),len(VM4)])
            P2=int(math.ceil(len(VM2)/Min))
            P4=int(math.ceil(len(VM4)/Min))
    else:
        P4=int(math.ceil(len(VM4)/Min))
        P2=int(math.ceil(len(VM2)/Min))
        P1=int(math.ceil(len(VM1)/Min))

    idx4=Cond_Sort(VM4)
    idx2=Cond_Sort(VM2)
    idx1=Cond_Sort(VM1)
    VMs=[] #reset
    i4=0
    i2=0
    i1=0
    for i in range(Min):
        for j in range(i4,(i4+P4),1):
            if(j<len(VM4)):
                VMs.append(VM4[idx4[j]])
                i4=i4+1
        for z in range(i2,(i2+P2),1):
            if(z<len(VM2)):
                VMs.append(VM2[idx2[z]])
                i2=i2+1
        for t in range(i1,(i1+P1),1):
            if(t<len(VM1)):
                VMs.append(VM1[idx1[t]])
                i1=i1+1
    CPU=[]
    CPU.append([])
    N_PCPU=0   #default 0
    VMSC=copy.deepcopy(VMs)
    while(1):
        CPU_limit=[CPU_kernal,CPU_memory]
        lenVM=len(VMs)
        for j in range(lenVM):
            VMs_info=[VMs[j][1],VMs[j][2]]
            if(CPU_limit[0]>=VMs_info[0] and CPU_limit[1]>=VMs_info[1]):
                CPU[N_PCPU].append(VMs[j][0])
                CPU_limit[0]=CPU_limit[0]-VMs_info[0]
                CPU_limit[1]=CPU_limit[1]-VMs_info[1]
                VMSC.remove(VMs[j])
        if(utils.SUM_Judge(VMSC,CPU_kernal,CPU_memory)):
            #CPU[0]=CLRes(CPU[0],VMSC,Pvm,N_Pvm,CPU_kernal,CPU_memory)
            break
        else:
            VMs=copy.deepcopy(VMSC)
            CPU.append([])
            N_PCPU=N_PCPU+1 
    return CPU,(N_PCPU+1)
        
def Cond_Sort(VM):
    T_VM=[]
    for i in range(len(VM)):
        T_VM.append(VM[i][1])
    idx=utils.argsort(T_VM)
    return idx

def CLRes(CPU0,VMSC,Pvm,N_Pvm,CPU_kernal,CPU_memory):
    L_k=0
    L_m=0
    for i in range(len(VMSC)):
        L_k=L_k+VMSC[i][1]
        L_m=L_m+VMSC[i][2]

    R_kernal=0
    R_memory=0
    CPU00=copy.deepcopy(CPU0)
    for i in range(len(CPU0)):
        info=utils.SelectVM(CPU0[i],Pvm,N_Pvm)
        if((R_kernal+info[0]<L_k)and(R_memory+info[1]<L_m)):
            R_kernal=R_kernal+info[0]
            R_memory=R_memory+info[1]
            CPU00.remove(CPU0[i])
    CPU0=CPU00
    
    CPU_limit=[CPU_kernal,CPU_memory]
    for j in range(len(CPU0)):
        CPU_limit[0]=CPU_limit[0]-(utils.SelectVM(CPU0[j],Pvm,N_Pvm))[0]
        CPU_limit[1]=CPU_limit[1]-(utils.SelectVM(CPU0[j],Pvm,N_Pvm))[1]
    
    for j in range(len(VMSC)):
            VMs_info=[VMSC[j][1],VMSC[j][2]]
            if((CPU_limit[0]>=VMs_info[0])and(CPU_limit[1]>=VMs_info[1])):
                CPU0.append(VMSC[j][0])
                CPU_limit[0]=CPU_limit[0]-VMs_info[0]
                CPU_limit[1]=CPU_limit[1]-VMs_info[1]
    return CPU0
    
            
            
        
        
    
    




















