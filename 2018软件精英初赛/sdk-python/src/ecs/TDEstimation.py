import math
import utils
def TDEstimate(History_Start,Predict_Start,LenD,S_Data,Predict_time):
    k=2 #bandwidth
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
            count=0
        else:
            break

    TD_Matrix.append([0 for i in range(21)])
    N=N+1
    for i in range(7):
        TD_Matrix[N][i]=TD_Matrix[(N-1)][(14+i)]

    Predict_index=[]
    for i in range(Predict_time):
        if((7+Predict_Start+i)%14!=0):
            Predict_index.append([N,(7+Predict_Start+i)%14])
        else:
            N=N+1
            Predict_index.append([N,((7+Predict_Start+i)%14)])


    for i in range(len(Predict_index)):
        for j in range(N):
            for z in range(21):
                NPvm=NPvm+float(TD_Matrix[j][z]*math.exp(((j-Predict_index[i][0])**2+(z-Predict_index[i][1])**2)/(-2.0*(k**2))))   
    return NPvm

def EstTD(History_Start,Predict_Start,LenD,N_Pvm,S_Data,Predict_time):
    NEPvm=[0 for i in range(N_Pvm)]
    for i in range(N_Pvm):
        NEPvm[i]=int(TDEstimate(History_Start,Predict_Start,LenD,S_Data[i],Predict_time))
    return NEPvm
        
    
    























