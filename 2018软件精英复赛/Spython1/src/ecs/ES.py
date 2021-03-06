from __future__ import division
import math

def Smirror(lenD,N_Pvm,S_Data,Predict_time):
    K=3
    NEPvm=[0 for i in range(N_Pvm)]
    for i in range(N_Pvm):
        Matrix=TSplit(lenD,N_Pvm,S_Data[i],Predict_time)
        NEPvm[i]=int(Estimation(Matrix,Predict_time,K)*0.9)+4
    return NEPvm

def ES(lenD,N_Pvm,S_Data,Predict_time):
    NEPvm=[0 for i in range(N_Pvm)]
    for i in range(N_Pvm):
        T_Array=TSplit(lenD,N_Pvm,S_Data[i],Predict_time)
        S=[]
        L=len(T_Array)
        for j in range((L-1),0,-1):
            S.append(sum(T_Array[j]))

        S2=DExp_S(0.2,S,1)
        
        NEPvm[i]=int(S2*1.7)
    return NEPvm

def DExp_S(alpha,S,N):
    Single_S=Exp_S(alpha,S)
    Double_S=Exp_S(alpha,Single_S)
    A=[]
    B=[]
    Len=len(S)
    for i in range(Len):
        A.append((2*Single_S[i]-Double_S[i]))
        B.append(((alpha/(1-alpha))*(Single_S[i]-Double_S[i])))
    S2=A[-1]+B[-1]*N
    return S2
def Exp_S(alpha,S):
    Len=len(S)
    S1=[0 for i in range(Len)]
    T_array=[S[i] for i in range((int(0.5*Len)),Len,1)]
    S1[0]=sum(T_array)/len(T_array)
    for i in range(1,Len,1):
        S1[i]=alpha*S[i]+(1-alpha)*S1[(i-1)]
    return S1

def Estimation(Matrix,Predict_time,K):
    NPvm=0
    l=0
    r=0
    u=len(Matrix)
    for i in range(Predict_time):
        # initial bandborder
        if((K+1)<len(Matrix)):
            u=K+1
        if(i-K>0):
            l=i-K+1
        if(i+K>Predict_time):
            r=Predict_time
        else:
            r=i+K
        N_Array=[]
        for j in range(u):
            for z in range(l,r,1):
                if(Matrix[j][z]!=0):
                    N_Array.append(Matrix[j][z])
        if(len(N_Array)==0):
            NPvm=NPvm+0
        else:
            NPvm=NPvm+float(sum(N_Array)/len(N_Array))
    return NPvm


def TSplit(lenD,N_Pvm,Data,Predict_time):
    TSArray=[] #data split, according to Predict_time
    up=lenD
    down=(up-Predict_time)
    while(down>0):
        TSArray.append([])
        for i in range(down,up,1):
            (TSArray[(len(TSArray)-1)]).append(Data[i])
        up=down
        down=(up-Predict_time)
    
    Matrix=[[0 for i in range(Predict_time)] for j in range((len(TSArray)+1))]
    L=len(TSArray)
    for i in range(L):
        for j in range(Predict_time):
            Matrix[(i+1)][j]=TSArray[i][j]
    return Matrix
