import math
def lwlr(testPoint,xArr,yArr,k=3):
    # locally weighted linear regression
    xMat=xArr
    yMat=yArr
    m=len(xMat)
    result=0
    weights=[1 for i in range(m)]
    diffMat=[0 for i in range(m)]
    for j in range(m):
        diffMat[j]=testPoint-xMat[j]
        weights[j]=math.exp(diffMat[j]**2/(-2.0*(k**2)))
    for i in range(m):
        result=result+weights[i]*yArr[i]
    #print result
    return result

def lwlr_predict(N_Pvm,lenD,S_Data,Predict_time):
    k=4.2
    xArr=[i for i in range(lenD)]
    yArr=[]
    for i in range(N_Pvm):
        yArr.append(S_Data[i])
    testArr=[j for j in range(lenD,(lenD+Predict_time),1)]
    NEPvm=[0 for i in range(N_Pvm)]   
    for i in range(N_Pvm):
        T=0
        for j in range(Predict_time):
            T=T+lwlr(testArr[j],xArr,yArr[i],k)
        NEPvm[i]=int(math.ceil(T))
    return NEPvm

def Prob_predict(N_Pvm,Len_History,S_Data,Predict_time):
    Probablity=[0 for i in range(N_Pvm)]
    for i in range(N_Pvm):
        for j in range(Len_History):
            Probablity[i]=Probablity[i]+S_Data[i][j]
    NEPvm=[math.ceil(Probablity[i]*Predict_time/Len_History) for i in range(N_Pvm)]
    return NEPvm




















