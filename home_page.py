import tkinter as tk
from tkinter import font
from tkinter import messagebox
from PIL import Image, ImageTk
import json


class UserManager:
    USER_DATA_FILE = 'user_data.json'

    def __init__(self):
        self.user_data = self.load_user_data()

    def load_user_data(self):
        try:
            with open(self.USER_DATA_FILE, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_user_data(self):
        with open(self.USER_DATA_FILE, 'w') as file:
            json.dump(self.user_data, file, indent=4)

    def search_user(self, username):
        for user_email, user_info in self.user_data.items():
            if user_info['username'] == username:
                return user_email, user_info
        return None, None

    def is_friend(self, user_email, friend_email):
        return friend_email in self.user_data[user_email]['friends']

    def send_friend_request(self, user_email, friend_email):
        # Check if the user is already friends or if the request is already pending
        if friend_email in self.user_data[user_email]['friends']:
            return False, "You are already friends."

        elif user_email in self.user_data[friend_email]['friend_requests']:
            return False, "Friend request already sent. Please wait for a response."

        elif friend_email in self.user_data[user_email]['friend_requests']:
            return False, "You have received a friend request from this user. Accept or reject it first."

        # Add the friend request
        self.user_data[friend_email]['friend_requests'].append(user_email)
        self.save_user_data()
        return True, "Friend request sent successfully!"

    def get_friend_requests(self, user_email):
        return self.user_data[user_email]['friend_requests']

    def get_friends(self, user_email):
        return self.user_data[user_email]['friends']

    def accept_friend_request(self, user_email, friend_email):
        if friend_email in self.user_data[user_email]['friend_requests']:
            self.user_data[user_email]['friend_requests'].remove(friend_email)
            self.user_data[user_email]['friends'].append(friend_email)
            self.user_data[friend_email]['friends'].append(user_email)
            self.save_user_data()

    def reject_friend_request(self, user_email, friend_email):
        if friend_email in self.user_data[user_email]['friend_requests']:
            self.user_data[user_email]['friend_requests'].remove(friend_email)
            self.save_user_data()

    def add_post(self, user_email, content):
        self.user_data[user_email]["posts"].append(content)
        self.save_user_data()

    def get_my_posts(self, user_email):
        return self.user_data[user_email]["posts"]

    def get_username(self, user_email):
        if user_email in self.user_data:
            return self.user_data[user_email]["username"]
        else:
            return None



class NewFeed:
    def __init__(self, cur_email):
        self.root = tk.Tk()
        self.root.title("SIC Community")
        self.root.geometry("700x600")
        self.current_user_email = cur_email
        self.user_manager = UserManager()

    def home_page(self):
        self.clear_window()
        self.title_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.post_font = font.Font(family="Helvetica", size=12)
        self.comment_font = font.Font(family="Helvetica", size=10)

        main_frame = tk.Frame(self.root, bg="#2c3e50", bd=5, relief="solid")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.buttons_frame = tk.Frame(main_frame, bg="#ecf0f1", bd=5, relief="solid", height=300)
        self.buttons_frame.pack(fill=tk.BOTH, side=tk.TOP, padx=10, pady=10)

        self.add_post = tk.Button(main_frame, text="Click here to add post...", font=self.title_font, width=40,
                                  height=3, bg="#3498db", fg="white", command= self.add_post_window)
        self.add_post.pack(side=tk.TOP, padx=(20, 10), pady=(10, 10))

        self.canvas = tk.Canvas(main_frame, bg="#2c3e50")
        self.scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2c3e50")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.friends_button = tk.Button(self.buttons_frame, text="Friends", bg="#1abc9c", font=self.button_font,
                                        width=10, height=3, fg="white", command=self.show_friends_page)
        self.friends_button.pack(side=tk.LEFT, padx=20)

        self.my_posts = tk.Button(self.buttons_frame, text="My posts", font=self.button_font, bg="#1abc9c", width=10,
                                  height=3, fg="white", command=self.show_my_posts)
        self.my_posts.pack(padx=21, side=tk.LEFT)

        # Search entry (beside the search button)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.buttons_frame, textvariable=self.search_var, font=self.post_font, width=20)
        self.search_entry.pack(side=tk.RIGHT, padx=5)

        self.search_button = tk.Button(self.buttons_frame, text="Search", font=self.button_font, bg="#1abc9c", width=10,
                                       height=3, fg="white", command=self.search_user)
        self.search_button.pack(side=tk.RIGHT, padx=5)

        self.load_posts_from_friends()

    def load_posts_from_friends(self):
        user_email = self.current_user_email
        friends = self.user_manager.get_friends(user_email)

        for friend_email in friends:
            friend_posts = self.user_manager.user_data[friend_email]['posts']
            friend_username = self.user_manager.user_data[friend_email]['username']
            for post in friend_posts:
                self.add_posts(self.scrollable_frame, post, friend_username, friend_email)

    def add_posts(self, frame, post, username, email):
        post_frame = tk.Frame(frame, bg="#ffffff", bd=2, relief="solid", padx=10, pady=15)
        post_frame.pack(fill=tk.X, pady=5, expand=True)

        username_label = tk.Label(post_frame, text=username, font=("Helvetica", 16, "bold"), bg="#ffffff")
        username_label.pack(anchor='w')

        content_label = tk.Label(post_frame, text=post['content'], font=("Helvetica", 12), bg="#ffffff")
        content_label.pack(anchor='w', pady=5)

        post_frame.likes = post['reactions']
        post_frame.liked = False
        post_frame.likes_label = tk.Label(post_frame, text=f"Likes: {post_frame.likes}", font=("Helvetica", 10),
                                          bg="#ffffff")
        post_frame.likes_label.pack(side=tk.LEFT, padx=5, pady=5)

        react_image = Image.open("react.png")
        react_image = react_image.resize((20, 20))
        post_frame.react_image = ImageTk.PhotoImage(react_image)

        react_button = tk.Button(post_frame, image=post_frame.react_image,
                                 command=lambda: self.toggle_like(post_frame, post, email))
        react_button.pack(side=tk.LEFT, padx=5, pady=5)

        comment_button = tk.Button(post_frame, text="Comment", font=("Helvetica", 10),
                                   command=lambda: self.add_comment(post_frame, post, email))
        comment_button.pack(side=tk.LEFT, padx=5, pady=5)

        comments_frame = tk.Frame(post_frame, bg="#f0f0f0", bd=1, relief="solid", padx=5, pady=5)
        comments_frame.pack(fill=tk.X, pady=5)
        post_frame.comments_frame = comments_frame

        for comment in post['comments']:
            self.display_comment(comments_frame, comment)

    def display_comment(self, comments_frame, comment):
        comment_label = tk.Label(comments_frame, text=comment, font=("Helvetica", 10), bg="#f0f0f0", anchor='w',
                                 wraplength=400)
        comment_label.pack(fill=tk.X, anchor='w', padx=5, pady=2)


    def toggle_like(self, post_frame, post, email):
        if post_frame.liked:
            post_frame.likes -= 1
            post_frame.liked = False
        else:
            post_frame.likes += 1
            post_frame.liked = True
        post_frame.likes_label.config(text=f"Likes: {post_frame.likes}")
        post['reactions'] = post_frame.likes

        # Update the user_data.json file
        self.save_to_user_data(email)

    def add_comment(self, post_frame, post, email):
        if hasattr(post_frame, 'comment_entry') and post_frame.comment_entry.winfo_exists():
            return

        comment_frame = tk.Frame(post_frame, bg="#f0f0f0", bd=1, relief="solid", padx=5, pady=5)
        comment_frame.pack(fill=tk.X, pady=5)

        post_frame.comment_entry = tk.Entry(comment_frame, font=("Helvetica", 10))
        post_frame.comment_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        submit_button = tk.Button(comment_frame, text="Submit", font=("Helvetica", 10),
                                  command=lambda: self.submit_comment(post_frame, post, email))
        submit_button.pack(side=tk.RIGHT, padx=5)

    def submit_comment(self, post_frame, post, email):
        comment_text = self.user_manager.get_username(self.current_user_email)+": "+post_frame.comment_entry.get()
        if comment_text:
            self.display_comment(post_frame.comments_frame, comment_text)
            post['comments'].append(comment_text)
            self.save_to_user_data(email)
            post_frame.comment_entry.destroy()

    def save_to_user_data(self, email):
        self.user_manager.save_user_data()
        messagebox.showinfo("Update", f"Post updated for {self.user_manager.user_data[email]['username']}")

    def show_friends_page(self):
        self.clear_window()

        main_frame = tk.Frame(self.root, bg="#2c3e50", bd=5, relief="solid")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        friends_label = tk.Label(main_frame, text="Friends", font=self.title_font, bg="#2c3e50", fg="white")
        friends_label.grid(row=1, column=0, padx=10, pady=10)

        # Friends List
        friends = self.user_manager.get_friends(self.current_user_email)
        for idx, friend_email in enumerate(friends):
            friend_label = tk.Label(main_frame, text=self.user_manager.user_data[friend_email]['username'],
                                    font=self.button_font, bg="#1abc9c", fg="white")
            friend_label.grid(row=idx + 2, column=0, padx=10, pady=5, sticky="w")

        # Friend Requests Section
        requests_label = tk.Label(main_frame, text="Friend Requests", font=self.title_font, bg="#2c3e50",
                                  fg="white")
        requests_label.grid(row=1, column=1, padx=10, pady=10)

        friend_requests = self.user_manager.get_friend_requests(self.current_user_email)
        for idx, request_email in enumerate(friend_requests):
            request_username = self.user_manager.user_data[request_email]['username']
            request_label = tk.Label(main_frame, text=request_username, font=self.button_font, bg="#ecf0f1",
                                     fg="black")
            request_label.grid(row=idx + 2, column=1, padx=10, pady=5, sticky="w")

            accept_button = tk.Button(main_frame, text="Accept", font=self.button_font, bg="#1abc9c", fg="white",
                                      command=lambda req_email=request_email: self.accept_friend_request(req_email))
            accept_button.grid(row=idx + 2, column=2, padx=10, pady=5)

            reject_button = tk.Button(main_frame, text="Reject", font=self.button_font, bg="#e74c3c", fg="white",
                                      command=lambda req_email=request_email: self.reject_friend_request(req_email))
            reject_button.grid(row=idx + 2, column=3, padx=10, pady=5)

        back_button = tk.Button(main_frame, text="← Back", font=self.button_font, bg="#3498db", fg="white",
                                command=self.home_page)
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def accept_friend_request(self, friend_email):
        self.user_manager.accept_friend_request(self.current_user_email, friend_email)
        messagebox.showinfo("Friend Request", "Friend request accepted.")
        self.show_friends_page()

    def reject_friend_request(self, friend_email):
        self.user_manager.reject_friend_request(self.current_user_email, friend_email)
        messagebox.showinfo("Friend Request", "Friend request rejected.")
        self.show_friends_page()

    def search_user(self):
        username = self.search_entry.get()
        friend_email, friend_info = self.user_manager.search_user(username)
        if username == self.user_manager.user_data[self.current_user_email]['username']:
            messagebox.showinfo("Search", "You cannot search for yourself.")
            return
        if friend_email:
            self.show_user_search_result(friend_email, friend_info)
        else:
            messagebox.showinfo("Search", "User not found.")

    def show_user_search_result(self, friend_email, friend_info):
        self.clear_window()

        main_frame = tk.Frame(self.root, bg="#2c3e50", bd=5, relief="solid")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        back_button = tk.Button(main_frame, text="← Back", font=self.button_font, bg="#3498db", fg="white",
                                command=self.home_page)
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        user_label = tk.Label(main_frame, text=friend_info['username'], font=self.title_font, bg="#1abc9c",
                              fg="white")
        user_label.grid(row=1, column=1, padx=10, pady=10)

        if self.user_manager.is_friend(self.current_user_email, friend_email):
            show_profile_button = tk.Button(main_frame, text="Show User Profile", font=self.button_font,
                                            bg="#1abc9c", fg="white", command= lambda: self.show_user_profile(friend_email))
            show_profile_button.grid(row=2, column=1, padx=10, pady=10)
        else:
            send_request_button = tk.Button(main_frame, text="Send Friend Request", font=self.button_font,
                                            bg="#1abc9c", fg="white",
                                            command=lambda: self.send_friend_request(friend_email))
            send_request_button.grid(row=2, column=1, padx=10, pady=10)

    def send_friend_request(self, friend_email):
        success, message = self.user_manager.send_friend_request(self.current_user_email, friend_email)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showwarning("Error", message)

    def show_user_profile(self, user_email):
        user_info = self.user_manager.user_data[user_email]

        # Create a new window (Toplevel)
        profile_window = tk.Toplevel(self.root)
        profile_window.title(f"{user_info['username']}'s Profile")
        profile_window.geometry("500x600")

        profile_frame = tk.Frame(profile_window, bg="#2c3e50", bd=5, relief="solid")
        profile_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        username_label = tk.Label(profile_frame, text=f"Username: {user_info['username']}", font=self.title_font,
                                  bg="#1abc9c", fg="white")
        username_label.pack(anchor="center", pady=20)

        email_label = tk.Label(profile_frame, text=f"Email: {user_email}", font=self.post_font, bg="#2c3e50",
                               fg="white")
        email_label.pack(anchor="center", pady=10)

        friends_label = tk.Label(profile_frame, text=f"Friends: {len(user_info['friends'])}", font=self.post_font,
                                 bg="#2c3e50", fg="white")
        friends_label.pack(anchor="center", pady=10)

        posts_label = tk.Label(profile_frame, text="Posts", font=self.title_font, bg="#1abc9c", fg="white")
        posts_label.pack(anchor="center", pady=20)

        # Display user posts in a scrollable frame
        post_canvas = tk.Canvas(profile_frame, bg="#2c3e50")
        post_scrollbar = tk.Scrollbar(profile_frame, orient="vertical", command=post_canvas.yview)
        post_scrollable_frame = tk.Frame(post_canvas, bg="#2c3e50")

        post_scrollable_frame.bind(
            "<Configure>",
            lambda e: post_canvas.configure(scrollregion=post_canvas.bbox("all"))
        )

        post_canvas.create_window((0, 0), window=post_scrollable_frame, anchor="nw")
        post_canvas.configure(yscrollcommand=post_scrollbar.set)

        post_canvas.pack(side="left", fill="both", expand=True)
        post_scrollbar.pack(side="right", fill="y")

        for post in user_info['posts']:
            post_frame = tk.Frame(post_scrollable_frame, bg="#ecf0f1", bd=2, relief="solid", padx=10, pady=15)
            post_frame.pack(fill=tk.X, pady=10, padx=5)

            # Add padding and better alignment for post content
            content_label = tk.Label(post_frame, text=post['content'], font=("Helvetica", 12), bg="#ecf0f1",
                                     wraplength=400, justify="left")
            content_label.pack(anchor='w', pady=5)

            likes_label = tk.Label(post_frame, text=f"Likes: {post['reactions']}", font=("Helvetica", 10), bg="#ecf0f1")
            likes_label.pack(anchor='w', pady=5)

        # Add a close button to the new window
        close_button = tk.Button(profile_frame, text="Close", font=("Helvetica", 12), bg="#3498db", fg="white",
                                 command=profile_window.destroy)
        close_button.pack(pady=20)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_post_window(self):
        add_post_window = tk.Toplevel(self.root)
        add_post_window.title("ADD POST")
        add_post_window.geometry("600x600")

        post_frame = tk.Frame(add_post_window, bg="#34433f", bd=5, relief="solid")
        post_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        write_post_here_frame = tk.Frame(post_frame, bg="#e1f6f0", bd=5, relief="solid")
        write_post_here_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True, pady=30, padx=30)

        submit_button = tk.Button(post_frame, text="Submit", bg="#638383", font="Tahoma 15 bold", width=15,
                                height=3, command=lambda: self.submit_post(add_post_window))
        submit_button.pack(pady=50)

        # Label and text box for post content
        content_label = tk.Label(write_post_here_frame, text="write here....", font="Arial 18 bold",
                                bg="#e1f6f0")
        content_label.pack(side=tk.TOP, pady=10)
        self.content_text = tk.Text(write_post_here_frame, font="Arial 15", height=5, width=45, bg="#e1f6f0")
        self.content_text.pack(pady=10)

    def submit_post(self, add_post_window):
        content = {
            "content": self.content_text.get("1.0", "end-1c"),
            "reactions": 0,
            "comments": [],
            "date": ""
        }
        self.user_manager.add_post(self.current_user_email, content)
        messagebox.showinfo("Post Added", "Your post has been added successfully!")
        add_post_window.destroy()

    def show_my_posts(self):
        self.clear_window()

        posts = self.user_manager.get_my_posts(self.current_user_email)

        # Create a scrollable frame for the posts
        self.canvas = tk.Canvas(self.root, bg="#2c3e50")
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2c3e50")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Add a back button
        back_button = tk.Button(self.scrollable_frame, text="← Back", font=self.button_font, bg="#3498db", fg="white",
                                command=self.home_page)
        back_button.pack(pady=10)

        # Display the posts
        for post in posts:
            self.display_post_with_edit_option(post)

    def display_post_with_edit_option(self, post):
        # Frame for each post
        post_frame = tk.Frame(self.scrollable_frame, bg="#ffffff", bd=2, relief="solid", padx=10, pady=15)
        post_frame.pack(fill=tk.X, pady=5, expand=True)

        # Display the post content
        post_content_label = tk.Label(post_frame, text=f"{post['content']}\n{post['reactions']}\n{post['comments']}", font=("Helvetica", 12), bg="#ffffff")
        post_content_label.pack(anchor='w', pady=5)

        # Edit button
        edit_button = tk.Button(post_frame, text="Edit", font=("Helvetica", 10), bg="#f39c12", fg="white",
                                command=lambda p=post: self.open_edit_post_window(p))
        edit_button.pack(side=tk.RIGHT, padx=10)

    def open_edit_post_window(self, post):
        # Open a new window to edit the post
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Post")
        edit_window.geometry("400x400")

        edit_frame = tk.Frame(edit_window, bg="#34433f", bd=5, relief="solid")
        edit_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        content_label = tk.Label(edit_frame, text="Edit your post:", font="Arial 15 bold", bg="#e1f6f0")
        content_label.pack(pady=10)

        self.edit_text = tk.Text(edit_frame, font="Arial 12", height=5, width=45, bg="#e1f6f0")
        self.edit_text.insert("1.0", post["content"])  # Insert current content into the text box
        self.edit_text.pack(pady=10)

        save_button = tk.Button(edit_frame, text="Save", font="Tahoma 12 bold", bg="#638383", width=15,
                                command=lambda: self.save_edited_post(edit_window, post))
        save_button.pack(pady=20)

    def save_edited_post(self, edit_window, post):
        # Get the updated content
        new_content = self.edit_text.get("1.0", "end-1c")

        if new_content.strip():
            # Update the post content
            post["content"] = new_content

            # Save changes to the JSON file
            self.user_manager.save_user_data()

            # Show a success message
            messagebox.showinfo("Success", "Post updated successfully!")

            # Close the edit window
            edit_window.destroy()

            # Refresh the posts view
            self.show_my_posts()
        else:
            messagebox.showwarning("Error", "Post content cannot be empty.")


if __name__ == "__main__":
    app = NewFeed("adam@gmail.com")
    app.home_page()
    app.root.mainloop()
