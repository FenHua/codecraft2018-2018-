import copy
import datetime
def splitEscData(ecs_infor_array):
    length=len(ecs_infor_array)
    CPU_kernal=int((ecs_infor_array[0]).split()[0])
    CPU_memery=int((ecs_infor_array[0]).split()[1])
    N_Pvm=int(ecs_infor_array[2])
    # The array to save VMs which need to predict 
    Pvm=[[0 for x in range(3)]for y in range(N_Pvm)]
    
    for i in xrange(3,3+N_Pvm):
        lines=(ecs_infor_array[i]).split()
        Pvm[(i-3)]=[lines[0],int(lines[1]),int(lines[2])/1024]
    
    condition=ecs_infor_array[4+N_Pvm]
    
    new_date=datetime.datetime.strptime(ecs_infor_array[7+N_Pvm][0:10],'%Y-%m-%d')
    old_date=datetime.datetime.strptime(ecs_infor_array[6+N_Pvm][0:10],'%Y-%m-%d')
    Predict_Start=old_date.weekday()
    Predict_time=(new_date-old_date).days+1
    return CPU_kernal,CPU_memery,N_Pvm,condition,Pvm,Predict_time,Predict_Start

def splitInputData(input_file_array):
    length=len(input_file_array)
    Hvm=[['' for x in range(2)] for y in range(length)]
    for i in range(length):
        Hvm[i]=[(input_file_array[i]).split()[1],(input_file_array[i]).split()[2]]
    History_Start=(datetime.datetime.strptime((input_file_array[0]).split()[2],'%Y-%m-%d')).weekday()
    return length,Hvm,History_Start

def Statistic_Split(length,Hvm,N_pvm,Pvm):
    #according to the history data,counting the Pvm
    temp_data=[h[1] for h in Hvm]
    #Try to get the second column
    Set_HDate=list(set(temp_data))
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


def results_expression(result,CPU,N_PCPU):
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






















    

    
