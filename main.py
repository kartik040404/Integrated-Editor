from tkinter import *
from tkinter import ttk
import subprocess
from tkinter.filedialog import askopenfilename,asksaveasfilename
import pyautogui as pag
from tkinter import colorchooser
from tkfontchooser import askfont
from gtts import  gTTS
import os
import wikipedia as wiki
from tkinter import scrolledtext
import tkinter.messagebox as tmsg
import cv2
import pytesseract


#editor interface configration
root = Tk()
root.title("Integrated Editor (IE)")
root.state("zoomed")
photo = PhotoImage(file = "img1.png")
root.iconphoto(False, photo)
root.resizable(0,0)

#Python functions
file_path = ''
#myfont=("Times New Roman", 12, "bold")


def set_file_path(path):
    global file_path
    file_path = path


def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        input_data.delete('1.0', END)
        input_data.insert('1.0', code)
        set_file_path(path)


def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = input_data.get('1.0', END)
        file.write(code)
        set_file_path(path)


def run():
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your code')
        text.pack()
        return
    command = f'python {file_path}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    con.insert('1.0', output)
    con.insert('1.0',  error)
def cut():
    pag.hotkey("ctrl","x")

def copy():
    pag.hotkey("ctrl","c")

def paste():
    pag.hotkey("ctrl","v")

def all():
    pag.hotkey("ctrl","a")

def find():
    pag.hotkey("ctrl","f")

def color():
    mycolor=colorchooser.askcolor(initialcolor='#ff0000')
    col=mycolor[1]
    print(mycolor)
    input_data.config(fg=col)


def action():
    file=askopenfilename()
    img=cv2.imread(file)
    tmsg.showinfo("submit","submitted sucessfully")
    config = ('-l eng --oem 1 --psm 3')
    # pytessercat
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
    data = pytesseract.image_to_string(img, config=config)
    # print text
    global data1
    print(data)
    data1 = data.replace('{} @ ® .$ >>> ','\n')
    input_data.delete("0.0",END)
    input_data.insert(0.0,data1)


def font_changed():
    myfont=askfont(root)
    print(myfont)
    nFont=(myfont['family'],myfont['size'],myfont['slant'] or myfont['weight'])
    print(nFont)
    input_data['font']=nFont

def Change_theme(x):
    if x==1:
        input_data.config(bg="#262626",fg="white",font=('consolas 12'),cursor="arrow white")
        text_area.config(bg="#262626",fg="white",font=('consolas 12'),cursor="arrow white")
        con.config(bg="#262626",fg="white",font=('consolas 12'),cursor="arrow white")
        l1.config(bg="#808080",fg="white")
        button.config(bg="#808080",fg="white")


    else:
        input_data.configure(background="white",fg="black")
        text_area.configure(bg="white",fg="black")
        con.configure(bg="white",fg="black")



# Audio Reading
is_playing = False
def play_pause():
    temp=Toplevel()
    play_button = Button(temp, text="Play", font=("Arial", 12), command=play_pause, bg="green", fg="white")
    play_button.pack(side=LEFT, padx=10, pady=10)

    pause_button = Button(temp, text="Pause", font=("Arial", 12), command=play_pause, bg="red", fg="white")
    pause_button.pack(side=LEFT, padx=10, pady=10)
    pause_button.config(state="disabled")
    global is_playing
    if not is_playing:
        content = input_data.get(1.0, END)
        if content:
            is_playing = True
            play_button.config(text="Pause")
            speech = gTTS(content)
            speech.save("text.mp3")
            os.system("start text.mp3")
    else:
        is_playing = False
        play_button.config(text="Play")
        os.system("taskkill /f /im Music.UI.exe")


#Data rendering
def fetch_wiki_data():
    search_query = enter.get()

    try:
        result = wiki.summary(search_query)
        text_area.delete(1.0, END)
        text_area.insert(INSERT, result)

    except wiki.exceptions.DisambiguationError as e:

        # Limiting the number of option for simplicity
        options = e.options[:30]
        text_area.delete(1.0, END)
        text_area.insert(INSERT, f'Please choose one of the option : \n\n')

        for i, option in enumerate(options):
            text_area.insert(INSERT, f'{i + 1}. {option}\n')

    except wiki.exceptions.PageError:
        text_area.delete(1.0, END)
        text_area.insert(INSERT, f'No result found for \'{search_query}\'.')


# Creating Menubar
menubar = Menu(root,activebackground="#98F5FF")

# Adding File Menu and commands
file = Menu(menubar, tearoff=0,bg="#98F5FF")
menubar.add_cascade(label='File', menu=file)
file.add_command(label='New File', command=None)
file.add_command(label='Open...', command=open_file)
file.add_command(label='Save', command=save_as)
file.add_separator()
file.add_command(label='Exit', command=root.destroy)

# Adding Edit Menu and commands
edit = Menu(menubar, tearoff=0,bg="#98F5FF")
menubar.add_cascade(label='Edit', menu=edit)
edit.add_command(label='Cut', command=cut)
edit.add_command(label='Copy', command=copy)
edit.add_command(label='Paste', command=paste)
edit.add_command(label='Select All', command=all)
edit.add_separator()
edit.add_command(label='Find...', command=None)

#Adding run menu
run_bar = Menu(menubar, tearoff=0,bg="#98F5FF")
run_bar.add_command(label='Run', command=run)
menubar.add_cascade(label='Run', menu=run_bar)

#adjusting properties
layout_bar = Menu(menubar, tearoff=0,bg="#98F5FF")
layout_bar.add_command(label='color', command=color)
layout_bar.add_command(label="Fonts",command=font_changed)
menubar.add_cascade(label='View', menu=layout_bar)

theme= Menu(menubar, tearoff=0,bg="#98F5FF")
menubar.add_cascade(label='Theme', menu=theme)
theme.add_radiobutton(label="Dark mode",command=lambda x=1:Change_theme(x))
theme.add_radiobutton(label="White mode",command=lambda x=2:Change_theme(x))

#Adding tools
tool_bar = Menu(menubar, tearoff=0,bg="#98F5FF")
tool_bar.add_command(label='Image Processing', command=action)
tool_bar.add_separator()
tool_bar.add_command(label='Data Rendering', command=None)
tool_bar.add_separator()
tool_bar.add_command(label='Audio reading', command=play_pause)
menubar.add_cascade(label='Tools', menu=tool_bar)


# Adding Help Menu
help_ = Menu(menubar, tearoff=0,bg="#98F5FF")
menubar.add_cascade(label='Help', menu=help_)
help_.add_command(label='Tk Help', command=None)
help_.add_command(label='Demo', command=None)
help_.add_separator()
help_.add_command(label='About Tk', command=None)



# display Menu
root.config(menu=menubar)

pane=PanedWindow(root,width=500)
pane.pack(fill="both",expand=1,side=LEFT)

input_data=scrolledtext.ScrolledText(pane,bd=7)
pane.add(input_data)


pane1=PanedWindow(pane,orient=VERTICAL,width=200)
pane.add(pane1)

l1=Label(pane1,text="Console")
pane1.add(l1)

con=Text(pane1,height=10)
pane1.add(con)

label = Label(pane1, text = 'Enter search query : ')
pane1.add(label)

enter = Entry(pane1)
pane1.add(enter)

# Create a button to fetch Wikipedia data
button=Button(pane1, text = 'Fetch Data',bd=5, command = fetch_wiki_data)
pane1.add(button)

# Create a scrolled text widget to display the fetch data
text_area = scrolledtext.ScrolledText(pane1, x = 80, y = 20,)
pane1.add(text_area)


root.mainloop()
