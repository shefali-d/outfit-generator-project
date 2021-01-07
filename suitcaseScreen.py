from generatorScreen import createLeftArrow
from PIL import ImageTk, Image
            
####################################
# suitcase mode
####################################
def suitcaseMousePressed(event,data):
    # click on back button
    if 0.15*data.width - data.width//20 <= event.x <= 0.15*data.width and 0.1*data.height-data.scroll3Y <= event.y <= 0.1*data.height + data.height//30 - data.scroll3Y:
        data.mode = 'generator'

def suitcaseKeyPressed(event,data):
    if event.keysym == "Up":
        if data.scroll3Y > 0:
            data.scroll3Y -=10
    elif event.keysym == "Down":
        #if data.scroll3Y < (5*data.height//8)*(len(data.finaloutfits)//3):
            data.scroll3Y +=10
    elif event.keysym == "Left":
        data.mode = 'generator'
    
def suitcaseRedrawAll(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height, fill= "light salmon")
    canvas.create_text(data.width//2, 0.12*data.height - data.scroll3Y, text = "SUITCASE", font = "Courier 20")
    createLeftArrow(canvas,data,0.15*data.width,0.1*data.height - data.scroll3Y)
    j = 0.12*data.height + data.height//16
    i = 1*data.width//16
    index = 0 
    while index <= len(data.convertedpacked)-1:    
        i = 1*data.width//16
        while i < 15*data.width//16:
            # draws packed outfits
            if index < len(data.convertedpacked):
                canvas.create_image(i + data.width//8,j + data.height//8 - data.scroll3Y,image = data.convertedpacked[index])
                index +=1
            i += 5*data.width//16 
        j += 3*data.width//8 