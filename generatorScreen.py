import random
import os
from PIL import ImageTk, Image
####################################
# generator mode
####################################

# CITATION: 15-112 course website
# reads files
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
        
# CITATION : 15-112 website  
# writes files
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)
        
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
            
# checks if profile was previously saved and loads that information in saved outfits
def loadsaved(data):
    if data.name != "":
        files = listFiles('Saved Outfits')
        filename = 'Saved Outfits/' + data.name + ".txt"
        for item in files:
            if item == filename:
                print('we found the file')
                newoutfits = readFile(filename)
                for outfit in newoutfits.splitlines():
                    top,bottom = outfit.split(',')
                    if (top,bottom) not in data.savedoutfits:
                        data.savedoutfits.add((top,bottom))   
def convertpacked(data):
    for filename in data.packeditems:
        item = Image.open(filename)
        item = item.resize((150,150), Image.ANTIALIAS)
        item_tk = ImageTk.PhotoImage(item)
        if item_tk not in data.convertedpacked:
            data.convertedpacked.append(item_tk)
            
# writes new file with person's saved outfits
def saveprofile(data):
    for outfit in data.savedoutfits:
        top,bottom = outfit[0],outfit[1]
        path = "Saved Outfits/" + data.name + ".txt"
        with open(path, 'a') as f:
            f.write(str(top) + "," + str(bottom) + '\n')

def convertsavedoutfit(data):
    data.convertedsaved = []
    for outfit in data.savedoutfits:
        topfile, bottomfile = outfit[0], outfit[1]
        top, bottom = Image.open(topfile), Image.open(bottomfile)
        top = top.resize((150,150), Image.ANTIALIAS)
        top_tk = ImageTk.PhotoImage(top)
        bottom = bottom.resize((150,150), Image.ANTIALIAS)
        bottom_tk = ImageTk.PhotoImage(bottom)
        data.convertedsaved.append((top_tk,bottom_tk))
                
