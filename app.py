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
    try:
        rating = soup.find('div',attrs={'class':'biGQs _P fiohW hzzSG uuBRH'})
        dict['rating'] = rating.text
    except:
        dict['rating'] = ''
    #Fetch Nos Of Reviews of Monument
    try:
        nosOfReviews = soup.find('span',attrs={'class':'biGQs _P pZUbB biKBZ KxBGd'})
        dict['nosOfReviews'] = nosOfReviews.text
    except:
        dict['nosOfReviews'] = ''
    #Nos Of Excellent Reviews
    try:
        nosOfExcellentReviews = soup.find_all('div',attrs={'class':'biGQs _P pZUbB osNWb'})
        dict['nosOfExcellentReviews'] = nosOfExcellentReviews[0].text
    except:
        dict['nosOfExcellentReviews'] = ''
    #Nos Of Very Good Reviews
    try:  
        dict['nosOfVeryGoodReviews'] = nosOfExcellentReviews[1].text
    except:
        dict['nosOfVeryGoodReviews'] = ''

    #Nos Of Average Reviews
    try:
        dict['nosOfAverageReviews'] = nosOfExcellentReviews[2].text
    except:
        dict['nosOfAverageReviews'] = ''
    #Nos Of Poor Reviews
    try:
        dict['nosOfPoorReviews'] = nosOfExcellentReviews[3].text    
    except:
        dict['nosOfPoorReviews'] = ''
    #Nos Of Terrible Reviews
    try:
        dict['nosOfTerribleReviews'] = nosOfExcellentReviews[4].text
    except:
        dict['nosOfTerribleReviews'] = ''
    #Fetch Reviews
    reviews = soup.find_all('div',attrs={'data-automation':'reviewCard'})
    arr = []
    for review in reviews:
        rdict = {}
        #Fetch Reviewer Name
        try:
            reviewerName = review.find('a',attrs={'class':'BMQDV _F G- wSSLS SwZTJ FGwzt ukgoS'})
        except:
            reviewerName = ''

        try:        
            r = review.find_all('span',attrs={'class':'yCeTE'})
        except:
            r = ''
        #Fetch Reviewer Rating
        try:
            reviewerRating = review.find_all('path',attrs={'d':'M 12 0C5.388 0 0 5.388 0 12s5.388 12 12 12 12-5.38 12-12c0-6.612-5.38-12-12-12z'})
        except:
            reviewerRating = ''
        # print(len(reviewerRating))        
        # print(r)

        #Fetch Review Title
        try:
            reviewTitle = r[0].text
        except:
            reviewTitle = ''

        #Fetch Review Text
        try:
            reviewText = r[1].text
        except:
            reviewText = ''

        
        #Fetch Review Date
        try:
            reviewDate = review.find('div',attrs={'class':'RpeCd'})
        except:
            reviewDate = ''
        try:
            rdict['reviewerName'] = reviewerName.text
        except:
            rdict['reviewerName'] = ''

        try:      
            rdict['reviewerRating'] = str(len(reviewerRating))
        except:
            rdict['reviewerRating'] = ''
        try:
            rdict['reviewTitle'] = reviewTitle
        except:
            rdict['reviewTitle'] = ''
        try:    
            rdict['reviewText'] = reviewText
        except:
            rdict['reviewText'] = ''
        try:
            rdict['reviewDate'] = reviewDate.text
        except:
            rdict['reviewDate'] = ''
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
    arr = []

    # hotel = soup.find('div',attrs={'id':'taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_dated_0'})
    # # for hotel in soup.find_all('div',attrs={'id':'taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_dated_0'}):
    # #     print(hotel)
    #     # print("\n******************************\n")

    # # soup = bs(hotel, 'html.parser')
    # hotels=[]
    # images = []
    # for image in hotel.find_all('img'):
    #     # i = image['src']
    #     # title = image['a']
    #     # print(title+"\t"+i)
    #     images.append(image['src'])
    #     # print("\n******************************\n")

    # titles = []
    # for h in hotel.find_all('a'):
    #     # titles.append(h.text)
    #     print(h)
    #     print("\n******************************\n")

    image = []
    for i in soup.find_all('img',attrs={'class':'_C _Z w'}):
        image.append(i['src'])
    
    # print(image)

    # print("\n******************************\n")

    
    hotel = []

    for name in soup.find_all('div',attrs={'class':'listing_title'}):
        hotel.append(name.text.strip())

    # print(hotel)

    ratings = []

    for rating in soup.find_all('a',{'class':'ui_bubble_rating'}):
        ratings.append(rating['alt'].strip())

    # print("\n******************************\n")

    # print(ratings)

    # print("\n******************************\n")

    price = []

    for p in soup.find_all('div',attrs={'class':'price-wrap'}):
        price.append(p.text.strip())
    
    # print(price)

    # print("\n******************************\n")

    i = 0

    
    for h in hotel:
        dict = {}
        dict['hotelName'] = h
        dict['price'] = price[i]
        dict['rating'] = ratings[i]
        if(i<len(image)):
            dict['image'] = image[i]
            # print(h+"\t"+ratings[i]+"\t"+price[i]+"\t"+image[i])
        else:
            dict['image'] = ""
            # print(h+"\t"+ratings[i]+"\t"+price[i]+"\t"+"")
        i+=1
        # print("\n******************************\n")
        arr.append(dict)
    
    
    return arr

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
    try:
        nearByPlacesCard = soup.find_all('article',attrs={'class':'GTuVU XJlaI'})
    except:
        nearByPlacesCard = []

    for place in nearByPlacesCard:
        rdict={}
        #Fetch Image url
        try:
            imageUrl = place.find('picture',attrs={'class':'NhWcC _R'}).img['src']
        except:
            imageUrl = ""
        #Fetch Place Name
        try:
            placeName = place.find('div',attrs={'class':'XfVdV o AIbhI'}).text
        except:
            placeName = ""
        #Fetch On Click Link
        try:
            onClickLink = "https://tripadvisor.in"+place.find('div',attrs={'class':'alPVI eNNhq PgLKC tnGGX'}).a['href']
        except:
            onClickLink = ""
        #Fetch Place short Description
        try:
            description = place.find('div',attrs={'class':'biGQs _P pZUbB hmDzD'}).text
        except:
            description = ""
        #Fetch Place Rating
        try:
            rating = len(place.find_all('path',attrs={'d':'M 12 0C5.388 0 0 5.388 0 12s5.388 12 12 12 12-5.38 12-12c0-6.612-5.38-12-12-12z'}))
        except:
            rating = 0
        
        rdict['image'] = imageUrl
        rdict['place'] = placeName
        rdict['link'] = onClickLink
        rdict['description'] = description
        rdict['rating'] = rating
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

