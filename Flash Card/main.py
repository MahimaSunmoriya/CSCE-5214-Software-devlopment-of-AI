######################################### IMPORT ALL IMPORTANT LIBRARY ###############################################
from tkinter import *
BACKGROUND_COLOR = "#B1DDC6"
import pandas as pd
import random 
import os.path

############################################# Tkinter Window ############################################################

window = Tk()
window.title("French Word Flash Crads")
window.config(padx=10, pady=10)
window['bg'] = '#B1DDC6'

########################## CHECK IF FILE EXIST OR EMPTY . IF NOT EXIST CREATE NEW ONE WITH FRENCH CSV #######################
if (os.path.exists("./words_to_learn.csv")):
    if os.stat("./words_to_learn.csv").st_size == 0:
        french_dataframe = pd.read_csv('./french_words.csv')
        french_dataframe.to_csv('./words_to_learn.csv' , index =False)
    words_to_learn_df = pd.read_csv('./words_to_learn.csv')
    
else:
    french_dataframe = pd.read_csv('./french_words.csv')
    words_to_learn_df = french_dataframe
    words_to_learn_df.to_csv('./words_to_learn.csv' , index =False)


######################### Loading dataframe to dictionary ##############################################
learn_dataframe = pd.DataFrame(words_to_learn_df, columns=['French', 'English'])
learn_dic =learn_dataframe.to_dict('records')
card_title = list(random.choice(learn_dic))
global random_key
random_key = list((random.choice(learn_dic).values()))

########### Random WOrd select ##############
def random_new_word():
    canvas.itemconfig(canvas_image, image = front_img)
    card_title = list(random.choice(learn_dic))
    global random_key
    random_key = list((random.choice(learn_dic).values())) 
    word_title_label.config(background = 'white',fg = 'black', text = card_title[0])
    word_label.config(background = 'white',fg = 'black',text= random_key[0])
    cancel_flip_card(firstid)
    window.after(3000, flip_card)

############ RIGHT CLICK REMOVE WORD AND DISPLAY NEW WORD #####################   

def Right_click_action():
    global random_key
    learn_dic.remove({'French': random_key[0], 'English': random_key[1]})
    df = pd.DataFrame(list(learn_dic),columns= ['French', 'English'])
    df.to_csv('./words_to_learn.csv' , index =False)
    ### If there in no word left in words_to_learn.csv program end window closed#########        
    if(len(df)== 0):
        os.remove('./words_to_learn.csv')
        sys.exit()
    random_new_word()
    
####################################### Flip Card ####################################
def flip_card():
    canvas.itemconfig(canvas_image, image = back_img)
    word_title_label.config(background = '#91c2af', fg = 'white',text =card_title[1])
    word_label.config(background = '#91c2af', fg = 'white',text =random_key[1])

################################# Cancel window After ID ############################
def cancel_flip_card(id):
    if id is not None:
        window.after_cancel(id)
        id = None
        return id

########### UI ############################################################

firstid = None

#------------ Canvas 1 configuration -----------------------------------------
canvas = Canvas(height=540, width=800)
front_img = PhotoImage(file="./card_front.png")
back_img = PhotoImage(file = "./card_back.png")
canvas_image = canvas.create_image(410, 300, image=front_img)
canvas.grid(row=0,column=1)
canvas.configure(background = BACKGROUND_COLOR,border = 0, relief =RIDGE,highlightthickness = 0)

#---------------- Another canvas for button images --------------------------------------
canvas1 = Canvas(height =100, width= 800)
canvas1.grid(row= 1, column = 1)
canvas1.configure(background = BACKGROUND_COLOR,border = 0, relief =RIDGE,highlightthickness = 0)

#---------------- Cross and Right button ---------------------------------------------------

cross_img = PhotoImage(file = "./wrong.png")
cross_button = Button(canvas1,image= cross_img,highlightthickness = 0,command = random_new_word)
cross_button.grid(row = 1, column = 0,padx = 70, pady = 20)
cross_button.configure(background = BACKGROUND_COLOR, border = 0, highlightthickness = 0)

right_img = PhotoImage(file = "./right.png")
right_button = Button(canvas1,image= right_img,command = Right_click_action)
right_button.grid( row = 1, column = 1,padx = 70,pady = 20)
right_button.configure(background = BACKGROUND_COLOR, border = 0, highlightthickness = 0)

# ---------------- Text labels for Title and  Words -----------------------------------------
word_title_label = Label(canvas, text=card_title[0])
word_title_label.config(font=("Ariel", 40, "italic"),background = 'white', highlightthickness = 0)
#word_label.grid(row = 1 , column= 1)
word_title_label.place(relx=0.5, rely=0.3, anchor="center")

word_label = Label(canvas, text= random_key[0])
word_label.config(font=("Ariel", 60, "bold"),background = 'white',highlightthickness = 0)
#word_label.grid(row = 1 , column= 1)
word_label.place(relx=0.5, rely=0.6, anchor="center")

#------------------ Cancel window after Id first and then use Window after to flip -------------------
cancel_flip_card(firstid)
firstid = window.after(3000, flip_card) 

window.mainloop()
