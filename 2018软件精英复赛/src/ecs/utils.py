import time
import copy
import datetime
def splitEscData(ecs_infor_array):
    N_Stype=int(ecs_infor_array[0])
    Servers=[]
    for i in range(N_Stype):
        Servers.append([(ecs_infor_array[(i+1)]).split()[0],int((ecs_infor_array[(i+1)]).split()[1]),int((ecs_infor_array[(i+1)]).split()[2])])
        
    N_Pvm=int(ecs_infor_array[(2+N_Stype)])
    # The array to save VMs which need to predict 
    Pvm=[]
    for i in xrange((3+N_Stype),(3+N_Stype+N_Pvm),1):
        lines=(ecs_infor_array[i]).split()
        Pvm.append([lines[0],int(lines[1]),int(lines[2])/1024])
    new_date=ecs_infor_array[(5+N_Stype+N_Pvm)][0:19]
    old_date=ecs_infor_array[(4+N_Stype+N_Pvm)][0:19]
    Predict_time=int(round((getTimeDiff(new_date,old_date))/86400))
    Predict_Start=old_date
    return N_Stype,Servers,N_Pvm,Pvm,Predict_time,Predict_Start

def splitInputData(input_file_array):
    length=len(input_file_array)
    Hvm=[['' for x in range(3)] for y in range(length)]
    for i in range(length):
        Hvm[i]=[(input_file_array[i]).split()[1],(input_file_array[i]).split()[2],(input_file_array[i]).split()[3]]
    History_end=(input_file_array[(length-1)]).split()[2]+" "+(input_file_array[(length-1)]).split()[3]
    return length,Hvm,History_end

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
        secondsDiff=(dataTimeb-dataTimea).total_seconds()
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

def results_expression(P_Servers,Servers_N,Servers,Pvm):
    result=[]
    VMs=[]  # total VM number
    for i in range(len(P_Servers)):
        for j in range(len(P_Servers[i])):
            VMs.append(P_Servers[i][j][0])
    result.append(len(VMs))
    Name_Servers=[]
    for i in range(len(P_Servers)):
        Name_Servers.append([])
        for j in range(len(P_Servers[i])):
            (Name_Servers[i]).append(P_Servers[i][j][0])
    
    N_Pvm=len(Pvm)
    for i in range(N_Pvm):
        result.append(str(Pvm[i][0])+" "+str(VMs.count(Pvm[i][0])))
    result.append(" ")

    S_flag=0
    N_Stype=len(Servers)  #the number of different servers
    for i in range(N_Stype):
        if(Servers_N[i]!=0):
            result.append(Servers[i][0]+" "+str(Servers_N[i]))
            for j in range(S_flag,(Servers_N[i]+S_flag),1):
                string=Servers[i][0]+"-"+str((j-S_flag+1))+" "
                T_Set=list(set(Name_Servers[j]))
                for z in range(len(T_Set)):
                    L=(Name_Servers[j]).count(T_Set[z])
                    string=string+T_Set[z]+" "+str(L)+" "
                result.append(string)
            result.append(" ")
            S_flag=S_flag+Servers_N[i]
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
        array[idx[i]]=-1000
    return idx
