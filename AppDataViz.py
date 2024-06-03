import dash
from dash import Dash,dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import webbrowser
import tkinter as tk
import threading
import numpy as np
import json


details_csv = pd.read_excel('Details_CSV.xlsx', header=0)

ts = pd.read_csv('TS_sec.csv')

## Plot acceleration

def plot_acc(participant, num_test, test_name):
    df = {}
    ide = []

    time = ts[ts['Participant']==participant]
    time.reset_index(drop=True, inplace=True)
    time = time[time['Test Number']==int(num_test)]
    time.reset_index(drop=True, inplace=True)
    start = time['Start timestamp'][0]

    bool1 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_back_motion_{num_test}.csv']
    bool1.reset_index(drop=True, inplace=True)
    if  bool1['empty ? '][0]== 'No':
        acc_back = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_back_motion_{num_test}.csv')
        acc_back['s'] = acc_back['timestamp']-start
        df['acc_back']=acc_back

    bool2 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_bangle_accel_{num_test}.csv']
    bool2.reset_index(drop=True, inplace=True)
    if bool2['empty ? '][0] == 'No':
        acc_bangle = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_bangle_accel_{num_test}.csv')
        acc_bangle['s'] = acc_bangle['timestamp']-start
        df['acc_bangle']=acc_bangle

    bool3 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_hand_motion_{num_test}.csv']
    bool3.reset_index(drop=True, inplace=True)
    if bool3['empty ? '][0] == 'No':
        acc_hand = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_hand_motion_{num_test}.csv')
        acc_hand['s'] = acc_hand['timestamp']-start
        df['acc_hand']=acc_hand

    bool4 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_msafety_acc_{num_test}.csv']
    bool4.reset_index(drop=True, inplace=True)
    if bool4['empty ? '][0] == 'No':
        acc_msafety = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_msafety_acc_{num_test}.csv')
        acc_msafety['s'] = acc_msafety['timestamp']-start
        df['acc_msafety']=acc_msafety

    bool5 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_shoes_lf_{num_test}.csv']
    bool5.reset_index(drop=True, inplace=True)
    if  bool5['empty ? '][0]== 'No':
        acc_shoes_lf = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_shoes_lf_{num_test}.csv')
        if (participant=="DS" or participant=="DL"):
            acc_shoes_lf['s'] = acc_shoes_lf['timestamp']-start-7200
        else:
            acc_shoes_lf['s'] = acc_shoes_lf['timestamp']-start-3600
        df['acc_shoes_lf']=acc_shoes_lf

    bool6 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_shoes_rf_{num_test}.csv']
    bool6.reset_index(drop=True, inplace=True)
    if  bool6['empty ? '][0]== 'No':
        acc_shoes_rf = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_shoes_rf_{num_test}.csv')
        if (participant=="DS" or participant=="DL"):
            acc_shoes_rf['s'] = acc_shoes_rf['timestamp']-start-7200
        else:
            acc_shoes_rf['s'] = acc_shoes_rf['timestamp']-start-3600
        df['acc_shoes_rf']=acc_shoes_rf

    if df :
        fig = []
        for key in df :

            if key == 'acc_back':

                fig1 = go.Figure()

                fig1.add_trace(go.Scatter(x=acc_back['s'], y=acc_back['accGx'], mode='lines', name='Acceleration X'))
                fig1.add_trace(go.Scatter(x=acc_back['s'], y=acc_back['accGy'], mode='lines', name='Acceleration Y'))
                fig1.add_trace(go.Scatter(x=acc_back['s'], y=acc_back['accGz'], mode='lines', name='Acceleration Z'))

                fig1.update_layout(title=f'Acceleration (with G) - Participant: {participant}, Test: {num_test}, Device: Back Phone',
                    xaxis_title='Time (sec)',
                    yaxis_title='Acceleration (with G) (m/s^2)',
                    legend=dict(x=0, y=1, traceorder='normal'),
                    clickmode='event+select')

                fig.append(fig1)
                ide.append(f'{participant}_{num_test}_acc_back')

            elif key == 'acc_bangle':

                fig2 = go.Figure()

                fig2.add_trace(go.Scatter(x=acc_bangle['s'], y=acc_bangle['accGGx'], mode='lines', name='Acceleration X'))
                fig2.add_trace(go.Scatter(x=acc_bangle['s'], y=acc_bangle['accGGy'], mode='lines', name='Acceleration Y'))
                fig2.add_trace(go.Scatter(x=acc_bangle['s'], y=acc_bangle['accGGz'], mode='lines', name='Acceleration Z'))

                fig2.update_layout(title=f'Acceleration (with G) - Participant: {participant}, Test: {num_test}, Device: Bangle',
                    xaxis_title='Time (sec)',
                    yaxis_title='Acceleration (g)',
                    legend=dict(x=0, y=1, traceorder='normal'),
                    clickmode='event+select')

                fig.append(fig2)
                ide.append(f'{participant}_{num_test}_acc_bangle')

            elif key == 'acc_hand':

                fig3 = go.Figure()

                fig3.add_trace(go.Scatter(x=acc_hand['s'], y=acc_hand['accGx'], mode='lines', name='Acceleration X'))
                fig3.add_trace(go.Scatter(x=acc_hand['s'], y=acc_hand['accGy'], mode='lines', name='Acceleration Y'))
                fig3.add_trace(go.Scatter(x=acc_hand['s'], y=acc_hand['accGz'], mode='lines', name='Acceleration Z'))

                fig3.update_layout(title=f'Acceleration (with G) - Participant: {participant}, Test: {num_test}, Device: Hand Phone',
                    xaxis_title='Time (sec)',
                    yaxis_title='Acceleration (with G) (m/s^2)',
                    legend=dict(x=0, y=1, traceorder='normal'),
                    clickmode='event+select')

                fig.append(fig3)
                ide.append(f'{participant}_{num_test}_acc_hand')

            elif key == 'acc_msafety':

                fig4 = go.Figure()

                fig4.add_trace(go.Scatter(x=acc_msafety['s'], y=acc_msafety['accGx'], mode='lines', name='Acceleration X'))
                fig4.add_trace(go.Scatter(x=acc_msafety['s'], y=acc_msafety['accGy'], mode='lines', name='Acceleration Y'))
                fig4.add_trace(go.Scatter(x=acc_msafety['s'], y=acc_msafety['accGz'], mode='lines', name='Acceleration Z'))

                fig4.update_layout(title=f'Acceleration (with G) - Participant: {participant}, Test: {num_test}, Device: Msafety',
                    xaxis_title='Time (sec)',
                    yaxis_title='Acceleration (with G) (m/s^2)',
                    legend=dict(x=0, y=1, traceorder='normal'),
                    clickmode='event+select')

                fig.append(fig4)
                ide.append(f'{participant}_{num_test}_acc_msafety')

            elif key=='acc_shoes_lf':

                fig5 = go.Figure()

                fig5.add_trace(go.Scatter(x=acc_shoes_lf['s'], y=acc_shoes_lf['accRawx'], mode='lines', name='Acceleration X'))
                fig5.add_trace(go.Scatter(x=acc_shoes_lf['s'], y=acc_shoes_lf['accRawy'], mode='lines', name='Acceleration Y'))
                fig5.add_trace(go.Scatter(x=acc_shoes_lf['s'], y=acc_shoes_lf['accRawz'], mode='lines', name='Acceleration Z'))


                fig5.update_layout(title=f'Acceleration - Participant: {participant}, Test: {num_test}, Device: Shoes lf',
                    xaxis_title='Time (sec)',
                    yaxis_title='Acceleration',
                    legend=dict(x=0, y=1, traceorder='normal'),
                    clickmode='event+select')

                fig.append(fig5)
                ide.append(f'{participant}_{num_test}_acc_shoesLF')


            elif key=='acc_shoes_rf':

                fig6 = go.Figure()

                fig6.add_trace(go.Scatter(x=acc_shoes_lf['s'], y=acc_shoes_lf['accRawx'], mode='lines', name='Acceleration X'))
                fig6.add_trace(go.Scatter(x=acc_shoes_lf['s'], y=acc_shoes_lf['accRawy'], mode='lines', name='Acceleration Y'))
                fig6.add_trace(go.Scatter(x=acc_shoes_lf['s'], y=acc_shoes_lf['accRawz'], mode='lines', name='Acceleration Z'))

                fig6.update_layout(title=f'Acceleration - Participant: {participant}, Test: {num_test}, Device: Shoes rf',
                    xaxis_title='Time (sec)',
                    yaxis_title='Acceleration',
                    legend=dict(x=0, y=1, traceorder='normal'),
                    clickmode='event+select')

                fig.append(fig6)
                ide.append(f'{participant}_{num_test}_acc_shoesRF')

        while len(fig)<6:
            fig.append([])

        return fig, ide

    else :
        return [],[]


## Plot rotation

