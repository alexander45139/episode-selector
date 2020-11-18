from tkinter import *
import random
from datetime import date, datetime, timedelta


#FUNCTIONS
# takes the drop down menu's (series_selector) chosen option and refreshes the objects in STORY selector
def set_up_random_selector(option_selected):
    global selected_series  # this variable can be called anywhere after and out
    selected_series = option_selected
    global series
    series = collect_csv_content(selected_series)  # array of stories and their info
    
    random_btn.pack_forget()  # this widget and ones below are visually removed from the window
    random_story.pack_forget()
    number_of_eps.pack_forget()
    story_last_watched.pack_forget()
    watched_btn.pack_forget()
    undo_watched_btn.pack_forget()

    random_btn.pack()  # this widget and ones below are visually added to the window
    random_story.pack()
    number_of_eps.pack()
    story_last_watched.pack()
    watched_btn.pack()
    undo_watched_btn.pack()
    
    random_story["text"] = ""  # these Label objects' text change to their original forms
    number_of_eps["text"] = "Number of episodes: "
    story_last_watched["text"] = "Last watched: "

    watched_btn["state"] = DISABLED  # both these buttons become unclickable
    undo_watched_btn["state"] = DISABLED

# selects a random story from a given series
def select_random_story():
    global random_index
    random_index = random.randint(0, len(series) - 1)  # a random number is found in the range of indexes of the array, series
    datestamp = series[random_index][len(series[random_index]) - 1]  # the last item in the randomly chosen story inside the array, series

    if datestamp != " " and datetime.strptime(datestamp, "%Y-%m-%d").date() > (date.today() - timedelta(days = convert_time_measurement_into_days(filtered_variable.get()))):
        select_random_story()  # function recalled if there's no date next to the story or if the date is too recent
    else:
        random_story["text"] = series[random_index][0]  # random_story's text writes the name of the randomly chosen story
        number_of_eps["text"] = "Number of episodes: " + series[random_index][1] # the story's episode count is written
        story_last_watched["text"] = "Last watched: " + datestamp  # the story's datestamp is written in story_last_watched

        watched_btn["state"] = NORMAL  # both these buttons become clickable
        undo_watched_btn["state"] = NORMAL

# converts a time measurement into its number of days and returns it
def convert_time_measurement_into_days(measurement):
    number = []  # number as an array
    for digit in measurement:  # this for loop adds each digit and point in the string argument to number
        if digit == " ":
            break
        else:
            number.append(digit)
    number = int("".join(number))  # the array joined as as a string to then be converted into a number

    # depending on the measurement given, number is converted into the number of days
    if "year" in measurement:
        days = 365 * number
    elif "month" in measurement:
        days = 30 * number
    elif "week" in measurement:
        days = 7 * number
    
    return days  # number of days is returned

# returns the content in a given file, ending in "Stories", as an array
def collect_csv_content(FILE):
    file = open("resources/" + FILE + " Stories.csv", "r")
    text = file.read()  # store text content from file
    series = []  # the entire info on the TV series (every story)
    story = []  # each story with its name, date last watched and other info (e.g. no. of episodes)
    story_info = []  # where each letter of an peice of info to be placed in story as a joined string
    index = 0  # current index of the text variable
    
    if text[0:3] == "ï»¿":
        index = 3  # skip adding these 3 characters that are sometimes in a csv
    
    while index < len(text):
        if text[index] == ",":  # a peice of info is completed and added as a string to story array
            story.append("".join(story_info))
            story_info = []
            if text[index + 1] == "\n":  # if there is no stamped date, then place a space where it's suppose to be
                story_info.append(" ")
        elif text[index] == "\n":  # another peice of info is completed and added as a string to story array, which is added to series array
            story.append("".join(story_info))
            series.append(story)
            story_info = []
            story = []
        else:
            story_info.append(text[index])  # the current letter is added to story_info array
        index += 1
    
    return series

# rewrite a file with the contents of a given array
def rewrite_csv(FILE):
    story_last_watched["text"] = "Last watched: " + str(series[random_index][len(series[random_index]) - 1])  # this element is updated with new date
    
    file = open("resources/" + FILE + " Stories.csv", "w")
    for story in series:  # for each array in the array called series
        for i in range(0, len(story)):
            file.write(str(story[i]))  # item i in the array, story, is written
            if (i < (len(story) - 1)):
                file.write(",")  # followed by a comma
        file.write("\n")  # new line is written to separate each story
    file.close()

# writes today's date next to the randomly selected story
def stamp_date():
    series[random_index][len(series[random_index]) - 1] = date.today()  # value of last watched item in the selected sub array becomes today's date
    rewrite_csv(selected_series)

# writes " " to the randomly selected story
def unstamp_date():
    series[random_index][len(series[random_index]) - 1] = " "  # value of last watched item in the selected sub array becomes a space character (as a sort of null value)
    rewrite_csv(selected_series)


#root
root = Tk()
root.title("Episode Selector")  # title of the window
root.geometry("600x400")  # window size


#TITLE
title_heading = Label(root, text="Episode Selector")  # title heading label in the window
title_heading.pack()  # displays the Label object


#TV SERIES SELECTOR
series_list = ("Doctor Who (1963 - 1989)", "Doctor Who (2005 - 2017)")  # the list of TV series

series_variable = StringVar(root)  # the Tkinter root will have a dynamic string value
series_variable.set("Select a series to pick a random story")  # default value
series_selector = OptionMenu(root, series_variable, *series_list, command=set_up_random_selector)  # an drop down menu to select a TV series
series_selector.pack()

Label(root, text="Filter out last watched:").pack()  # a Label
filtered_variable = StringVar(root)  # default value for a dropdown list
filtered_variable.set("1 year")  # sets the value
filtered_episode_count = OptionMenu(root, filtered_variable, "1 year", "6 months", "3 months", "2 months", "1 month", "2 weeks")  # drop menu to filter the number of max. eps a story has in order to be chosen
filtered_episode_count.pack()


#STORY SELECTOR
random_btn = Button(root, text="Select Random", command=select_random_story)  # button to select a random story
random_story = Label(root, text="")  # the label where the name of the story will go
number_of_eps = Label(root, text="Number of episodes: ")  # the label where the number of episodes, in the aforementioned story, is displayed
story_last_watched = Label(root, text="Last watched: ")  # the label where the date the episode(s) was last watched will go
watched_btn = Button(root, text="Watched", state=DISABLED, command=stamp_date)  # button (unclickable atm) that writes the todays date in the array next to the story
undo_watched_btn = Button(root, text="Undo 'Watched'", state=DISABLED, command=unstamp_date)  # button (unclickable atm) that rewrites " " to the array next to the story


root.mainloop()
