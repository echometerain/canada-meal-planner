import customtkinter as ctk
import datetime
import calendar
from enum import StrEnum
from PIL import Image
import os
import json
import configparser
import back_end

config = configparser.ConfigParser()
config.read('settings.ini')
language_code = config['miscellaneous']['language']
text_json = json.load(open(f'locales/{language_code}.json', encoding='utf-8'))
default_planner_names = text_json['default planner names']


class Colors(StrEnum):
    BLACK = "#231717"
    GREY = "#9CA2AE"
    DARK_GREY = "#303030"
    WHITE = "#FFFFFF"
    RED = "#FA5151"
    BLUE = "#4278E0"


date_today = datetime.date.today()
year_current = date_today.year
month_current = date_today.month
day_current = date_today.day
month_lookup = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                "November", "December"]

# initialise app
app = ctk.CTk()
app.geometry("960x540")
app.title("Canada Meal Planner")
app.iconbitmap(os.path.join("./images/cmp logo.ico"))
planner_selected = None


def search_entered(search_term=None):
    if search_term is None:
        search_term = search_entry.get()
    if search_term == "":
        return False
    # when the search button is entered, this function gets called,
    # which will get the data from the backend, and then forward it to the planner and some such function
    food_items = back_end.fuzzy_match(search_term)
    for suggestions_slaves, i in zip(suggestions_frame.grid_slaves(), range(9, -1, -1)):
        print(i)
        suggestions_slaves.configure(text=food_items[i])


def change_month(offset=0):
    global month_current
    global year_current
    month_current += offset
    if month_current <= 0:
        year_current -= 1
        month_current = 12
    if month_current >= 13:
        year_current += 1
        month_current = 1
    days = calendar.monthrange(year_current, month_current)[1]
    calender_month_year_label.configure(text=f"{month_lookup[month_current - 1]} {year_current}")
    slaves = calender_days_frame.grid_slaves()
    for slave in slaves[0:31 - days]:
        slave.configure(fg_color=Colors.GREY, state="disabled")
    for slave in slaves[31 - days:31]:
        slave.configure(fg_color=Colors.BLUE, state="enabled")


def change_planner_focus(hf=None):
    global planner_selected
    if planner_selected is not None:
        planner_selected.configure(border_width=0)
    planner_selected = hf
    if hf is not None:
        hf.configure(border_width=3, border_color='#ff0000')


def regenerate_planner(plans: dict):
    # fill planner_scrollable_frame with that days entries, or placeholder text if there are none.
    global planner_selected
    planner_selected = None
    for planner_item in planner_scrollable_frame.grid_slaves():
        planner_item.grid_forget()
        planner_item.destroy()
    if not plans:
        for i in range(0 if plans else 4):
            hour_frame = ctk.CTkFrame(planner_scrollable_frame)
            hour_frame.bind("<Button-1>", lambda e, hf=hour_frame: change_planner_focus(hf))
            hour_frame.configure()
            planner_hour_name_entry = ctk.CTkEntry(hour_frame, height=20, font=('', 11),
                                                   placeholder_text='' if plans else default_planner_names[i])
            if i % 2:
                hour_frame.configure(fg_color="#555555")
            hour_frame.columnconfigure(0, weight=1)
            hour_frame.rowconfigure(0, weight=1)
            hour_frame.grid(column=0, row=i, sticky='ew')
            planner_hour_name_entry.grid(column=0, row=0, padx=3, pady=3, sticky='nw')
    planner_add_button = ctk.CTkButton(planner_scrollable_frame, text='Add new')
    planner_add_button.grid(column=0, sticky='ew')


def change_day(day=day_current):
    # when a date is clicked on in the calendar, this function is called and will change the current day displayed
    global day_current
    day_current = day
    current_date_label.configure(text=f"{month_lookup[month_current - 1]} {day_current}")
    regenerate_planner({})


# Search Bar

search_frame = ctk.CTkFrame(app, height=40)
search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search through Canada Meal Planner’s food catalogue..",
                            fg_color='#FA5151',
                            border_width=0, text_color='#FFFFFF', placeholder_text_color="#FFFFFF", font=('', 13))
search_submit_button = ctk.CTkButton(search_frame, text="Search", command=search_entered)

cmp_icon = ctk.CTkImage(Image.open(os.path.join("images/cmp64.png")), size=(64, 64))
icon_label = ctk.CTkLabel(app, image=cmp_icon, text='')

