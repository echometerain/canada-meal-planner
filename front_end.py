import customtkinter as ctk
import tkinter as tk
import datetime
import calendar as cal
from enum import StrEnum
from PIL import Image
import os
import json
import configparser
import back_end

config = configparser.ConfigParser()
config.read('settings.ini')
language_code = config['miscellaneous']['language']
user = config['miscellaneous']['current user']
user_data_dir = config[f"users.{user}"]['save']
user_data = json.load(open(user_data_dir))
text_json = json.load(open(f'locales/{language_code}.json', encoding='utf-8'))
default_planner_names = text_json['default planner names']

page = "Home"


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
date_current = f"{month_lookup[month_current - 1]} {day_current} {year_current}"
first_weekday = datetime.datetime(year_current, month_current, 1).weekday()
calendar_month_year_text = ""

# initialise app
app = ctk.CTk()
app.geometry("800x600")
app.title("Canada Meal Planner")
pi = tk.PhotoImage(file=os.path.join("./images/cmp logo.png"))
app.iconphoto(False, pi)
app.minsize(800, 600)
planner_selection = None


def recipe_entered():
    if search_term is None:
        search_term = search_entry.get()
    if search_term == "":
        return False


def change_planner_table(combooption):
    for slave in planner_scrollable_frame.grid_slaves():
        slave.forget()
        slave.destroy()
    food_items = user_data[user]['dates'][date_current][combooption]
    for item, i in zip(food_items, range(len(food_items))):
        food_label = ctk.CTkLabel(
            planner_scrollable_frame, text=item, height=20, font=('', 20))
        food_label.grid(column=0, row=i, sticky='w')


def search_entered(search_term=None):
    if search_term is None:
        search_term = search_entry.get()
    if search_term == "":
        return None
    # when the search button is entered, this function gets called,
    # which will get the data from the backend, and then forward it to the planner and some such function
    food_items = back_end.fuzzy_match(search_term)
    for suggestion_label, i in zip(suggestions_frame.grid_slaves(), range(9, -1, -1)):
        suggestion_label.configure(text=food_items[i])
        suggestion_label.unbind("<Button-1>")
        suggestion_label.bind("<Button-1>",
                              lambda e, food=suggestion_label.cget("text"): add_to_planner(food))


def add_to_planner(food):
    planner_table = planner_combobox_var.get()
    user_data[user]['dates'][date_current][planner_combobox_var.get()
                                           ].append(food)
    change_planner_table(planner_combobox_var.get())


def change_month(offset=0):
    global month_current, year_current, first_weekday, calendar_month_frame, calendar_month_year_text
    month_current += offset
    if month_current <= 0:
        year_current -= 1
        month_current = 12
    if month_current >= 13:
        year_current += 1
        month_current = 1
    days = cal.monthrange(year_current, month_current)[1]
    calendar_month_year_text = f"{month_lookup[month_current - 1]} {year_current}"
    slaves = calendar_days_frame.grid_slaves()
    for slave in slaves[0:31 - days]:
        slave.configure(fg_color=Colors.GREY, state="disabled")
    for slave in slaves[31 - days:31]:
        slave.configure(fg_color=Colors.BLUE, state="enabled")
    first_weekday = datetime.datetime(year_current, month_current, 1).weekday()
    calendar_month_frame.destroy()
    generate_calendar()


def change_day(day=day_current):
    # when a date is clicked on in the calendar, this function is called and will change the current day displayed
    global day_current, date_current
    day_current = day
    current_date_label.configure(
        text=f"{month_lookup[month_current - 1]} {day_current} {year_current}")
    date_current = f"{month_lookup[month_current - 1]} {day_current} {year_current}"
    if date_current not in user_data[user]['dates']:
        user_data[user]['dates'][date_current] = dict.fromkeys(
            default_planner_names, [])
    keys = list(user_data[user]['dates'][date_current].keys())
    planner_combobox.configure(values=keys)
    planner_combobox_var.set(keys[0])
    change_planner_table(keys[0])


