'''
制作在线问卷调查
要用到的知识: https://getbootstrap.com, 这个是一个CSS框架, 在dash_bootstrap_components里面用到
dash_bootstrap_components 是对于 dash-core-components 的扩展, 有一些区别, 后者不包括button按钮, 不提供container
https://dash.plotly.com/dash-core-components
https://dash-bootstrap-components.opensource.faculty.ai
https://medium.com/analytics-vidhya/dash-bootstrap-bring-your-projects-to-life-in-a-beautiful-way-6b1c3bd7cfcf
https://www.datarevenue.com/en-blog/data-dashboarding-streamlit-vs-dash-vs-shiny-vs-voila

'''

import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import json
import re

app = dash.Dash(__name__)

app.layout = html.Div(
    dbc.Container(
        [
            html.H1('2023年县级政府绩效评价录入系统',
                style={'color': '#b00404','text-align':'center'
                }
            ),
            html.Br(),

            html.H2('第一部分 - 录入员个人信息',
                style={'color': '#3156de','text-align':'center'
                }
            ),
            html.Hr(),

            html.P('1.姓名：'),
            dbc.Input(
                id='recorder',
                placeholder='填写录入员姓名',
                autoComplete='off',
                style={
                    'width': '250px',
                }
            ),

            html.P('2.手机号码：'),
            dbc.Input(
                id='tel',
                placeholder='填写登记手机号',
                autoComplete='off',
                style={
                    'width': '250px',
                }
            ),

            html.P('3.分组：'),
            dbc.RadioItems(
                style = {'inline': 'True'},
                id = 'group',
                options=[
                    {'label': '1组', 'value': 'g1', 'color': '#b00404', 'font-size': 20},
                    {'label': '2组', 'value': 'g2', 'color': 'Warning', 'font-size': 20},
                    {'label': '3组', 'value': 'g3', 'color': '#b00404', 'font-size': 20},
                    {'label': '4组', 'value': 'g4', 'color': 'Success', 'font-size': 20},
                ],
                inline = True,
                labelStyle = {
                    'color': '#3156de',
                    'text-align': 'justify'
                },
#                labelCheckedStyle = {
#                    'color': '#b00404',
#                    'text-align': 'justify'
#                }
            ),

            html.P('4.录入日期：'),
            dbc.Input(
                id = 'date',
                placeholder = '例: 20230725',
                autoComplete = 'off',
                style = {
                    'width': '250px'
                }
            ),
            html.Hr(),
            html.Br(),

            html.H2('第二部分 - 基本绩效信息',
                style = {'color': '#3156de','text-align':'center'
                }
            ),
            html.Hr(),

            html.P('5.所在省份：'),
            dbc.RadioItems(
                id='province',
                inline=True,
#                switch=True,             
                options=[
                    {'label': item, 'value': item}
                    for item in list ('甘肃''陕西''青海''西藏''宁夏''新疆''浙江')
                ],
                style={
                    'width': '200px'
                }
            ),

            html.Br(),

            html.P('6.满意度：'),
            dbc.Input(id='sat-range',
                placeholder='满意度',
                type='range',
                style={'width': '300px'},
                min=0,
                max=100,
                step=5,
            ),
            html.P(id='output-range'),

            html.P('6.所在城市：'),
            dbc.RadioItems(
                id = 'frequency',
                inline = True,
                options = [
                    {'label': '经常', 'value': 'often'},
                    {'label': '偶尔', 'value': 'little'},
                    {'label': '没用过', 'value': 'no-use'}
                ]
            ),
            html.Br(),
            
            html.P('7.所在县：'),
            dbc.Checklist(
                id = 'hobbies',
                options = [
                    {'label': '构建在线数据可视化作品', 'value': 'web'},
                    {'label': '制作机器学习demo', 'value': 'ml'},
                    {'label': '为企业开发BI仪表盘', 'value': 'bi'},
                    {'label': '为企业开发酷炫的指标监控大屏', 'value': 'screen'},
                    {'label': '开发有用的在线小工具', 'value': 'tools'},
                    {'label': '其他', 'value': 'other'},
                    ]
                ),
            html.Br(),
            
            html.P('8.所在部门：'),
            dbc.RadioItems(
                id = 'career',
                options = [
                    {'label': '科研人员', 'value': '科研人员'},
                    {'label': '运营', 'value': '运营'},
                    {'label': '数据分析师', 'value': '数据分析师'},
                    {'label': '算法工程师', 'value': '算法工程师'},
                    {'label': '大数据开发工程师', 'value': '大数据开发工程师'},
                    {'label': '金融分析师', 'value': '金融分析师'},
                    {'label': '爬虫工程师', 'value': '爬虫工程师'},
                    {'label': '学生', 'value': '学生'},
                    {'label': '其他', 'value': '其他'},
                    ]
                ),
            html.Br(),

            html.H2('第三部分 - 信息核对',
                style = {'color': '#3156de','text-align':'center'
                }
            ),
            html.Hr(),

            html.P('9.手机号码：'),
            dbc.Input(
                id = 'tel',
                placeholder = '填写登记手机号',
                autoComplete = 'off',
                style = {
                    'width': '250px'
                }
            ),
            html.Hr(),
            
            html.Button(
                '点击提交',
                id = 'submit'
            ),
            
            html.P(id = 'user-info')
        ],
#        style = {
#            'display': 'inline-block',
#            'margin-top': '50px',
#            'margin-bottom': '200px'
#        }
    )
)

@app.callback(
    Output('user-info', 'children'),
    Input('submit', 'n_clicks'),
    [
        State('group', 'value'),
        State('date', 'value'),
        State('frequency', 'value'),
        State('hobbies', 'value'),
        State('tel', 'value')
    ],
    prevent_initial_call=True
)

@app.callback(
    Output('output-range', 'children'),
    Input('sat-range', 'value')
)
def output_range(value):
    return value

def fetch_info(n_clicks, gender, province, frequency, hobbies, tel):
    if all([gender, province, frequency, hobbies, tel]):
        with open(tel + '.json', mode='w', encoding='utf-8') as jf:
            json.dump(
                {
                    'gender': gender,
                    'code_language': code_language,
                    'frequency': frequency,
                    'hobbies': hobbies,
                }, jf
            )
        return '填写完毕，请刷新页面！'
    else:
        return '信息未填写完全！'
    
@app.callback(
    [Output('recorder', 'valid'),
     Output('tel', 'valid'),
     Output('tel', 'invalid')],
     Input('tel', 'value'),
     prevent_initial_call=True
)

def check_tel(value):
    try: 
        if re.findall('\d+', value)[0] == value and len(value) == 11:
            return True, False
    except:
        pass
    return False, True

if __name__ == '__main__':
    app.run_server(debug=True)
