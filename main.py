from tkinter import *
from tkinter import messagebox
import random

window = Tk()
window.config(padx=100, pady=50, bg="white")
window.option_add('*font', 'Ariel 15 ', )
window.title("Typing Speed Test")
wpm=0
accuracy=0
initial_text=[]
timer = 60

def speed_calc():
    global initial_text,correct_words_count, wrong_words_count,seconds, wpm,accuracy
    correct_words_count = 0
    wrong_words_count = 0
    user_entered_para = user_entry.get().split()
    matched_words = []
    wrong_words=[]
    mycorrectwords = ""
    mywrongwords=""

    for i in range(len(initial_text)):
        start_index = sample_text_text.search(initial_text[i], "1.0", stopindex="end", nocase=True)
        if start_index:
            end_index = f"{start_index}+{len(initial_text[i])}c"
            if i < len(user_entered_para):
                if user_entered_para[i] == initial_text[i].lower():
                    sample_text_text.tag_remove("no_match", start_index, end_index)
                    sample_text_text.tag_add("match", start_index, end_index)
                    matched_words.append(user_entered_para[i])
                    correct_words_count += 1
                else:
                    wrong_words.append(user_entered_para[i])
                    sample_text_text.tag_remove("match", start_index, end_index)
                    sample_text_text.tag_add("no_match", start_index, end_index)
                    wrong_words_count += 1
    try:

        for x in matched_words:
            mycorrectwords += x
        characters_count = len(mycorrectwords)
        wpm =round( (characters_count/5)/((60-seconds)/60))
        wpm_label.config(text=f"Net WPM:{wpm}")
        for y in wrong_words:
            mywrongwords += y
        wrongwordscharacter=len(mywrongwords)
        totalcharacter=wrongwordscharacter+characters_count
        accuracy=round((characters_count/totalcharacter)*100)
        accuracy_label.config(text=f"Accuracy:{accuracy}%")
    except ZeroDivisionError:
        pass
def clear():
    global initial_text,correct_words_count, wrong_words_count,seconds, wpm,accuracy,timer,timer_event
    sample_text_text.configure(state=NORMAL, )
    initial_text=[]
    correct_words_count=0
    wrong_words_count=0
    seconds=0
    wpm=0
    accuracy=0
    timer=60
    sample_text_text.delete("1.0",END)
    text_string = ""
    with open("simple_english_words.txt", mode="r") as ft:
        words_file = ft.readlines()
    for i in range(0, 45):
        initial_text.append(random.choice(words_file).split("\n")[0])
    # print(initial_text)
    for i in range(0, 45):
        text_string += initial_text[i].lower() + " "
    sample_text_text.insert(1.0, text_string, )
    sample_text_text.configure(state=DISABLED, )
    timer_label.config(text=f"Timer: {timer%60:02d}")
    wpm_label.config(text=f"Net WPM:{wpm}")
    accuracy_label.config(text=f"Accuracy:{accuracy}%")
    window.after_cancel(timer_event)
    user_entry.delete(0,END)
    user_entry.focus_set()
    user_entry.grid(row=2, column=0, padx=10, pady=10, columnspan=3)
    user_entry.bind("<Key>", start_timer_event)


def start_timer():
    global timer,seconds,timer_event
    if timer>=0:
        seconds = timer % 60
        timer_label.config(text=f"Timer: {seconds:02d}")
        timer -= 1
        timer_event=window.after(1000, start_timer)
        speed_calc()
    else:
        print("Time's up!")
        user_entry.grid_forget()
        messagebox.showinfo(title="Time's Up",message=f"Time is up\nNo of Correct Words:{correct_words_count}\nNo of Wrong Words:{wrong_words_count}\nNet WPM:{wpm}\nAccuracy:{accuracy}")

def start_timer_event(event=None):
    if timer == 60:
        start_timer()

text_string=""
with open("simple_english_words.txt",mode="r")as ft:
    words_file=ft.readlines()
for i in range(0,45):
    initial_text.append(random.choice(words_file).split("\n")[0])
# print(initial_text)
for i in range(0,45):
    text_string+=initial_text[i].lower()+" "

sample_text_text=Text( window, wrap='word',height=15,width=30,bg="#A7C7E7",relief=GROOVE,border=5,)
sample_text_text.insert(1.0,text_string,)
sample_text_text.configure(state=DISABLED,)
sample_text_text.grid(row=1, column=0, padx=10, pady=10,columnspan=3)
sample_text_text.tag_configure("match", background="light green")
sample_text_text.tag_configure("no_match", background="red")

user_entry = Entry(width=50,bg="#A7C7E7",)
user_entry.bind("<Key>", start_timer_event)
user_entry.focus_set()
user_entry.grid(row=2, column=0, padx=10, pady=10,columnspan=3)

timer_label = Label(window,text=f"Timer: {timer%60:02d}",bg="white")
timer_label.grid(row=3, column=1)
wpm_label=Label(window,text=f"Net WPM:{wpm}",bg="white")
wpm_label.grid(row=4,column=0)
accuracy_label=Label(window,text=f"Accuracy:{accuracy}%",bg="white")
accuracy_label.grid(row=4,column=2)
clear_button=Button(text="Clear",command=clear)
clear_button.grid(row=5,column=0,padx=5,pady=5)
exit_button=Button(text="Exit",command=window.destroy)
exit_button.grid(row=5,column=2)

window.mainloop()