# suggestions
suggestions_frame = ctk.CTkFrame(app, height=60)
for i in range(10):
    suggestion_label = ctk.CTkLabel(suggestions_frame, text="")
    suggestion_label.grid(column=i % 2, row=i // 2, sticky='nesw')
    suggestions_frame.columnconfigure(i % 2, weight=1)
    suggestions_frame.rowconfigure(i // 2, weight=1)

# Calender
calender_frame = ctk.CTkFrame(app)
calender_month_frame = ctk.CTkFrame(calender_frame, height=30)
calender_month_prior_button = ctk.CTkButton(calender_month_frame, text="<", width=50)
calender_month_prior_button.bind("<Button-1>", lambda e: change_month(-1))
calender_month_following_button = ctk.CTkButton(calender_month_frame, text=">", width=50)
calender_month_following_button.bind("<Button-1>", lambda e: change_month(1))
calender_month_year_label = ctk.CTkLabel(calender_month_frame)
calender_days_frame = ctk.CTkFrame(calender_frame)
i = 0
buttons = []
for z in range(35):
    i += 1
    button = ctk.CTkButton(calender_days_frame, text=str(i), command=lambda day=i: change_day(day))
    button.configure(width=50, height=50, font=("", 14), text_color=Colors.WHITE, text_color_disabled=Colors.WHITE)
    button.grid(column=z % 7, row=z // 7, padx=1, pady=1, sticky='nesw')
    calender_days_frame.rowconfigure(z // 7, weight=1)
    calender_days_frame.columnconfigure(z % 7, weight=1)
    if z % 7 == 6:
        button.grid(padx=(1, 10), sticky='nesw')
    if z % 7 == 0:
        button.grid(padx=(10, 1), sticky='nesw')
    if i <= 7:
        button.grid(pady=(10, 1), sticky='nesw')
    elif i >= 29:
        button.grid(pady=(1, 10), sticky='nesw')
    buttons.append(button)
    if i == 31:
        break
# Planner
planner_frame = ctk.CTkFrame(app)
current_date_label = ctk.CTkLabel(planner_frame, text=f"{month_lookup[month_current - 1]} {day_current}")
planner_scrollable_frame = ctk.CTkScrollableFrame(planner_frame)

# Footer
footer_frame = ctk.CTkFrame(app, height=75)
leaderboard_button = ctk.CTkButton(footer_frame, text="Leaderboard", width=75, height=75)
home_button = ctk.CTkButton(footer_frame, text="Home", width=75, height=75)
recipe_button = ctk.CTkButton(footer_frame, text="Recipe", width=75, height=75)
profile_button = ctk.CTkButton(footer_frame, text="Profile", width=75, height=75)

# grid
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=5)
app.grid_columnconfigure(2, weight=5)
app.grid_columnconfigure(3, weight=5)
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=8)
app.grid_rowconfigure(3, weight=2)
calender_frame.rowconfigure(0, weight=1)
calender_frame.rowconfigure(1, weight=8)
calender_frame.columnconfigure(0, weight=1)
calender_frame.grid(column=0, row=1, columnspan=2, sticky='new', rowspan=2)
calender_month_frame.grid(column=0, row=0)
calender_month_prior_button.grid(column=0, row=0)
calender_month_year_label.grid(column=1, row=0, padx=30)
calender_month_following_button.grid(column=2, row=0)
calender_days_frame.grid(column=0, row=1, sticky='new')
icon_label.grid(column=0, row=0, pady=(4, 8))
search_frame.columnconfigure(0, weight=10)
search_frame.columnconfigure(1, weight=1)
search_frame.grid(column=1, row=0, columnspan=3, padx=8, pady=8, sticky='ew')
search_entry.grid(column=0, row=0, sticky='ew')
search_submit_button.grid(column=1, row=0, sticky='ew')
suggestions_frame.grid(column=2, row=1, columnspan=2, padx=8, pady=(0, 4), sticky='nesw')
planner_frame.grid_columnconfigure(0, weight=1)
planner_frame.grid_rowconfigure(0, weight=1)
planner_frame.grid_rowconfigure(1, weight=8)
planner_frame.grid(column=2, row=2, columnspan=2, padx=8, sticky='nesw')
current_date_label.grid(column=0, row=0, sticky='ew')
planner_scrollable_frame.grid_columnconfigure(0, weight=1)
planner_scrollable_frame.grid(column=0, row=1, sticky='nesw')
footer_frame.columnconfigure(0, weight=1)
footer_frame.columnconfigure(1, weight=1)
footer_frame.columnconfigure(2, weight=1)
footer_frame.columnconfigure(3, weight=1)
footer_frame.rowconfigure(0, weight=1)
footer_frame.grid(column=0, row=3, columnspan=4, sticky='nesw')
leaderboard_button.grid(column=0, row=0, sticky='ew')
home_button.grid(column=1, row=0, sticky='ew')
recipe_button.grid(column=2, row=0, sticky='ew')
profile_button.grid(column=3, row=0, sticky='ew')

change_month()
change_day()
app.mainloop()
