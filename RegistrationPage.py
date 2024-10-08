import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu
import json
import os
from LoginPage import loginPage

class RegistrationPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Registration Page")
        self.root.geometry("600x800")
        self.root.configure(bg="#073763")
        self.root.eval('tk::PlaceWindow . center')

        frame = tk.Frame(self.root, bg="#073763", padx=30, pady=30, relief="raised", bd=2)
        frame.pack(expand=True, fill='both')

        titleLabel = tk.Label(frame, text="Register for SIC community", font=("Arial", 30, "bold"), bg="#1abc9c", fg="white")
        titleLabel.pack()

        # Fields for registration
        tk.Label(frame, text="Name:", font=("Arial", 15, "bold"), bg="#073763", fg="white").pack(pady=5)
        self.name_entry = tk.Entry(frame, width=30, font=("Arial", 12))
        self.name_entry.pack(pady=5)

        tk.Label(frame, text="Phone Number:", font=("Arial", 15, "bold"), bg="#073763", fg="white").pack(pady=5)
        self.phone_entry = tk.Entry(frame, width=30, font=("Arial", 12))
        self.phone_entry.pack(pady=5)

        tk.Label(frame, text="Email:", font=("Arial", 15, "bold"), bg="#073763", fg="white").pack(pady=5)
        self.email_entry = tk.Entry(frame, width=30, font=("Arial", 12))
        self.email_entry.pack(pady=5)

        tk.Label(frame, text="Password:", font=("Arial", 15, "bold"), bg="#073763", fg="white").pack(pady=5)
        self.password_entry = tk.Entry(frame, width=30, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        tk.Label(frame, text="National ID:", font=("Arial", 15, "bold"), bg="#073763", fg="white").pack(pady=5)
        self.national_id_entry = tk.Entry(frame, width=30, font=("Arial", 12))
        self.national_id_entry.pack(pady=5)

        tk.Label(frame, text="Age:", font=("Arial", 15, "bold"), bg="#073763", fg="white").pack(pady=5)
        self.age_entry = tk.Entry(frame, width=30, font=("Arial", 12))
        self.age_entry.pack(pady=5)

        # Gender and Governorate as option menus
        self.gender_var = StringVar()
        self.gender_var.set("Select Gender")
        tk.Label(frame, text="Gender:", font=("Arial", 15, "bold"), bg="#073763", fg="white").pack(pady=5)
        self.gender_menu = OptionMenu(frame, self.gender_var, "Male", "Female")
        self.gender_menu.pack(pady=5)

        self.governorate_var = StringVar()
        self.governorate_var.set("Select Governorate")
        tk.Label(frame, text="Governorate:", font=("Arial", 15, "bold"), bg="#073763", fg="white").pack(pady=5)
        self.governorate_menu = OptionMenu(frame, self.governorate_var, "Cairo", "Alexandria", "Giza", "Aswan", "Luxor",
                                           "Other")
        self.governorate_menu.pack(pady=5)

        self.registerButton = tk.Button(frame, text="Register", font=("Arial", 12), bg="#ba4244", fg="white",
                                        activebackground="#45a049", width=15, command=self.register)
        self.registerButton.pack(pady=10)

        self.loginButton = tk.Button(frame, text="Go to Login Page", font=("Arial", 12), bg="#2196f3", fg="white",
                                     activebackground="#1976d2", width=20, command=self.go_to_login)
        self.loginButton.pack(side='bottom', pady=10)
        self.root.mainloop()

    def register(self):
        name = self.name_entry.get()
        phone_number = self.phone_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        national_id = self.national_id_entry.get()
        age = self.age_entry.get()
        gender = self.gender_var.get()
        governorate = self.governorate_var.get()

        if os.path.exists("user_data.json"):
            with open("user_data.json", "r") as file:
                data = json.load(file)
        else:
            data = {}

        if email in data:
            messagebox.showwarning("Input Error", "This email is already exists")
            return

        if not all([name, phone_number, email, password, national_id, age, gender, governorate]):
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return

        try:
            age = int(age)
            if age <= 0 or age > 120:
                messagebox.showwarning("Age Error", "Please enter a valid age between 1 and 120")
                return
        except ValueError:
            messagebox.showwarning("Age Error", "Age must be a number")
            return

        if gender == "Select Gender":
            messagebox.showwarning("Gender Error", "Please select a gender")
            return

        if governorate == "Select Governorate":
            messagebox.showwarning("Governorate Error", "Please select a governorate")
            return

        new_user = {
            "username": name,
            "phone_number": phone_number,
            "email": email,
            "gender": gender,
            "governorate": governorate,
            "password": password,
            "age": age,
            "national_id": national_id,
            "friends": [],
            "posts": [],
            "friend_requests": [],
        }

        data[email]=new_user

        with open("user_data.json", "w") as file:
            json.dump(data, file, indent=4)

        messagebox.showinfo("Registration Success", "User registered successfully")
        self.go_to_login()

    def go_to_login(self):
        self.root.destroy()
        loginPage()

if(__name__=="__main__"):
    RegistrationPage()
