## TP 3!
import module_manager
module_manager.review()

from tkinter import *
from PIL import ImageTk, Image
import glob
import random
from splashScreen import *
from generatorScreen import *
from savedOutfitsScreen import *
from personalizeScreen import *
from recommendedScreen import *
from suitcaseScreen import *
from shoppingScreen import *

####################################
# init
####################################

def init(data):
    data.mode = "splashScreen"
    data.savedoutfits = set()
    data.rectops = []
    data.recbottoms = []
    data.toplist = []
    data.bottomlist = []
    data.topcount = 0
    data.bottomcount = 0
    data.scrollY = 0
    data.scroll2Y = 0
    data.typing = False
    data.typing2 = False
    data.city = ""
    data.currtemp = ""
    data.condition = ""
    data.newrecoutfit = []
    data.recoutfit = []
    data.finaloutfits = []
    data.name = ""
    data.bottoms = []
    data.tops = []
    data.convertedsaved = []
    data.topsites= dict()
    data.bottomsites = dict()
    data.maxprice = ''
    data.typingprice = False
    data.topprices = dict()
    data.bottomprices = dict()
    data.packeditems = set()
    data.suitcase = ""
    data.shopping = ""
    data.scroll3Y = 0
    data.convertedpacked = []
        
    # CITATION: images taken from https://www.ae.com/
    # CITATION: inputting images code adapted from https://stackoverflow.com/questions/26392336/importing-images-from-a-directory-python
    # open/load bottoms
    # glob goes through a path
    for filename in glob.glob("bottoms/*.jpg"):
        data.bottoms.append(filename)
        # need to open images in init so they can process in time
        bottoms = Image.open(filename)
        # scales image to proper size
        bottoms = bottoms.resize((150,150), Image.ANTIALIAS)
        # converts to Tkinter compatible image
        bottoms_tk = ImageTk.PhotoImage(bottoms)
        # adds to list of bottoms
        data.bottomlist.append(bottoms_tk)
        
    # open/load tops
    for filename in glob.glob("tops/*.jpg"):
        data.tops.append(filename)
        tops = Image.open(filename)
        # scales image to proper size
        tops = tops.resize((150,150), Image.ANTIALIAS)
        tops_tk = ImageTk.PhotoImage(tops)
        data.toplist.append(tops_tk)
        
    
    suitcase = Image.open("suitcase.png")
    # scales image to proper size
    suitcase = suitcase.resize((75,75), Image.ANTIALIAS)
    suitcase_tk = ImageTk.PhotoImage(suitcase)
    data.suitcase = suitcase_tk

    shopping = Image.open("shoppingbag2.jpg")
    # scales image to proper size
    shopping = shopping.resize((75,75), Image.ANTIALIAS)
    shopping_tk = ImageTk.PhotoImage(shopping)
    data.shopping = shopping_tk
  
    # CITATION: 15-112 course website
    # reads files
    def readFile(path):
        with open(path, "rt") as f:
            return f.read()    
            
    # create dictionary matching filename to url
    topsites = readFile('topsites.txt')  
    topsites2 = topsites.split(',')
    for i in range(len(data.tops)):
        data.topsites[data.tops[i]] = topsites2[i]
    
    bottomsites = readFile('bottomsites.txt')  
    bottomsites2 = bottomsites.split(',')
    for i in range(len(data.bottoms)):
        data.bottomsites[data.bottoms[i]] = bottomsites2[i]

    def findprice(url): 
        page = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'}) 
        infile = urllib.request.urlopen(page).read()
        data = infile.decode('ISO-8859-1') # Read the content as string decoded with ISO-8859-1
        soup = BeautifulSoup(data, 'html.parser') # Parses through html text
        div_1 = soup.find("div", {"class": "psp-mobile-layout"}).find("span", {"class": "psp-product-saleprice"}) 
        if div_1 != None:
            div = div_1
        else:
            div = soup.find("div", {"class": "psp-mobile-layout"}).find_all("span", {"class": "psp-product-regularprice"})
            div = div[1]
        for item in div:
            price = item
            return price
    '''
    for top in data.tops:
        url = data.topsites[top]
        price = findprice(url)
        data.topprices[top] = price
        
    for bottom in data.bottoms:
        url = data.bottomsites[bottom]
        price = findprice(url)
        data.bottomprices[bottom] = price
    '''

####################################
# mode dispatcher
####################################
def mousePressed(event,data):
    if (data.mode == "splashScreen"): splashScreenMousePressed(event,data)
    elif (data.mode == "generator"): generatorMousePressed(event,data)
    elif (data.mode == "savedOutfits"): savedOutfitsMousePressed(event,data)
    elif (data.mode == "personalize"): personalizeMousePressed(event,data)
    elif (data.mode == "recommended"): recommendedMousePressed(event,data)
    elif (data.mode == "suitcase"): suitcaseMousePressed(event,data)
    elif (data.mode == "shopping"): shoppingMousePressed(event,data)

def keyPressed(event,data):
    if (data.mode == "splashScreen"): splashScreenKeyPressed(event,data)
    elif (data.mode == "savedOutfits"): savedOutfitsKeyPressed(event,data)
    elif (data.mode == "personalize"): personalizeKeyPressed(event,data)
    elif (data.mode == "recommended"): recommendedKeyPressed(event,data)
    elif (data.mode == "suitcase"): suitcaseKeyPressed(event,data)
    elif (data.mode == "shopping"): shoppingKeyPressed(event,data)
    
def redrawAll(canvas,data):
    if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas,data)
    elif (data.mode == "generator"): generatorRedrawAll(canvas,data)
    elif (data.mode == "savedOutfits"): savedOutfitsRedrawAll(canvas,data)
    elif (data.mode == "personalize"): personalizeRedrawAll(canvas,data)
    elif (data.mode == "recommended"): recommendedRedrawAll(canvas,data)
    elif (data.mode == "suitcase"): suitcaseRedrawAll(canvas,data)
    elif (data.mode == "shopping"): shoppingRedrawAll(canvas,data)
    
####################################
# animation starter code adapted from course website
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()

    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAllWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600,600)