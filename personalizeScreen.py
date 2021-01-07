from generatorScreen import createLeftArrow
from weather import Weather, Unit
import os
import requests, json 
import string
from PIL import ImageTk, Image
import numpy as np
import cv2 as cv
from bs4 import BeautifulSoup
import urllib

####################################
# weather mode
####################################
# uses api to get weather and condition
def getWeather(data):
    # personal api key
    key = "db0b40809ea4b051bad95e4f5e5ce755"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    # get user location
    location = data.city
    # complete url to call
    complete_url = base_url + "appid=" + key + "&q=" + location + "&units=imperial"
    # make api request
    response = requests.get(complete_url) 
    # convert json respond to python format
    x = response.json()
    # make sure the city name was found
    if x["cod"] != "404":
        # save current temp
        data.currtemp = str(x["main"]["temp"])
        data.condition = str(x["weather"][0]["main"])
        
# helps get city when user is typing
def getCity(letter, data):
    data.city += letter
'''
# helps get price when user is typing
def getPrice(value,data):
    data.maxprice +=value
'''     
# CITATION : 15-112 website  
# returns list of all the files in a folder
def listFiles(path):
    if os.path.isfile(path):
        return [ path ]
    else:
        files = [ ]
        for filename in os.listdir(path):
            files += listFiles(path + "/" + filename)
        return files
        
# CITATION : 15-112 website          
# removes DS extraneous files
def removeTmpFiles(path):
    if path.split("/")[-1] == '.DS_Store':
        os.remove(path)
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            removeTmpFiles(path + "/" + filename) 
              

def convertoutfit(data):
    for outfit in data.newrecoutfit:
        topfile, bottomfile = outfit[0], outfit[1]
        top, bottom = Image.open(topfile), Image.open(bottomfile)
        top = top.resize((150,150), Image.ANTIALIAS)
        top_tk = ImageTk.PhotoImage(top)
        bottom = bottom.resize((150,150), Image.ANTIALIAS)
        bottom_tk = ImageTk.PhotoImage(bottom)
        data.finaloutfits.append((top_tk,bottom_tk))
'''
def findprice(url): 
    page = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'}) 
    infile = urllib.request.urlopen(page).read()
    data = infile.decode('ISO-8859-1') # Read the content as string decoded with ISO-8859-1
    soup = BeautifulSoup(data, 'html.parser')
    div_1 = soup.find("div", {"class": "psp-mobile-layout"}).find("span", {"class": "psp-product-saleprice"})
    if div_1 != None:
        div = div_1
    else:
        div = soup.find("div", {"class": "psp-mobile-layout"}).find_all("span", {"class": "psp-product-regularprice"})
        div = div[1]
    for item in div:
        price = item
        return price
        
def checkprice(data,topfile, bottomfile):
    urltop = data.topsites[topfile]
    urlbottom = data.bottomsites[bottomfile]
    topprice = float(findprice(urltop))
    bottomprice = float(findprice(urlbottom))
    outfitprice = topprice + bottomprice
    print(topfile,bottomfile,outfitprice, data.maxprice)
    if outfitprice <= float(data.maxprice):
        return True
'''            
# CITATION: https://stackoverflow.com/questions/12187354/get-rgb-value-opencv-python
def colorfinder(data, filename):
    image = cv.imread(filename)
    b1,g1,r1 = int(image[400,200,0]),int(image[400,200,1]),int(image[400,200,2])
    b2,g2,r2 = int(image[500,500,0]),int(image[500,500,1]),int(image[500,500,2])
    b3,g3,r3 = int(image[600,600,0]),int(image[600,600,1]),int(image[600,600,2])
    b4,g4,r4 = int(image[700,700,0]),int(image[700,700,1]),int(image[700,700,2])
    b5,g5,r5 = int(image[800,800,0]),int(image[800,800,1]),int(image[800,800,2])
    b6,g6,r6 = int(image[650,700,0]),int(image[650,700,1]),int(image[650,700,2])
    blueval = (b1+b2+b3+b4+b5+b6)//6
    greenval = (g1+g2+g3+g4+g5+g6)//6
    redval = (r1+r2+r3+r4+r5+r6)//6
    return blueval, greenval, redval
    
# compares two colors and returns False if colors are too close
def colorcomparision(data,topfile,bottomfile):
    b1, g1, r1 = colorfinder(data, topfile)
    b2, g2, r2 = colorfinder(data, bottomfile)
    if abs(b1-b2) <= 25 and abs(g1-g2) <= 25 and abs(r1-r2) <= 25:
        return False
    return True
    
# CITATION: https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html
def haspattern(filename):
    im = cv.imread(filename)
    blurred = cv.GaussianBlur(im,(5,5),0)
    imgray = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) >= 750: return True
    else: return False
        
# recommends tops based on the temperature    
def recommendtops(data):
    removeTmpFiles("tops")
    mytops = listFiles("tops")
    for filename in mytops:
        if float(data.currtemp) <= 40:
            if "sweatshirt" in filename:
                data.rectops.append(filename)
            elif "sweater" in filename:
                data.rectops.append(filename)
        elif 40 <= float(data.currtemp) < 60:
            if "sweatshirt" in filename:
                data.rectops.append(filename)
            elif "buttondown" in filename:
                data.rectops.append(filename)
            elif "sweater" in filename:
                data.rectops.append(filename)
            elif "long" in filename:
                data.rectops.append(filename)
        elif float(data.currtemp) >= 60:
            if "tank" in filename: 
                data.rectops.append(filename)

