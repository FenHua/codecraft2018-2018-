def Mirror(lenD,N_Pvm,S_Data,Predict_time):
    NEPvm=[0 for i in range(N_Pvm)]
    for i in range(N_Pvm):
        T_Array=[]
        for j in range((lenD-Predict_time),lenD,1):
            T_Array.append(S_Data[i][j])
        NEPvm[i]=sum(T_Array)+7
    return NEPvm
