import time
import copy
import datetime
def splitEscData(ecs_infor_array):
    length=len(ecs_infor_array)
    CPU_kernel=int((ecs_infor_array[0]).split()[0])
    CPU_memery=int((ecs_infor_array[0]).split()[1])
    N_Pvm=int(ecs_infor_array[2])
    # The array to save VMs which need to predict 
    Pvm=[[0 for x in range(3)]for y in range(N_Pvm)]
    
    for i in xrange(3,3+N_Pvm):
        lines=(ecs_infor_array[i]).split()
        Pvm[(i-3)]=[lines[0],int(lines[1]),int(lines[2])/1024]

    
    if(ecs_infor_array[4+N_Pvm][0:3]=='CPU'):
        condition=0
    else:
        condition=1
    new_date=datetime.datetime.strptime(ecs_infor_array[7+N_Pvm][0:10],'%Y-%m-%d')
    old_date=datetime.datetime.strptime(ecs_infor_array[6+N_Pvm][0:10],'%Y-%m-%d')
    Predict_Start=old_date.weekday()
    Predict_time=(new_date-old_date).days
    return CPU_kernel,CPU_memery,N_Pvm,condition,Pvm,Predict_time,Predict_Start

def splitInputData(input_file_array):
    length=len(input_file_array)
    Hvm=[['' for x in range(3)] for y in range(length)]
    for i in range(length):
        Hvm[i]=[(input_file_array[i]).split()[1],(input_file_array[i]).split()[2],(input_file_array[i]).split()[3]]
    History_Start=(datetime.datetime.strptime((input_file_array[0]).split()[2],'%Y-%m-%d')).weekday()
    return length,Hvm,History_Start
def Denoise_Split(length,Hvm,N_pvm,Pvm):
    #according to the history data,counting the Pvm
    temp_data=[h[1] for h in Hvm]
    #Try to get the second column
    Set_HDate=list(set(temp_data))
    Set_HDate.sort(key=temp_data.index)
    lenD=len(Set_HDate)#The length of Set
    S_Data=[[0 for j in range(lenD)] for t in range(N_pvm)]
    
    # intilize S_Data
    for j in range(N_pvm):
        for z in range(lenD):
            outliers=[]
            for y in range(length):
                if (Set_HDate[z]==Hvm[y][1])and(Pvm[j][0]==Hvm[y][0]):
                    if(len(outliers)==0):
                        S_Data[j][z]=S_Data[j][z]+1
                        outliers.append((Hvm[y][1]+' '+Hvm[y][2]))
                    else:
                        #If time gap is small, throw
                        timeB=Hvm[y][1]+' '+Hvm[y][2]
                        T=1
                        for t in range(len(outliers)):
                            if(getTimeDiff(timeB,outliers[t])<10):
                                T=0
                                break
                        if(T):
                            S_Data[j][z]=S_Data[j][z]+1
                            outliers.append((Hvm[y][1]+' '+Hvm[y][2]))                          
    return lenD,S_Data

def getTimeDiff(timeStrb,timeStra):
        tb = time.strptime(timeStrb, "%Y-%m-%d %H:%M:%S")
        ta = time.strptime(timeStra, "%Y-%m-%d %H:%M:%S")
        y,m,d,H,M,S = tb[0:6]
        dataTimeb=datetime.datetime(y,m,d,H,M,S)
        y,m,d,H,M,S = ta[0:6]
        dataTimea=datetime.datetime(y,m,d,H,M,S)
        secondsDiff=(dataTimeb-dataTimea).seconds
        return secondsDiff




    
def Statistic_Split(length,Hvm,N_pvm,Pvm):
    #according to the history data,counting the Pvm
    temp_data=[h[1] for h in Hvm]
    #Try to get the second column
    Set_HDate=list(set(temp_data))
    Set_HDate.sort(key=temp_data.index)
    lenD=len(Set_HDate)
    #The length of Set
    S_Data=[[0 for j in range(lenD)] for t in range(N_pvm)]
    # intilize S_Data
    for j in range(N_pvm):
        for z in range(lenD):
            for y in range(length):
                if (Set_HDate[z]==Hvm[y][1])and(Pvm[j][0]==Hvm[y][0]):
                    S_Data[j][z]=S_Data[j][z]+1
    return lenD,S_Data

def SelectVM(name,Pvm,N_Pvm):
    for i in range(N_Pvm):
        if(name==Pvm[i][0]):
            return [Pvm[i][1],Pvm[i][2]]


def results_expression(CPU,N_PCPU,N_Pvm,Pvm):
    result=[]
    VM=[]
    for i in range(N_PCPU):
        for j in range(len(CPU[i])):
            VM.append(CPU[i][j])
    result.append(len(VM))
    # total VM number
    for i in range(N_Pvm):
        result.append(str(Pvm[i][0])+" "+str(VM.count(Pvm[i][0])))
    result.append("")
    
    result.append(str(N_PCPU))
    for i in range(N_PCPU):
        string=""
        T_Set=list(set(CPU[i]))
        for j in range(len(T_Set)):
            L=(CPU[i]).count(T_Set[j])
            string=string+T_Set[j]+" "+str(L)+" "
        result.append(str(i+1)+" "+string)
    return result

def argsort(index):
    array=copy.deepcopy(index)
    length=len(array)
    idx=[0 for i in range(length)]
    for i in range(length):
        max=array[i]
        idx[i]=i
        for j in range(length):
            if(max<array[j]):
                max=array[j]
                idx[i]=j
        array[idx[i]]=-100
    return idx


def iden_week(date):
    T=datetime.datetime.strptime(date,'%Y-%m-%d')
    w=T.weekday()
    return W

def SUM_Judge(VMs,CPU_kernel,CPU_memory):
    K=0
    M=0
    for i in range(len(VMs)):
        K=K+VMs[i][1]
        M=M+VMs[i][2]
    if ((K<float(0.3*CPU_kernel))or(M<float(0.3*CPU_memory))):
        return True
    return False




















    

    
