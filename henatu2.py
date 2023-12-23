import PySimpleGUI as sg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import make_interp_spline
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
fig = plt.figure(figsize=(13,8))
fig.tight_layout()
ax = fig.add_subplot()
plt.grid()

xdata = [ #一次電流
    0,
    0.5, 
    1.0, 
    1.5, 
    2.0, 
    2.5, 
    3.0, 
    3.5, 
    4.0, 
    4.5, 
    5.0 
]

xdata_neo = [ #一次電流(欠損データ対応用)
    0.5, 
    1.0, 
    1.5, 
    2.0, 
    2.5, 
    3.0, 
    3.5, 
    4.0, 
    4.5, 
    5.0 
]

ydata = [ #一次電圧
    0.00, 
    0.376, 
    0.758, 
    1.13, 
    1.51, 
    1.88, 
    2.28, 
    2.66, 
    3.03, 
    3.40, 
    3.75 
]

ydata2 = [ #入力電力
    0.00, 
    0.183, 
    0.744, 
    1.66, 
    3.12, 
    4.50, 
    6.67, 
    9.11, 
    11.8, 
    15.0, 
    18.4 
]

ydata3 = [ #インピーダンス
    None,
    0.752, 
    0.758, 
    0.753, 
    0.755, 
    0.752, 
    0.760, 
    0.760, 
    0.758, 
    0.756, 
    0.750 
]

ydata3_neo = [ #インピーダンス(欠損データ除去)
    0.752, 
    0.758, 
    0.753, 
    0.755, 
    0.752, 
    0.760, 
    0.760, 
    0.758, 
    0.756, 
    0.750 
]

ydata4 = [ #銅損
    0.00, 
    0.128, 
    0.520, 
    1.09, 
    2.24, 
    3.19, 
    4.62, 
    6.36, 
    8.32, 
    11.0, 
    13.1 
]

#近似用の係数
res = np.polyfit(xdata,ydata,1)
res2 = np.polyfit(xdata,ydata2,2)
res3 = np.polyfit(xdata_neo,ydata3_neo,1)
res4 = np.polyfit(xdata,ydata4,2)

#近似式の計算
y1 = np.poly1d(res)(xdata)
y2 = np.poly1d(res2)(xdata)
y3 = np.poly1d(res3)(xdata_neo)
y4 = np.poly1d(res4)(xdata)

p1 = ax.scatter(xdata,ydata,marker=',',s=31,alpha=1,label='一次電圧$V_{1}$')
#ax.plot(xdata,ydata,alpha=0.6,linestyle='dashed')
ax.plot(xdata,y1,alpha=0.6,linestyle='dashed')
ax2 = ax.twinx()
p2 = ax2.scatter(xdata,ydata2,marker='o',s=30,alpha=0.8,color='tab:green',label='入力電力$W_{1}$')
#ax2.plot(xdata,ydata2,alpha=0.6,linestyle='dashed',color='tab:green')
ax2.plot(xdata,y2,alpha=0.6,linestyle='dashed',color='tab:green')
ax3 = ax.twinx()
ax3.spines['right'].set_position(('axes',1.15))
p3 = ax3.scatter(xdata,ydata3,marker='o',s=30,alpha=1,color='tab:orange',label='インピーダンスZ')
#ax3.plot(xdata,ydata3,alpha=0.6,linestyle='dashed',color='tab:orange')
ax3.plot(xdata_neo,y3,alpha=0.6,linestyle='dashed',color='tab:orange')
p4 = ax2.scatter(xdata,ydata4,marker='o',s=30,alpha=1,color='tab:red',label='銅損$W_{c}$')
#ax2.plot(xdata,ydata4,alpha=0.6,linestyle='dashed',color='tab:red')
ax2.plot(xdata,y4,alpha=0.6,linestyle='dashed',color='tab:red')

ax.set_xlabel('一次電流$I_{1}$ [A]',fontsize=16)
ax.set_ylabel('一次電圧$V_{1}$ [V]',fontsize=16)
ax2.set_ylabel('入力電力$W_{1}$, 銅損$W_{c}$ [W]',fontsize=16)
ax3.set_ylabel('インピーダンスZ [Ω]',fontsize=16)

ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f')) #軸目盛小数点以下表示設定
ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
ax3.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

ax.set_ylim(-0.01,5.0)
ax.set_xlim(-0.01,5.1)
ax2.set_ylim(-0.01,20.0)
ax3.set_ylim(-0.01,1.0)

ax.tick_params(labelsize=14) #軸メモリフォントサイズ設定
ax2.tick_params(labelsize=14)
ax3.tick_params(labelsize=14)

ax.legend(handles=[p1,p2,p3,p4],loc='lower right',fontsize=14)

plt.show()
# fig_agg = draw_figure(window["-CANVAS-"].TKCanvas, fig)
# fig_agg.draw()

# while True:
#     event,values = window.read()
    
#     if event == sg.WIN_CLOSED:
#         break
    
#     elif event == 'save':
#         fig_agg.draw()
#         #plt.show()
#         plt.pause(0.01)
    
# window.close()
