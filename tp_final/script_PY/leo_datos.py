
# coding: utf-8

# In[ ]:

#TP curso Python
#
# Voy a leer los datos de precipitacion diarios de estaciones de Argentina, y me voy a quedar
# con el mes seleccionado y realizo un histograma de la estacion Azul
#
#################################################################################################################


# In[ ]:

#Leo Archivo
import numpy as np
import pandas as pd
fname='../Precipitacion_2.txt'
#f=open('../Precipitacion_2.txt','r')


# In[ ]:

#leo con np fromtxt
#datos=np.genfromtxt(fname,dtype=None,skip_header=1,usecols = (4))


# In[ ]:

#Leo con Pandas
#data = pd.read_csv(fname, skiprows=1, header=None, sep='\t')
data = pd.read_csv(fname, header=0, index_col=0, sep='\t', dtype=float)


# In[ ]:

#Imprimo los datos por pantalla:
#print(data)


# In[ ]:

data=data.replace(-999, np.nan)
len(data)


# In[ ]:

# Datos del mes utilizado en el histograma para la estacion Azul
mesh=4
enero=data[data.mes==mesh]
enero=enero.Azul[enero.Azul>0]
len(enero)


# In[ ]:

#Vemos el mes elegido
if mesh == 1:
    tmes="Mes de Enero"
    print("Mes de Enero") 
elif mesh ==2: 
    tmes="Mes de Febrero"
    print("Mes de Febrero")
elif mesh ==3: 
    tmes="Mes de Marzo"
    print("Mes de Marzo")
elif mesh ==4: 
    tmes="Mes de Abril"
    print("Mes de Abril")
elif mesh ==5: 
    tmes="Mes de Mayo"
    print("Mes de Mayo")
elif mesh ==6: 
    tmes="Mes de Junio"
    print("Mes de Junio")
elif mesh ==7: 
    tmes="Mes de Julio"
    print("Mes de Julio")
elif mesh ==8: 
    tmes="Mes de Agosto"
    print("Mes de Agosto")
elif mesh ==9: 
    tmes="Mes de Septiembre"
    print("Mes de Septiembre")
elif mesh ==10: 
    tmes="Mes de Octubre"
    print("Mes de Octubre")
elif mesh ==11: 
    tmes="Mes de Noviembre"
    print("Mes de Noviembre")
elif mesh ==12: 
    tmes="Mes de Diciembre"
    print("Mes de Diciembre")
else:
    print("Ese numero no corresponde a un mes")


# In[ ]:

#Calculo de Percentiles
p10=np.percentile(enero,10)
p20=np.percentile(enero,20)
p30=np.percentile(enero,30)
p40=np.percentile(enero,40)
p50=np.percentile(enero,50)
p60=np.percentile(enero,60)
p70=np.percentile(enero,70)
p80=np.percentile(enero,80)
p90=np.percentile(enero,90)
p100=np.percentile(enero,100)


# In[ ]:

#Ejemplo
print(p100)
#Record historico de Azul del mes de enero:
#anio
var1=data[data.mes==mesh]
a=var1.anio[var1.Azul==p100]
aa=a.values[0]
#mes
mesh2=str(mesh)
#dia
var2=data[data.mes==mesh]
d=var2.dia[var2.Azul==p100]
dd=d.values[0]

#fecha
aa=np.array(aa,dtype=np.int)
dd=np.array(dd,dtype=np.int)
aa=str(aa)
dd=str(dd)
fecha=dd+"/"+mesh2+"/"+aa


# In[ ]:

#Plotear el histograma de la estacion 1
import matplotlib.pyplot as plt

plt.hist(enero, bins=12,facecolor='green', alpha=0.5)
plt.title("Histograma de precipitacion de Azul - " + tmes)
plt.xlabel("Precipitacion")
plt.ylabel("Frecuencia")

#
plt.text(p100-20, 25, "Record", fontsize = 14, weight='bold')
plt.text(p100-25, 12, fecha, fontsize = 14)
#plt.show()
#Guardo
#plt.savefig("hist_azul.eps")
plt.savefig("../output/hist_azul.png",bbox_inches='tight')
plt.show()
#plt.close()

# VIEJO
#import potly.potly as py
#ax.annotate("129",xy=(125,10),arrowprops=dict(arrowstyle="->"))
#plt.hist(enero[:,1],bins=[0,20,40,60,80,100])
#EJEMPLO FRANCO
#a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
#a
#a[a > 4]


# In[ ]:

fecha


# In[ ]:




# In[ ]:



