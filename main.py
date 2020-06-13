import os
import dialogflow_v2 as dialogflow
from flask import render_template, redirect, url_for, request, Flask, redirect, url_for, request,jsonify, make_response
from flask_ngrok import run_with_ngrok

from bs4 import BeautifulSoup
from urllib.request import urlopen

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib import parse
import json

from pandas import Series, DataFrame
import pandas as pd



options = Options()
options.headless = True
driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './credentials1.json' # 여러분의 인증서 명
def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    for text in texts:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)
        return response.query_result.fulfillment_text #추가


app = Flask(__name__) # Flask 객체를 생성하고 그 이름을 app 으로 설정
project_id = "-"
session_id = "-"



def frame(data):
    frame = DataFrame(data)
    return frame

@app.route('/',methods=['GET', 'POST']) # route 설정, URL 을 설정하는 것이다.
@app.route('/index',methods=['GET', 'POST'])
def page_main():
    return render_template('index.html')

@app.route('/medibot/<msg>', methods=['GET', 'POST'])
def medibot_dialogflow(msg):
    ans = detect_intent_texts(project_id,session_id,[msg],'ko');
    anslist = ans.split('/')

    if anslist[0] =='통합':
        base_url='https://www.lost112.go.kr/find/findList.do'
        search = parse.quote(anslist[0]+"검색")
        url=base_url+search
        print(url)
        driver.get(url)  #설정해주어야 제대로 열림

        def show_tables():
           data = pd.read_html('https://www.lost112.go.kr/find/findList.do#none', header=0)[0]
           data.index.name=None
           data= data[data['습득물명'].astype(str).str.contains(anslist[3])]
           return render_template('index.html',tables=[data.to_html(classes='female')],
            titles = ['Find_lost'])
        show_tables()

        return show_tables()
        return render_template('index.html',ans=ans)

    elif anslist[0] =='합번호':
        base_url='https://www.lost112.go.kr/find/findList.do'
        search = parse.quote(anslist[0]+"검색_number")
        url=base_url+search
        print(url)

        a=[]
        x=0
        for i in range(1):
            for page in range(2,11):
                tag_names = driver.find_element_by_css_selector(".find_listBox").find_elements_by_tag_name("tbody>tr")
                for tag in tag_names:
                    if x in (tag.text):
                         a[x]=(tag.text.split("\n")) #출력코드
                         return a[x]

        ans = anslist[1]+anslist[2]+"분실물입니다."+'\n'+str(a)
        return render_template('index.html',ans=ans)


    elif anslist[0] =='이미지검색':
        base_url='https://www.lost112.go.kr/find/findList.do'
        search = parse.quote(anslist[0]+"검색_number")
        url=base_url+search
        print(url)
        ans= anslist[1]
        return render_template('이미지검색.html',ans=ans)

    elif anslist[0] =='지하철':
        base_url='https://www.lost112.go.kr/find/findList.do'
        search = parse.quote(anslist[0]+"info")
        url=base_url+search
        print(url)
        if(anslist[1]=='수도권'):
            if(anslist[2]=='1','3','4'):
                ans = anslist[1]+anslist[2]+anslist[3]+"1544-7788"+anslist[4]
            elif(anslist[2]=='2'):
                ans = anslist[1]+anslist[2]+anslist[3]+"1577-1234"+anslist[4]
            elif(anslist[2]=='5','6','7','8'):
                ans = anslist[1]+anslist[2]+anslist[3]+"1577-5678"+anslist[4]
            else:
                ans = anslist[1]+anslist[2]+anslist[3]+"02-2656-0009"+anslist[4]
        return render_template('index.html',ans=ans)
