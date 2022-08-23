from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json



def generate():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    symbols = ['!', '#', '$', '%', '&', '*', '+']

    char_list = [choice(letters) for char in range(randint(8, 10))]
    number_list = [choice(numbers) for num in range(randint(2, 4))]
    symbol_list = [choice(symbols) for special in range(randint(2, 4))]

    password_list = char_list + number_list + symbol_list
    shuffle(password_list)

    pass_word = "".join(password_list)
    password_entry.insert(0, pass_word)

    ok = messagebox.askyesno(title="Clipboard", message="Do you want to copy the password")
    if ok:
        pyperclip.copy(pass_word)


def save():
    website_name = website_entry.get()
    email_id = email_entry.get()
    pass_word = password_entry.get()
    new_data = {
        website: {
            "email": email_id,
            "password": pass_word,
        },
    }

    if len(website_name) == 0 or len(pass_word) == 0:
        messagebox.showinfo(title="Don't be over smart", message="Don't leave any fields empty")
    else:
        is_ok = messagebox.askokcancel(title=website_name,
                                       message=f"These are the details entered: \nWebsite: {website_name}\n"
                                               f"Email: {email_id}\nPassword: "f"{pass_word}\nDo you want to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


def find_password():
    web_site = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except ValueError:
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        if web_site in data:
            email_id = data[web_site]["email"]
            pass_word = data[web_site]["password"]
            messagebox.showinfo(title=web_site, message=f"Email: {email_id}\nPassword: {pass_word}")
        else:
            messagebox.showinfo(title="Error", message=f"No Details for {web_site} exists")


windows = Tk()
windows.title("Password Manager")
windows.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

website = Label(text="Website", font=("courier", 15, "bold"))
website.grid(column=0, row=1)

email = Label(text="Email/Username ", font=("courier", 15, "bold"))
email.grid(column=0, row=2)

password = Label(text="Password", font=("courier", 15, "bold"))
password.grid(column=0, row=3)

website_entry = Entry(width=32, font=("courier", 13, "bold"))
website_entry.grid(column=1, row=1)
website_entry.focus()

email_entry = Entry(width=45, font=("courier", 11, "bold"))
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "")

password_entry = Entry(width=32, font=("courier", 13, "bold"))
password_entry.grid(column=1, row=3)

gene_rate = Button(text="Generate", width=10, command=generate)
gene_rate.grid(column=2, row=3)

add = Button(text="Add", width=57, command=save)
add.grid(column=1, row=4, columnspan=2)

search = Button(text="Search", width=10, command=find_password)
search.grid(column=2, row=1)

windows.mainloop()
