import tkinter as tk
from tkinter import messagebox
import json
from PIL import Image, ImageTk
from Users import NormalUser
from home_page import NewFeed

class loginPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login Page")
        self.root.geometry("500x600")
        self.root.configure(bg="#073763")

        # Load and display the image
        self.image = Image.open("logo.png")
        self.image = self.image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(self.root, image=self.photo, bg="#f0f0f0")
        self.image_label.pack(pady=20)

        # Title Label
        self.title_label = tk.Label(self.root, text="Welcome back to SIC Community", font=("Arial", 20, "bold"),
                                    bg="#073763", fg="white")
        self.title_label.pack(pady=20)

        # Email Label and Entry
        tk.Label(self.root, text="Email:", bg="#073763", font=("Arial", 20, "bold"), fg="white").pack(pady=10)
        self.username_entry = tk.Entry(self.root, width=25, font="Tahoma 15")
        self.username_entry.pack(pady=10, padx=20)

        # Password Label and Entry
        tk.Label(self.root, text="Password:", bg="#073763", font=("Arial", 20, "bold"), fg="white").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", width=25, font="Tahoma 15")
        self.password_entry.pack(pady=10, padx=20)

        # Login Button
        self.loginButton = tk.Button(self.root, text="Login", bg="#4caf50", font="Arial 18 bold", fg="white", width=10,
                                     command=self.goToHomePage)
        self.loginButton.pack(pady=20)
        self.root.mainloop()

    def goToHomePage(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "" or password == "":
            messagebox.showwarning("Input Error", "Please fill in both fields")
            return
       

        try:
            with open("user_data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "Database not found!")
            return

        user_found = False
        logged_in_user = None
        for key,val in data.items():
            if key == username and val['password']== password:
                logged_in_user = NormalUser(
                    username=val.get("email"),
                    password=val.get("password"),
                    name=val.get("username"),
                    phone_number=val.get("phone_number"),
                    email=val.get("email"),
                    governorate=val.get("governorate"),
                    age=val.get("age"),
                    national_id=val.get("national_id"),
                )
                user_found = True
                break

        if user_found:
            messagebox.showinfo("Login Success", f"Welcome, {logged_in_user.get_name()}!")
            self.root.destroy()  
            app=NewFeed(logged_in_user.get_email())
            app.home_page()
             
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


if __name__=="__main__":
    
    loginPage()