# recommends bottoms based on the temperature       
def recommendbottoms(data):
    removeTmpFiles("bottoms")
    mybottoms = listFiles("bottoms")
    for filename in mybottoms:
        if float(data.currtemp) <= 60:
            if "jeans" in filename:
                data.recbottoms.append(filename)
            elif "pants" in filename:
                data.recbottoms.append(filename)
        elif float(data.currtemp) > 60:
            if "skirt" in filename:
                data.recbottoms.append(filename)
            elif "short" in filename:
                data.recbottoms.append(filename)
                
# allows a user to type in city name    
def personalizeKeyPressed(event,data):
    if data.typing == True:
        # check if its actually a letter though!
        if event.keysym in string.ascii_letters:
            getCity(event.keysym,data)
        elif event.keysym == 'space':
            getCity(" ",data)
        elif event.keysym == 'BackSpace':
            data.city = data.city[:-1]
        elif event.keysym == 'Return':
            getWeather(data)
            data.typing = False
'''
    elif data.typingprice == True:
        # check if its actually a number though!
        if event.keysym in string.digits or event.keysym in string.punctuation:
            getPrice(event.keysym,data)
        elif event.keysym == 'space':
            getPrice(" ",data)
        elif event.keysym == 'BackSpace':
            data.maxprice = data.maxprice[:-1]
        elif event.keysym == 'Return':
            data.typingprice = False
'''           
def personalizeMousePressed(event,data):
    # click back button to get outfit results
    if 0.15*data.width - data.width//20 <= event.x <= 0.15*data.width and 0.1*data.height-data.scroll2Y <= event.y <= 0.1*data.height + data.height//30 - data.scroll2Y:
        # creates list of recommended tops by filename
        recommendtops(data)
        # creates list of recommended bottoms by filename
        recommendbottoms(data)
        # creates list of all possible outfits combos using filenames
        for top in data.rectops:
            for bottom in data.recbottoms:
                data.recoutfit.append((top,bottom))
        # compares the colors of top & bottom and adds it to newrecoutfit if its a good combo
        for outfit in data.recoutfit:
            topfile, bottomfile = outfit[0], outfit[1]
            if colorcomparision(data,topfile,bottomfile) == True:
                if not (haspattern(topfile) and haspattern(bottomfile)):
                    if data.maxprice != "":
                        outfitprice = float(data.topprices[topfile]) + float(data.bottomprices[bottomfile])
                        if outfitprice <= float(data.maxprice):
                            data.newrecoutfit.append(outfit)
        # converts newrecoutfit list to tkinter/PIL displayable format
        convertoutfit(data)
        data.mode = 'generator'
    # goes into typing mode when user clicks location box
    elif data.width//4 <= event.x <= 3*data.width//4 and data.height//3 <= event.y <= data.height//3+data.height//10:
        data.typing = True
    #elif data.width//4 <= event.x <= 3*data.width//4 and 0.85*data.height <= event.y <= 0.95*data.height:
        #data.typingprice = True
    else: data.typing = False
    
def personalizeRedrawAll(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height,fill= 'peach puff')
    canvas.create_text(data.width//2, 0.15*data.height, text = "WEATHER", font = "Courier 20")
    canvas.create_text(data.width//2, 0.25*data.height, text = "Click on the location box and begin typing", font = "Courier 18")
    # creates back arrow
    createLeftArrow(canvas,data,0.15*data.width,0.1*data.height)
    canvas.create_rectangle(data.width//4,data.height//3, 3*data.width//4, data.height//3+data.height//10, fill = 'snow')
    canvas.create_text(data.width//2,data.height//3+data.height//20, text = "Location: " + data.city, font = 'Courier 18')
    canvas.create_rectangle(data.width//4,data.height//3+data.height//10, 3*data.width//4, data.height//3+2*data.height//10, fill = 'snow')
    canvas.create_text(data.width//2,data.height//3+3*data.height//20, text = "Temperature: " + data.currtemp + " F", font = 'Courier 18')
    canvas.create_rectangle(data.width//4,data.height//3+2*data.height//10, 3*data.width//4, data.height//3+3*data.height//10, fill = 'snow')
    canvas.create_text(data.width//2,data.height//3+5*data.height//20, text = "Condition: " + data.condition, font = 'Courier 18')
    '''
    canvas.create_text(data.width//2,0.69*data.height, text = "BUDGET", font = 'Courier 20')
    canvas.create_text(data.width//2,0.79*data.height, text = "Click on the price box and begin typing", font = 'Courier 18')
    canvas.create_rectangle(data.width//4,0.85*data.height, 3*data.width//4, 0.95*data.height, fill = 'snow')
    canvas.create_text(data.width//2,0.9*data.height, text = "Max Price: $" + data.maxprice, font = 'Courier 18')
    '''

   
    

    