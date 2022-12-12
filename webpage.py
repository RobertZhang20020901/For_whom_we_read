import os

import plotly.express as px
import plotly.io as pio
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
df0 = pd.read_csv('data/opt/summary_follow_modi_3_1.csv').astype({"ratio":float})
df0.sort_values('ratio', inplace=True)
df0 = df0[-80:]
df0["ratio"] = df0["ratio"].map(lambda x: x ** 0.4)


fig_dict = fig = px.scatter(df0, x='follower', y='ratio',size='Frequency', color='class',hover_name="Name", log_x=True,log_y= True, size_max=60,title='《朗读者》活跃用户群体关注UP主粉丝数及其显著系数')


df = pd.read_csv('data/opt/summary_follow_modi_3_strip.csv').astype({"ratio":float})
fig = px.box(df, x="class", y="ratio", points="all",range_y=[0,0.2], title='《朗读者》活跃用户关注UP主分区箱线图')


fig1 = px.pie(df0, values='Frequency', names='class', title='《朗读者》活跃用户关注UP主分区饼图（按出现频次）')

fig2 = px.pie(df, values='ratio', names='class', title='《朗读者》活跃用户注意力饼图(按照关注系数加权并去除《朗读者》相关内容）')

df3 = pd.read_csv('data/opt/heat.csv').astype({"Frequency":float,"TimeStamp":int})
df = px.data.tips()

fig3 = px.density_heatmap(df3, x="TimeStamp", y="Class",z="Frequency", histfunc="avg",title="《朗读者》三季弹幕密度图", height= 1200)
fig3.layout.font.family = 'Huiwen-mincho'
fig.layout.font.family = 'Huiwen-mincho'
fig2.layout.font.family = 'Huiwen-mincho'
fig1.layout.font.family = 'Huiwen-mincho'
fig_dict.layout.font.family = 'Huiwen-mincho'


df10 = pd.read_csv('data/reader_3_1.csv').astype({"feeling":float})
df10.sort_values('TimeStamp',inplace=True)

# fig = px.bar(df, labels={ 'index': 'TimeStamp' }, hover_name='Comment', y='feeling')
fig11 = px.line(df10, x='TimeStamp',  hover_name='Comment', y="feeling",title="S3E1")

df11 = pd.read_csv('data/reader_3_2.csv').astype({"feeling":float})
df11.sort_values('TimeStamp',inplace=True)

# fig = px.bar(df, labels={ 'index': 'TimeStamp' }, hover_name='Comment', y='feeling')
fig12 = px.line(df11, x='TimeStamp',  hover_name='Comment', y="feeling",title="S3E2")

df12 = pd.read_csv('data/reader_3_3.csv').astype({"feeling":float})
df12.sort_values('TimeStamp',inplace=True)

# fig = px.bar(df, labels={ 'index': 'TimeStamp' }, hover_name='Comment', y='feeling')
fig13 = px.line(df12, x='TimeStamp',  hover_name='Comment', y="feeling",title="S3E3")

df13 = pd.read_csv('data/reader_3_4.csv').astype({"feeling":float})
df13.sort_values('TimeStamp',inplace=True)

# fig = px.bar(df, labels={ 'index': 'TimeStamp' }, hover_name='Comment', y='feeling')
fig14 = px.line(df13, x='TimeStamp',  hover_name='Comment', y="feeling",title="S3E4")

fig11.layout.font.family = 'Huiwen-mincho'
fig12.layout.font.family = 'Huiwen-mincho'
fig13.layout.font.family = 'Huiwen-mincho'
fig14.layout.font.family = 'Huiwen-mincho'


df21 = pd.read_csv('data/opt/pn.csv').eval("overall = feeling_positive - feeling_negative")

groupobj21 = df21.groupby(by='Class')

fig21 = go.Figure()
fig21.layout.font.family = 'Huiwen-mincho'

bot = []
yy = 0
for i,j in groupobj21:

    k = groupobj21.get_group(i)
    fig21.add_trace(go.Scatter(x=k["TimeStamp"], y=k["feeling_positive"],
                               mode='lines',
                               visible= False,
                               name=i.strip(".csv") + " positive"))
    fig21.add_trace(go.Scatter(x=k["TimeStamp"], y=k["feeling_negative"].map(lambda x: x * -1),
                               mode='lines',
                               visible=False,
                               name=i.strip(".csv") + " negative"))

    ll = []
    for x in range(int(len(groupobj21))):
        if x == yy:
            ll.append(True)
            ll.append(True)
        else:
            ll.append(False)
            ll.append(False)
    bot.append(dict(label=i.strip(".csv"),method="update",args=[{"visible": [x for x in ll]}]))
    yy += 1
