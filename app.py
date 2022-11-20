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




def fetchReviews(url):
    r = requests.get(url,  headers={'User-Agent': "Mozilla/5.0"})             
    soup = bs(r.content, 'html.parser') 
    dict = {}

    #Fetch Average Rating of Monument
    rating = soup.find('div',attrs={'class':'biGQs _P fiohW hzzSG uuBRH'})
    dict['rating'] = rating.text

    #Fetch Nos Of Reviews of Monument
    nosOfReviews = soup.find('span',attrs={'class':'biGQs _P pZUbB biKBZ KxBGd'})
    dict['nosOfReviews'] = nosOfReviews.text

    #Nos Of Excellent Reviews
    nosOfExcellentReviews = soup.find_all('div',attrs={'class':'biGQs _P pZUbB osNWb'})
    dict['nosOfExcellentReviews'] = nosOfExcellentReviews[0].text

    #Nos Of Very Good Reviews
    dict['nosOfVeryGoodReviews'] = nosOfExcellentReviews[1].text

    #Nos Of Average Reviews
    dict['nosOfAverageReviews'] = nosOfExcellentReviews[2].text

    #Nos Of Poor Reviews
    dict['nosOfPoorReviews'] = nosOfExcellentReviews[3].text

    #Nos Of Terrible Reviews
    dict['nosOfTerribleReviews'] = nosOfExcellentReviews[4].text

    reviews = soup.find_all('div',attrs={'data-automation':'reviewCard'})
    arr = []
    for review in reviews:
        rdict = {}
        #Fetch Reviewer Name
        reviewerName = review.find('a',attrs={'class':'BMQDV _F G- wSSLS SwZTJ FGwzt ukgoS'})
        
        r = review.find_all('span',attrs={'class':'yCeTE'})

        #Fetch Reviewer Rating
        reviewerRating = review.find_all('path',attrs={'d':'M 12 0C5.388 0 0 5.388 0 12s5.388 12 12 12 12-5.38 12-12c0-6.612-5.38-12-12-12z'})
        # print(len(reviewerRating))        
        # print(r)

        #Fetch Review Title
        reviewTitle = r[0].text


        #Fetch Review Text
        reviewText = r[1].text

        #Fetch Review Date
        reviewDate = review.find('div',attrs={'class':'RpeCd'})

        rdict['reviewerName'] = reviewerName.text
        rdict['reviewerRating'] = str(len(reviewerRating))
        rdict['reviewTitle'] = reviewTitle
        rdict['reviewText'] = reviewText
        rdict['reviewDate'] = reviewDate.text

        print(reviewerName.text+"\t"+reviewDate.text+"\t"+str(len(reviewerRating))+"\t"+ reviewTitle+ "\t" +reviewText)
        print("\n******************************\n")


        arr.append(rdict)
        
        # return rdict
        # reviewCard = ReviewCard()
        # r.append(reviewCard)
        # r.append(reviewerName.text)
        # r
    # dict['reviewerNames',r]
    # print(reviews)
    # print(soup)
    # reviews = soup.find_all('div',attrs={'class' : 'review-container'})
    # reviewList = []
    # for i in reviews:
    #     reviewList.append(i.text)
    dict['reviews']=arr
    # print(arr)
    return dict
    

@app.route('/reviews',methods=['POST'])
def getMonumentReviews():
    url = request.form.get('url')
    # time.sleep(2) # to limit the number of requests
    data = fetchReviews(url)
    # r = requests.get(url,headers=headers_Get)
    # soup = bs(r.content, 'html.parser')
    # print(url)
    return jsonify(data)


def fetchHotels(url):
    r = requests.get(url,  headers={'User-Agent': "Mozilla/5.0"})             
    soup = bs(r.content, 'html.parser') 
    dict = {}

    #Fetch Average Rating of Monument
    hotelCards = soup.find_all('div',attrs={'class':'listing_title ui_columns is-gapless is-mobile is-multiline'})
    for hotel in hotelCards:
        print(hotel)
        print("\n******************************\n")
    
    return dict

@app.route('/hotels',methods=['POST'])
def getHotels():
    url = request.form.get('url')
    # time.sleep(2) # to limit the number of requests
    data = fetchHotels(url)
    return jsonify(data)

def fetchNearbyPlaces(url):
    r = requests.get(url,  headers={'User-Agent': "Mozilla/5.0"})             
    soup = bs(r.content, 'html.parser') 
    dict = {}

    arr=[]
    #Fetch NaerBy Places card
    nearByPlacesCard = soup.find_all('article',attrs={'class':'GTuVU XJlaI'})
    for place in nearByPlacesCard:
        rdict={}
        #Fetch Image url
        imageUrl = place.find('picture',attrs={'class':'NhWcC _R'}).img['src']

        rdict['image'] = imageUrl
        print(imageUrl)
        print("\n******************************\n")
        arr.append(rdict)
    
    # dict['places']=arr
    return arr

@app.route('/nearByPlaces',methods=['POST'])
def getNearbyPlaces():
    url = request.form.get('url')
    # time.sleep(2) # to limit the number of requests
    data = fetchNearbyPlaces(url)
    return jsonify(data)

@app.errorhandler(500)
def page_not_found(e):
    print(e)
    return jsonify({'error': 'Something went wrong'}), 500


if __name__ == '__main__':
    app.run()