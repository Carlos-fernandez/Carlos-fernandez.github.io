import chart_studio.plotly as py
# import chart_studio
# import plotly.express as px
#
# username = 'carlos-fernandez' # your username
# api_key = 'ypsXlXfluUGW4Dlj0RV1' # your api key - go to profile > settings > regenerate
# chart_studio.tools.set_credentials_file(username=username, api_key=api_key)
#
import plotly.graph_objects as go
from plotly.offline import iplot
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import itertools
import numpy as np
import plotly.figure_factory as ff
import scipy
# importing Statistics module
import statistics

df = pd.read_csv('07_29_21_16_37_record.csv', skiprows= 11)
df_P40 = pd.read_csv('P20SV3020210819A02(Black Stem)11-9-2021.csv', skiprows=11)
df_P1KS = pd.read_csv('P1KSV3020210819A03(w-probe_attached)-11-9-2021.csv', skiprows=11)
df_P1KS_anodized_removed = pd.read_csv('P1KSV3020210819A03(removed Anodized).csv', skiprows=11)
df_P1KS_anodized = pd.read_csv('P1KSV3020210819A03(Anodized-probe_attached).csv', skiprows = 11)


# make a list of trial strings to use later
def calculate_trials(n):
    trials = []
    for t in range(1, n+1):
        trials.append('trial {}'.format(t))
    return trials

def obtain_dataframe(dataframe, trials):
    new_df = dataframe[
            [
             'Dial Indicator(mm)',
             'Phase']
           ]

    triggered_distance = []
    for trial in trials:
        p_data = new_df.loc[new_df['Phase'] == trial]
        point = p_data['Dial Indicator(mm)'][p_data.index[-1]]
        triggered_distance.append(point)

    accuracy = pd.DataFrame({'Triggered Point(mm)': triggered_distance, 'Trials': [i for i in range(1,len(trials)+1)]})
    return accuracy


#------------------------------------
trials = calculate_trials(500)
accuracy = obtain_dataframe(df_P40, trials)


#---------------------------------------

trials_2 = calculate_trials(152)
accuracy_2 = obtain_dataframe(df, trials_2)

#------------------------------------------------


trials_3 = calculate_trials(408)
accuracy_3 = obtain_dataframe(df_P1KS, trials_3)

#--------------------------------------------------

trials_3 = calculate_trials(408)
accuracy_3 = obtain_dataframe(df_P1KS, trials_3)

#--------------------------------------------------

x  = list(accuracy['Triggered Point(mm)'])
y = list(accuracy_2['Triggered Point(mm)'])
z = list(accuracy_3['Triggered Point(mm)'])
fig = ff.create_distplot([accuracy['Triggered Point(mm)'], accuracy_2['Triggered Point(mm)'], accuracy_3['Triggered Point(mm)']],
                         ['(P40S-w/o Probe)', 'P3HS-Proto-3-w/ Probe', 'P1KS-w/ Probe'],
                         bin_size=0.01,
                         #histnorm = 'probability',
                         curve_type='normal')

fig.update_xaxes(title_text = 'Triggered Position(mm)')
fig.update_yaxes(title_text = 'Frequency(%)')
fig.update_layout(title_text='Capacitive Triggered Displacement',
                         #xaxis = dict(dtick=4),
                         yaxis = dict(dtick=2))
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='show')
fig.show()

py.plot(fig, filename = 'Cap_data', auto_open=True)



import plotly.io as pio
pio.write_html(fig, file='index.html', auto_open=True)
