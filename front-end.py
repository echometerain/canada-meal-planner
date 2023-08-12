import customtkinter as ctk
import datetime, time

# the current date is the default whenever the program is opened
date_today = datetime.date.today()
month_current = date_today.month
day_current = date_today.day
month_lookup = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                "November", "December"]

# initialise app
app = ctk.CTk()
app.geometry("960x540")
app.title("Canada Meal Planner")


def search_entered(search_term):
    # when the search button is entered, this function gets called,
    # which will get the data from the backend, and then forward it to the planner and some such function
    print(search_term)
    food_name = ""
    return food_name


def regenerate_planner(plans: dict):
    # fill planner_scrollable_frame with that days entries, or placeholder text if there are none.
    for planner_item in planner_scrollable_frame.grid_slaves():
        planner_item.grid_forget()
    if plans:
        pass
    else:
        placeholder_planner_label.grid(column=0, row=0)


def switch_day(day):
    # when a date is clicked on in the calendar, this function is called and will change the current day displayed
    global day_current
    day_current = day
    current_date_label.configure(text=f"{month_lookup[month_current - 1]} {day_current}")
    hours.clear()
    regenerate_planner({})


# Search Bar
search_bar = ctk.CTkEntry(app, placeholder_text="What do you plan on eating this day?", width=500)
search_bar.bind("<Return>", lambda e: search_entered(search_bar.get()))

# Calender
calender_frame = ctk.CTkFrame(app)
i = 0
buttons = []
for z in range(35):
    i += 1
    button = ctk.CTkButton(calender_frame, text=str(i), command=lambda day=i: switch_day(day))
    button.configure(width=50, height=50)
    button.grid(column=z % 7, row=z // 7, padx=1, pady=1)
    if z % 7 == 6:
        button.grid(padx=(1, 10))
    if z % 7 == 0:
        button.grid(padx=(10, 1))
    if i <= 7:
        button.grid(pady=(10, 1))
    elif i >= 29:
        button.grid(pady=(1, 10))
    buttons.append(button)
    if i == 31:
        break

# Planner
planner_frame = ctk.CTkFrame(app)
current_date_label = ctk.CTkLabel(planner_frame, text=f"{month_lookup[month_current - 1]} {day_current}")
planner_scrollable_frame = ctk.CTkScrollableFrame(planner_frame, height=400)
placeholder_planner_label = ctk.CTkLabel(planner_scrollable_frame, text="You haven't planned out any meals for today. Why not now!")

hours = []
for i in range(6):
    hour_frame = ctk.CTkFrame(planner_scrollable_frame)
    hour_frame.configure(height=100)
    if i % 2:
        hour_frame.configure(fg_color="#555555")
    hour_frame.grid(column=0, row=i, sticky='ew')
    hours.append(hour_frame)

# grid
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=5)
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
calender_frame.grid(column=0, row=1, sticky='ne')
search_bar.grid(column=1, row=0, padx=30, pady=10, sticky='ws')
planner_frame.grid_columnconfigure(0, weight=1)
planner_frame.grid(column=1, row=1, padx=8, sticky='new')
current_date_label.grid(column=0, row=0, sticky='ew')
planner_scrollable_frame.grid_columnconfigure(0, weight=1)
planner_scrollable_frame.grid(column=0, row=1, sticky='ew')

app.mainloop()