def plot_rot(participant, num_test,test_name):
    df = {}
    ide = []

    time = ts[ts['Participant']==participant]
    time.reset_index(drop=True, inplace=True)
    time = time[time['Test Number']==int(num_test)]
    time.reset_index(drop=True, inplace=True)
    start = time['Start timestamp'][0]

    bool1 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_back_orientation_{num_test}.csv']
    bool1.reset_index(drop=True, inplace=True)
    if  bool1['empty ? '][0]== 'No':
        rot_back = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_back_orientation_{num_test}.csv')
        rot_back['s'] = rot_back['timestamp']-start
        df['rot_back']=rot_back

    bool2 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_hand_orientation_{num_test}.csv']
    bool2.reset_index(drop=True, inplace=True)
    if bool2['empty ? '][0] == 'No':
        rot_hand = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_hand_orientation_{num_test}.csv')
        rot_hand['s'] = rot_hand['timestamp']-start
        df['rot_hand']=rot_hand

    bool3 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_shoes_rf_{num_test}.csv']
    bool3.reset_index(drop=True, inplace=True)
    if  bool3['empty ? '][0]== 'No':
        rot_shoes_rf = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_shoes_rf_{num_test}.csv')
        if (participant=="DS" or participant=="DL"):
            rot_shoes_rf['s'] = rot_shoes_rf['timestamp']-start-7200
        else:
            rot_shoes_rf['s'] = rot_shoes_rf['timestamp']-start-3600
        df['rot_shoes_rf']=rot_shoes_rf

    bool4 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_shoes_lf_{num_test}.csv']
    bool4.reset_index(drop=True, inplace=True)
    if  bool4['empty ? '][0]== 'No':
        rot_shoes_lf = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_shoes_lf_{num_test}.csv')
        if (participant=="DS" or participant=="DL"):
            rot_shoes_lf['s'] = rot_shoes_lf['timestamp']-start-7200
        else:
            rot_shoes_lf['s'] = rot_shoes_lf['timestamp']-start-3600
        df['rot_shoes_lf']=rot_shoes_lf

    if df :
        fig = []
        for key in df :

            if key == 'rot_back':

                fig1 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig1.add_trace(go.Scatter(x=rot_back['s'], y=rot_back['alpha'], mode='lines', name='Alpha'))
                fig1.add_trace(go.Scatter(x=rot_back['s'], y=rot_back['beta'], mode='lines', name='Beta'))
                fig1.add_trace(go.Scatter(x=rot_back['s'], y=rot_back['gamma'], mode='lines', name='Gamma'))

                # Mettre à jour la disposition de la figure
                fig1.update_layout(title=f'Rotation - Participant: {participant}, Test: {num_test}, Device: Back Phone',
                    xaxis_title='Time (sec)',
                    yaxis_title='Rotation',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig1)
                ide.append(f'{participant}_{num_test}_rot_back')


            elif key == 'rot_hand':

                fig2 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig2.add_trace(go.Scatter(x=rot_hand['s'], y=rot_hand['alpha'], mode='lines', name='Alpha'))
                fig2.add_trace(go.Scatter(x=rot_hand['s'], y=rot_hand['beta'], mode='lines', name='Beta'))
                fig2.add_trace(go.Scatter(x=rot_hand['s'], y=rot_hand['gamma'], mode='lines', name='Gamma'))

                # Mettre à jour la disposition de la figure
                fig2.update_layout(title=f'Rotation - Participant: {participant}, Test: {num_test}, Device: Hand Phone',
                    xaxis_title='Time (sec)',
                    yaxis_title='Rotation',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig2)
                ide.append(f'{participant}_{num_test}_rot_hand')

            elif key=='rot_shoes_lf':

                fig3 = go.Figure()

                fig3.add_trace(go.Scatter(x=rot_shoes_lf['s'], y=rot_shoes_lf['rotRawx'], mode='lines', name='Rotation X'))
                fig3.add_trace(go.Scatter(x=rot_shoes_lf['s'], y=rot_shoes_lf['rotRawy'], mode='lines', name='Rotation Y'))
                fig3.add_trace(go.Scatter(x=rot_shoes_lf['s'], y=rot_shoes_lf['rotRawz'], mode='lines', name='Rotation Z'))

                fig3.update_layout(title=f'Rotation - Participant: {participant}, Test: {num_test}, Device: Shoes lf',
                    xaxis_title='Time (sec)',
                    yaxis_title='Rotation',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig3)
                ide.append(f'{participant}_{num_test}_rot_shoesLF')

            elif key=='rot_shoes_rf':

                fig4 = go.Figure()

                fig4.add_trace(go.Scatter(x=rot_shoes_lf['s'], y=rot_shoes_lf['rotRawx'], mode='lines', name='Rotation X'))
                fig4.add_trace(go.Scatter(x=rot_shoes_lf['s'], y=rot_shoes_lf['rotRawy'], mode='lines', name='Rotation Y'))
                fig4.add_trace(go.Scatter(x=rot_shoes_lf['s'], y=rot_shoes_lf['rotRawz'], mode='lines', name='Rotation Z'))

                fig4.update_layout(title=f'Rotation - Participant: {participant}, Test: {num_test}, Device: Shoes rf',
                    xaxis_title='Time (sec)',
                    yaxis_title='Rotation',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig4)
                ide.append(f'{participant}_{num_test}_rot_shoesRF')


        while len(fig)<4:
            fig.append([])

        return fig, ide

    else :
        return [],[]


## Plot mag

def plot_mag(participant, num_test, test_name):
    df = {}
    ide=[]

    time = ts[ts['Participant']==participant]
    time.reset_index(drop=True, inplace=True)
    time = time[time['Test Number']==int(num_test)]
    time.reset_index(drop=True, inplace=True)
    start = time['Start timestamp'][0]

    bool1 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_bangle_compass_{num_test}.csv']
    bool1.reset_index(drop=True, inplace=True)
    if bool1['empty ? '][0] == 'No':
        mag_bangle = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_bangle_compass_{num_test}.csv')
        mag_bangle['s'] = mag_bangle['timestamp']-start
        df['mag_bangle']=mag_bangle

    bool2 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_shoes_lf_{num_test}.csv']
    bool2.reset_index(drop=True, inplace=True)
    if  bool2['empty ? '][0]== 'No':
        mag_shoes_lf = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_shoes_lf_{num_test}.csv')
        if (participant=="DS" or participant=="DL"):
            mag_shoes_lf['s'] = mag_shoes_lf['timestamp']-start-7200
        else:
            mag_shoes_lf['s'] = mag_shoes_lf['timestamp']-start-3600
        df['mag_shoes_lf']=mag_shoes_lf

    bool3 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_shoes_rf_{num_test}.csv']
    bool3.reset_index(drop=True, inplace=True)
    if  bool3['empty ? '][0]== 'No':
        mag_shoes_rf = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_shoes_rf_{num_test}.csv')
        if (participant=="DS" or participant=="DL"):
            mag_shoes_rf['s'] = mag_shoes_rf['timestamp']-start-7200
        else:
            mag_shoes_rf['s'] = mag_shoes_rf['timestamp']-start-3600
        df['mag_shoes_rf']=mag_shoes_rf

    if df :
        fig = []
        for key in df :

            if key == 'mag_bangle':

                fig1 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig1.add_trace(go.Scatter(x=mag_bangle['s'], y=mag_bangle['magnRawx'], mode='lines', name='Magnetic Field X'))
                fig1.add_trace(go.Scatter(x=mag_bangle['s'], y=mag_bangle['magnRawy'], mode='lines', name='Magnetic Field Y'))
                fig1.add_trace(go.Scatter(x=mag_bangle['s'], y=mag_bangle['magnRawz'], mode='lines', name='Magnetic Field Y'))

                # Mettre à jour la disposition de la figure
                fig1.update_layout(title=f'Magnetic Field - Participant: {participant}, Test: {num_test}, Device: Bangle',
                    xaxis_title='Time (sec)',
                    yaxis_title='Magnetic Field',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig1)
                ide.append(f'{participant}_{num_test}_mag_bangle')


            elif key=='mag_shoes_lf':

                fig2 = go.Figure()

                fig2.add_trace(go.Scatter(x=mag_shoes_lf['s'], y=mag_shoes_lf['magnRawx'], mode='lines', name='Magnetic Field X'))
                fig2.add_trace(go.Scatter(x=mag_shoes_lf['s'], y=mag_shoes_lf['magnRawy'], mode='lines', name='Magnetic Field Y'))
                fig2.add_trace(go.Scatter(x=mag_shoes_lf['s'], y=mag_shoes_lf['magnRawz'], mode='lines', name='Magnetic Field Z'))

                fig2.update_layout(title=f'Magnetic Field - Participant: {participant}, Test: {num_test}, Device: Shoes lf',
                    xaxis_title='Time (sec)',
                    yaxis_title='Magnetic Field',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig2)
                ide.append(f'{participant}_{num_test}_mag_shoesLF')

            elif key=='mag_shoes_rf':

                fig3 = go.Figure()

                fig3.add_trace(go.Scatter(x=mag_shoes_lf['s'], y=mag_shoes_lf['magnRawx'], mode='lines', name='Magnetic Field X'))
                fig3.add_trace(go.Scatter(x=mag_shoes_lf['s'], y=mag_shoes_lf['magnRawy'], mode='lines', name='Magnetic Field Y'))
                fig3.add_trace(go.Scatter(x=mag_shoes_lf['s'], y=mag_shoes_lf['magnRawz'], mode='lines', name='Magnetic Field Z'))

                fig3.update_layout(title=f'Magnetic Field - Participant: {participant}, Test: {num_test}, Device: Shoes rf',
                    xaxis_title='Time (sec)',
                    yaxis_title='Magnetic Field',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig3)
                ide.append(f'{participant}_{num_test}_mag_shoesRF')

        while len(fig)<3:
            fig.append([])

        return fig, ide

    else :
        return [],[]


## Plot ppg

