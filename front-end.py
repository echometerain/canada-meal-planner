import customtkinter as ctk
import datetime, time

# the current date is the default whenever the program is opened
date_today = datetime.date.today()
day_current = date_today.day


# initialise app
app = ctk.CTk()
app.geometry("960x540")
app.title("Canada Meal Planner")



def search_entered(event):
    # when the search button is entered, this function gets called,
    # which will get the data from the backend, and then forward it to the planner and some such function
    print(event)
    food_name = ""
    return food_name


def switch_day(day):
    global day_current
    day_current = day
    print(day_current)


search_bar = ctk.CTkEntry(app, placeholder_text="Fuck")
search_bar.bind("<Return>", search_entered)
search_bar.pack()

calender_frame = ctk.CTkFrame(app)
i = 0
buttons = []
for z in range(5 * 7):
    i += 1
    # noinspection PyTypeChecker
    buttons.append(ctk.CTkButton(calender_frame, text=str(i), command=lambda day=i: switch_day(day)))
    buttons[i-1].grid(column=z % 7, row=z // 7)
    if i == 31:
        break
buttons = list(map(lambda e: e.configure(width=50, height=50), buttons))
calender_frame.pack(anchor="w", side='left')

planner_frame = ctk.CTkFrame(app)
planner_frame.pack(side='right')

app.mainloop()
