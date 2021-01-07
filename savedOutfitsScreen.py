from generatorScreen import createLeftArrow
from PIL import ImageTk, Image
####################################
# savedOutfits mode
####################################
def convertsavedoutfit(data):
    for outfit in data.savedoutfits:
        topfile, bottomfile = outfit[0], outfit[1]
        top, bottom = Image.open(topfile), Image.open(bottomfile)
        top = top.resize((150,150), Image.ANTIALIAS)
        top_tk = ImageTk.PhotoImage(top)
        bottom = bottom.resize((150,150), Image.ANTIALIAS)
        bottom_tk = ImageTk.PhotoImage(bottom)
        if (top_tk,bottom_tk) not in data.convertedsaved:
            data.convertedsaved.append((top_tk,bottom_tk))
            
# allows user to go back to main generator screen
def savedOutfitsMousePressed(event,data):
    if 0.15*data.width - data.width//20 <= event.x <= 0.15*data.width and 0.1*data.height-data.scrollY <= event.y <= 0.1*data.height + data.height//30 - data.scrollY:
        data.mode = 'generator'
        
# allows user to scroll or go back a screen
def savedOutfitsKeyPressed(event,data):
    if event.keysym == "Up":
        if data.scrollY > 0:
            data.scrollY -=10
    elif event.keysym == "Down":
        #if data.scrollY < (5*data.height//8)*(len(data.savedoutfits)//3):
        data.scrollY +=10
    elif event.keysym == "Left":
        data.mode = 'generator'
    
def savedOutfitsRedrawAll(canvas,data): 
    canvas.create_rectangle(0,0,data.width,data.height, fill = 'lemon chiffon')
    canvas.create_text(data.width//2, 0.12*data.height - data.scrollY, text = "SAVED OUTFITS", font = "Courier 20")
    createLeftArrow(canvas,data,0.15*data.width,0.1*data.height - data.scrollY)
    # draws grid
    j = 0.12*data.height + data.height//16
    i = 1*data.width//16
    index = 0 
    while index <= len(data.convertedsaved)-1:    
        i = 1*data.width//16
        while i < 15*data.width//16:
            # draws saved outfits
            if index < len(data.convertedsaved):
                canvas.create_image(i + data.width//8,j + data.height//8 - data.scrollY,image = data.convertedsaved[index][0])
                canvas.create_image(i + data.width//8,j + 3*data.height//8 - data.scrollY,image = data.convertedsaved[index][1])
                index +=1
            i += 5*data.width//16 
        j += 5*data.width//8 
