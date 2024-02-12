import PySimpleGUI as sg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import make_interp_spline
from sklearn.linear_model import LinearRegression
import matplotlib
import japanize_matplotlib
matplotlib.use('TkAgg')

# 描画用の関数
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def make_main():
    # ------------ メインウィンドウ作成 ------------
    main_layout = [
        [sg.Text("multiaxial_graph_application")],
        [sg.Frame('data', [
            [sg.Button('draw')],
            [sg.Text("x:"), sg.Button('setting_x')],
            [sg.Text("y:"), sg.Button('setting_y')],
            [sg.Text("y2:"), sg.Button('setting_y2')]
            ]), sg.Canvas(key='-CANVAS-'),],
        [sg.Button('Exit')]
    ]
    return sg.Window("multiaxial_graph_application",main_layout,finalize=True,font='Monospace 18',resizable=True)

def import_main_data():
    # ------------ サブウィンドウ(x)作成 ------------
    flame_import = sg.Frame('import', [
        [sg.Multiline(key='-Data-',size=(15,20)),sg.Button('import')]
    ])
    
    flame_settings = sg.Frame('settings', [
        [sg.Text('data label :'),sg.InputText(key='-LABEL-',size=(15,5),enable_events=True)]
    ], vertical_alignment='top')
    
    data_layout = [
        [flame_import, flame_settings],
        [sg.Button('close')]
    ]
    
    data_window = sg.Window('import xdata', data_layout, finalize=True,font='Monospace 18')
    res = []
    result = []
    data_label = ''
    
    while True:
        event, values = data_window.read()
        
        data_label = values['-LABEL-']
        
        if event == 'close' or event  == sg.WIN_CLOSED:
            try:
                break
            except Exception as e:
                sg.popup(e)
                continue
        
        if event == 'import':
            res = values['-Data-']
            result = res.replace("\n", ",")
            print(type(result))
            sg.popup(data_label)
            
    data_window.close()
    return result

def import_sub_data():
    # ------------ サブウィンドウ(y)作成 ------------
    flame_import = sg.Frame('import', [
        [sg.Multiline(key='-Data-',size=(15,20)),sg.Button('import')]
    ])
    
    radio_main = sg.Radio(text='main',group_id='axis',default=True,key='-MAIN-',enable_events=True)
    radio_second = sg.Radio(text='second',group_id='axis',default=False,key='-SECOND-',enable_events=True)
    
    def judge_axis(values): 
        selected_axis = 1   #デフォルトは主軸
        
        if values['-MAIN-']:
            selected_axis = 1
        elif values['-SECOND-']:
            selected_axis = 2
        
        return selected_axis
    
    flame_settings = sg.Frame('settings', [
        [sg.Text('data label :'),sg.InputText(key='-LABEL-',size=(15,5),enable_events=True)],
        [sg.Text('Axis to be used:')],
        [radio_main,radio_second]
    ], vertical_alignment='top')
    
    data_layout = [
        [flame_import, flame_settings],
        [sg.Button('close')]
    ]
    
    data_window = sg.Window('import data', data_layout, finalize=True,font='Monospace 18',disable_close=True)
    res = []
    result = []
    used_axis = 0 
    data_label = ''
    
    while True:
        event, values = data_window.read()
        
        data_label = values['-LABEL-']
        
        used_axis = judge_axis(values)
        
        if event == 'close' or event  == sg.WIN_CLOSED:
            try:
                break
            except Exception as e:
                sg.popup(e)
                continue
            
        
        if event == 'import':
            res = values['-Data-']
            result = res.replace("\n", ",")
            print(type(result))
            
            sg.popup(used_axis)
            sg.popup(data_label) 
            
    data_window.close()
    return result,used_axis

window = make_main()

# 埋め込むfigを作成
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
#ax2 = ax.twinx()
#ax3 = ax.twinx()
plt.grid()
plt.xlabel("x")
plt.ylabel("y")

xdata = []
ydata = []
ydata2 = []

#x_axis = np.arange(10.2, 11.3, 0.2)
#y_axis = np.arange(3.5, 7.3, 0.5)
#print(x_axis)
#print(y_axis)

#plt.xticks(x_axis)
#plt.yticks(y_axis)
        
ax.plot(xdata , ydata, marker='.', alpha=0.8)
        
# fig-agg作成
fig_agg = draw_figure(window["-CANVAS-"].TKCanvas, fig)
fig_agg.draw()

while True:
    event,values = window.read()
    
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    elif event == 'setting_x':
        xdata = import_main_data()
        print(xdata)
        try:
            imported_x = [float(x) for x in xdata.split(',')]
        except:
            continue
        
    elif event == 'setting_y':
        ydata = import_main_data()
        print(ydata)
        try:
            imported_y = [float(y) for y in ydata.split(',')]
        except:
            continue
        
    elif event == 'setting_y2':
        tmp_y2 = import_sub_data()
        ydata2 = tmp_y2[0]
        try:
            imported_y2 = [float(y2) for y2 in ydata2.split(',')]
        except:
            continue
        
    elif event == 'draw':
        try:
            print('---------------------------------------------------------------------------')
            type(imported_x)
            print(imported_x)
            print('---------------------------------------------------------------------------')
            type(imported_y)
            print(imported_y)
            print('----------------------------------------------------------------------------')
            print(imported_y2)
            print('-------------------------------------------------------------------------')
            print(tmp_y2[1])
            print('//////////////////////////////////////////////////////////////////////////////////')
            plt.cla()
            
            
            ax.plot(imported_x, imported_y, marker='o', alpha=0.8)
            
            if tmp_y2[1] == 1:
                ax.plot(imported_x, imported_y2, marker='o', alpha=0.8, color='tab:red')
                ax2.axis('off')
            elif tmp_y2[1] == 2:
                ax2 = ax.twinx()
                ax2.plot(imported_x, imported_y2, marker='o', alpha=0.8, color='tab:red')
            
            #ax.plot(imported_x, imported_y2, marker='o', alpha=0.8, color='tab:red')
            fig_agg.draw()
            #plt.pause(0.01)
        except Exception as e:
            print(e)
            sg.popup(e)
            continue
    
window.close()
