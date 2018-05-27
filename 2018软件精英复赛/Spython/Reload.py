from __future__ import division
import copy
import utils
def SUPEREX(Total_S,P_SRate,P_SCondition,P_Servers,VMSC):
    P_SRate,P_SCondition,P_Servers,VMSC=Reload(Total_S,P_SRate,P_SCondition,P_Servers,VMSC)
    P_SRate,P_SCondition,P_Servers,VMSC=Rebalance(Total_S,P_SRate,P_SCondition,P_Servers,VMSC)
    P_SRate,P_SCondition,P_Servers,VMSC=Reload(Total_S,P_SRate,P_SCondition,P_Servers,VMSC)
    return P_SRate,P_SCondition,P_Servers,VMSC
    
def Reload(Total_S,P_SRate,P_SCondition,P_Servers,VMSC):
    BigM=[]
    BigK=[]
    for i in range(Total_S):
        if((sum(P_SCondition[i])!=0)and(min(P_SCondition[i])==0)):
            if(P_SCondition[i][0]>0):
                BigK.append(i)
            else:
                BigM.append(i)
    for i in range(len(BigM)):
        for j in range(len(BigK)):
          P_SCondition[BigM[i]],P_Servers[BigM[i]],P_SCondition[BigK[j]],P_Servers[BigK[j]]=superEX(P_SCondition[BigM[i]],P_Servers[BigM[i]],P_SCondition[BigK[j]],P_Servers[BigK[j]])



    for i in range(Total_S):
        if(sum(P_SCondition[i])!=0):
            if(P_SCondition[i][0]==0):
                P_SRate[i]=0
            else:
                P_SRate[i]=(P_SCondition[i][1]/P_SCondition[i][0])

    LenV=len(VMSC)
    VMSC=Adjust_Order(LenV,VMSC)
    TVMS=copy.deepcopy(VMSC)
    for i in range(LenV):
        info=[VMSC[i][1],VMSC[i][2]]
        # select according to rate
        S_rate=[abs(P_SRate[t]-info[1]/info[0]) for t in range(Total_S)]
        idx=utils.argsort(S_rate)[-1]
        if((P_SCondition[idx][0]>=info[0])and(P_SCondition[idx][1]>=info[1])):
            P_Servers[idx].append(VMSC[i])
            P_SCondition[idx][0]=P_SCondition[idx][0]-info[0]
            P_SCondition[idx][1]=P_SCondition[idx][1]-info[1]
            if(P_SCondition[idx][0]==0):
               P_SRate[idx]=0
            else:
               P_SRate[idx]=(P_SCondition[idx][1]/P_SCondition[idx][0])
            TVMS.remove(VMSC[i])
        else:
            for j in range((Total_S-2),-1,-1):
                idx=utils.argsort(S_rate)[j]
                if((P_SCondition[idx][0]>=info[0])and(P_SCondition[idx][1]>=info[1])):
                    P_Servers[idx].append(VMSC[i])
                    P_SCondition[idx][0]=P_SCondition[idx][0]-info[0]
                    P_SCondition[idx][1]=P_SCondition[idx][1]-info[1]
                    if(P_SCondition[idx][0]==0):
                       P_SRate[idx]=0
                    else:
                       P_SRate[idx]=(P_SCondition[idx][1]/P_SCondition[idx][0])
                    TVMS.remove(VMSC[i])
                    break
    return P_SRate,P_SCondition,P_Servers,TVMS

def superEX(P_SCondition1,Server1,P_SCondition2,Server2):
    # 1: memory big
    # 2: kernel big
    len1=len(Server1)
    len2=len(Server2)
    S1=copy.deepcopy(Server1)
    S2=copy.deepcopy(Server2)
    for i in range(len1):
        if(P_SCondition1[1]>0):
            for j in range(len2):
                if((Server1[i][1]==Server2[j][1])and(Server1[i][2]<Server2[j][2])):
                    if((P_SCondition1[1]-Server2[j][2]+Server1[i][2])>=0):
                        P_SCondition1[1]=P_SCondition1[1]-Server2[j][2]+Server1[i][2]
                        P_SCondition2[1]=P_SCondition2[1]+Server2[j][2]-Server1[i][2]
                        S2.append(Server1[i])
                        S1.append(Server2[j])
                        S1.remove(Server1[i])
                        S2.remove(Server2[i])
                        break
    Server1=copy.deepcopy(S1)
    Server2=copy.deepcopy(S2)
    return P_SCondition1,Server1,P_SCondition2,Server2

def Rebalance(Total_S,P_SRate,P_SCondition,P_Servers,VMSC):
    # rebalance
    for i in range(Total_S):
        if(sum(P_SCondition[i])!=0):
            VMSC,P_Servers[i],P_SCondition[i]=D_EX(VMSC,P_Servers[i],P_SCondition[i])
            if(P_SCondition[i][0]==0):
                P_SRate[i]=0
            else:
                P_SRate[i]=(P_SCondition[i][1]/P_SCondition[i][0])
    LenV=len(VMSC)
    VMSC=Adjust_Order(LenV,VMSC)
    TVMS=copy.deepcopy(VMSC)
    for i in range(LenV):
        info=[VMSC[i][1],VMSC[i][2]]
        # select according to rate
        S_rate=[abs(P_SRate[t]-info[1]/info[0]) for t in range(Total_S)]
        idx=utils.argsort(S_rate)[-1]
        if((P_SCondition[idx][0]>=info[0])and(P_SCondition[idx][1]>=info[1])):
            P_Servers[idx].append(VMSC[i])
            P_SCondition[idx][0]=P_SCondition[idx][0]-info[0]
            P_SCondition[idx][1]=P_SCondition[idx][1]-info[1]
            if(P_SCondition[idx][0]==0):
               P_SRate[idx]=0
            else:
               P_SRate[idx]=(P_SCondition[idx][1]/P_SCondition[idx][0])
            TVMS.remove(VMSC[i])
        else:
            for j in range((Total_S-2),-1,-1):
                idx=utils.argsort(S_rate)[j]
                if((P_SCondition[idx][0]>=info[0])and(P_SCondition[idx][1]>=info[1])):
                    P_Servers[idx].append(VMSC[i])
                    P_SCondition[idx][0]=P_SCondition[idx][0]-info[0]
                    P_SCondition[idx][1]=P_SCondition[idx][1]-info[1]
                    if(P_SCondition[idx][0]==0):
                       P_SRate[idx]=0
                    else:
                       P_SRate[idx]=(P_SCondition[idx][1]/P_SCondition[idx][0])
                    TVMS.remove(VMSC[i])
                    break
    return P_SRate,P_SCondition,P_Servers,TVMS

def D_EX(VMSC,P_Server,P_SC):
    if(P_SC[0]==0):
        #delete the big kernel
        benchmark=P_SC[1]
        # sub the kernel
        P_Servers=Adjust(P_Server,0)
        TT=[]
        for i in range(len(P_Server)):
            if((P_Server[i][2]/P_Server[i][1]<=2)and(benchmark>=P_Server[i][1])):
                benchmark=benchmark-P_Server[i][1]
                TT.append(P_Server[i])
        for  j in range(len(TT)):
            P_SC[0]=P_SC[0]+int(TT[j][1])
            P_SC[1]=P_SC[1]+int(TT[j][2])
            VMSC.append(TT[j])
            P_Server.remove(TT[j])
    else:
        #delete the big memory
        benchmark=P_SC[0]
        # sub the memory
        P_Servers=Adjust(P_Server,1)
        TT=[]
        for i in range(len(P_Server)):
            if(benchmark>=P_Server[i][2]):
                benchmark=benchmark-P_Server[i][2]
                TT.append(P_Server[i])
        for  j in range(len(TT)):
            P_SC[0]=P_SC[0]+int(TT[j][1])
            P_SC[1]=P_SC[1]+int(TT[j][2])
            VMSC.append(TT[j])
            P_Server.remove(TT[j])
    return VMSC,P_Server,P_SC



def Adjust_Order(lenVMs,VMs):
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
    VM4=Adjust(VM4,0)
    VM2=Adjust(VM2,0)
    VM1=Adjust(VM1,0)
    T_VMs=[]
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
    VMs=[] #reset
    for i in range(lenVMs):
        TEMP=[(len(T_VMs[0])/len4),(len(T_VMs[1])/len2),(len(T_VMs[2])/len1)]
        
        M=TEMP.index(max(TEMP))
        if(len(T_VMs[M])!=0):
            VMs.append(T_VMs[M][0])
            (T_VMs[M]).remove(T_VMs[M][0])
    return VMs

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