fig21.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=bot,
        )
    ])

# Set title
fig21.update_layout(title_text="《朗读者》每集弹幕情感曲线图")
root22 = 'data/sep/out/'

already_find_list = os.listdir(root22)


fig22 = go.Figure()
fig22.layout.font.family = 'Huiwen-mincho'

bot = []
yy = 0
for i in already_find_list:

    df22 = pd.read_csv('data/sep/out/' + i).sort_values("Ratio",ascending= False)
    fig22.add_trace(go.Bar(x=df22["Word"], y=df22["Ratio"],
                               visible= False,
                               name=i.strip(".csv")))
    ll = []
    for x in range(int(len(already_find_list))):
        if x == yy:
            ll.append(True)
        else:
            ll.append(False)
    bot.append(dict(label=i.split('.')[0],method="update",args=[{"visible": [x for x in ll]}]))
    yy += 1
fig22.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=bot,
        )
    ])

# Set title
fig22.update_layout(title_text="《朗读者》活跃用户高频词")

fig23 = go.Figure()
fig23.layout.font.family = 'Huiwen-mincho'
fig23 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
fig23.add_trace(go.Pie(labels=['低质量', '高质量'], values=[0.191705233179067, 1-0.191705233179067], pull=[0.2, 0], title="核心用户"),1,1)
fig23.add_trace(go.Pie(labels=['低质量', '高质量'], values=[0.225806451612903, 1-0.225806451612903], pull=[0.2, 0], title="全部用户"),1,2)
fig23.layout.font.family = 'Huiwen-mincho'
fig23.update_layout(title_text="《朗读者》用户弹幕质量分析")

import dash
from dash import dcc, html, Input, Output, State
gen = pd.read_csv('data/opt/generation.csv')
nonsense_words = gen['nonsense_words'].tolist()
app = dash.Dash()