#뭐야 그냥 연결되어서 나오는데...

 #버스
    elif anslist[0] =='버스':
        base_url='https://www.lost112.go.kr/find/findList.do'
        search = parse.quote(anslist[0]+"info")
        url=base_url+search
        print(url)

        def show_tables():
           data =pd.read_excel('bus.xls')
           data.index.name=None
           b = anslist[1].split('번')[0]
           data = data[data['노선번호']==b]
           data= data[['관할관청','노선번호', '운행업체','연락처']]
           return render_template('index.html',tables=[data.to_html(classes='bus')],
            titles = ['bus_num'])
        show_tables()

        return show_tables()
        return render_template('index.html',ans=ans)

#일택시================================
    elif anslist[0] =='일반택시':
        base_url='https://www.lost112.go.kr/find/findList.do'
        search = parse.quote(anslist[0]+"info")
        url=base_url+search
        print(url)

        if(anslist[1]=='서울특별시'):
            ans = anslist[1]+anslist[2]+' 02-2033-9200'+anslist[3]

        elif(anslist[1] =='부산광역시'):
            ans = anslist[1]+anslist[2]+' 051-462-4651'+anslist[3]

        elif(anslist[1] =='경기'):
            ans = anslist[1]+anslist[2]+' 031-255-7881'+anslist[3]

        elif(anslist[1] =='대구광역시'):
            ans = anslist[1]+anslist[2]+' 053-765-4111'+anslist[3]

        elif(anslist[1] =='인천광역시'):
            ans = anslist[1]+anslist[2]+' 032-466-5101'+anslist[3]

        elif(anslist[1] =='광주광역시'):
            ans = anslist[1]+anslist[2]+' 062-676-8031'+anslist[3]

        elif(anslist[1] =='대전광역시'):
            ans = anslist[1]+anslist[2]+' 042-527-1241'+anslist[3]

        elif(anslist[1] =='울산광역시'):
            ans = anslist[1]+anslist[2]+'052-274-9998'+anslist[3]
            #강원
        elif(anslist[1] =='속초시'or '원주시'or'강릉시'or'삼척시'or'춘천시'or'평창군'or'동해시'):
            ans = anslist[1]+anslist[2]+'033-253-4244'+anslist[3]
            #충북
        elif(anslist[1] =='청주시'or'제천시'or'충주시'or'진천군'or'세종특별자치시'or'이천시'or'천안시'or'안성시'or'상주시'):
            ans = anslist[1]+anslist[2]+'043-252-5701'+anslist[3]
            #충남
        elif(anslist[1] =='공주시'or'보령시'or'아산시'or'논산시'or'서산시'or'당진시'or'계룡시'or'평택시'or'상주시'):
            ans = anslist[1]+anslist[2]+'041-853-4841'+anslist[3]
            #전북
        elif(anslist[1] =='전주시'or'군산시'or'익산시'or'남원시'or'김제시'or'정읍시'or'하동군'or'장성군'or'거창군'):
            ans = anslist[1]+anslist[2]+'063-254-1443'+anslist[3]
            #전남
        elif(anslist[1] =='여수시'or'목포시'or'순천시'or'나주군'or'광양시'or'보성군'or'장성군'or'강진군'or'신안군'):
            ans = anslist[1]+anslist[2]+'062-673-2922'+anslist[3]
            #경북
        elif(anslist[1] =='안동시'or'경주시'or'포항시'or'김천시'or'문경시'or'구미시'or'상주시'or'영주시'or'영천시'or'영양군'or'선산읍'):
            ans = anslist[1]+anslist[2]+'053-742-6528'+anslist[3]
            #경남
        elif(anslist[1] =='창원시'or'진주시'or'김해시'or'사천시'or'양산시'or'토양시'or'함양시'or'남해시'or'의령군'or'마산시'or'창원시'or'합천군'or'고성군'or'거창군'or'창녕군'or'산청군'):
            ans = anslist[1]+anslist[2]+'055-288-3311'+anslist[3]

        elif(anslist[1] =='제주시'):
            ans = anslist[1]+anslist[2]+'064-722-0274'+anslist[3]
        return render_template('index.html',ans=ans)

