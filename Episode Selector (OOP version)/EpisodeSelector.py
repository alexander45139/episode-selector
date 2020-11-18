from tkinter import *
import random
from datetime import date, datetime, timedelta


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


# class holds the attributes of a story from a TV series
class Story:
    # constructor
    def __init__(self, name, no_of_eps, last_watched, series_name):
        self.name = name
        self.number_of_episodes = no_of_eps
        self.last_watched = last_watched
        self.series_name = series_name

    # writes either today's date next or " " to the story and rewrites a file with the contents of a given array
    def stamp_date(self, is_today):
        if is_today == True:
            self.last_watched = str(date.today())
        else:
            self.last_watched = " "


# class holds an array of Story objects for a TV series
class Series:
    def __init__(self, name):
        self.name = name  # name of the TV series
        self.stories = []  # stores every object of Story created, containing info about each story of a TV series
        self.random_index = 0  # the index of series array that will be randomly selected to display in the window

        # STORY SELECTOR (to be added below TV SERIES SELECTOR)
        self.random_btn = Button(root, text="Select Random", command=self.select_random_story)  # button to select a random story
        self.random_story = Label(root, text="")  # the label where the name of the story will go
        self.number_of_eps = Label(root, text="Number of episodes: ")  # the label where the number of episodes, in the aforementioned story, is displayed
        self.story_last_watched = Label(root, text="Last watched: ")  # the label where the date the episode(s) was last watched will go
        self.watched_btn = Button()  # button to be created in display method (unclickable atm) that writes the todays date in the array next to the story
        self.undo_watched_btn = Button()  # button to be created in display method (unclickable atm) that rewrites " " to the array next to the story
        self.search_story = Entry(root)
        self.submit_search_btn = Button(root, text="Submit Search", command=self.select_searched_story)

    # creates Story objects from a file with the name of this object, adds it to the self.stories array and displays the story selector (labels and buttons)
    def create_story_selector(self):

        file = open("../resources/" + self.name + " Stories.csv", "r")
        text = file.read()  # store text content from file

        if len(text) == 0:  # if there is no text a message will appear below
            self.random_story.pack_forget()
            self.random_story["text"] = "I'm sorry but the file for the information on this TV series is empty!"
            self.random_story.pack()
        else:  # otherwise...
            self.remove_story_selector()

            story = []  # each story with its name, date last watched and other info (e.g. no. of episodes)
            story_info = []  # where each letter of an piece of info to be placed in story as a joined string
            index = 0  # current index of the text variable

            if text[0:3] == "ï»¿":  # note: sometimes csv files can have these characters in front of what was originally added
                index = 3  # skip adding these 3 characters that are sometimes in a csv

            while index < len(text):  # loop goes through each in the string, join each item together and create Story objects with their attributes from text
                if text[index] == ",":  # a peice of info is completed and added as a string to story array
                    story.append("".join(story_info))
                    story_info = []
                    if text[
                        index + 1] == "\n":  # if there is no stamped date, then place a space where it's suppose to be
                        story_info.append(" ")
                elif text[index] == "\n":  # another peice of info is completed and added as a string to story array, which is added to stories array
                    story.append("".join(story_info))
                    story_object = Story(story[0], story[1], story[len(story) - 1], self.name)
                    self.stories.append(story_object)
                    story_info = []
                    story = []
                else:
                    story_info.append(text[index])  # the current letter is added to story_info array
                index += 1

            self.display_story_selector()

    # displays all the widgets from the story selector to be visually added to the window
    def display_story_selector(self):
        self.watched_btn = Button(root, text="Watched", state=DISABLED, command=self.rewrite_stories_to_file(True))  # set a method to call when clicked on
        self.undo_watched_btn = Button(root, text="Undo 'Watched'", state=DISABLED, command=self.rewrite_stories_to_file(False))

        self.random_btn.pack()
        self.random_story.pack()
        self.number_of_eps.pack()
        self.story_last_watched.pack()
        self.watched_btn.pack()
        self.undo_watched_btn.pack()
        self.search_story.pack()
        self.submit_search_btn.pack()

    # removes all the widgets from the story selector to be visually added to the window
    def remove_story_selector(self):
        self.random_btn.pack_forget()  # this widget and ones below are visually removed from the window
        self.random_story.pack_forget()
        self.number_of_eps.pack_forget()
        self.story_last_watched.pack_forget()
        self.watched_btn.pack_forget()
        self.undo_watched_btn.pack_forget()
        self.search_story.pack_forget()
        self.submit_search_btn.pack_forget()

    # takes the drop down menu's (series_selector) chosen option and refreshes the objects in STORY selector
    def update_random_selector(self):
        story_object = self.stories[self.random_index]  # current Story object selected

        # these Label objects' text change to their original forms
        self.random_story["text"] = story_object.name  # random_story's text writes the name of the randomly chosen story
        self.number_of_eps["text"] = "Number of episodes: " + story_object.number_of_episodes  # the story's episode count is written
        self.story_last_watched["text"] = "Last watched: " + story_object.last_watched  # the story's last watched date is written in story_last_watched

        self.watched_btn["state"] = NORMAL  # both these buttons become clickable
        self.undo_watched_btn["state"] = NORMAL

        self.display_story_selector()

    # selects a random story from the series
    def select_random_story(self):
        story_object = self.stories[self.random_index]
        self.random_index = int(random.randint(0, len(self.stories) - 1))  # a random number is found in the range of indexes of the array, stories
        datestamp = story_object.last_watched  # date of story that was last watched

        if datestamp != " " and datetime.strptime(datestamp, "%Y-%m-%d").date() > (date.today() - timedelta(days=convert_time_measurement_into_days(filtered_variable.get()))):
            self.select_random_story()  # function recalled if there's no date next to the story or if the date is too recent
        else:
            self.update_random_selector()  # otherwise, the random selector's info is updated

    # updates current Story object's attribute, last_watched, and rewrites the file of this TV series with the updated information from the array of Story objects
    def rewrite_stories_to_file(self, last_watched_today):
        story_object = self.stories[self.random_index]

        story_object.stamp_date(last_watched_today)  # story_object's method is called

        self.story_last_watched["text"] = "Last watched: " + story_object.last_watched  # this element is updated with new date

        if not self.stories:  # if stories array is empty display an error message
            self.random_story["text"] = "I'm sorry but the file for the information on this TV series is empty!"
            self.random_story.pack_forget()
            self.random_story.pack()
        else:  # otherwise...
            file = open("../resources/" + self.name + " Stories.csv", "w")
            for story in self.stories:  # for each array in the array called self.stories
                file.write(story.name + "," + story.number_of_episodes + "," + story.last_watched)  # these three attributes in this Story object are written into file
                file.write("\n")  # new line is written to separate each story
            file.close()

    # selects the story entered in the search bar
    def select_searched_story(self):
        s = 0
        while s < len(self.stories):  # linear search through the stories
            if self.search_story.get() in self.stories[s].name:
                self.select_random_story()  # method is called when the typed in value roughly matches a Story object's name attribute
            s += 1


# creates a Series after removing the widgets of the previous one
def create_series(selected_series):
    Series(selected_series).create_story_selector()  # add new Series object



# root
root = Tk()
root.title("Episode Selector")  # title of the window
root.geometry("600x400")  # window size

# TITLE
title_heading = Label(root, text="Episode Selector")  # title heading label in the window
title_heading.pack()  # displays the Label object

# TV SERIES SELECTOR
series_list = ("Doctor Who (1963 - 1989)", "Doctor Who (2005 - 2017)")  # the list of TV series

series_variable = StringVar(root)  # the Tkinter root will have a dynamic string value
series_variable.set("Select a series to pick a random story")  # default value
series_selector = OptionMenu(root, series_variable, *series_list, command=create_series)  # an drop down menu to select a TV series
series_selector.pack()

Label(root, text="Filter out last watched:").pack()  # a Label
filtered_variable = StringVar(root)  # default value for a dropdown list
filtered_variable.set("1 year")  # sets the value
filtered_episode_count = OptionMenu(root, filtered_variable, "1 year", "6 months", "3 months", "2 months", "1 month", "2 weeks")  # drop menu to filter the number of max. eps a story has in order to be chosen
filtered_episode_count.pack()

root.mainloop()
