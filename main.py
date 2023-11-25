import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap
import os


def get_weather(city):
    api_key = os.environ['weather_app_key']
    complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=" + api_key
    api_link = requests.get(complete_api_link)

    if api_link.status_code == 404:
        messagebox.showerror("Error, City not found")
        return None

    weather_data = api_link.json()

    icon_id = weather_data['weather'][0]['icon']
    tempature = weather_data['main']['temp']- 273.15
    description = weather_data['weather'][0]['description']
    city = weather_data['name']
    country = weather_data['sys']['country']

    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, tempature, description, city, country)
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return

    icon_url, tempature, description, city, country = result
    location_label.configure(text=f"{city}, {country}")

    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    tempature_label.configure(text=f"Tempature: {tempature:.2f}\u00b0C")
    description_label.configure(text=f"Description: {description}")

root = ttkbootstrap.Window(themename="morph")
root.title("Weather Application")
root.geometry("1000x700")

city_entry= ttkbootstrap.Entry(root,font="Helvetica, 18")
city_entry.pack(pady=10)

search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning", width="50")
search_button.pack(pady=10)


location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

icon_label = tk.Label(root)
icon_label.pack()

tempature_label = tk.Label(root, font="Helvetica, 20")
tempature_label.pack()

description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

root.mainloop()