# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 05:23:02 2020

@author: rjsta
"""
from plotly.offline import plot
import pandas as pd
import plotly.io as pio
import plotly.express as px

pio.templates.default = "plotly_dark"


df = pd.read_csv('CHL.csv')

fig = px.line(df, x = 'Hour', y = 'Covid Half Life (hrs)', title='Covid Half Life at Time of Day')

plot(fig)
#fig.show()

df2 = pd.read_csv('Visitors.csv')

fig2 = px.line(df2, x = 'Hour', y = 'Visitors', title='Visitors at Time of Day')


plot(fig2)
#fig2.show()