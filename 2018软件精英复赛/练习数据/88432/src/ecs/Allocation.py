from __future__ import division
import math
import utils
import copy
def Allocate(NEPvm,Pvm,N_Stype,Servers):
    VMs=[]
    N_Pvm=len(NEPvm) # The number of predicted VMs
    for i in range(N_Pvm):
        for j in range(int(NEPvm[i])):
            VMs.append(Pvm[i])
    Servers_N=Compute_Servers(VMs,N_Stype,Servers)
    Total_S=sum(Servers_N) #the total number of servers
    P_Servers=[]
    P_SCondition=[]
    P_SRate=[]
    # initialize predicted servers
    for i in range(Total_S):
        P_Servers.append([])
    # initialize condition of each server
    for i in range(N_Stype):
        for j in range(Servers_N[i]):
            P_SCondition.append([Servers[i][1],Servers[i][2]])
            P_SRate.append(Servers[i][2]/Servers[i][1])

    # allocate
    lenVMs=len(VMs)
    VMs=Adjust_Order(lenVMs,VMs)
    VMSC=copy.deepcopy(VMs)
    #print VMSC
    for i in range(lenVMs):
        info=[VMs[i][1],VMs[i][2]]
        # select according to rate
        S_rate=[abs(P_SRate[t]-info[1]/info[0]) for t in range(Total_S)]
        idx=utils.argsort(S_rate)[-1]
        if((P_SCondition[idx][0]>=info[0])and(P_SCondition[idx][1]>=info[1])):
            P_Servers[idx].append(VMs[i])
            P_SCondition[idx][0]=P_SCondition[idx][0]-info[0]
            P_SCondition[idx][1]=P_SCondition[idx][1]-info[1]
            if(P_SCondition[idx][0]==0):
               P_SRate[idx]=0
            else:
               P_SRate[idx]=(P_SCondition[idx][1]/P_SCondition[idx][0])
            VMSC.remove(VMs[i])
        else:
            for j in range((Total_S-2),-1,-1):
                idx=utils.argsort(S_rate)[j]
                if((P_SCondition[idx][0]>=info[0])and(P_SCondition[idx][1]>=info[1])):
                    P_Servers[idx].append(VMs[i])
                    P_SCondition[idx][0]=P_SCondition[idx][0]-info[0]
                    P_SCondition[idx][1]=P_SCondition[idx][1]-info[1]
                    if(P_SCondition[idx][0]==0):
                       P_SRate[idx]=0
                    else:
                       P_SRate[idx]=(P_SCondition[idx][1]/P_SCondition[idx][0])
                    VMSC.remove(VMs[i])
                    break

    P_SRate,P_SCondition,P_Servers,TVMS=Rebalance(Total_S,P_SRate,P_SCondition,P_Servers,VMSC)
    P_Servers=EXchange(TVMS,P_SCondition,P_Servers,Pvm)
    return Servers_N,P_Servers
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


def EXchange(VMSC,P_SCondition,P_Servers,Pvm):
    N_Pvm=len(Pvm)
    LenS=len(P_SCondition)
    for i in range(LenS):
        TTS=copy.deepcopy(P_Servers[i])
        if(P_SCondition[i][0]>0):
            for j in range(len(TTS)):
                TT=[]
                info=[TTS[j][1],TTS[j][2]]
                for z in range(len(VMSC)):
                    if((info[1]==VMSC[z][2])and(info[0]<VMSC[z][1])):
                        if((info[0]+P_SCondition[i][0])>=VMSC[z][1]):
                            P_SCondition[i][0]=P_SCondition[i][0]-(int(VMSC[z][1]))+info[0]
                            TT.append(VMSC[z])
                            VMSC.remove(VMSC[z])
                            break
                if(len(TT)!=0):
                    (P_Servers[i]).remove(TTS[j])
                    (P_Servers[i]).append(TT[0])
                    
        if(P_SCondition[i][1]>0):
            for j in range(len(TTS)):
                TT=[]
                info=[TTS[j][1],TTS[j][2]]
                for z in range(len(VMSC)):
                    if((info[0]==VMSC[z][1])and(info[1]<VMSC[z][2])):
                        if((info[1]+P_SCondition[i][1])>=VMSC[z][2]):
                            P_SCondition[i][1]=P_SCondition[i][1]-(int(VMSC[z][2]))+info[1]
                            TT.append(VMSC[z])
                            VMSC.remove(VMSC[z])
                            break
                if(len(TT)!=0):
                    (P_Servers[i]).remove(TTS[j])
                    (P_Servers[i]).append(TT[0])
    return P_Servers


def Compute_Servers(VMs,N_Stype,Servers):
    Servers_N=[0 for i in range(N_Stype)]
    minL=Limit(N_Stype,Servers)
    T_k,T_m=Total_R(VMs)
    print T_k,T_m
    L=[]#the up limit
    N=[]
    for i in range(N_Stype):
        L.append([i,int(max([math.ceil(T_k/Servers[i][1]),math.ceil(T_m/Servers[i][2])]))])
        N.append(L[i][1])
    # Sort low to high
    idx=utils.argsort(N)
    Min=(T_k+T_m)
    S_N=[]
    if(N_Stype==3):
        for t1 in range(N[idx[0]]):
            for t2 in range(N[idx[1]]):
                for t3 in range(N[idx[2]]):
                    M=abs(T_k-(Servers[L[idx[0]][0]][1]*t1)-(Servers[L[idx[1]][0]][1]*t2)-(Servers[L[idx[2]][0]][1]*t3))
                    M=M+abs(T_m-(Servers[L[idx[0]][0]][2]*t1)-(Servers[L[idx[1]][0]][2]*t2)-(Servers[L[idx[2]][0]][2]*t3))
                    if(M<Min):
                        Min=M
                        Servers_N[idx[0]]=t1
                        Servers_N[idx[1]]=t2
                        Servers_N[idx[2]]=t3                   
    elif(N_Stype==2):
        for t1 in range(N[idx[0]]):
            for t2 in range(N[idx[1]]):
                M=abs(T_k-(Servers[L[idx[0]][0]][1]*t1)-(Servers[L[idx[1]][0]][1]*t2))
                M=M+abs(T_m-(Servers[L[idx[0]][0]][2]*t1)-(Servers[L[idx[1]][0]][2]*t2))
                if(M<Min):
                    Min=M
                    Servers_N[idx[0]]=t1
                    Servers_N[idx[1]]=t2
    else:
        for t1 in range(N[idx[0]]):
            M=abs(T_k-(Servers[L[idx[0]][0]][1]*t1))+abs(T_m-(Servers[L[idx[0]][0]][2]*t1))
            if(M<Min):
                Min=M
                Servers_N[idx[0]]=t1
    print Servers_N
    return Servers_N

def Limit(N_Stype,Servers):
    kernel=[]
    memory=[]
    for i in range(N_Stype):
        kernel.append(Servers[i][1])
        memory.append(Servers[i][2])
    minL=[min(kernel),min(memory)]
    return minL

def Total_R(VMs):
    T_k=0
    T_m=0
    for i in range(len(VMs)):
        T_k=T_k+VMs[i][1]
        T_m=T_m+VMs[i][2]
    return T_k,T_m

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
