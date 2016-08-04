
# coding: utf-8

# In[75]:

#TP curso Python
#
# Voy a leer los datos de precipitacion diarios de estaciones de Argentina, y me voy a quedar con el mes de enero
#
#################################################################################################################


# In[3]:

#Leo Archivo
import numpy as np
import pandas as pd
fname='../Precipitacion_2.txt'
#f=open('../Precipitacion_2.txt','r')


# In[4]:

#leo con np fromtxt
#datos=np.genfromtxt(fname,dtype=None,skip_header=1,usecols = (4))


# In[5]:

#Leo con Pandas
#data = pd.read_csv(fname, skiprows=1, header=None, sep='\t')
data = pd.read_csv(fname, header=0, index_col=0, sep='\t', dtype=float)


# In[6]:

#print(data)


# In[30]:

data=data.replace(-999, np.nan)
len(data)


# In[32]:

#Mes de enero
enero=data[data.mes==1]
enero=enero.Azul[enero.Azul>0]

len(enero)


# In[9]:

#EJEMPLO FRANCO
#a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
#a
#a[a > 4]


# In[23]:

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


# In[95]:

#Ejemplo
p100
#Record historico de Azul del mes de enero:
#anio
var1=data[data.mes==1]
a=var1.anio[var1.Azul==p100]
aa=a.values[0]
#dia
var2=data[data.mes==1]
d=var2.dia[var2.Azul==p100]
dd=d.values[0]

#fecha
aa=np.array(aa,dtype=np.int)
dd=np.array(dd,dtype=np.int)
aa=str(aa)
dd=str(dd)
fecha=dd+"/01/"+aa


# In[105]:

#Plotear el histograma de la estacion 1
import matplotlib.pyplot as plt
#import potly.potly as py

#plt.hist(enero[:,1],bins=[0,20,40,60,80,100])
plt.hist(enero, bins=12,facecolor='green', alpha=0.5)
plt.title("Histograma de precipitacion de Azul - Mes de Enero")
plt.xlabel("Precipitacion")
plt.ylabel("Frecuencia")

#
plt.text(115, 25, "Record", fontsize = 14)
plt.text(110, 12, fecha, fontsize = 14)
#ax.annotate("129",xy=(125,10),arrowprops=dict(arrowstyle="->"))

plt.show()


# In[97]:

fecha


# In[ ]:




# In[ ]:



