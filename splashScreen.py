import string
####################################
# slashScreen mode
####################################
# helps get name when user is typing
def getName(letter, data):
    data.name += letter

# enter generator mode once user clicks enter or allow user to type name
def splashScreenKeyPressed(event, data):
    if event.keysym == "Return" or event.keysym == "Enter":
        data.mode = "generator"
    # check if its actually a letter though!
    elif event.keysym in string.ascii_letters:
        getName(event.keysym,data)
    elif event.keysym == 'space':
        getName(" ",data)
    elif event.keysym == 'BackSpace':
        data.name = data.name[:-1]

# click in box to allow user to type name
def splashScreenMousePressed(event,data):
    if data.width//4 <= event.x <= 3*data.width//4:
        data.typing2 = True
    
def splashScreenRedrawAll(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height, fill = 'pale turquoise')
    canvas.create_text(data.width/2, data.height/2-40, text="Welcome to your outfit generator!", font="Courier 26 bold")
    canvas.create_text(data.width/2, data.height/2+20,
                       text="Press enter to begin!", font="Courier 20")
    canvas.create_rectangle(data.width//4,2*data.height//3, 3*data.width//4, 2*data.height//3+data.height//10, fill = 'snow')
    canvas.create_text(data.width//2, 2*data.width//3+data.height//20, text = "Enter Name: " + data.name, font = "Courier 18")