#개인택시================================
    elif anslist[0] =='개인택시':
        base_url='https://www.lost112.go.kr/find/findList.do'
        search = parse.quote(anslist[0]+"info")
        url=base_url+search
        print(url)

        if(anslist[1]=='서울특별시'):
            ans = anslist[1]+anslist[2]+'02-2084-6300'+anslist[3]

        elif(anslist[1] =='부산광역시'):
            ans = anslist[1]+anslist[2]+'051-500-8500'+anslist[3]

        elif(anslist[1] =='경기'):
            ans = anslist[1]+anslist[2]+'031-255-5001'+anslist[3]

        elif(anslist[1] =='대구광역시'):
            ans = anslist[1]+anslist[2]+'053-765-8500'+anslist[3]

        elif(anslist[1] =='인천광역시'):
            ans = anslist[1]+anslist[2]+'032-578-5431'+anslist[3]

        elif(anslist[1] =='광주광역시'):
            ans = anslist[1]+anslist[2]+'062-570-6800'+anslist[3]

        elif(anslist[1] =='대전광역시'):
            ans = anslist[1]+anslist[2]+'042-583-6460'+anslist[3]

        elif(anslist[1] =='울산광역시'):
            ans = anslist[1]+anslist[2]+'052-211-1830'+anslist[3]
            #강원
        elif(anslist[1] =='속초시'or '원주시'or'강릉시'or'삼척시'or'춘천시'or'평창군'or'동해시'):
            ans = anslist[1]+anslist[2]+'033-253-4244'+anslist[3]
            #충북
        elif(anslist[1] =='청주시'or'제천시'or'충주시'or'진천군'or'세종특별자치시'or'이천시'or'천안시'or'안성시'or'상주시'):
            ans = anslist[1]+anslist[2]+'043-259-8483'+anslist[3]
            #충남
        elif(anslist[1] =='공주시'or'보령시'or'아산시'or'논산시'or'서산시'or'당진시'or'계룡시'or'평택시'or'상주시'):
            ans = anslist[1]+anslist[2]+'041-331-1611'+anslist[3]
            #전북
        elif(anslist[1] =='전주시'or'군산시'or'익산시'or'남원시'or'김제시'or'정읍시'or'하동군'or'장성군'or'거창군'):
            ans = anslist[1]+anslist[2]+'063-212-3994'+anslist[3]
            #전남
        elif(anslist[1] =='여수시'or'목포시'or'순천시'or'나주군'or'광양시'or'보성군'or'장성군'or'강진군'or'신안군'):
            ans = anslist[1]+anslist[2]+'061-800-8010'+anslist[3]
            #경북
        elif(anslist[1] =='안동시'or'경주시'or'포항시'or'김천시'or'문경시'or'구미시'or'상주시'or'영주시'or'영천시'or'영양군'or'선산읍'):
            ans = anslist[1]+anslist[2]+'053-756-3357'+anslist[3]
            #경남
        elif(anslist[1] =='창원시'or'진주시'or'김해시'or'사천시'or'양산시'or'토양시'or'함양시'or'남해시'or'의령군'or'마산시'or'창원시'or'합천군'or'고성군'or'거창군'or'창녕군'or'산청군'):
            ans = anslist[1]+anslist[2]+'055-274-0626'+anslist[3]

        elif(anslist[1] =='제주시'):
            ans = anslist[1]+anslist[2]+'064-744-2793'+anslist[3]
        return render_template('index.html',ans=ans)


    else:
        return render_template('index.html',ans=ans)

@app.route('/action',methods = ['POST', 'GET'])
def action():
    if request.method == 'POST':
        msg = request.form['msg']
        return redirect(url_for('medibot_dialogflow', msg=msg))
    elif act =='total':     #불러올 인텐트명 total
        output = get_info() #크롤링 결과를 output에 넣는다
        msg = request.form = {'fulfillmentText': "\n"+output,
               'outputContexts': req['queryResult']['outputContexts']}    #결과물

    else:
        msg = request.args.get('msg')
        return redirect(url_for('medibot_dialogflow', msg=msg))


if __name__ == '__main__':
    app.run(debug=True) #