def createRightArrow(canvas,data,x,y):
    canvas.create_polygon(x,y,x,y+data.height//30,x+data.width//20,y+data.height//60,fill = 'black')

def createLeftArrow(canvas,data,x,y):
    canvas.create_polygon(x,y,x,y+data.height//30,x-data.width//20,y+data.height//60,fill = 'black')

# generates a random new outfit, making sure its not the same as present
def randomize(data):
    data.topcount = random.randint(0,len(data.tops)-1)
    data.bottomcount = random.randint(0,len(data.bottoms)-1)

def generatorKeyPressed(event,data):
    if event.keysym == "Left":
        data.mode = "splashScreen"
        
def generatorMousePressed(event, data):
    # click top right arrow
    if 4*data.width//5 <= event.x <= 17*data.width//20 and 0.35*data.height <= event.y <= 0.35*data.height + data.height//30:
        data.topcount +=1 

    # click top left arrow
    if  3*data.width//20 <= event.x <= data.width//5 and 0.35*data.height <= event.y <= 0.35*data.height + data.height//30:
        data.topcount -=1 

    # click bottom right arrow
    if 4*data.width//5 <= event.x <= 17*data.width//20 and 0.75*data.height <= event.y <= 0.75*data.height + data.height//30:
        data.bottomcount +=1 

    # click bottom left arrow
    if  3*data.width//20 <= event.x <= data.width//5 and 0.75*data.height <= event.y <= 0.75*data.height + data.height//30:
        data.bottomcount -=1 

    # click randomize button
    if 0.25*data.width < event.x < 0.45*data.width and 0.92*data.height < event.y < 0.98*data.height:
        randomize(data)
        
    # click save outfit button
    if 0.55*data.width < event.x < 3*data.width//4 and 0.92*data.height < event.y < 0.98*data.height:
        data.savedoutfits.add((data.tops[data.topcount % len(data.tops)], data.bottoms[data.bottomcount % len(data.bottoms)]))
        
    # click saved outfits
    if 0.8*data.width <= event.x <= data.width and 0.9*data.height <= event.y <= data.height:
        loadsaved(data)
        convertsavedoutfit(data)
        if data.savedoutfits != set():
            data.mode = "savedOutfits"
        
    # click recommended button
    if 0.8*data.width <= event.x <= data.width and 0.8*data.height <= event.y <= 0.9*data.height:
        data.mode = "recommended"
        
    # click personalize button
    if 0 <= event.x <= 0.2*data.width and 0.9*data.height <= event.y <= data.height:
        data.mode = "personalize"

    # click save profile button
    if 0 <= event.x <= 0.2*data.width and 0.8*data.height <= event.y <= 0.9*data.height:
        saveprofile(data)
    
    # click on suitcase
    if (0.9*data.width - data.width//8) <= event.x <= (0.9*data.width + data.width//8) and (0.15*data.height - data.width//8) <= event.y <= (0.15*data.height + data.width//8):
        print('hiiiii')
        convertpacked(data)
        data.mode = "suitcase"
        
    # click on shopping bag
    if (0.1*data.width-data.width//8) <= event.x <= (0.1*data.width+data.width//8) and (0.15*data.height - data.width//8) <= event.y <= (0.15*data.height + data.width//8):
        print('helloooo')
        data.mode = "shopping"
    
    # click pack top
    if data.width//4 <= event.x <= 0.45*data.width and 0.52*data.height <= event.y <= 0.58*data.height:
        data.packeditems.add(data.tops[data.topcount % len(data.tops)])

    # click pack bottom
    if 0.55*data.width <= event.x <= 0.75*data.width and 0.52*data.height <= event.y <= 0.58*data.height:
        data.packeditems.add(data.bottoms[data.bottomcount % len(data.bottoms)])
    
def generatorRedrawAll(canvas, data):
    # draw in canvas
    canvas.create_rectangle(0,0,data.width,data.height, fill = 'lavender')
    canvas.create_rectangle(data.width//4,data.height//5,3*data.width//4,data.height//2, fill = 'snow')
    canvas.create_rectangle(data.width//4,3*data.height//5,3*data.width//4,9*data.height//10, fill = 'snow')
    canvas.create_text(data.width//2, 0.15*data.height, text = "OUTFIT GENERATOR!", font = "Courier 20")
    
    # Randomize button
    canvas.create_rectangle(data.width//4, 0.92*data.height,0.45*data.width,0.98*data.height, fill = 'pink')
    canvas.create_text(0.35*data.width, 0.95*data.height, text = "Randomize!", font = "Courier 15")
    
    # Save Outfit button
    canvas.create_rectangle(0.55*data.width, 0.92*data.height,3*data.width//4,0.98*data.height, fill = 'pink')
    canvas.create_text(0.65*data.width, 0.95*data.height, text = "Save Outfit!", font = "Courier 15") 

    # Saved Oufits button
    canvas.create_rectangle(0.8*data.width, 0.9*data.height, data.width, data.height, fill = 'misty rose')
    canvas.create_text(0.9*data.width, 0.95*data.height, text = "Saved Outfits", font = "Courier 15")
    
    # Personalize button
    canvas.create_rectangle(0,0.9*data.height,0.2*data.width,data.height, fill = 'misty rose')
    canvas.create_text(0.1*data.width,0.95*data.height,text = "Personalize", font = "Courier 15")
    
    # Recommended button
    canvas.create_rectangle(0.8*data.width,0.8*data.height,data.width,0.9*data.height, fill = 'azure')
    canvas.create_text(0.9*data.width,0.85*data.height,text = "Recommended", font = "Courier 15")
    
    # Save Profile button
    canvas.create_rectangle(0,0.8*data.height,0.2*data.width,0.9*data.height, fill = 'azure')
    canvas.create_text(0.1*data.width,0.85*data.height,text = "Save Profile", font = "Courier 15")
    
    # create top arrows
    createRightArrow(canvas,data,4*data.width//5,0.35*data.height)
    createLeftArrow(canvas,data,data.width//5,0.35*data.height)
   
    # create bottom arrow
    createRightArrow(canvas,data,4*data.width//5,0.75*data.height)
    createLeftArrow(canvas,data,data.width//5,0.75*data.height)
    
    # draw bottom image
    canvas.create_image(data.width//2,0.75*data.height,image = data.bottomlist[data.bottomcount % len(data.bottomlist)])
    
    # draw top image 
    canvas.create_image(data.width//2,0.35*data.height,image = data.toplist[data.topcount % len(data.toplist)])

    # draw suitcase
    canvas.create_image(0.9*data.width, 0.15*data.height, image = data.suitcase)
    
    # draw shopping bag
    canvas.create_image(0.1*data.width,0.15*data.height,image = data.shopping)
    
    # pack top button
    canvas.create_rectangle(data.width//4, 0.52*data.height,0.45*data.width,0.58*data.height, fill = 'pink')
    canvas.create_text(0.35*data.width, 0.55*data.height, text = "Pack Top", font = "Courier 15")
    
    # pack bottom button
    canvas.create_rectangle(0.55*data.width,0.52*data.height,0.75*data.width,0.58*data.height, fill = 'pink')
    canvas.create_text(0.65*data.width,0.55*data.height,text = "Pack Bottom", font = "Courier 15")
    
    