from __future__ import division
import utils
def Score(ONEPvm,Pvm,Servers_N,P_Servers,Servers):
    
    VMs=[]  # total VM number
    for i in range(len(P_Servers)):
        for j in range(len(P_Servers[i])):
            VMs.append(P_Servers[i][j])
    
    N_Pvm=len(ONEPvm)
    NNEPvm=[]
    for i in range(N_Pvm):
        NNEPvm.append(VMs.count(Pvm[i]))

    yi_yj=0
    for i in range(N_Pvm):
        yi_yj=yi_yj+(ONEPvm[i]-NNEPvm[i])**2
    yi_yj=(yi_yj/N_Pvm)**(0.5)

    yi=0
    for i in range(N_Pvm):
        yi=yi+(ONEPvm[i])**2
    yi=(yi)**(0.5)

    yj=0
    for i in range(N_Pvm):
        yj=yj+(NNEPvm[i])**2
    yj=(yj)**(0.5)
    Score=1-yi_yj/(yi+yj)
    
    T_k=0
    T_m=0
    for i in range(len(VMs)):
        T_k=T_k+int(VMs[i][1])
        T_m=T_m+int(VMs[i][2])

    S_K=0
    S_M=0
    for i in range(len(Servers_N)):
        for j in range(Servers_N[i]):
            S_K=S_K+Servers[i][1]
            S_M=S_M+Servers[i][2]

    Score=((T_k/S_K)+(T_m/S_M))*0.5*Score
    return Score



















            