# Search Bar
def generate_search():
    global search_frame, search_entry, search_submit_button
    search_frame = ctk.CTkFrame(app, height=40)
    search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search through Canada Meal Planner’s food catalogue..",
                                fg_color='#FA5151', border_width=0, text_color='#FFFFFF',
                                placeholder_text_color="#FFFFFF", font=('', 13), corner_radius=10)
    search_submit_button = ctk.CTkButton(
        search_frame, text="Search", command=search_entered)
    search_frame = ctk.CTkFrame(app, height=40)
    search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search through Canada Meal Planner’s food catalogue..",
                                fg_color='#FA5151',
                                border_width=0, text_color='#FFFFFF', placeholder_text_color="#FFFFFF", font=('', 13),
                                corner_radius=10)
    search_entry.bind("<Return>", lambda e: search_entered())
    search_submit_button = ctk.CTkButton(
        search_frame, text="Search", command=search_entered)
    search_frame.columnconfigure(0, weight=10)
    search_frame.columnconfigure(1, weight=1)
    search_entry.grid(column=0, row=0, sticky='ew')
    search_submit_button.grid(column=1, row=0, sticky='ew')


# Search Bar for recipe page
def recipe_search():
    global recipe_search_frame, recipe_search_entry, recipe_search_submit_button
    recipe_search_frame = ctk.CTkFrame(app, height=40)
    recipe_search_entry = ctk.CTkEntry(recipe_search_frame,
                                       placeholder_text="Search recipes through Canada Meal Planner..",
                                       fg_color='#FA5151', border_width=0, text_color='#FFFFFF',
                                       placeholder_text_color="#FFFFFF", font=('', 13), corner_radius=10)
    recipe_search_submit_button = ctk.CTkButton(
        recipe_search_frame, text="Search", command=recipe_entered)
    recipe_search_frame = ctk.CTkFrame(app, height=40)
    recipe_search_entry = ctk.CTkEntry(recipe_search_frame,
                                       placeholder_text="Search recipes through Canada Meal Planner..",
                                       fg_color='#FA5151',
                                       border_width=0, text_color='#FFFFFF', placeholder_text_color="#FFFFFF",
                                       font=('', 13), corner_radius=10)
    recipe_search_entry.bind("<Return>", lambda e: recipe_entered())
    recipe_search_submit_button = ctk.CTkButton(
        recipe_search_frame, text="Search", command=recipe_entered)


# Title for leaderboard page
def leaderboard_title():
    global leaderboard_title_frame, leaderboard_label
    leaderboard_title_frame = ctk.CTkFrame(app, height=40)
    leaderboard_label = ctk.CTkLabel(leaderboard_title_frame, text="Leaderboard", fg_color='#FA5151',
                                     text_color='#FFFFFF', font=('', 13), corner_radius=10, anchor="w")


def profile_title():
    global profile_title_frame, profile_label
    profile_title_frame = ctk.CTkFrame(app, height=40)
    profile_label = ctk.CTkLabel(profile_title_frame, text="Profile", fg_color='#FA5151', text_color='#FFFFFF',
                                 font=('', 13), corner_radius=10, anchor="w")

# suggestions


def suggestions():
    global suggestions_frame, suggestion_label