def fetchTours(url):
    arr=[]
    r = requests.get(url,  headers={'User-Agent': "Mozilla/5.0"})
    soup = bs(r.content, 'html.parser')

    for article in soup.find_all('article',attrs={'class':'GTuVU XJlaI rHoxO'}):
        dict={}
        try:
            dict['image'] = article.find('picture',attrs={'class':'NhWcC _R'}).img['src']
        except:
            dict['image'] = ""

        try:
            dict['title'] = article.find('div',attrs={'class':'XfVdV o AIbhI'}).text
        except:
            dict['title'] = ""   

        try:
            dict['rating'] = article.find('div',attrs={'class','jVDab o W f u w JqMhy'}).svg['aria-label']
        except:
            dict['rating'] = "" 
        
        try:
            dict['added-by'] = article.find('div',attrs={'class','biGQs _P pZUbB hmDzD'}).a.text
        except:
            dict['added-by'] = ""

        try:
            dict['type'] = article.find_all('div',attrs={'class':'biGQs _P pZUbB hmDzD'})[2].text
        except:
            dict['type'] = ""

        try:
            dict['time'] = article.find_all('div',attrs={'class':'biGQs _P pZUbB hmDzD'})[3].text
        except:
            dict['time'] = ""   

        
        # dict['rating'] = len(article.find_all('path',attrs={'d':'M 12 0C5.388 0 0 5.388 0 12s5.388 12 12 12 12-5.38 12-12c0-6.612-5.38-12-12-12z'}))
        
        
        
        try:
            dict['description'] = article.find('span',attrs={'class':'SwTtt'}).text
        except:
            dict['description'] = ""
        
        try:
            dict['subInfo1'] = article.find_all('span',attrs={'class':'biGQs _P pZUbB egaXP hmDzD'})[0].text
        except:
            dict['subInfo1'] = ""
        try:
            dict['subInfo2'] = article.find('div',attrs={'class':'GvxaA'}).span.text
        except:
            dict['subInfo2'] = ""

        try:
            dict['amount-per-adult'] = article.find('div',attrs={'class':'biGQs _P fiohW avBIb ngXxk'}).text
        except:
            dict['amount-per-adult'] = ""

        try:
            dict['link'] = "https://www.tripadvisor.in"+article.find('a',attrs={'class':'rmyCe _G B- z _S c Wc wSSLS jWkoZ XDcOZ'})['href']
        except:
            dict['link'] = ""

        # print(article.find('div',attrs={'class':'GvxaA'}).span.text)
        print("\n******************************\n")
        

        arr.append(dict)

    # names=[]
    # for name in soup.find_all('div',attrs={'class':'XfVdV o AIbhI'}):
    #     names.append(name.text)
    #     # print(name.text)
    #     # print("\n******************************\n")
    # # print(names)

    # images=[]

    # for image in soup.find_all('picture',attrs={'class':'NhWcC _R mdkdE'}):
    #     # images.append(image.img['src'])
    #     print(image)
    #     print("\n******************************\n")

    return arr

@app.route('/tours',methods=['POST'])
def getTours():
    url = request.form.get('url')
    # time.sleep(2) # to limit the number of requests
    data = fetchTours(url)
    return jsonify(data)


@app.errorhandler(500)
def page_not_found(e):
    print(e)
    return jsonify({'error': 'Something went wrong'}), 500


if __name__ == '__main__':
    app.run()