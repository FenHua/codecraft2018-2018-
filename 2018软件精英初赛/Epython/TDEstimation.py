import math
import utils
def TDEstimate(History_Start,Predict_Start,LenD,S_Data,Predict_time):
    K=3
    NPvm=0
    #Initialize the 2D matrix
    TD_Matrix=[[0 for i in range(21)]]
    N=0
    T=0
    while(T<LenD):
        for j in range(History_Start,21,1):
            if(T<LenD):
                TD_Matrix[N][j]=S_Data[T]
                T=T+1
            else:
                break
        if(T<LenD):
            TD_Matrix.append([0 for i in range(21)])
            N=N+1
            T=T-14
            History_Start=0
        else:
            break

    TD_Matrix.append([0 for i in range(21)])
    N=N+1
    for i in range(7):
        TD_Matrix[N][i]=TD_Matrix[(N-1)][(14+i)]

    Predict_index=[]
    for i in range(Predict_time):
        if((Predict_Start+i)%7!=0):
            Predict_index.append([N,7+(Predict_Start+i)%7])
        else:
            N=N+1
            Predict_index.append([N,7+(Predict_Start+i)%7])
    for i in range(len(Predict_index)):
        l=0
        r=0
        up=N
        down=0
        # initial bandborder
        if(Predict_index[i][0]-K>=0):
            down=Predict_index[i][0]-K
        if(Predict_index[i][1]-K>0):
            l=Predict_index[i][1]-K
        if(Predict_index[i][1]+K>21):
            r=21
        else:
            r=Predict_index[i][1]+K
        N_Array=[]
        for j in range(down,up,1):
            for z in range(l,r,1):
                if(TD_Matrix[j][z]!=0):
                    N_Array.append(TD_Matrix[j][z])
        if(len(N_Array)==0):
            NPvm=NPvm+0
        else:
            NPvm=NPvm+float(sum(N_Array)/len(N_Array))
    return math.ceil(NPvm)

def EstTD(History_Start,Predict_Start,LenD,N_Pvm,S_Data,Predict_time):
    NEPvm=[0 for i in range(N_Pvm)]
    for i in range(N_Pvm):
        NEPvm[i]=int(TDEstimate(History_Start,Predict_Start,LenD,S_Data[i],Predict_time))
    return NEPvm
        
    
    