def generate_suggestions():  # IGNORE THE MISNOMER.
    global suggestions_frame
    suggestions_frame = ctk.CTkFrame(app, height=60)
    for i in range(10):
        if i == 0:
            suggestion_label = ctk.CTkLabel(suggestions_frame,
                                            text="Use the search bar above to search for a food item. Suggestions will appear here.")
        else:
            suggestion_label = ctk.CTkLabel(suggestions_frame, text="")
        suggestion_label.grid(column=i % 2, row=i // 2, sticky='nesw')
        suggestions_frame.columnconfigure(i % 2, weight=1)
        suggestions_frame.rowconfigure(i // 2, weight=1)


def generate_calendar():
    global calendar_frame, calendar_month_year_label, calendar_days_frame, calendar_month_frame
    if "calendar_frame" not in globals():
        calendar_frame = ctk.CTkFrame(app)
    calendar_month_frame = ctk.CTkFrame(calendar_frame, height=30)
    calendar_month_prior_button = ctk.CTkButton(
        calendar_month_frame, text="<", width=50)
    calendar_month_prior_button.bind("<Button-1>", lambda e: change_month(-1))
    calendar_month_following_button = ctk.CTkButton(
        calendar_month_frame, text=">", width=50)
    calendar_month_following_button.bind(
        "<Button-1>", lambda e: change_month(1))
    calendar_month_year_label = ctk.CTkLabel(calendar_month_frame)
    calendar_month_year_label.configure(text=calendar_month_year_text)
    calendar_days_frame = ctk.CTkFrame(calendar_frame)

    i = -first_weekday
    buttons = []
    for z in range(35):
        i += 1
        if i < 1:
            continue
        button = ctk.CTkButton(calendar_days_frame, text=str(
            i), command=lambda day=i: change_day(day))
        button.configure(width=50, height=50, font=(
            "", 14), text_color=Colors.WHITE, text_color_disabled=Colors.WHITE)
        button.grid(column=z % 7, row=z // 7, padx=1, pady=1, sticky='nesw')
        calendar_days_frame.rowconfigure(z // 7, weight=1)
        calendar_days_frame.columnconfigure(z % 7, weight=1)
        if z % 7 == 6:
            button.grid(padx=(1, 10), sticky='nesw')
        if z % 7 == 0:
            button.grid(padx=(10, 1), sticky='nesw')
        # if i <= 7:
        #     button.grid(pady=(10, 1), sticky='nesw')
        # elif i >= 29:
        #     button.grid(pady=(1, 10), sticky='nesw')
        buttons.append(button)
        if i == 31:
            break
    calendar_frame.rowconfigure(0, weight=1)
    calendar_frame.rowconfigure(1, weight=8)
    calendar_frame.columnconfigure(0, weight=1)
    calendar_month_frame.grid(column=0, row=0)
    calendar_month_prior_button.grid(column=0, row=0)
    calendar_month_year_label.grid(column=1, row=0, padx=30)
    calendar_month_following_button.grid(column=2, row=0)
    calendar_days_frame.grid(column=0, row=1, sticky='new')


def generate_planner():
    global planner_frame, current_date_label, planner_scrollable_frame, planner_combobox, planner_combobox_var
    planner_frame = ctk.CTkFrame(app)
    planner_combobox_var = ctk.StringVar(value='')
    planner_combobox = ctk.CTkComboBox(
        planner_frame, variable=planner_combobox_var, command=change_planner_table)
    current_date_label = ctk.CTkLabel(
        planner_frame, text=f"{month_lookup[month_current - 1]} {day_current}")
    planner_scrollable_frame = ctk.CTkScrollableFrame(planner_frame)
    planner_frame.grid_columnconfigure(0, weight=1)
    planner_frame.grid_rowconfigure(0, weight=1)
    planner_frame.grid_rowconfigure(1, weight=8)
    planner_frame.grid_rowconfigure(2, weight=8)
    current_date_label.grid(column=0, row=0, sticky='ew')
    planner_combobox.grid(column=0, row=1, sticky='sew')
    planner_scrollable_frame.grid_columnconfigure(0, weight=1)
    planner_scrollable_frame.grid(column=0, row=2, sticky='nesw')


def generate_footer():
    global footer_frame
    footer_frame = ctk.CTkFrame(app)
    leaderboard_button = ctk.CTkButton(footer_frame, text="",
                                       image=ctk.CTkImage(Image.open(
                                           "images/leaderboard.png"), size=(76, 73)),
                                       command=lambda: display_page("Leaderboard"))
    home_button = ctk.CTkButton(footer_frame, text="", image=ctk.CTkImage(Image.open("images/home.png"), size=(76, 73)),
                                command=lambda: display_page("Home"))
    recipe_button = ctk.CTkButton(footer_frame, text="",
                                  image=ctk.CTkImage(Image.open(
                                      "images/recipe.png"), size=(76, 73)),
                                  command=lambda: display_page("Recipe"))
    profile_button = ctk.CTkButton(footer_frame, text="",
                                   image=ctk.CTkImage(Image.open(
                                       "images/profile.png"), size=(76, 73)),
                                   command=lambda: display_page("Profile"))
    footer_frame.columnconfigure(0, weight=1)
    footer_frame.columnconfigure(1, weight=1)
    footer_frame.columnconfigure(2, weight=1)
    footer_frame.columnconfigure(3, weight=1)
    footer_frame.rowconfigure(0, weight=1)
    leaderboard_button.grid(column=0, row=0, ipady=6, sticky='ew')
    home_button.grid(column=1, row=0, ipady=6, sticky='ew')
    recipe_button.grid(column=2, row=0, ipady=6, sticky='ew')
    profile_button.grid(column=3, row=0, ipady=6, sticky='ew')


def generate_logo():
    global icon_label
    cmp_icon = ctk.CTkImage(Image.open(
        os.path.join("images/cmp64.png")), size=(64, 64))
    icon_label = ctk.CTkLabel(app, image=cmp_icon, text='')


def display_page(page="Home"):
    for slave in app.grid_slaves():
        slave.grid_forget()
    if page == "Home":
        app.grid_columnconfigure(0, weight=1)
        app.grid_columnconfigure(1, weight=5)
        app.grid_columnconfigure(2, weight=5)
        app.grid_columnconfigure(3, weight=5)
        app.grid_rowconfigure(0, weight=1)
        app.grid_rowconfigure(1, weight=1)
        app.grid_rowconfigure(2, weight=8)
        app.grid_rowconfigure(3, weight=2)
        calendar_frame.grid(column=0, row=1, columnspan=2,
                            sticky='new', rowspan=2)
        search_frame.grid(column=1, row=0, columnspan=3,
                          padx=8, pady=8, sticky='ew')
        suggestions_frame.grid(column=2, row=1, columnspan=2,
                               padx=8, pady=(0, 4), sticky='nesw')
        planner_frame.grid(column=2, row=2, columnspan=2,
                           padx=8, sticky='nesw')
        footer_frame.grid(column=0, row=3, columnspan=4, sticky='nesw')
    elif page == "Recipe":
        recipe_search()
        recipe_search_frame.columnconfigure(0, weight=10)
        recipe_search_frame.columnconfigure(1, weight=1)
        recipe_search_frame.grid(
            column=1, row=0, columnspan=3, padx=8, pady=8, sticky='ew')
        recipe_search_entry.grid(column=0, row=0, sticky='ew')
        recipe_search_submit_button.grid(column=1, row=0, sticky='ew')
    elif page == "Profile":
        profile_title()
        profile_title_frame.columnconfigure(0, weight=10)
        profile_title_frame.columnconfigure(1, weight=1)
        profile_title_frame.grid(
            column=1, row=0, columnspan=3, padx=8, pady=8, sticky='ew')
        profile_label.grid(column=0, row=0, sticky='ew')
    elif page == "Leaderboard":
        leaderboard_title()
        leaderboard_title_frame.columnconfigure(0, weight=10)
        leaderboard_title_frame.columnconfigure(1, weight=1)
        leaderboard_title_frame.grid(
            column=1, row=0, columnspan=3, padx=8, pady=8, sticky='ew')
        leaderboard_label.grid(column=0, row=0, sticky='ew')


def generate_app():
    generate_suggestions()
    generate_calendar()
    generate_search()
    generate_logo()
    generate_planner()
    generate_footer()
    change_month()
    change_day()


generate_app()
display_page()


def on_close():
    json.dump(user_data, open(user_data_dir, 'w+', encoding='utf-8'), indent=4)
    app.destroy()


app.protocol("WM_DELETE_WINDOW", on_close)
app.mainloop()
