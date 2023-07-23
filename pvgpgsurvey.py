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

app = dash.Dash(__name__) # 两种写法，这一行可以写成app = dash.Dash(external_stylesheets=[dbc.themes.SOLAR]), 则不用下面一行了 #Darkly, Quartz, SLATE, SOLAR，具体可以参考 https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/explorer/
app.config.external_stylesheets = [dbc.themes.SOLAR]
app.title = '政府绩效录入小能手 V1'
locations = ["甘肃", "陕西", "青海", "宁夏", "浙江", "四川"]
departments = ["工商", "税务", "人事", "市政", "公安", "卫生"]

app.layout = html.Div(
    dbc.Container(
        [
            html.H1('2023年县级政府绩效评价录入系统',
                style = {'color': '#b00404', 'text-align':'center'
                }
            ),
            html.Br(),

            html.H2('第一部分 - 录入员个人信息',
                style = {'color': '#3156de','text-align':'center'
                }
            ),
            html.Hr(),

            html.P('1.姓名：'),
            dbc.Input(
                id = 'recorder',
                placeholder = '填写录入员姓名',
                autoComplete = 'off',
                style = {
                    'width': '250px',
                }
            ),

            html.P('2.手机号码：'),
            dbc.Input(
                id = 'tel',
                placeholder = '填写登记手机号',
                autoComplete = 'off',
                style = {
                    'width': '250px',
                }
            ),

            html.P('3.分组：'),
            dbc.RadioItems(
                id = 'group',
                inline = True,
                switch = True,
                options=[
                    {'label': '1组', 'value': 'g1', 'color': '#b00404', 'font-size': 20},
                    {'label': '2组', 'value': 'g2', 'color': 'Warning', 'font-size': 20},
                    {'label': '3组', 'value': 'g3', 'color': '#b00404', 'font-size': 20},
                    {'label': '4组', 'value': 'g4', 'color': 'Success', 'font-size': 20},
                ],
                labelStyle = {
                    'color': '#3156de',
                    'text-align': 'justify'
                },
                labelCheckedStyle = {
                    'color': '#b00404',
                    'text-align': 'justify'
                }
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
                id = 'province',
                inline = True,
                switch = True,      
                options = [
                    {'label': item, 'value': item}
                    for item in list (set(locations))
                ],
                style = {
                    'width': '800px'
                }
            ),

            html.Br(),

            html.P('6.满意度：'),
            dbc.Input(
                id = 'sat-range',
                placeholder = '满意度',
                type = 'range',
                style = {'width': '300px'},
                min = 0,
                max = 100,
                step = 2,
            ),
            html.P(id = 'output-range'),

            html.P('7.所在城市：'),
            dbc.Input(
                id = 'city',
                placeholder = '请直接填写，例: 兰州',
                autoComplete = 'off',
                style = {
                    'width': '250px'
                }
            ),
            html.Br(),

            html.P('8.所在县：'),
            dbc.Input(
                id = 'county',
                placeholder = '请直接填写，例: 城关',
                autoComplete = 'off',
                style = {
                    'width': '250px'
                }
            ),
            html.Br(),
            
            html.P('9.涉及部门：'),
            dbc.Checklist(
                id = 'dptment',
                inline = True,
                switch = True,
                options=[
                    {'label': item, 'value': item}
                    for item in list (set(departments))
                ],
#                labelStyle = {
#                    'color': '#3156de',
#                    'text-align': 'justify'
#                },
                labelCheckedStyle = {
                    'color': '#b00404',
                    'text-align': 'justify'
                },
                style = {
                    'width': '400px'
                }
                ),
            html.Br(),
            
            html.P('10.所在部门：'),
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
                    ],
                labelStyle = {
                    'color': '#3156de',
                    'text-align': 'justify'
                },
                labelCheckedStyle = {
                    'color': '#b00404',
                    'text-align': 'justify'
                }
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
            
            html.P(id = 'user-info'),

            html.H6('~骄傲地由中国地方政府绩效中心开发和维护~',
                style = {'color': '#ffa000','text-align':'center'
                }
            ),
            html.Hr()
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
