from generatorScreen import createLeftArrow, createRightArrow
import string
####################################
# shopping mode
####################################
# helps get price when user is typing
def getPrice(value,data):
    data.maxprice +=value

# webscrapes price of item using url
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
        
# compares price of outfit to max price      
def checkprice(data,topfile, bottomfile):
    urltop = data.topsites[topfile]
    urlbottom = data.bottomsites[bottomfile]
    topprice = float(findprice(urltop))
    bottomprice = float(findprice(urlbottom))
    outfitprice = topprice + bottomprice
    print(topfile,bottomfile,outfitprice, data.maxprice)
    if outfitprice <= float(data.maxprice):
        return True
        
def shoppingKeyPressed(event,data):
    if data.typingprice == True:
        # check if its actually a number though!
        if event.keysym in string.digits or event.keysym in string.punctuation:
            getPrice(event.keysym,data)
        elif event.keysym == 'space':
            getPrice(" ",data)
        elif event.keysym == 'BackSpace':
            data.maxprice = data.maxprice[:-1]
        elif event.keysym == 'Return':
            data.typingprice = False

def shoppingMousePressed(event,data):
    # click on price box to type
    if data.width//4 <= event.x <= 3*data.width//4 and 0.4*data.height <= event.y <= 0.5*data.height:
        data.typingprice = True
    # click back button
    elif 0.15*data.width - data.width//20 <= event.x <= 0.15*data.width and 0.1*data.height-data.scrollY <= event.y <= 0.1*data.height + data.height//30 - data.scrollY:
        data.mode = 'generator'
    elif 0.85*data.width - data.width//20 <= event.x <= 0.85*data.width and 0.1*data.height-data.scrollY <= event.y <= 0.1*data.height + data.height//30 - data.scrollY:
        data.mode = 'shopoutfits'

def shoppingRedrawAll(canvas,data):
    createLeftArrow(canvas,data,0.15*data.width,0.1*data.height - data.scroll3Y)
    createRightArrow(canvas,data,0.85*data.width,0.1*data.height - data.scroll3Y)
    canvas.create_rectangle(0,0,data.width,data.height, fill= "thistle1")
    canvas.create_text(data.width//2, 0.15*data.height, text = "SHOPPING", font = "Courier 20")
    canvas.create_text(data.width//2,0.3*data.height, text = "Click on the price box and begin typing", font = 'Courier 16')
    canvas.create_text(data.width//2,0.35*data.height, text = "to set your max budget", font = 'Courier 16')
    # max price box
    canvas.create_rectangle(data.width//4,0.4*data.height, 3*data.width//4, 0.5*data.height, fill = 'snow')
    canvas.create_text(data.width//2,0.45*data.height, text = "Max Price: $" + data.maxprice, font = 'Courier 18')