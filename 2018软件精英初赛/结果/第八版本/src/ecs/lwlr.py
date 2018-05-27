import math
import utils
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
    k=4.3
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


def EachD_predict(week,Hweek,VM,Len_History,S_Data):
    N=0
    #intialize list of week
    CD_week=[]
    for i in range(7):
        CD_week.append([])
    
    # split history data according to week
    for i in range(Len_History):
        time=(Hweek+i)%7
        (CD_week[time]).append(S_Data[VM][i])
    if(week==0):
        #monday
        T_length=len(CD_week[0])
        day=[i for i in range(T_length)]
        a1,a2,a3=NLRegress.Leastsq(day,CD_week[0],T_length)
        N=a3*((T_length+1)**2)+a2*(T_length+1)+a3
        # test only once
        if(N>=0):
            N=math.ceil(N)
        else:
            N=0
        return N
    elif(week==1):
        #tueseday
        T_length=len(CD_week[1])
        day=[i for i in range(T_length)]
        a1,a2,a3=NLRegress.Leastsq(day,CD_week[0],T_length)
        N=a3*((T_length+1)**2)+a2*(T_length+1)+a3
        # test only once
        if(N>=0):
            N=math.ceil(N)
        else:
            N=0
        return N
    elif(week==2):
        #wednesday
        T_length=len(CD_week[2])
        day=[i for i in range(T_length)]
        a1,a2,a3=NLRegress.Leastsq(day,CD_week[0],T_length)
        N=a3*((T_length+1)**2)+a2*(T_length+1)+a3
        # test only once
        if(N>=0):
            N=math.ceil(N)
        else:
            N=0
        return N
    elif(week==3):
        #thursday
        T_length=len(CD_week[3])
        day=[i for i in range(T_length)]
        a1,a2,a3=NLRegress.Leastsq(day,CD_week[0],T_length)
        N=a3*((T_length+1)**2)+a2*(T_length+1)+a3
        # test only once
        if(N>=0):
            N=math.ceil(N)
        else:
            N=0
        return N
    elif(week==4):
        #friday
        T_length=len(CD_week[4])
        day=[i for i in range(T_length)]
        a1,a2,a3=NLRegress.Leastsq(day,CD_week[0],T_length)
        N=a3*((T_length+1)**2)+a2*(T_length+1)+a3
        # test only once
        if(N>=0):
            N=math.ceil(N)
        else:
            N=0
        return N
    elif(week==5):
        #saturday
        T_length=len(CD_week[5])
        day=[i for i in range(T_length)]
        a1,a2,a3=NLRegress.Leastsq(day,CD_week[0],T_length)
        N=a3*((T_length+1)**2)+a2*(T_length+1)+a3
        # test only once
        if(N>=0):
            N=math.ceil(N)
        else:
            N=0
        return N
    else:
        #sunday
        T_length=len(CD_week[6])
        day=[i for i in range(T_length)]
        a1,a2,a3=NLRegress.Leastsq(day,CD_week[0],T_length)
        N=a3*((T_length+1)**2)+a2*(T_length+1)+a3
        # test only once
        if(N>=0):
            N=int(math.ceil(N))
        else:
            N=0
        return N
    return N

def Week_predict(N_Pvm,lenD,S_Data,Predict_time,last_date):
    week=utils.iden_week(date)
    Hweek=utils.iden_week(last_date)
    NEPvm=[0 for i in range(N_Pvm)]
    for i in range(N_Pvm):
        N=0
        for j in range(Predict_time):
            date=(week+j)%7
            N=N+EachD_predict(date,Hweek,i,LenD,S_Data)
        NEPvm[i]=N

def Simp_regress(N_Pvm,lenD,S_Data,Predict_time):
    xdata=[i for i in range(lenD)]
    NEPvm=[0 for i in range(N_Pvm)]
    for i in range(N_Pvm):
        
        [a1,a2,a3]=NLRegress.Leastsq(xdata,S_Data[i],lenD)
        
        for j in range(Predict_time):
            N=a3*((lenD+j)**2)+a2*(j+lenD)+a3
            if(N>=0):
                NEPvm[i]=NEPvm[i]+N
        if(NEPvm[i]>1.5*max(S_Data[i])):
            NEPvm[i]=math.ceil(1.5*max(S_Data[i]))
        else:
            NEPvm[i]=math.ceil(NEPvm[i])
    return NEPvm
















