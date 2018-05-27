def Leastsq(Xdata,Ydata,lenD):
       X=defX(lenD,Xdata)
       Y=defY(lenD,Xdata,Ydata)
       
       T1=(X[1][2]*X[2][1]-X[1][1]*X[2][2])
       T2=(X[0][2]*X[1][1]-X[0][1]*X[1][2])
       a1=float(T1*(X[1][1]*Y[0]-X[0][1]*Y[1])-T2*(X[2][1]*Y[1]-X[1][1]*Y[2]))/(T1*(X[0][0]*X[1][1]-X[0][1]*X[1][0])-T2*(X[1][0]*X[2][1]-X[1][1]*X[2][0]))

       
       T1=(X[0][2]*X[1][0]-X[0][0]*X[1][2])
       T2=(X[2][0]*X[1][2]-X[2][2]*X[1][0])
       a2=float(T1*(X[2][0]*Y[1]-X[1][0]*Y[2])-T2*(X[1][0]*Y[0]-X[0][0]*Y[1]))/(T1*(X[2][0]*X[1][1]-X[2][1]*X[1][0])-T2*(X[0][1]*X[1][0]-X[0][0]*X[1][1]))
       
       T1=(X[0][1]*X[1][0]-X[0][0]*X[1][1])
       T2=(X[2][0]*X[1][1]-X[2][1]*X[1][0])
       a3=float(T1*(X[2][0]*Y[1]-X[1][0]*Y[2])-T2*(X[1][0]*Y[0]-X[0][0]*Y[1]))/(T1*(X[2][0]*X[1][2]-X[2][2]*X[1][0])-T2*(X[0][2]*X[1][0]-X[0][0]*X[1][2]))
       return a1,a2,a3

def defX(lenD,Xdata):
       X=[[0 for i in range(3)]for j in range(3)]
       for i in range(3):
              for j in range(3):
                     for t in range(lenD):
                            X[i][j]=X[i][j]+(Xdata[t])**(i+j)
       return X

def defY(lenD,Xdata,Ydata):
       Y=[0 for i in range(3)]
       for i in range(3):
              for j in range(lenD):
                     Y[i]=Y[i]+((Xdata[j])**(i))*Ydata[j]
       return Y

    
