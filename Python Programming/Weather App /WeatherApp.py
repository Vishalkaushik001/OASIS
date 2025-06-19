from tkinter import *
from tkinter import ttk, messagebox
import requests
import threading

API_KEY = "6c2f07653f59fbea76fd6ba4d0d23c2d"  # place your API key here 

def get_location_by_ip():
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        if data['status'] == 'success':
            return data['city']
        else:
            return None
    except Exception as e:
        print("Location detection error:", e)
        return None


def tell_weather():
    city_name = city_field.get()
    if not city_name:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return
    loading_label.place(x=290, y=340)
    threading.Thread(target=fetch_weather, args=(city_name,)).start()

def fetch_weather(city_name):
    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}appid={API_KEY}&q={city_name}"
        response = requests.get(complete_url)
        x = response.json()

        if x["cod"] != "404":
            y = x["main"]
            temp = y["temp"]
            pressure = y["pressure"]
            humidity = y["humidity"]
            desc = x["weather"][0]["description"]

            temp_field_var.set(f"{temp} K")
            atm_field_var.set(f"{pressure} hPa")
            humid_field_var.set(f"{humidity} %")
            desc_field_var.set(desc.title())
        else:
            messagebox.showerror("Error", "City Not Found.")
            city_field.delete(0, END)
    finally:
        loading_label.place_forget()

def clear_all():
    city_field.delete(0, END)
    temp_field_var.set("")
    atm_field_var.set("")
    humid_field_var.set("")
    desc_field_var.set("")

def autofill_city():
    city = get_location_by_ip()
    if city:
        city_field.delete(0, END)
        city_field.insert(0, city)
    else:
        messagebox.showwarning("Warning", "Could not detect location.")


root = Tk()
root.title("🌤️ Weather Application")
root.geometry("700x400")
root.configure(bg="#e0f7fa")

style = ttk.Style()
style.configure("TLabel", font=('Segoe UI', 12), background="#e0f7fa")
style.configure("TEntry", font=('Segoe UI', 12))
style.configure("TButton", font=('Segoe UI', 11, 'bold'), padding=6)


headlabel = Label(root, text="🌍 Weather  Application", fg='white', bg='#00796b',
                  font=('Segoe UI', 20, 'bold'), pady=10, padx=10)
headlabel.pack(fill=X, pady=(10, 20))


temp_field_var = StringVar()
atm_field_var = StringVar()
humid_field_var = StringVar()
desc_field_var = StringVar()

frame = Frame(root, bg="#e0f7fa")
frame.pack()

Label(frame, text="📍 City Name:", anchor="e").grid(row=0, column=0, sticky="e", padx=10, pady=5)
city_field = ttk.Entry(frame, width=40)
city_field.grid(row=0, column=1, pady=5)

Label(frame, text="🌡️ Temperature:", anchor="e").grid(row=1, column=0, sticky="e", padx=10, pady=5)
temp_field = ttk.Entry(frame, textvariable=temp_field_var, width=40, state='readonly')
temp_field.grid(row=1, column=1, pady=5)

Label(frame, text="🌬️ Pressure:", anchor="e").grid(row=2, column=0, sticky="e", padx=10, pady=5)
atm_field = ttk.Entry(frame, textvariable=atm_field_var, width=40, state='readonly')
atm_field.grid(row=2, column=1, pady=5)

Label(frame, text="💧 Humidity:", anchor="e").grid(row=3, column=0, sticky="e", padx=10, pady=5)
humid_field = ttk.Entry(frame, textvariable=humid_field_var, width=40, state='readonly')
humid_field.grid(row=3, column=1, pady=5)

Label(frame, text="📝 Description:", anchor="e").grid(row=4, column=0, sticky="e", padx=10, pady=5)
desc_field = ttk.Entry(frame, textvariable=desc_field_var, width=40, state='readonly')
desc_field.grid(row=4, column=1, pady=5)

button_frame = Frame(root, bg="#e0f7fa")
button_frame.pack(pady=15)

ttk.Button(button_frame, text="🔍 Get Weather", command=tell_weather).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="📡 Detect Location", command=autofill_city).grid(row=0, column=1, padx=10)
ttk.Button(button_frame, text="🧹 Clear", command=clear_all).grid(row=0, column=2, padx=10)

loading_label = Label(root, text="⏳ Loading...", font=("Segoe UI", 12, "italic"), fg="#00796b", bg="#e0f7fa")

root.mainloop()
