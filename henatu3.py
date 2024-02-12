import PySimpleGUI as sg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import make_interp_spline
from scipy.interpolate import make_smoothing_spline
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

xdata = [ #二次電流
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
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100,
    100
]

ydata2 = [ #二次電圧
    104,
    104,
    104,
    103,
    103,
    102,
    102,
    101,
    101,
    101
]

ydata3 = [ #一次電流
    0.683,
    1.18,
    1.70,
    2.22,
    2.73,
    3.26,
    3.78,
    4.27,
    4.77,
    5.33 
]

ydata4 = [ #入力電力
    62.6,
    115,
    170,
    222,
    273,
    326,
    379,
    429,
    481,
    536
]

ydata5 = [ #出力電力
    51.3,
    104,
    158,
    208,
    258,
    308,
    360,
    403,
    453,
    506
]

ydata6 = [ #効率
    81.9, 
    90.4, 
    92.9, 
    93.7, 
    94.5, 
    94.5, 
    95.0, 
    93.9, 
    94.2, 
    94.4 
]

ydata7 = [ #力率
    91.7, 
    97.5, 
    100, 
    100, 
    100, 
    100, 
    100, 
    100, 
    100, 
    100 
]

#近似式の係数
res1 = np.polyfit(xdata,ydata,1)
res2 = np.polyfit(xdata,ydata2,1)
res3 = np.polyfit(xdata,ydata3,1)
res4 = np.polyfit(xdata,ydata4,1)
res5 = np.polyfit(xdata,ydata5,1)

#近似式の計算
y1 = np.poly1d(res1)(xdata)
y2 = np.poly1d(res2)(xdata)
y3 = np.poly1d(res3)(xdata)
y4 = np.poly1d(res4)(xdata)
y5 = np.poly1d(res5)(xdata)

spl_6 = make_smoothing_spline(xdata,ydata6,lam=0.065)
spl_7 = make_smoothing_spline(xdata,ydata7,lam=0.065)
# xdata_s = np.linspace(0.5,5.0,50)
# print('----------------------------------------------')
# print(spl_6(xdata))
# print('-----------------------------------------------')

p1 = ax.scatter(xdata,ydata,marker=',',s=31,alpha=1,label='一次電圧$V_{1}$')
#ax.plot(xdata,ydata,alpha=1)
ax.plot(xdata,y1,alpha=0.6,linestyle='dashed')
p2 = ax.scatter(xdata,ydata2,marker='o',s=30,alpha=1,color='tab:purple',label='二次電圧$V_{2}$')
#ax.plot(xdata,ydata2,alpha=1,color='tab:purple')
ax.plot(xdata,y2,alpha=0.6,color='tab:purple',linestyle='dashed')
ax2 = ax.twinx()
p3 = ax2.scatter(xdata,ydata3,marker='o',s=30,alpha=0.8,color='tab:green',label='一次電流$I_{1}$')
#ax2.plot(xdata,ydata3,alpha=1,color='tab:green')
ax2.plot(xdata,y3,alpha=0.6,color='tab:green',linestyle='dashed')
ax3 = ax.twinx()
ax3.spines['right'].set_position(('axes',1.15))
p4 = ax3.scatter(xdata,ydata4,marker='o',s=30,alpha=1,color='tab:orange',label='入力電力$W_{1}$')
#ax3.plot(xdata,ydata4,alpha=1,color='tab:orange')
ax3.plot(xdata,y4,alpha=0.6,color='tab:orange',linestyle='dashed')
p5 = ax3.scatter(xdata,ydata5,marker='o',s=30,alpha=1,color='tab:red',label='出力電力$W_{2}$')
#ax3.plot(xdata,ydata5,alpha=1,color='tab:red')
ax3.plot(xdata,y5,alpha=0.6,color='tab:red',linestyle='dashed')
ax4 = ax.twinx()
ax4.spines['right'].set_position(('axes',1.3))
p6 = ax4.scatter(xdata,ydata6,marker='o',s=30,alpha=1,color='tab:pink',label='効率η')
#ax4.plot(xdata,ydata6,alpha=1,color='tab:pink')
ax4.plot(xdata,spl_6(xdata),alpha=0.6,color='tab:pink',linestyle='dashed')
p7 = ax4.scatter(xdata,ydata7,marker='o',s=30,alpha=1,color='tab:cyan',label='力率pf')
#ax4.plot(xdata,ydata7,alpha=1,color='tab:cyan')
ax4.plot(xdata,spl_7(xdata),alpha=0.6,color='tab:cyan',linestyle='dashed')

ax.set_xlabel('二次電流$I_{2}$ [A]',fontsize=16)
ax.set_ylabel('一次電圧$V_{1}$, 二次電圧$V_{2}$ [V]',fontsize=16)
ax2.set_ylabel('一次電流$I_{1}$ [A]',fontsize=16)
ax3.set_ylabel('入力電力$W_{1}$, 出力電力$W_{2}$ [W]',fontsize=16)
ax4.set_ylabel('効率η, 力率pf [%]',fontsize=16)

ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f')) #軸目盛小数点以下表示設定
ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
ax3.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
ax4.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))

ax.set_ylim(-0.01,120.0)
ax.set_xlim(-0.01,5.1)
ax2.set_ylim(-0.01,6.0)
ax3.set_ylim(-0.01,1000)
ax4.set_ylim(-0.01,140)

ax.tick_params(labelsize=14) #軸メモリフォントサイズ設定
ax2.tick_params(labelsize=14)
ax3.tick_params(labelsize=14)
ax4.tick_params(labelsize=14)

ax.legend(handles=[p1,p2,p3,p4,p5,p6,p7],loc='lower right',fontsize=14)

plt.show()
