from __future__ import division
import math
import utils
import copy
def Boxing(NEPvm,Pvm,N_Pvm,CPU_kernel,CPU_memory,condition):
    # Add
    T_idx=utils.argsort(NEPvm)
    NEPvm[(T_idx[0])]=NEPvm[(T_idx[0])]+1
    
    VMs=[]
    # all Predicted vms
    for i in range(N_Pvm):
        for j in range(int(NEPvm[i])):
            VMs.append(Pvm[i])

    VMs=First_Delete(VMs,CPU_kernel,CPU_memory,condition)
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
    VMs=[] #reset
    VM4=Adjust(VM4,0)
    VM2=Adjust(VM2,0)
    VM1=Adjust(VM1,0)
    T_VMs=[VM4,VM2,VM1]
    len4=len(VM4)
    len2=len(VM2)
    len1=len(VM1)
    #maybe exist zero
    if(len4==0):
        len4=100
    if(len2==0):
        len2=100
    if(len1==0):
        len1=100
        
    for i in range(lenVMs):
        TEMP=[(len(T_VMs[0])/len4),(len(T_VMs[1])/len2),(len(T_VMs[2])/len1)]
        M=TEMP.index(max(TEMP))
        if(len(T_VMs[M])!=0):
            VMs.append(T_VMs[M][0])
            (T_VMs[M]).remove(T_VMs[M][0])

    CPU=[]
    CPU.append([])
    CPULR=[] #resorce left
    N_PCPU=0   #default 0
    VMSC=copy.deepcopy(VMs)
    while(1):
        CPU_limit=[CPU_kernel,CPU_memory]
        lenVM=len(VMs)
        for j in range(lenVM):
            VMs_info=[VMs[j][1],VMs[j][2]]
            if(CPU_limit[0]>=VMs_info[0] and CPU_limit[1]>=VMs_info[1]):
                CPU[N_PCPU].append(VMs[j][0])
                CPU_limit[0]=CPU_limit[0]-VMs_info[0]
                CPU_limit[1]=CPU_limit[1]-VMs_info[1]
                VMSC.remove(VMs[j])
        CPULR.append(CPU_limit)
        if(utils.SUM_Judge(VMSC,CPU_kernel,CPU_memory)):
            #CPU=Optimize(CPU,CPULR,VMSC,Pvm,N_Pvm)
            break
        else:
            VMs=copy.deepcopy(VMSC)
            CPU.append([])
            N_PCPU=N_PCPU+1
    return CPU,(N_PCPU+1)
        
def Adjust(VM,condition):
    idx=Cond_Sort(VM,condition)
    T=[]
    for i in range(len(VM)):
        T.append(VM[idx[i]])
    VM=T
    return VM
def Cond_Sort(VM,condition):
    T_VM=[]
    if(condition==0):
        for i in range(len(VM)):
            T_VM.append(VM[i][1])
        idx=utils.argsort(T_VM)
        return idx
    else:
        for i in range(len(VM)):
            T_VM.append(VM[i][2])
        idx=utils.argsort(T_VM)
        return idx

def Optimize(CPU,CPULR,VMSC,Pvm,N_Pvm):
    idx=left_idx(CPULR)
    for i in range(len(CPULR)):
        CCPU=copy.deepcopy(CPU[idx[i]])
        if(CPULR[idx[i]][0]>0):
            VMSC=Adjust(VMSC,0)
            for j in range(len(CCPU)):
                TT_list=[]
                info=utils.SelectVM(CCPU[j],Pvm,N_Pvm)
                for t in range(len(VMSC)):
                    if(info[1]==VMSC[t][2]):
                        if((VMSC[t][1]>info[0])and((info[0]+CPULR[idx[i]][0])>=VMSC[t][1])):
                            TT_list.append(VMSC[t])
                            VMSC.remove(VMSC[t])
                            break
                if(len(TT_list)!=0):
                    CPU[idx[i]].remove(CCPU[j])
                    CPU[idx[i]].append(TT_list[0][0])
        if(CPULR[idx[i]][1]>0):
            VMSC=Adjust(VMSC,1)
            for j in range(len(CCPU)):
                TT_list=[]
                info=utils.SelectVM(CCPU[j],Pvm,N_Pvm)
                for t in range(len(VMSC)):
                    if(info[0]==VMSC[t][1]):
                        if((VMSC[t][2]>info[1])and((info[1]+CPULR[idx[i]][1])>VMSC[t][2])):
                            TT_list.append(VMSC[t])
                            VMSC.remove(VMSC[t])
                            break
                if(len(TT_list)!=0):
                    CPU[idx[i]].remove(CCPU[j])
                    CPU[idx[i]].append(TT_list[0][0])
    return CPU
                    
def left_idx(CPULR):
    T_L=[]
    for i in range(len(CPULR)):
        T_L.append(CPULR[0]+CPULR[1])
    idx=utils.argsort(T_L)
    return idx
    
def First_Delete(VMs,CPU_kernel,CPU_memory,condition):
    #the numbor of predicted vms
    T_k=0
    T_m=0
    for i in range(len(VMs)):
        T_k=T_k+VMs[i][1]
        T_m=T_m+VMs[i][2]
    
    KN=float(T_k/CPU_kernel)
    MN=float(T_m/CPU_memory)
    if (KN>=MN):
        N=int(KN)
    else:
        N=int(MN)
        
    if(condition==0):
        index=[]
        for i in range(len(VMs)):
            index.append(VMs[i][2]-VMs[i][1])
        idx=utils.argsort(index)
        end=0
        for i in range(len(VMs)):
            if((T_k-VMs[idx[i]][1])<(N*CPU_kernel+0.1*CPU_kernel)):
                break
            else:
                T_k=T_k-VMs[idx[i]][1]
                end=i
        TVM=copy.deepcopy(VMs)
        for j in range(end):
            VMs.remove(TVM[idx[j]])
    else:
        index=[]
        for i in range(len(VMs)):
            index.append(VMs[i][1]*4-VMs[i][2])
        idx=utils.argsort(index)
        end=0
        for i in range(len(VMs)):
            if((T_m-VMs[idx[i]][2])<(N*CPU_memory+0.1*CPU_memory)):
                break
            else:
                T_m=T_m-VMs[idx[i]][2]
                end=i
        TVM=copy.deepcopy(VMs)
        for j in range(end):
            VMs.remove(TVM[idx[j]])
    return VMs













