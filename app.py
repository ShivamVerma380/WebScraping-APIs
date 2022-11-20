from bs4 import BeautifulSoup as bs
import requests 


headers_Get = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Firefox/49.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/json'
}


def getHeadingPara(monumentName):
    data = {}

    url = 'https://en.wikipedia.org/wiki/'+monumentName

    r = requests.get(url, headers=headers_Get)             

    soup = bs(r.content, 'html.parser') 
    intro = soup.find_all('div',attrs={'class' : 'mw-parser-output'})
    
    intro = soup.find_all('div',attrs={'class' : 'mw-parser-output'})[0].find_all('p')
    if intro == []:
        intro = soup.find_all('div',attrs={'class' : 'mw-parser-output'})[1].find_all('p')[1].text
    else:
        intro = soup.find_all('div',attrs={'class' : 'mw-parser-output'})[0].find_all('p')[1].text
    
    for i in intro:
        pos1 = intro.find('[')
        pos2 = intro.find(']')
        intro = intro.replace(intro[pos1:pos2+1],'')
        intro = intro.replace('\"' ,'')
        intro = intro.replace('\n' ,'')

    data['Introduction'] = intro
    headings = soup.find_all('div',attrs={'class' : 'mw-parser-output'})[0].find_all('h2') #find all headings
    # print(headings)
    if headings == []:
        headings = soup.find_all('div',attrs={'class' : 'mw-parser-output'})[1].find_all('h2')
    # print(headings)
    text = ''
    for i in headings:
        # print(i.text, '\n')
        description = i.find_next('p')
        if description != None:

            description = description.get_text()
            for j in description:
                text = text + j
            for j in text:
                pos1 = text.find('[')
                pos2 = text.find(']')
                text = text.replace(text[pos1:pos2+1],'')
                text = text.replace('\"' ,'')
            pos3 = text.find('.mw-parser-output')
            text = text.replace(text[pos3:],'')
            head = i.text
            head = head.replace('[edit]','')
            data[head] = text
            text = ''
    return data

# flask api
from flask import Flask,request, jsonify
import time


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'


@app.route('/<monumentName>',methods=['GET'])
def getDetails(monumentName):
    
        time.sleep(2) # to limit the number of requests
        data = getHeadingPara(monumentName)
        return jsonify(data)


@app.route('/image/<monumentName>',methods=['GET'])
def getImageSrc(monumentName):
    url = 'https://en.wikipedia.org/wiki/'+monumentName
    r = requests.get(url, headers=headers_Get)             
    soup = bs(r.content, 'html.parser') 
    image = soup.find_all('div',attrs={'class' : 'mw-parser-output'})[0].find_all('img')
    if len(image) == 1:
        image = soup.find_all('div',attrs={'class' : 'mw-parser-output'})[1].find_all('img')
    imgList = []
    for i in image:
        imgList.append(i['src'])
    return jsonify(imgList)

# def fetchReviews(url):
    

@app.route('/reviews',methods=['POST'])
def getMonumentReviews():
    url = request.form.get('url')
    # data = fetchReviews(url)
    # r = requests.get(url,headers=headers_Get)
    # soup = bs(r.content, 'html.parser')
    print(url)
    return jsonify(url)

@app.errorhandler(500)
def page_not_found(e):
    print(e)
    return jsonify({'error': 'Something went wrong'}), 500


if __name__ == '__main__':
    app.run()