def plot_ppg(participant, num_test,test_name):
    df = {}
    ide=[]

    time = ts[ts['Participant']==participant]
    time.reset_index(drop=True, inplace=True)
    time = time[time['Test Number']==int(num_test)]
    time.reset_index(drop=True, inplace=True)
    start = time['Start timestamp'][0]

    bool1 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_msafety_ppg_{num_test}.csv']
    bool1.reset_index(drop=True, inplace=True)
    if  bool1['empty ? '][0]== 'No':
        ppg = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_msafety_ppg_{num_test}.csv')
        ppg['s'] = ppg['timestamp']-start
        df['ppg']=ppg

    if df :
        fig = []

        for key in df :

            if key == 'ppg':

                fig1 = go.Figure()

                fig1.add_trace(go.Scatter(x=ppg['s'], y=ppg['ppg'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig1.update_layout(title=f'PPG - Participant: {participant}, Test: {num_test}, Device: Msafety',
                    xaxis_title='Time (sec)',
                    yaxis_title='PPG',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig1)
                ide.append(f'{participant}_{num_test}_ppg_msafety')

        return fig, ide

    else :
        return [],[]


## Plot hr

def plot_hr(participant, num_test,test_name):
    df = {}
    ide=[]

    time = ts[ts['Participant']==participant]
    time.reset_index(drop=True, inplace=True)
    time = time[time['Test Number']==int(num_test)]
    time.reset_index(drop=True, inplace=True)
    start = time['Start timestamp'][0]

    bool1 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_bangle_hr_{num_test}.csv']
    bool1.reset_index(drop=True, inplace=True)
    if  bool1['empty ? '][0]== 'No':
        hr = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_bangle_hr_{num_test}.csv')
        hr['s'] = hr['timestamp']-start
        df['hr']=hr

    if df :
        fig=[]
        for key in df :

            if key == 'hr':

                fig1 = go.Figure()

                fig1.add_trace(go.Scatter(x=hr['s'], y=hr['hr'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig1.update_layout(title=f'Heart Rate - Participant: {participant}, Test: {num_test}, Device: Bangle',
                    xaxis_title='Time (sec)',
                    yaxis_title='Heart Rate',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig1)
                ide.append(f'{participant}_{num_test}_hr_bangle')

        return fig, ide

    else :
        return [],[]


## Plot steps

def plot_step(participant,num_test, test_name):
    df = {}
    ide=[]

    time = ts[ts['Participant']==participant]
    time.reset_index(drop=True, inplace=True)
    time = time[time['Test Number']==int(num_test)]
    time.reset_index(drop=True, inplace=True)
    start = time['Start timestamp'][0]

    bool1 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_bangle_steps_{num_test}.csv']
    bool1.reset_index(drop=True, inplace=True)
    if  bool1['empty ? '][0]== 'No':
        steps_bangle = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_bangle_steps_{num_test}.csv')
        steps_bangle['s'] = steps_bangle['timestamp']-start
        df['steps_bangle']=steps_bangle

    bool2 = details_csv[details_csv['Chemin fichier']==f'Results/{participant}/{num_test}/{participant}_hand_cadence_{num_test}.csv']
    bool2.reset_index(drop=True, inplace=True)
    if bool2['empty ? '][0] == 'No':
        steps_hand = pd.read_csv(f'Results/{participant}/{num_test}/{participant}_hand_cadence_{num_test}.csv')
        steps_hand['s'] = steps_hand['timestamp']-start
        df['steps_hand']=steps_hand

    if df :
        fig=[]
        for key in df :

            if key == 'steps_bangle':

                fig1 = go.Figure()

                fig1.add_trace(go.Scatter(x=steps_bangle['s'], y=steps_bangle['steps'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig1.update_layout(title=f'Step - Participant: {participant}, Test: {num_test}, Device: Bangle',
                    xaxis_title='Time (sec)',
                    yaxis_title='Step',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig1)
                ide.append(f'{participant}_{num_test}_step_bangle')

            elif key == 'steps_hand':

                fig2 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig2.add_trace(go.Scatter(x=steps_hand['s'], y=steps_hand['instantaneousSpeed'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig2.update_layout(title=f'Speed - Participant: {participant}, Test: {num_test}, Device: Hand Phone',
                    xaxis_title='Time (sec)',
                    yaxis_title='Speed',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig2)
                ide.append(f'{participant}_{num_test}_speed_hand')

                fig3 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig3.add_trace(go.Scatter(x=steps_hand['s'], y=steps_hand['instantaneousCadence'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig3.update_layout(title=f'Step - Participant: {participant}, Test: {num_test}, Device: Hand Phone',
                    xaxis_title='Time (sec)',
                    yaxis_title='Step',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig3)
                ide.append(f'{participant}_{num_test}_step_hand')

                fig4 = go.Figure()

                # Ajouter des traces de ligne pour l'accélération dans les trois axes
                fig4.add_trace(go.Scatter(x=steps_hand['s'], y=steps_hand['instantaneousStrideLength'], mode='lines'))

                # Mettre à jour la disposition de la figure
                fig4.update_layout(title=f'Stride Length - Participant: {participant}, Test: {num_test}, Device: Hand Phone',
                    xaxis_title='Time (sec)',
                    yaxis_title='Stride Length',
                    legend=dict(x=0, y=1, traceorder='normal'))

                fig.append(fig4)
                ide.append(f'{participant}_{num_test}_stride_hand')

        while len(fig)<4:
            fig.append([])

        return fig, ide

    else :
        return [],[]


## main
class DashThread(threading.Thread):
    def __init__(self, data_list):
        threading.Thread.__init__(self)
        self.data_list = data_list

        self.app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

        ## Markers dictionary
        markers =  {'DS':{
                    '1':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '2':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '3':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '4':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '5':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '6':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '7':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '8':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '9':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '10':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}}
                },
            'DL':{
                    '1':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '2':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '3':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '4':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '5':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '6':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '7':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '8':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '9':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '10':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}}
                },
            'MB':{
                    '1':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '2':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '3':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '4':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '5':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '6':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '7':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '8':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '9':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '10':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}}
                },
            'RC':{
                    '1':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '2':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '3':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '4':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '5':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '6':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '7':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '8':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '9':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '10':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}}
                },
            'PB':{
                    '1':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '2':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '3':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '4':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '5':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '6':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '7':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '8':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '9':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '10':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}}
                },
            'LC':{
                    '1':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '2':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '3':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '4':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '5':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '6':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '7':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '8':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '9':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}},
                    '10':{'acc_back':{'x':{}, 'y':{}, 'z':{}}, 'acc_hand':{'x':{}, 'y':{}, 'z':{}}, 'acc_bangle':{'x':{}, 'y':{}, 'z':{}}, 'acc_msafety':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'acc_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'rot_back':{'a':{}, 'b':{}, 'g':{}}, 'rot_hand':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesLF':{'a':{}, 'b':{}, 'g':{}}, 'rot_shoesRF':{'a':{}, 'b':{}, 'g':{}}, 'mag_bangle':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesLF':{'x':{}, 'y':{}, 'z':{}}, 'mag_shoesRF':{'x':{}, 'y':{}, 'z':{}}, 'ppg_msafety':{}, 'hr_bangle':{}, 'step_bangle':{}, 'step_hand':{}, 'speed_hand':{}, 'stride_hand':{}}
                }
        }

        # Data
        participants = ['DS', 'DL', 'MB', 'RC', 'PB', 'LC']
        tests = ['TUG 1','TUG 2','TUG slow 1','TUG slow 2','30CST','Locomo','10MWT 1','10MWT 2','partial 6MWT 1','partial 6MWT 2']

        # Creation of the participant selection drop-down list
        dropdown_participant = dcc.Dropdown(
            id='dropdown-participant',
            options=[{'label': participant, 'value': participant} for participant in participants],
            value=None
        )

        # Creation of the drop-down list for test selection
        dropdown_test = dcc.Dropdown(
            id='dropdown-test',
            options=[{'label': test, 'value': test} for test in tests],
            value=None
        )
        mats_button_next = dbc.Button('Add', id='next-button',n_clicks=0, color='primary', className='mt-2')
        mats_button_clear = dbc.Button('Clear mats', id='clear-button-mats',n_clicks=0, color='primary', className='mt-2')
        mats_graph_container = html.Div(id='mats-graph-container')
        ## Application layout
        self.app.layout = dbc.Container([
            html.Div([
            html.H1("Data Visualization"),
            html.Div([
                html.Label('Participant'),
                dropdown_participant,
                html.Label('Test'),
                dropdown_test
            ], id='selection-form'),
            html.Div([
                dbc.Button('Show markers', id='show-markers-btn', color='primary', className='mt-2'),
            ]),
            dcc.Tabs(id="tabs", value='tab-1', children=[
                dcc.Tab(label='Acceleration', value='tab-1', children=[
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='acc_g1'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-acc1', type='text'),
                            dbc.Button('Add marker', id='add-marker-acc1', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-acc1', color='primary', className='mt-2'),
                            html.Div(id='marker-list-acc1')
                        ], width=4)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='acc_g2'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-acc2', type='text'),
                            dbc.Button('Add marker', id='add-marker-acc2', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-acc2', color='primary', className='mt-2'),
                            html.Div(id='marker-list-acc2')
                        ], width=4)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='acc_g3'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-acc3', type='text'),
                            dbc.Button('Add marker', id='add-marker-acc3', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-acc3', color='primary', className='mt-2'),
                            html.Div(id='marker-list-acc3')
                        ], width=4)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='acc_g4'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-acc4', type='text'),
                            dbc.Button('Add marker', id='add-marker-acc4', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-acc4', color='primary', className='mt-2'),
                            html.Div(id='marker-list-acc4')
                        ], width=4)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='acc_g5'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-acc5', type='text'),
                            dbc.Button('Add marker', id='add-marker-acc5', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-acc5', color='primary', className='mt-2'),
                            html.Div(id='marker-list-acc5')
                        ], width=4)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='acc_g6'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-acc6', type='text'),
                            dbc.Button('Add marker', id='add-marker-acc6', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-acc6', color='primary', className='mt-2'),
                            html.Div(id='marker-list-acc6')
                        ], width=4)
                    ])
                ]),
                dcc.Tab(label='Rotation', value='tab-2', children=[
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='rot_g1'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-rot1', type='text'),
                            dbc.Button('Add marker', id='add-marker-rot1', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-rot1', color='primary', className='mt-2'),
                            html.Div(id='marker-list-rot1')
                        ], width=4)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='rot_g2'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-rot2', type='text'),
                            dbc.Button('Add marker', id='add-marker-rot2', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-rot2', color='primary', className='mt-2'),
                            html.Div(id='marker-list-rot2')
                        ], width=4)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='rot_g3'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-rot3', type='text'),
                            dbc.Button('Add marker', id='add-marker-rot3', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-rot3', color='primary', className='mt-2'),
                            html.Div(id='marker-list-rot3')
                        ], width=4)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='rot_g4'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-rot4', type='text'),
                            dbc.Button('Add marker', id='add-marker-rot4', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-rot4', color='primary', className='mt-2'),
                            html.Div(id='marker-list-rot4')
                        ], width=4)
                    ])
                ]),
                dcc.Tab(label='Magnetic Field', value='tab-3', children=[
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='mag_g1'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-mag1', type='text'),
                            dbc.Button('Add marker', id='add-marker-mag1', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-mag1', color='primary', className='mt-2'),
                            html.Div(id='marker-list-mag1')
                        ], width=4)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='mag_g2'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-mag2', type='text'),
                            dbc.Button('Add marker', id='add-marker-mag2', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-mag2', color='primary', className='mt-2'),
                            html.Div(id='marker-list-mag2')
                        ], width=4)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='mag_g3'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-mag3', type='text'),
                            dbc.Button('Add marker', id='add-marker-mag3', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-mag3', color='primary', className='mt-2'),
                            html.Div(id='marker-list-mag3')
                        ], width=4)
                    ])
                ]),
                dcc.Tab(label='PPG', value='tab-4', children=[
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='ppg_g1'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-ppg1', type='text'),
                            dbc.Button('Add marker', id='add-marker-ppg1', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-ppg1', color='primary', className='mt-2'),
                            html.Div(id='marker-list-ppg1')
                        ], width=4)
                    ])
                ]),
                dcc.Tab(label='Heart Rate', value='tab-5', children=[
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='hr_g1'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-hr1', type='text'),
                            dbc.Button('Add marker', id='add-marker-hr1', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-hr1', color='primary', className='mt-2'),
                            html.Div(id='marker-list-hr1')
                        ], width=4)
                    ])
                ]),
                dcc.Tab(label='Step', value='tab-6', children=[
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='step_g1'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-step1', type='text'),
                            dbc.Button('Add marker', id='add-marker-step1', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-step1', color='primary', className='mt-2'),
                            html.Div(id='marker-list-step1')
                        ], width=4)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='step_g2'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-step2', type='text'),
                            dbc.Button('Add marker', id='add-marker-step2', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-step2', color='primary', className='mt-2'),
                            html.Div(id='marker-list-step2')
                        ], width=4)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='step_g3'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-step3', type='text'),
                            dbc.Button('Add marker', id='add-marker-step3', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-step3', color='primary', className='mt-2'),
                            html.Div(id='marker-list-step3')
                        ], width=4)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='step_g4'
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Label('Marker name'),
                            dbc.Input(id='marker-name-step4', type='text'),
                            dbc.Button('Add marker', id='add-marker-step4', color='primary', className='mt-2'),
                            dbc.Button('Reset marker', id='reset-marker-step4', color='primary', className='mt-2'),
                            html.Div(id='marker-list-step4')
                        ], width=4)
                    ])
                ]),
                dcc.Tab(label='Mats', value='tab-7', children=[
                    html.Div([
                        html.H1("Mats Visualization"),
                        mats_button_next,
                        mats_button_clear,
                        html.H4("Slider seat"),
                        dcc.Slider(
                            id='slider-seat',
                            min=0,
                            max=300,
                            step=1,
                            value=0,  # Valeur initiale
                            marks={i: str(i) for i in range(0, 301, 5)}  # Marques sur le slider
                        ),
                        html.H4("Slider floor"),
                        dcc.Slider(
                            id='slider-floor',
                            min=0,
                            max=300,
                            step=1,
                            value=0,  # Valeur initiale
                            marks={i: str(i) for i in range(0, 301, 5)}  # Marques sur le slider
                        ),
                        dcc.Store(id='clicks-store-seat', data=0),
                        dcc.Store(id='clicks-store-floor', data=0),
                        mats_graph_container
                    ])
                ]),
                dcc.Tab(label='Shoes', value='tab-8', children=[
                    html.Div([
                        html.H1("Shoes Visualization")
                    ])
                ]),
                dcc.Tab(label='Skeleton', value='tab-9', children=[
                    html.Div([
                        html.H1("Skeleton Visualization")
                    ])
                ])
            ])
            ])
        ], fluid=True, style={"margin": "2px"})

        # Define the modal window
        self.app.layout.children.append(dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Marker dictionary")),
                dbc.ModalBody(id='modal-body'),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            id="modal",
            is_open=False,
        ))

        ## Acceleration management
        @self.app.callback(
            [Output('acc_g1', 'figure'),
            Output('acc_g2', 'figure'),
            Output('acc_g3', 'figure'),
            Output('acc_g4', 'figure'),
            Output('acc_g5', 'figure'),
            Output('acc_g6', 'figure')],
            [Output('marker-list-acc1', 'children'),
            Output('marker-list-acc2', 'children'),
            Output('marker-list-acc3', 'children'),
            Output('marker-list-acc4', 'children'),
            Output('marker-list-acc5', 'children'),
            Output('marker-list-acc6', 'children')],
            [Input('dropdown-participant', 'value'),
            Input('dropdown-test', 'value')],
            [Input('reset-marker-acc1', 'n_clicks'),
            Input('reset-marker-acc2', 'n_clicks'),
            Input('reset-marker-acc3', 'n_clicks'),
            Input('reset-marker-acc4', 'n_clicks'),
            Input('reset-marker-acc5', 'n_clicks'),
            Input('reset-marker-acc6', 'n_clicks')],
            [Input('add-marker-acc1', 'n_clicks'),
            Input('add-marker-acc2', 'n_clicks'),
            Input('add-marker-acc3', 'n_clicks'),
            Input('add-marker-acc4', 'n_clicks'),
            Input('add-marker-acc5', 'n_clicks'),
            Input('add-marker-acc6', 'n_clicks')],
            [State('acc_g1', 'clickData'),
            State('acc_g2', 'clickData'),
            State('acc_g3', 'clickData'),
            State('acc_g4', 'clickData'),
            State('acc_g5', 'clickData'),
            State('acc_g6', 'clickData')],
            [State('marker-name-acc1', 'value'),
            State('marker-name-acc2', 'value'),
            State('marker-name-acc3', 'value'),
            State('marker-name-acc4', 'value'),
            State('marker-name-acc5', 'value'),
            State('marker-name-acc6', 'value')]
        )

        def update_acc(participant, test,*vals):

            if participant is None or test is None :
                return [],[],[],[],[],[],[],[],[],[],[],[]

            return_divs_acc = [html.Div(), html.Div(), html.Div(), html.Div(), html.Div(), html.Div()]

            # Transform the test name into a test number
            if test == 'TUG 1' :
                t = 1
            elif test == 'TUG 2':
                t = 2
            elif test == 'TUG slow 1':
                t = 3
            elif test == 'TUG slow 2':
                t = 4
            elif test == '30CST':
                t=5
            elif test == 'Locomo':
                t=6
            elif test == '10MWT 1':
                t=7
            elif test == '10MWT 2':
                t=8
            elif test == 'partial 6MWT 1':
                t=9
            elif test == 'partial 6MWT 2':
                t=10

            # Call the function to obtain the initial graphics
            return_graphs_acc,id_graphs_acc = plot_acc(participant,t,test)

            n_t=str(t)

            id_bt_reset_acc = ['reset-marker-acc1','reset-marker-acc2','reset-marker-acc3','reset-marker-acc4','reset-marker-acc5','reset-marker-acc6']

            ide = ctx.triggered[0]['prop_id'].split('.')[0]

            # Reset button management
            if ide in id_bt_reset_acc :
                ind =  id_bt_reset_acc.index(ide)
                ide_g = id_graphs_acc[ind]
                device = ide_g[5:]
                device = ''.join(device)
                markers[participant][n_t][device]['x'].clear()
                markers[participant][n_t][device]['y'].clear()
                markers[participant][n_t][device]['z'].clear()

            # Markers management
            else :
                id_bt_add_acc = ['add-marker-acc1','add-marker-acc2','add-marker-acc3','add-marker-acc4','add-marker-acc5','add-marker-acc6']

                if ide in id_bt_add_acc :

                    ind =  id_bt_add_acc.index(ide) #we find out which button he clicked on
                    add_b = vals[ind+6] #retrieve the button corresponding to the graph where it was clicked
                    val = vals[ind+12] #retrieve the graph corresponding to the graph where it was clicked
                    name = vals[ind+18] #name of the marker
                    if add_b is not None and val is not None and name:
                        ide_g = id_graphs_acc[ind]
                        device = ide_g[5:]
                        device = ''.join(device)

                        # Retrieving click details
                        x = val['points'][0]['x']
                        y = val['points'][0]['y']

                        # Retrieving the name of the curve clicked on
                        curve_name = val['points'][0]['curveNumber']

                        # Save the marker in the corresponding dictionary
                        if curve_name==0:
                            markers[participant][n_t][device]['x'][name]=(x,y)
                        if curve_name==1:
                            markers[participant][n_t][device]['y'][name]=(x,y)
                        if curve_name==2:
                            markers[participant][n_t][device]['z'][name]=(x,y)


            # Browse all graphs to update points on graphs and lists of selected points
            for ide in id_graphs_acc:
                i = id_graphs_acc.index(ide)
                d = ide[5:]
                d = ''.join(d)

                marker_items = (
                [html.Li(f"Point ({x}, {y}): {n}") for n, (x, y) in markers[participant][n_t][d]['x'].items()]
                +[html.Li(f"Point ({x}, {y}): {n}") for n, (x, y) in markers[participant][n_t][d]['y'].items()]
                +[html.Li(f"Point ({x}, {y}): {n}") for n, (x, y) in markers[participant][n_t][d]['z'].items()])

                if marker_items:
                    return_divs_acc[i] = html.Ul(marker_items)

                for name_m, point in markers[participant][n_t][d]['x'].items():
                    return_graphs_acc[i].add_trace(
                        go.Scatter(
                        x=[point[0]],
                        y=[point[1]],
                        mode='markers',
                        marker=dict(color='red', size=10),
                        name=name_m,
                        showlegend=False)
                    )

                for name_m, point in markers[participant][n_t][d]['y'].items():
                    return_graphs_acc[i].add_trace(
                        go.Scatter(
                        x=[point[0]],
                        y=[point[1]],
                        mode='markers',
                        marker=dict(color='red', size=10),
                        name=name_m,
                        showlegend=False)
                    )

                for name_m, point in markers[participant][n_t][d]['z'].items():
                    return_graphs_acc[i].add_trace(
                        go.Scatter(
                        x=[point[0]],
                        y=[point[1]],
                        mode='markers',
                        marker=dict(color='red', size=10),
                        name=name_m,
                        showlegend=False)
                    )

            return return_graphs_acc[0], return_graphs_acc[1], return_graphs_acc[2], return_graphs_acc[3], return_graphs_acc[4], return_graphs_acc[5], return_divs_acc[0], return_divs_acc[1], return_divs_acc[2], return_divs_acc[3], return_divs_acc[4], return_divs_acc[5]


        ## Rotation management
        @self.app.callback(
            [Output('rot_g1', 'figure'),
            Output('rot_g2', 'figure'),
            Output('rot_g3', 'figure'),
            Output('rot_g4', 'figure')],
            [Output('marker-list-rot1', 'children'),
            Output('marker-list-rot2', 'children'),
            Output('marker-list-rot3', 'children'),
            Output('marker-list-rot4', 'children')],
            [Input('dropdown-participant', 'value'),
            Input('dropdown-test', 'value')],
            [Input('reset-marker-rot1', 'n_clicks'),
            Input('reset-marker-rot2', 'n_clicks'),
            Input('reset-marker-rot3', 'n_clicks'),
            Input('reset-marker-rot4', 'n_clicks')],
            [Input('add-marker-rot1', 'n_clicks'),
            Input('add-marker-rot2', 'n_clicks'),
            Input('add-marker-rot3', 'n_clicks'),
            Input('add-marker-rot4', 'n_clicks')],
            [State('rot_g1', 'clickData'),
            State('rot_g2', 'clickData'),
            State('rot_g3', 'clickData'),
            State('rot_g4', 'clickData')],
            [State('marker-name-rot1', 'value'),
            State('marker-name-rot2', 'value'),
            State('marker-name-rot3', 'value'),
            State('marker-name-rot4', 'value')]
        )

        def update_rot(participant, test,*vals):

            if participant is None or test is None :
                return [],[],[],[],[],[],[],[]

            return_divs_rot = [html.Div(), html.Div(), html.Div(), html.Div()]

            # Transform the test name into a test number
            if test == 'TUG 1' :
                t = 1
            elif test == 'TUG 2':
                t = 2
            elif test == 'TUG slow 1':
                t = 3
            elif test == 'TUG slow 2':
                t = 4
            elif test == '30CST':
                t=5
            elif test == 'Locomo':
                t=6
            elif test == '10MWT 1':
                t=7
            elif test == '10MWT 2':
                t=8
            elif test == 'partial 6MWT 1':
                t=9
            elif test == 'partial 6MWT 2':
                t=10

            # Call the function to obtain the initial graphics
            return_graphs_rot,id_graphs_rot = plot_rot(participant,t,test)

            n_t=str(t)

            id_bt_reset_rot = ['reset-marker-rot1','reset-marker-rot2','reset-marker-rot3','reset-marker-rot4']

            ide = ctx.triggered[0]['prop_id'].split('.')[0]

            # Reset button management
            if ide in id_bt_reset_rot :
                ind =  id_bt_reset_rot.index(ide)
                ide_g = id_graphs_rot[ind]
                device = ide_g[5:]
                device = ''.join(device)
                markers[participant][n_t][device]['a'].clear()
                markers[participant][n_t][device]['b'].clear()
                markers[participant][n_t][device]['g'].clear()

            # Markers management
            else :
                id_bt_add_rot = ['add-marker-rot1','add-marker-rot2','add-marker-rot3','add-marker-rot4']

                if ide in id_bt_add_rot :

                    ind =  id_bt_add_rot.index(ide) #we find out which button he clicked on
                    add_b = vals[ind+4] #retrieve the button corresponding to the graph where it was clicked
                    val = vals[ind+8] #retrieve the graph corresponding to the graph where it was clicked
                    name = vals[ind+12] #name of the marker
                    if add_b is not None and val is not None and name:
                        ide_g = id_graphs_rot[ind]
                        device = ide_g[5:]
                        device = ''.join(device)

                        # Retrieving click details
                        x = val['points'][0]['x']
                        y = val['points'][0]['y']

                        # Retrieving the name of the curve clicked on
                        curve_name = val['points'][0]['curveNumber']

                        # Save the marker in the corresponding dictionary
                        if curve_name==0:
                            markers[participant][n_t][device]['a'][name]=(x,y)
                        if curve_name==1:
                            markers[participant][n_t][device]['b'][name]=(x,y)
                        if curve_name==2:
                            markers[participant][n_t][device]['g'][name]=(x,y)


            # Browse all graphs to update points on graphs and lists of selected points
            for ide in id_graphs_rot:
                i = id_graphs_rot.index(ide)
                d = ide[5:]
                d = ''.join(d)

                marker_items = (
                [html.Li(f"Point ({x}, {y}): {n}") for n, (x, y) in markers[participant][n_t][d]['a'].items()]
                +[html.Li(f"Point ({x}, {y}): {n}") for n, (x, y) in markers[participant][n_t][d]['b'].items()]
                +[html.Li(f"Point ({x}, {y}): {n}") for n, (x, y) in markers[participant][n_t][d]['g'].items()])

                if marker_items:
                    return_divs_rot[i] = html.Ul(marker_items)

                for name_m, point in markers[participant][n_t][d]['a'].items():
                    return_graphs_rot[i].add_trace(
                        go.Scatter(
                        x=[point[0]],
                        y=[point[1]],
                        mode='markers',
                        marker=dict(color='red', size=10),
                        name=name_m,
                        showlegend=False)
                    )

                for name_m, point in markers[participant][n_t][d]['b'].items():
                    return_graphs_rot[i].add_trace(
                        go.Scatter(
                        x=[point[0]],
                        y=[point[1]],
                        mode='markers',
                        marker=dict(color='red', size=10),
                        name=name_m,
                        showlegend=False)
                    )

                for name_m, point in markers[participant][n_t][d]['g'].items():
                    return_graphs_rot[i].add_trace(
                        go.Scatter(
                        x=[point[0]],
                        y=[point[1]],
                        mode='markers',
                        marker=dict(color='red', size=10),
                        name=name_m,
                        showlegend=False)
                    )

            return return_graphs_rot[0], return_graphs_rot[1], return_graphs_rot[2], return_graphs_rot[3], return_divs_rot[0], return_divs_rot[1], return_divs_rot[2], return_divs_rot[3]


        ## Magnetic field management
        @self.app.callback(
            [Output('mag_g1', 'figure'),
            Output('mag_g2', 'figure'),
            Output('mag_g3', 'figure')],
            [Output('marker-list-mag1', 'children'),
            Output('marker-list-mag2', 'children'),
            Output('marker-list-mag3', 'children')],
            [Input('dropdown-participant', 'value'),
            Input('dropdown-test', 'value')],
            [Input('reset-marker-mag1', 'n_clicks'),
            Input('reset-marker-mag2', 'n_clicks'),
            Input('reset-marker-mag3', 'n_clicks')],
            [Input('add-marker-mag1', 'n_clicks'),
            Input('add-marker-mag2', 'n_clicks'),
            Input('add-marker-mag3', 'n_clicks')],
            [State('mag_g1', 'clickData'),
            State('mag_g2', 'clickData'),
            State('mag_g3', 'clickData')],
            [State('marker-name-mag1', 'value'),
            State('marker-name-mag2', 'value'),
            State('marker-name-mag3', 'value')]
        )

        def update_mag(participant, test,*vals):

            if participant is None or test is None :
                return [],[],[],[],[],[]

            return_divs_mag = [html.Div(), html.Div(), html.Div()]

            # Transform the test name into a test number
            if test == 'TUG 1' :
                t = 1
            elif test == 'TUG 2':
                t = 2
            elif test == 'TUG slow 1':
                t = 3
            elif test == 'TUG slow 2':
                t = 4
            elif test == '30CST':
                t=5
            elif test == 'Locomo':
                t=6
            elif test == '10MWT 1':
                t=7
            elif test == '10MWT 2':
                t=8
            elif test == 'partial 6MWT 1':
                t=9
            elif test == 'partial 6MWT 2':
                t=10

            # Call the function to obtain the initial graphics
            return_graphs_mag,id_graphs_mag = plot_mag(participant,t,test)

            n_t=str(t)

            id_bt_reset_mag = ['reset-marker-mag1','reset-marker-mag2','reset-marker-mag3']

            ide = ctx.triggered[0]['prop_id'].split('.')[0]

            # Reset button management
            if ide in id_bt_reset_mag :
                ind =  id_bt_reset_mag.index(ide)
                ide_g = id_graphs_mag[ind]
                device = ide_g[5:]
                device = ''.join(device)
                markers[participant][n_t][device]['x'].clear()
                markers[participant][n_t][device]['y'].clear()
                markers[participant][n_t][device]['z'].clear()

            # Markers management
            else :
                id_bt_add_mag = ['add-marker-mag1','add-marker-mag2','add-marker-mag3']

                if ide in id_bt_add_mag :

                    ind =  id_bt_add_mag.index(ide) #we find out which button he clicked on
                    add_b = vals[ind+3] #retrieve the button corresponding to the graph where it was clicked
                    val = vals[ind+6] #retrieve the graph corresponding to the graph where it was clicked
                    name = vals[ind+9] #name of the marker
                    if add_b is not None and val is not None and name:
                        ide_g = id_graphs_mag[ind]
                        device = ide_g[5:]
                        device = ''.join(device)

                        # Retrieving click details
                        x = val['points'][0]['x']
                        y = val['points'][0]['y']

                        # Retrieving the name of the curve clicked on
                        curve_name = val['points'][0]['curveNumber']

                        # Save the marker in the corresponding dictionary
                        if curve_name==0:
                            markers[participant][n_t][device]['x'][name]=(x,y)
                        if curve_name==1:
                            markers[participant][n_t][device]['y'][name]=(x,y)
                        if curve_name==2:
                            markers[participant][n_t][device]['z'][name]=(x,y)


            # Browse all graphs to update points on graphs and lists of selected points
            for ide in id_graphs_mag:
                i = id_graphs_mag.index(ide)
                d = ide[5:]
                d = ''.join(d)

                marker_items = (
                [html.Li(f"Point ({x}, {y}): {n}") for n, (x, y) in markers[participant][n_t][d]['x'].items()]
                +[html.Li(f"Point ({x}, {y}): {n}") for n, (x, y) in markers[participant][n_t][d]['y'].items()]
                +[html.Li(f"Point ({x}, {y}): {n}") for n, (x, y) in markers[participant][n_t][d]['z'].items()])

                if marker_items:
                    return_divs_mag[i] = html.Ul(marker_items)

                for name_m, point in markers[participant][n_t][d]['x'].items():
                    return_graphs_mag[i].add_trace(
                        go.Scatter(
                        x=[point[0]],
                        y=[point[1]],
                        mode='markers',
                        marker=dict(color='red', size=10),
                        name=name_m,
                        showlegend=False)
                    )

                for name_m, point in markers[participant][n_t][d]['y'].items():
                    return_graphs_mag[i].add_trace(
                        go.Scatter(
                        x=[point[0]],
                        y=[point[1]],
                        mode='markers',
                        marker=dict(color='red', size=10),
                        name=name_m,
                        showlegend=False)
                    )

                for name_m, point in markers[participant][n_t][d]['z'].items():
                    return_graphs_mag[i].add_trace(
                        go.Scatter(
                        x=[point[0]],
                        y=[point[1]],
                        mode='markers',
                        marker=dict(color='red', size=10),
                        name=name_m,
                        showlegend=False)
                    )

            return return_graphs_mag[0], return_graphs_mag[1], return_graphs_mag[2], return_divs_mag[0], return_divs_mag[1], return_divs_mag[2]


        ## PPG management
        @self.app.callback(
            [Output('ppg_g1', 'figure')],
            [Output('marker-list-ppg1', 'children')],
            [Input('dropdown-participant', 'value'),
            Input('dropdown-test', 'value')],
            [Input('reset-marker-ppg1', 'n_clicks')],
            [Input('add-marker-ppg1', 'n_clicks')],
            [State('ppg_g1', 'clickData')],
            [State('marker-name-ppg1', 'value')]
        )

        def update_ppg(participant, test,*vals):

            if participant is None or test is None :
                return [],[]

            return_divs_ppg = [html.Div()]

            # Transform the test name into a test number
            if test == 'TUG 1' :
                t = 1
            elif test == 'TUG 2':
                t = 2
            elif test == 'TUG slow 1':
                t = 3
            elif test == 'TUG slow 2':
                t = 4
            elif test == '30CST':
                t=5
            elif test == 'Locomo':
                t=6
            elif test == '10MWT 1':
                t=7
            elif test == '10MWT 2':
                t=8
            elif test == 'partial 6MWT 1':
                t=9
            elif test == 'partial 6MWT 2':
                t=10

            # Call the function to obtain the initial graphics
            return_graphs_ppg,id_graphs_ppg = plot_ppg(participant,t,test)

            n_t=str(t)

            id_bt_reset_ppg = ['reset-marker-ppg1']

            ide = ctx.triggered[0]['prop_id'].split('.')[0]

            # Reset button management
            if ide in id_bt_reset_ppg :
                ind =  id_bt_reset_ppg.index(ide)
                ide_g = id_graphs_ppg[ind]
                device = ide_g[5:]
                device = ''.join(device)
                markers[participant][n_t][device].clear()

            # Markers management
            else :
                id_bt_add_ppg = ['add-marker-ppg1']

                if ide in id_bt_add_ppg :

                    ind =  id_bt_add_ppg.index(ide) #we find out which button he clicked on
                    add_b = vals[ind+1] #retrieve the button corresponding to the graph where it was clicked
                    val = vals[ind+2] #retrieve the graph corresponding to the graph where it was clicked
                    name = vals[ind+3] #name of the marker
                    if add_b is not None and val is not None and name:
                        ide_g = id_graphs_ppg[ind]
                        device = ide_g[5:]
                        device = ''.join(device)

                        # Retrieving click details
                        x = val['points'][0]['x']
                        y = val['points'][0]['y']

                        # Save the marker in the corresponding dictionary
                        markers[participant][n_t][device][name]=(x,y)



            # Browse all graphs to update points on graphs and lists of selected points
            for ide in id_graphs_ppg:
                i = id_graphs_ppg.index(ide)
                d = ide[5:]
                d = ''.join(d)

                marker_items = (
                [html.Li(f"Point ({x}, {y}): {n}") for n, (x, y) in markers[participant][n_t][d].items()]
                )

                if marker_items:
                    return_divs_ppg[i] = html.Ul(marker_items)

                for name_m, point in markers[participant][n_t][d].items():
                    return_graphs_ppg[i].add_trace(
                        go.Scatter(
                        x=[point[0]],
                        y=[point[1]],
                        mode='markers',
                        marker=dict(color='red', size=10),
                        name=name_m,
                        showlegend=False)
                    )

            return return_graphs_ppg[0], return_divs_ppg[0]


        ## Heart-Rate management
        @self.app.callback(
            [Output('hr_g1', 'figure')],
            [Output('marker-list-hr1', 'children')],
            [Input('dropdown-participant', 'value'),
            Input('dropdown-test', 'value')],
            [Input('reset-marker-hr1', 'n_clicks')],
            [Input('add-marker-hr1', 'n_clicks')],
            [State('hr_g1', 'clickData')],
            [State('marker-name-hr1', 'value')]
        )

        def update_hr(participant, test,*vals):

            if participant is None or test is None :
                return [],[]

            return_divs_hr = [html.Div()]

            # Transform the test name into a test number
            if test == 'TUG 1' :
                t = 1
            elif test == 'TUG 2':
                t = 2
            elif test == 'TUG slow 1':
                t = 3
            elif test == 'TUG slow 2':
                t = 4
            elif test == '30CST':
                t=5
            elif test == 'Locomo':
                t=6
            elif test == '10MWT 1':
                t=7
            elif test == '10MWT 2':
                t=8
            elif test == 'partial 6MWT 1':
                t=9
            elif test == 'partial 6MWT 2':
                t=10

            # Call the function to obtain the initial graphics
            return_graphs_hr,id_graphs_hr = plot_hr(participant,t,test)

            n_t=str(t)

            id_bt_reset_hr = ['reset-marker-hr1']

            ide = ctx.triggered[0]['prop_id'].split('.')[0]

            # Reset button management
            if ide in id_bt_reset_hr :
                ind =  id_bt_reset_hr.index(ide)
                ide_g = id_graphs_hr[ind]
                device = ide_g[5:]
                device = ''.join(device)
                markers[participant][n_t][device].clear()

            # Markers management
            else :
                id_bt_add_hr = ['add-marker-hr1']

                if ide in id_bt_add_hr :

                    ind =  id_bt_add_hr.index(ide) #we find out which button he clicked on
                    add_b = vals[ind+1] #retrieve the button corresponding to the graph where it was clicked
                    val = vals[ind+2] #retrieve the graph corresponding to the graph where it was clicked
                    name = vals[ind+3] #name of the marker
                    if add_b is not None and val is not None and name:
                        ide_g = id_graphs_hr[ind]
                        device = ide_g[5:]
                        device = ''.join(device)

                        # Retrieving click details
                        x = val['points'][0]['x']
                        y = val['points'][0]['y']

                        # Save the marker in the corresponding dictionary
                        markers[participant][n_t][device][name]=(x,y)



            # Browse all graphs to update points on graphs and lists of selected points
            for ide in id_graphs_hr:
                i = id_graphs_hr.index(ide)
                d = ide[5:]
                d = ''.join(d)

                marker_items = (
                [html.Li(f"Point ({x}, {y}): {n}") for n, (x, y) in markers[participant][n_t][d].items()]
                )

                if marker_items:
                    return_divs_hr[i] = html.Ul(marker_items)

                for name_m, point in markers[participant][n_t][d].items():
                    return_graphs_hr[i].add_trace(
                        go.Scatter(
                        x=[point[0]],
                        y=[point[1]],
                        mode='markers',
                        marker=dict(color='red', size=10),
                        name=name_m,
                        showlegend=False)
                    )

            return return_graphs_hr[0], return_divs_hr[0]


        ## Step management
        @self.app.callback(
            [Output('step_g1', 'figure'),
            Output('step_g2', 'figure'),
            Output('step_g3', 'figure'),
            Output('step_g4', 'figure')],
            [Output('marker-list-step1', 'children'),
            Output('marker-list-step2', 'children'),
            Output('marker-list-step3', 'children'),
            Output('marker-list-step4', 'children')],
            [Input('dropdown-participant', 'value'),
            Input('dropdown-test', 'value')],
            [Input('reset-marker-step1', 'n_clicks'),
            Input('reset-marker-step2', 'n_clicks'),
            Input('reset-marker-step3', 'n_clicks'),
            Input('reset-marker-step4', 'n_clicks')],
            [Input('add-marker-step1', 'n_clicks'),
            Input('add-marker-step2', 'n_clicks'),
            Input('add-marker-step3', 'n_clicks'),
            Input('add-marker-step4', 'n_clicks')],
            [State('step_g1', 'clickData'),
            State('step_g2', 'clickData'),
            State('step_g3', 'clickData'),
            State('step_g4', 'clickData')],
            [State('marker-name-step1', 'value'),
            State('marker-name-step2', 'value'),
            State('marker-name-step3', 'value'),
            State('marker-name-step4', 'value')]
        )

        def update_step(participant, test,*vals):

            if participant is None or test is None :
                return [],[],[],[],[],[],[],[]

            return_divs_step = [html.Div(), html.Div(), html.Div(), html.Div()]

            # Transform the test name into a test number
            if test == 'TUG 1' :
                t = 1
            elif test == 'TUG 2':
                t = 2
            elif test == 'TUG slow 1':
                t = 3
            elif test == 'TUG slow 2':
                t = 4
            elif test == '30CST':
                t=5
            elif test == 'Locomo':
                t=6
            elif test == '10MWT 1':
                t=7
            elif test == '10MWT 2':
                t=8
            elif test == 'partial 6MWT 1':
                t=9
            elif test == 'partial 6MWT 2':
                t=10

            # Call the function to obtain the initial graphics
            return_graphs_step,id_graphs_step = plot_step(participant,t,test)

            n_t=str(t)

            id_bt_reset_step = ['reset-marker-step1','reset-marker-step2','reset-marker-step3','reset-marker-step4']

            ide = ctx.triggered[0]['prop_id'].split('.')[0]

            # Reset button management
            if ide in id_bt_reset_step :
                ind =  id_bt_reset_step.index(ide)
                ide_g = id_graphs_step[ind]
                device = ide_g[5:]
                device = ''.join(device)
                markers[participant][n_t][device].clear()

            # Markers management
            else :
                id_bt_add_step = ['add-marker-step1','add-marker-step2','add-marker-step3','add-marker-step4']

                if ide in id_bt_add_step :

                    ind =  id_bt_add_step.index(ide) #we find out which button he clicked on
                    add_b = vals[ind+4] #retrieve the button corresponding to the graph where it was clicked
                    val = vals[ind+8] #retrieve the graph corresponding to the graph where it was clicked
                    name = vals[ind+12] #name of the marker
                    if add_b is not None and val is not None and name:
                        ide_g = id_graphs_step[ind]
                        device = ide_g[5:]
                        device = ''.join(device)

                        # Retrieving click details
                        x = val['points'][0]['x']
                        y = val['points'][0]['y']

                        # Save the marker in the corresponding dictionary
                        markers[participant][n_t][device][name]=(x,y)

            # Browse all graphs to update points on graphs and lists of selected points
            for ide in id_graphs_step:
                i = id_graphs_step.index(ide)
                d = ide[5:]
                d = ''.join(d)

                marker_items = (
                [html.Li(f"Point ({x}, {y}): {n}") for n, (x, y) in markers[participant][n_t][d].items()]
                )

                if marker_items:
                    return_divs_step[i] = html.Ul(marker_items)

                for name_m, point in markers[participant][n_t][d].items():
                    return_graphs_step[i].add_trace(
                        go.Scatter(
                        x=[point[0]],
                        y=[point[1]],
                        mode='markers',
                        marker=dict(color='red', size=10),
                        name=name_m,
                        showlegend=False)
                    )

            return return_graphs_step[0], return_graphs_step[1], return_graphs_step[2], return_graphs_step[3], return_divs_step[0], return_divs_step[1], return_divs_step[2], return_divs_step[3]


        ## Management Mats
        @self.app.callback(
            Output('mats-graph-container', 'children'),
            Output('slider-seat','step'),
            Output('slider-floor','step'),
            Output('slider-seat', 'data'),
            Output('slider-floor','data'),
            Output('slider-seat', 'max'),
            Output('slider-floor','max'),
            [Input('clear-button-mats','n_clicks'),
             Input ('next-button', 'n_clicks'),
            Input('slider-seat', 'value'),
            Input('slider-floor','value')],
            [State('dropdown-participant', 'value'),
             State('dropdown-test', 'value'),
             State('clicks-store-seat', 'data'),
             State('clicks-store-floor', 'data')]
        )
        def update_mats_graphs(clear_clicks,n_clicks, slider_seat,slider_floor, participant, test,click_seat,click_floor):
            if 'clear-button-mats'==ctx.triggered_id :
                return [dcc.Markdown('Choose a participant and a test.')],1,1,0,0,100,100
            if  n_clicks==0 or participant is None or test is None:
                return [dcc.Markdown('Choose a participant and a test.')],1,1,0,0,100,100
            else :
                    if test == 'TUG 1' :
                        num_test= 1
                    elif test == 'TUG 2':
                        num_test = 2
                    elif test == 'TUG slow 1':
                        num_test = 3
                    elif test == 'TUG slow 2':
                        num_test = 4
                    elif test == '30CST':
                        num_test=5
                    elif test == 'Locomo':
                        num_test=6
                    elif test == '10MWT 1':
                        num_test=7
                    elif test == '10MWT 2':
                        num_test=8
                    elif test == 'partial 6MWT 1':
                        num_test=9
                    elif test == 'partial 6MWT 2':
                        num_test=10
                    fig=[]
                    time = ts[ts['Participant']==participant]
                    time.reset_index(drop=True, inplace=True)
                    time = time[time['Test Number']==int(num_test)]
                    time.reset_index(drop=True, inplace=True)
                    start = time['Start timestamp'][0]
                    if (num_test==7 or num_test==8 or num_test==9 or num_test==10):
                        file_path_mat1=f'Results/{participant}/{num_test}/{participant}_mats_Floor1_{num_test}.csv'
                        file_path_mat2=f'Results/{participant}/{num_test}/{participant}_mats_Floor2_{num_test}.csv'
                        floor1=pd.read_csv(file_path_mat1)
                        floor2=pd.read_csv(file_path_mat2)
                        floor1['timestamp']=floor1['timestamp']-start
                        floor2['timestamp']=floor2['timestamp']-start
                        mat1=[]
                        mat2=[]
                        for index, ligne in floor1.iterrows():
                            matrices=floor1.iloc[index,1:].to_numpy().reshape((28, 80))
                            mat1.append(matrices)
                        for index, ligne in floor2.iterrows():
                            matrices=floor2.iloc[index,1:].to_numpy().reshape((28, 80))
                            mat2.append(matrices)
                        index_floor1=round(slider_floor/((max(floor1['timestamp'].max(),floor2['timestamp'].max())-min(floor1['timestamp'].min(),floor2['timestamp'].min()))/min(len(mat1)-1,len(mat2)-1)))
                        index_floor2=round(slider_floor/((max(floor1['timestamp'].max(),floor2['timestamp'].max())-min(floor1['timestamp'].min(),floor2['timestamp'].min()))/min(len(mat1)-1,len(mat2)-1)))
                        heatmap_floor1 = go.Heatmap(z=mat1[index_floor1])
                        fig1 = go.Figure(data=[heatmap_floor1])
                        fig1.update_layout(
                        title=f"Heatmap floor 1, time: {floor1.loc[index_floor1, 'timestamp']} sec",
                            width= 1200,
                            height= 300
                        )
                        fig.append(fig1)
                        fig3_data=0
                        fig3_layout=0
                        heatmap_floor2 = go.Heatmap(z=mat2[index_floor2])
                        fig2 = go.Figure(data=[heatmap_floor2])
                        fig2.update_layout(
                        title=f"Heatmap floor 2, time: {floor2.loc[index_floor2, 'timestamp']} sec",
                            width= 1200,
                            height= 300
                        )
                        fig.append(fig2)
                    else:
                        if (num_test==6 and (participant=="LC" or participant=="PB" or participant=="RC")):
                            return [dcc.Markdown('No Locomo test.')],1,1,0,0,100,100
                        elif (participant!="DS" and participant!="DL"):
                            file_path_mat1=f'Results/{participant}/{num_test}/{participant}_mats_Floor1_{num_test}.csv'
                            file_path_mat2=f'Results/{participant}/{num_test}/{participant}_mats_Floor2_{num_test}.csv'
                            file_path_seat=f'Results/{participant}/{num_test}/{participant}_mats_Seat_{num_test}.csv'
                            floor1=pd.read_csv(file_path_mat1)
                            floor2=pd.read_csv(file_path_mat2)
                            seats=pd.read_csv(file_path_seat)
                            floor1['timestamp']=floor1['timestamp']-start
                            floor2['timestamp']=floor2['timestamp']-start
                            seats['timestamp']=seats['timestamp']-start
                            mat1=[]
                            mat2=[]
                            seat=[]
                            for index, ligne in floor1.iterrows():
                                matrices=floor1.iloc[index,1:].to_numpy().reshape((28, 80))
                                mat1.append(matrices)
                            for index, ligne in floor2.iterrows():
                                matrices=floor2.iloc[index,1:].to_numpy().reshape((28, 80))
                                mat2.append(matrices)
                            for index, ligne in seats.iterrows():
                                matrices=seats.iloc[index,1:].to_numpy().reshape((20, 20))
                                seat.append(matrices)
                            index_floor1=round(slider_floor/((max(floor1['timestamp'].max(),floor2['timestamp'].max())-min(floor1['timestamp'].min(),floor2['timestamp'].min()))/min(len(mat1)-1,len(mat2)-1)))
                            index_floor2=round(slider_floor/((max(floor1['timestamp'].max(),floor2['timestamp'].max())-min(floor1['timestamp'].min(),floor2['timestamp'].min()))/min(len(mat1)-1,len(mat2)-1)))
                            index_seat=round(slider_seat/((seats['timestamp'].max()-seats['timestamp'].min())/(len(seat)-1)))
                            heatmap_seat=go.Heatmap(z=seat[index_seat])
                            fig3=go.Figure(data=[heatmap_seat])
                            fig3.update_layout(
                            title=f"Heatmap seat, time: {seats.loc[index_seat, 'timestamp']} sec",
                                width= 500,
                                height= 500
                            )
                            fig.append(fig3)
                            fig3_data=fig3.data
                            fig3_layout=fig3.layout
                            heatmap_floor1 = go.Heatmap(z=mat1[index_floor1])
                            fig1 = go.Figure(data=[heatmap_floor1])
                            fig1.update_layout(
                            title=f"Heatmap floor 1, time: {floor1.loc[index_floor1, 'timestamp']} sec",
                                width= 1200,
                                height= 300
                            )
                            fig.append(fig1)
                            heatmap_floor2 = go.Heatmap(z=mat2[index_floor2])
                            fig2 = go.Figure(data=[heatmap_floor2])
                            fig2.update_layout(
                            title=f"Heatmap floor 2, time: {floor2.loc[index_floor2, 'timestamp']} sec",
                                width= 1200,
                                height= 300
                            )
                            fig.append(fig2)

                        else:
                            if (num_test==1 or num_test==2 or num_test==3 or num_test==4):
                                file_path_mat1=f'Results/{participant}/{num_test}/{participant}_mats_Floor1_{num_test}.csv'
                                file_path_mat2=f'Results/{participant}/{num_test}/{participant}_mats_Floor2_{num_test}.csv'
                                file_path_seat=f'Results/{participant}/{num_test}/{participant}_mats_Seat_{num_test}.csv'
                                floor1=pd.read_csv(file_path_mat1)
                                floor2=pd.read_csv(file_path_mat2)
                                seats=pd.read_csv(file_path_seat)
                                floor1['timestamp']=floor1['timestamp']-start
                                floor2['timestamp']=floor2['timestamp']-start
                                seats['timestamp']=seats['timestamp']-start
                                mat1=[]
                                mat2=[]
                                seat=[]
                                for index, ligne in floor1.iterrows():
                                    matrices=floor1.iloc[index,1:].to_numpy().reshape((28, 80))
                                    mat1.append(matrices)
                                for index, ligne in floor2.iterrows():
                                    matrices=floor2.iloc[index,1:].to_numpy().reshape((28, 80))
                                    mat2.append(matrices)
                                for index, ligne in seats.iterrows():
                                    matrices=seats.iloc[index,1:].to_numpy().reshape((20, 20))
                                    seat.append(matrices)
                                index_floor1=round(slider_floor/((max(floor1['timestamp'].max(),floor2['timestamp'].max())-min(floor1['timestamp'].min(),floor2['timestamp'].min()))/min(len(mat1)-1,len(mat2)-1)))
                                index_seat=round(slider_seat/((seats['timestamp'].max()-seats['timestamp'].min())/(len(seat)-1)))
                                index_floor2=round(slider_floor/((max(floor1['timestamp'].max(),floor2['timestamp'].max())-min(floor1['timestamp'].min(),floor2['timestamp'].min()))/min(len(mat1)-1,len(mat2)-1)))
                                heatmap_seat=go.Heatmap(z=seat[index_seat])
                                fig3=go.Figure(data=[heatmap_seat])
                                fig3.update_layout(
                                title=f"Heatmap seat, time: {seats.loc[index_seat, 'timestamp']} sec",
                                    width= 500,
                                    height= 500
                                )
                                fig.append(fig3)
                                fig3_data=fig3.data
                                fig3_layout=fig3.layout
                                heatmap_floor1 = go.Heatmap(z=mat1[index_floor1])
                                fig1 = go.Figure(data=[heatmap_floor1])
                                fig1.update_layout(
                                title=f"Heatmap floor 1, time: {floor1.loc[index_floor1, 'timestamp']} sec ",
                                    width= 1200,
                                    height= 300
                                )
                                fig.append(fig1)
                                heatmap_floor2 = go.Heatmap(z=mat2[index_floor2])
                                fig2 = go.Figure(data=[heatmap_floor2])
                                fig2.update_layout(
                                title=f"Heatmap floor 2, time: {floor2.loc[index_floor2, 'timestamp']} sec",
                                    width= 1200,
                                    height= 300
                                )
                                fig.append(fig2)

                            else:
                                file_path_mat1=f'Results/{participant}/{num_test}/{participant}_mats_Floor1_{num_test}.csv'
                                file_path_seat=f'Results/{participant}/{num_test}/{participant}_mats_Seat_{num_test}.csv'
                                floor1=pd.read_csv(file_path_mat1)
                                seats=pd.read_csv(file_path_seat)
                                floor1['timestamp']=floor1['timestamp']-start
                                seats['timestamp']=seats['timestamp']-start
                                mat1=[]
                                seat=[]
                                for index, ligne in floor1.iterrows():
                                    matrices=floor1.iloc[index,1:].to_numpy().reshape((28, 80))
                                    mat1.append(matrices)
                                for index, ligne in seats.iterrows():
                                    matrices=seats.iloc[index,1:].to_numpy().reshape((20, 20))
                                    seat.append(matrices)
                                index_floor1=round(slider_floor/((floor1['timestamp'].max()-floor1['timestamp'].min())/(len(mat1)-1)))
                                index_seat=round(slider_seat/((seats['timestamp'].max()-seats['timestamp'].min())/(len(seat)-1)))
                                heatmap_seat=go.Heatmap(z=seat[index_seat])
                                fig3=go.Figure(data=[heatmap_seat])
                                fig3.update_layout(
                                title=f"Heatmap seat, time: {seats.loc[index_seat, 'timestamp'] } sec",
                                    width= 500,
                                    height= 500
                                )
                                fig.append(fig3)
                                fig3_data=fig3.data
                                fig3_layout=fig3.layout
                                heatmap_floor1 = go.Heatmap(z=mat1[index_floor1])
                                fig1 = go.Figure(data=[heatmap_floor1])
                                fig1.update_layout(
                                title=f"Heatmap floor 1, time: {floor1.loc[index_floor1, 'timestamp']} sec",
                                    width= 1200,
                                    height= 300
                                )
                                fig.append(fig1)
                    # Return updated figures and indices
                    if len(fig)==3:
                        return  [html.Div([
                            dcc.Graph(id='heatmap-graph-1', figure=fig[0]),
                            dcc.Graph(id='heatmap-graph-2', figure=fig[1]),
                            dcc.Graph(id='heatmap-graph-3', figure=fig[2])
                        ])],(seats['timestamp'].max()-seats['timestamp'].min())/len(seat),(max(floor1['timestamp'].max(),floor2['timestamp'].max())-min(floor1['timestamp'].min(),floor2['timestamp'].min()))/max(len(mat1),len(mat2)),click_seat,click_floor,seats['timestamp'].max()-seats['timestamp'].min(),max(floor1['timestamp'].max(),floor2['timestamp'].max())-min(floor1['timestamp'].min(),floor2['timestamp'].min())
                    else :
                        if any(fig.data == fig3_data and fig.layout == fig3_layout for fig in fig):
                            return  [html.Div([
                                dcc.Graph(id='heatmap-graph-1', figure=fig[0]),
                                dcc.Graph(id='heatmap-graph-2', figure=fig[1])
                            ])],(seats['timestamp'].max()-seats['timestamp'].min())/(len(seat)-1),(floor1['timestamp'].max()-floor1['timestamp'].min())/(len(mat1)-1),click_seat,click_floor,seats['timestamp'].max()-seats['timestamp'].min(),floor1['timestamp'].max()-floor1['timestamp'].min()
                        else:
                            return  [html.Div([
                                dcc.Graph(id='heatmap-graph-1', figure=fig[0]),
                                dcc.Graph(id='heatmap-graph-2', figure=fig[1])
                            ])],1,(max(floor1['timestamp'].max(),floor2['timestamp'].max())-min(floor1['timestamp'].min(),floor2['timestamp'].min()))/max(len(mat1)-1,len(mat2)-1),0,click_floor,20,max(floor1['timestamp'].max(),floor2['timestamp'].max())-min(floor1['timestamp'].min(),floor2['timestamp'].min())

        ## Additional tab management to display the dictionary
        @self.app.callback(
            Output("modal", "is_open"),
            Output("modal-body", "children"),
            [Input("show-markers-btn", "n_clicks"), Input("close", "n_clicks")],
            [State("modal", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                if not is_open:
                    markers_list = html.Pre(json.dumps(markers,indent=1))
                    return not is_open, markers_list
                return not is_open, []
            return is_open, []


    def run(self):
        self.app.run_server(debug=False,port=8074)



class App:
    def __init__(self, root):
        self.root = root
        self.data_list = {"ETHUSDT": [], "BTCUSD": [], "BNBUSDT": []}

        # Start the Dash application in a separate thread
        dash_thread = DashThread(self.data_list)
        dash_thread.start()

        # Open Dash app in web browser
        webbrowser.open("http://localhost:8074")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)