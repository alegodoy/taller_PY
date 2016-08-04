
# coding: utf-8

# In[75]:

#TP curso Python
#
# Voy a leer los datos de precipitacion diarios de estaciones de Argentina, y me voy a quedar con el mes de enero
#
#################################################################################################################


# In[76]:

#Leo Archivo
import numpy as np
import pandas as pd
fname='../Precipitacion_2.txt'
#f=open('../Precipitacion_2.txt','r')


# In[107]:

#leo con np fromtxt
#datos=np.genfromtxt(fname,dtype=None,skip_header=1,usecols = (4))


# In[109]:

#Leo con Pandas
#data = pd.read_csv(fname, skiprows=1, header=None, sep='\t')
data = pd.read_csv(fname, header=0, index_col=0, sep='\t', dtype=float)


# In[112]:

#print(data)


# In[119]:

data=data.replace(-999, np.nan)


# In[131]:

enero=data[data.mes==1.]
len(enero)


# In[133]:

#EJEMPLO FRANCO
#a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
#a
#a[a > 4]


# In[ ]:



