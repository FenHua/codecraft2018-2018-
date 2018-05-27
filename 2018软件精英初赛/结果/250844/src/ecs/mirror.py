from __future__ import division
import Regress


def Mirror(lenD,N_Pvm,S_Data,Predict_time):
    NEPvm=[0 for i in range(N_Pvm)]
    for i in range(N_Pvm):
        T_Array=TSplit(lenD,N_Pvm,S_Data[i],Predict_time)
        #NEPvm[i]=int(sum(T_Array[1])+0.7*sum(T_Array[2]))
        NEPvm[i]=int(sum(T_Array[1])*1.3+9)
    return NEPvm


def Smirror(lenD,N_Pvm,S_Data,Predict_time):
    K=3
    NEPvm=[0 for i in range(N_Pvm)]
    for i in range(N_Pvm):
        Matrix=TSplit(lenD,N_Pvm,S_Data[i],Predict_time)
        NEPvm[i]=Estimation(Matrix,Predict_time,K)
    return NEPvm

def Commirror(lenD,N_Pvm,S_Data,Predict_time):
    NEPvm=[0 for i in range(N_Pvm)]
    for i in range(N_Pvm):
        T_Array=TSplit(lenD,N_Pvm,S_Data[i],Predict_time)
        # First value
        Value1=Estimation(T_Array,Predict_time,2)
        
        #  Second value
        X=[(1-len(T_Array))]
        Y=[0] #avoid predict result is zero
        for j in range((len(T_Array)-1),0,-1):
            Y.append(sum(T_Array[j]))
            X.append((len(T_Array)-j))
        Y.append(0)
        X.append((2*len(T_Array)-1))
        c,b,a=Regress.Leastsq(X,Y,len(Y))
        Value2=a*((len(X)-1)**2)+b*(len(X)-1)+c
        
        NEPvm[i]=int(Value1+0.9*Value2+3.4)
    return NEPvm





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






