app.layout = html.Div([
    # 偷设院网站校徽一枚（读书人的事情能叫偷吗？
    html.P(html.Img(src="http://sodcn.jiangnan.edu.cn/__local/B/20/1F/85E03E00FA88B2F38552C2B93D7_444202F0_811E.png?e=.png",width="150px"),),
    html.H1(children="“云深不知处”—— 《朗读者》观众行为与用户画像",style={'font-family':"Huiwen-mincho"}),
    html.P(children="\t来自Bilibili弹幕，所有图表均可以交互。", className="app__header__title--grey",style={'font-family':"Huiwen-mincho"}),
    dcc.Graph(figure=fig3),
    html.P(children="呀~观众朋友们看起来有些没长性呢，怎么每次看了第一集就走了……", className="app__header__title--grey",style={'font-family':"Huiwen-mincho", 'color':'grey'}),
    html.P(children="因此，我们希望筛选出那批坚持在每集打卡的“铁粉”（活跃用户）。", className="app__header__title--grey",style={'font-family':"Huiwen-mincho", 'color':'purple'}),
    dcc.Graph(figure=fig_dict),
    html.P(children="上图中，气泡大小表示该UP主被核心用户关注的人次。颜色代表分区，点击图例，可以筛选某一类别UP。", className="app__header__title--grey",style={'font-family':"Huiwen-mincho", 'color':'purple'}),
    html.P(children="「董卿粉丝」的显著系数高于其他所有UP，说明《朗读者》的死忠粉，往往是节目主持人董卿的粉丝。", className="app__header__title--grey",style={'font-family':"Huiwen-mincho", 'color':'purple'}),
    html.P(children="【显著系数】显著系数是该UP在《朗读者》核心用户中受关注程度与在B站用户总体中受关注程度之比。显著系数越大（在Y轴方向越高），越能断定《朗读者》核心观众群体同样也是该UP主的目标观众群体。", className="app__header__title--grey",
           style={'font-family': "Huiwen-mincho", 'color':'blue'}),
    dcc.Graph(figure=fig),
    dcc.Graph(figure=fig1),
    html.P(children="上图（频次图）中，大量B站用户普遍关注的娱乐类UP主占据了大量的频次，我们认为这是由于B站娱乐视频平台的性质决定的，不能代表《朗读者》用户情况。", className="app__header__title--grey",
           style={'font-family': "Huiwen-mincho", 'color':'purple'}),
    html.P(children="因此有了下图（加权频次图），按照显著系数加权得出，其中“教育”类凸显出来，说明教育类UP在该用户群体中具备极高的关注度，我们合理推测《朗读者》核心观众以学生群体为主。", className="app__header__title--grey",
           style={'font-family': "Huiwen-mincho", 'color':'purple'}),
    dcc.Graph(figure=fig2),
    html.P(children="“观其行，听其言”：核心用户弹幕关注点分析", className="app__header__title--grey",style={'font-family':"Huiwen-mincho"}),
    dcc.Graph(figure=fig22),
    html.P(children="【弹幕关注点】我们统计了核心用户所发送弹幕的高频词，并将其与所有弹幕对比，发现与一般用户相比，核心用户更喜欢用以上词汇。", className="app__header__title--grey",style={'font-family':"Huiwen-mincho", 'color':'blue'}),
    html.P(children="在上表中不难发现，用户对诸如“读者”、“老师”等名词更加敏感，符合学生群体的特征。“致敬”是典型的刷频弹幕关键词，而在核心群体中，这类关键词出现的频率大大降低.",
           className="app__header__title--grey", style={'font-family': "Huiwen-mincho", 'color':'purple'}),
    html.P(children="事已至此，我们不妨更进一步，对观众们的弹幕质量展开分析。", className="app__header__title--grey",
           style={'font-family': "Huiwen-mincho", 'color':'purple'}),
    html.P(children=" ", className="app__header__title--grey",
           style={'font-family': "Huiwen-mincho"}),
    html.H1(children="“契阔谈讌”——弹幕情感倾向与质量分析",style={'font-family':"Huiwen-mincho"}),
    dcc.Graph(figure=fig23),
    html.P(children="上图中，核心用户的有效弹幕质量比一般用户高出"+str(22.58 - 19.17) + "%", className="app__header__title--grey",
           style={'font-family': "Huiwen-mincho"}),
    dcc.Graph(figure=fig21),

    html.P(children="AI观众Steven", className="app__header__title--grey",
           style={'font-family': "Huiwen-mincho"}),
    html.P(children="我们采用隐马尔科夫链，以《朗读者》三季弹幕为基础，构建了能够自动生成《朗读者》弹幕的AI机器人Steven，点击下面的按钮，让Steven发弹幕。", className="app__header__title--grey",
           style={'font-family': "Huiwen-mincho"}),
    html.Div([
        html.Button('Steven，发弹幕。', id='submit-val', n_clicks=0, style={'font-family': "Huiwen-mincho"}),
        html.P(children=" ", className="app__header__title--grey",
               style={'font-family': "Huiwen-mincho"}),
        html.Div(id='container-button-basic',
                 children='Enter a value and press submit', style={'font-family': "Huiwen-mincho", 'font-size': '24px'})
    ]),
    html.H1(children="原始数据|Raw Data",style={'font-family':"Huiwen-mincho"}),
    html.P(children="常言道：“Talk is cheap, show me the code.” ", className="app__header__title--grey",style={'font-family':"Huiwen-mincho"}),
    html.P(children="对于ZJZ而言，只有原始数据才是最刺激的（误）…所以，以下是所有爬取到的弹幕构成的频谱图，鼠标悬浮以读取弹幕内容。希望也能满足你的好奇心~", className="app__header__title--grey",style={'font-family':"Huiwen-mincho", 'color':'indigo'}),
    dcc.Graph(figure=fig11),
    dcc.Graph(figure=fig12),
    dcc.Graph(figure=fig13),
    dcc.Graph(figure=fig14),


    html.P(children="By Zhang Jingzhe & Chen Tiange, all rights reserved.", className="app__header__title--grey",style={'font-family':"Huiwen-mincho"}),
])
@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
)
def update_output(n_clicks):
    return 'Steven：“ {}”'.format(
        nonsense_words[n_clicks%500]
    )
app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter