from generatorScreen import createLeftArrow
####################################
# recommended mode
####################################
# scrolling up and down
def recommendedKeyPressed(event,data):
    if event.keysym == "Up":
        if data.scroll2Y > 0:
            data.scroll2Y -=10
    elif event.keysym == "Down":
        if data.scroll2Y < (5*data.height//8)*(len(data.finaloutfits)//3):
            data.scroll2Y +=10
    elif event.keysym == "Left":
        data.mode = 'generator'

# if user clicks arrow, go back to generator screen
def recommendedMousePressed(event,data):
    if 0.15*data.width - data.width//20 <= event.x <= 0.15*data.width and 0.1*data.height-data.scroll2Y <= event.y <= 0.1*data.height + data.height//30 - data.scroll2Y:
        data.mode = 'generator'
    
def recommendedRedrawAll(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height,fill = "thistle1")
    canvas.create_text(data.width//2, 0.12*data.height - data.scroll2Y, text = "RECOMMENDED OUTFITS", font = "Courier 20")
    # creates arrow
    createLeftArrow(canvas,data,0.15*data.width,0.1*data.height - data.scroll2Y)
    # draws grid
    j = 0.12*data.height + data.height//16
    i = 1*data.width//16
    index = 0 
    while index <= len(data.finaloutfits)-1:    
        i = 1*data.width//16
        while i < 15*data.width//16:
            # draws recommended outfits
            if index < len(data.newrecoutfit):
                canvas.create_image(i + data.width//8,j + data.height//8 - data.scroll2Y,image = data.finaloutfits[index][0])
                canvas.create_image(i + data.width//8,j + 3*data.height//8 - data.scroll2Y,image = data.finaloutfits[index][1])
                index +=1
            i += 5*data.width//16 
        j += 5*data.width//8 
            
        