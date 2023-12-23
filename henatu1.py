import PySimpleGUI as sg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import make_interp_spline,make_smoothing_spline
from sklearn.linear_model import LinearRegression
import matplotlib
import japanize_matplotlib
import matplotlib.ticker as ticker
matplotlib.use('TkAgg')

# 描画用の関数
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

layout = [
    [sg.Text("Viewer")],
    [sg.Frame('data', [[sg.Button('save')]]), sg.Canvas(key='-CANVAS-'),]
]

window = sg.Window("multiaxial_graph_application",layout,finalize=True,font='Monospace 18',resizable=True)

# 埋め込むfigを作成
#plt.rcParams['font.family'] = 'Times New Roman'
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot()
#plt.tick_params(labelsize=14)
#plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
plt.grid()


xdata = [
    0,
    25,
    50,
    75,
    100,
    125
]
ydata = [ #電流
    0.00,
    0.057,
    0.092, 
    0.15,
    0.30, 
    0.66 
]

y2data = [
    0.00, 
    0.910, 
    3.16, 
    6.56, 
    11.0, 
    17.2
]

xdata_s = np.linspace(0,125,500)

#近似用の係数
res = np.polyfit(xdata,ydata,2)
res2 = np.polyfit(xdata,y2data,2)

#to do polyfitの場合、xdataの広がり方によっては近似の精度が格段に落ちる

#近似式の計算
y1 = np.poly1d(res)(xdata)
y2 = np.poly1d(res2)(xdata)

spl_1 = make_smoothing_spline(xdata,ydata,lam=3500)
spl_2 = make_smoothing_spline(xdata,y2data,lam=500)

#欠損データはNoneでOK

# y2data = [
#     None, 
#     0.910, 
#     None, 
#     6.56, 
#     11.0, 
#     17.2
# ]

#x_axis = np.arange(10.2, 11.3, 0.2)
#y_axis = np.arange(3.5, 7.3, 0.5)
#print(x_axis)
#print(y_axis)

#plt.xticks(x_axis)
#plt.yticks(y_axis)
        
#ax.plot(xdata , ydata, marker='.', alpha=0.8)
ax.scatter(xdata,ydata,marker=',',s=31,alpha=1,label='入力電流$I_{1}$')
ax.plot(xdata_s,spl_1(xdata_s),linestyle='dashed',alpha=0.6)
ax2 = ax.twinx()
ax2.scatter(xdata,y2data,marker='o',s=30,alpha=1,color='tab:orange',label='入力電力$W_{1}$')
#ax2.plot(xdata,y2data,marker='.',color='tab:orange')
#ax2.plot(xdata,y2,linestyle='dashed',alpha=0.6,color='tab:orange')
ax2.plot(xdata_s,spl_2(xdata_s),linestyle='dashed',alpha=0.6,color='tab:orange')

ax.set_xlabel('入力電圧V [V]',fontsize=16)
#ax.set_ylabel('電流I [A]',fontsize=16)
ax.set_ylabel('入力電流$I_{1}$ [A]',fontsize=16)
ax2.set_ylabel('入力電力$W_{1}$ [W]',fontsize=16)

ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f')) #軸目盛小数点以下表示設定
ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

ax.set_ylim(-0.01,0.7)
ax.set_xlim(-1,140.0)
ax2.set_ylim(-0.01,18.0)

ax.tick_params(labelsize=14) #軸メモリフォントサイズ設定
ax2.tick_params(labelsize=14)

h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2,fontsize=14)

#ax.legend(fontsize=14)
#ax2.legend(fontsize=14)
        
# fig-agg作成
fig_agg = draw_figure(window["-CANVAS-"].TKCanvas, fig)
fig_agg.draw()

while True:
    event,values = window.read()
    
    if event == sg.WIN_CLOSED:
        break
    
    elif event == 'save':
        fig_agg.draw()
        plt.pause(0.01)
    
window.close()