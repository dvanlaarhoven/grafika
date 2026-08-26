from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog
import customtkinter
import json
import sqlite3
import re
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

# Sets the initial theme and colour for the app
customtkinter.set_default_color_theme("blue")
customtkinter.set_appearance_mode("System")

window = customtkinter.CTk()
window.title('GRAFIKA')
icon_path = os.path.join(os.path.dirname(__file__), 'GrafikaPictures', 'GrafikaLogo1.ico')
window.iconbitmap(icon_path)
window.geometry('1920x1080')
window.resizable(True, True)

# Creating a database for the user details
conn = sqlite3.connect('grafika_users.db')

# Creates cursor
cursor = conn.cursor()

# Creates Table
cursor.execute("""CREATE TABLE IF NOT EXISTS userdetails (
           username text,
          password text
           )""")
# cursor.execute('DELETE FROM userdetails')

# Commit any changes
conn.commit()


username1 = 'Guest'
password1 = ''
project_name = ''


prev_x = None
prev_y = None


def guestAcc():
    global username1
    username1 = 'Guest'

    return username1


def x():
    pass


def loginPage():
    # This function is used to display the login page to the user
    clearWindow()

    def showPass():
        # Toggles password visibility on
        pass_entry.configure(show='')
        show_btn.configure(text='Hide', command=hidePass)

    def hidePass():
        # Toggles password visibility off
        pass_entry.configure(show='*')
        show_btn.configure(text='Show', command=showPass)

    def validateUser():
        global username1
        global password1

        # Stores username and password inputs
        username1 = username_entry.get()
        password1 = pass_entry.get()

    # Checks that the user has entered values
        if username1 != '' or password1 != '':

            # Selects all records from userdetails where the username = user input
            cursor.execute(
                'SELECT * FROM userdetails WHERE username=?', [username1])

            # Displays message if the username is not found within the database
            db_records = cursor.fetchall()

            if not db_records:
                error_label.configure(text='Account Does Not Exist!')
                guestAcc()

            else:
                # Checks that the password stored matches the user input
                cursor.execute(
                    'SELECT password FROM userdetails WHERE username=?', [username1])

                db_pass = cursor.fetchone()[0]

                if db_pass == password1:

                    error_label.configure(text='')
                    verify_label.configure(text='Login Successful!')
                    login_frame.after(400, startPage)

                else:
                    error_label.configure(
                        text=f'Incorrect Password for {username1}')
                    guestAcc()

        else:
            error_label.configure(text='Must enter a Username and Password')
            guestAcc()

    # Creates a frame for the widgets within the login page
    login_frame = customtkinter.CTkFrame(
        window, width=550, height=650, corner_radius=15)
    login_frame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    # These labels are used for the title and as indicators for the entry boxes
    login_label1 = customtkinter.CTkLabel(login_frame,
                                          text='\n Log In to Grafika ',
                                          font=('Calibri', 30))
    login_label1.place(relx=0.3)

    # Creates an entry box for the username
    username_entry = customtkinter.CTkEntry(login_frame,
                                            width=220,
                                            placeholder_text='Username',
                                            validatecommand=x
                                            )
    username_entry.place(relx=0.3, rely=0.3)

    # Creates an entry box for the password
    pass_entry = customtkinter.CTkEntry(login_frame,
                                        show='*',
                                        width=220,
                                        placeholder_text='Password',
                                        validatecommand=x)
    pass_entry.place(relx=0.3, rely=0.4)

    show_btn = customtkinter.CTkButton(login_frame,
                                       text='Show',
                                       width=50,
                                       corner_radius=5,
                                       font=('Calibri', 12),
                                       command=showPass)

    show_btn.place(relx=0.72, rely=0.4)

    login_btn = customtkinter.CTkButton(login_frame,
                                        text='Login',
                                        width=220,
                                        corner_radius=5,
                                        font=('Calibri', 16),
                                        command=validateUser)

    login_btn.place(relx=0.3, rely=0.53)

    sign_up_label = customtkinter.CTkLabel(
        login_frame, text='Don\'t have an account?', font=('Calibri', 12))
    sign_up_label.place(relx=0.29, rely=0.6)

    sign_up_btn = customtkinter.CTkButton(login_frame,
                                          text='Sign Up',
                                          width=80,
                                          corner_radius=5,
                                          font=('Calibri', 12),
                                          command=signUpPage)

    sign_up_btn.place(relx=0.55, rely=0.6)

    guest_label = customtkinter.CTkLabel(login_frame,
                                         text='Or...',
                                         font=('Calibri', 20))
    guest_label.place(relx=0.47, rely=0.75)

    guest_btn = customtkinter.CTkButton(login_frame,
                                        text='Continue As Guest',
                                        width=100,
                                        height=50,
                                        corner_radius=5,
                                        font=('Calibri', 16),
                                        command=startPage)

    guest_btn.place(relx=0.365, rely=0.8)

    verify_label = customtkinter.CTkLabel(login_frame,
                                          text='',
                                          text_color='#54a175',
                                          font=('Calibri', 16))
    verify_label.place(relx=0.3, rely=0.7)

    # Creates labels for displaying invalid input messages
    error_label = customtkinter.CTkLabel(login_frame,
                                         text='',
                                         text_color='red',
                                         font=('Calibri', 16))
    error_label.place(relx=0.25, rely=0.7)


def signUpPage():

    def showPass():
        # Toggles password visibility on
        pass_entry.configure(show='')
        show_btn.configure(text='Hide', command=hidePass)

    def hidePass():
        # Toggles password visibility off
        pass_entry.configure(show='*')
        show_btn.configure(text='Show', command=showPass)

    def createUser():
        global username1
        global password1

        def pass_check(password1):

            # Stores range of characters
            special_char = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
            upper_char = re.compile(r'[A-Z]')
            lower_char = re.compile(r'[a-z]')
            digit = re.compile(r'[0-9]')

            # Checks if atleast one of each character appears in the password
            symbol_check = special_char.search(password1) is not None
            upper_check = upper_char.search(password1) is not None
            lower_check = lower_char.search(password1) is not None
            digit_check = digit.search(password1) is not None

            if symbol_check and upper_check and lower_check and digit_check:
                return True
            else:
                return False

        def user_check(username1):

            # Stores range of characters
            upper_char = re.compile(r'[A-Z]')
            lower_char = re.compile(r'[a-z]')

            # Checks if atleast one of these characters appears in the username
            upper_check = upper_char.search(username1[0]) is not None
            lower_check = lower_char.search(username1[0]) is not None

            # Checks if the first character is a letter
            if upper_check or lower_check:
                return True
            else:
                return False

        global username1
        global password1
        # Stores username and password inputs
        username1 = username_entry.get()
        password1 = pass_entry.get()

        # Checks that the user has entered values
        if username1 != '' and password1 != '':

            # Checks that the password and username lengths are suitable
            if len(password1) >= 8 and len(username1) >= 5:

                # Checks if the username starts with a letter
                if user_check(username1) == True:

                    # Checks if the password contains all the required characters
                    if pass_check(password1) == True:

                        # Selects all records from table where the username = user input
                        cursor.execute(
                            'SELECT * FROM userdetails WHERE username=?', [username1])

                        # Displays message if any records are returned
                        db_records = cursor.fetchall()

                        # Displays error message if a username is found
                        if db_records:
                            error_label.configure(
                                text='Username Already Taken')
                            guestAcc()

                        else:
                            # Username and password added to database
                            cursor.execute('INSERT INTO userdetails VALUES (?,?)', [
                                username1, password1])
                            conn.commit()

                            error_label.configure(text='')
                            verify_label.configure(text='Sign-Up Successful!')
                            sign_up_frame.after(4000, startPage)

                    else:
                        error_label.configure(
                            text='Invalid Password - Must contain at Least: \n1 Special Character\n1 Uppercase character\n1 Lowercase character\n 1 Digit')
                        guestAcc()

                else:
                    error_label.configure(
                        text='Username Must Start With a letter!')
                    guestAcc()

            else:
                error_label.configure(
                    text='Invalid Details\nPlease Ensure that the Username and Password\n Meet the Requirements')
                guestAcc()
        else:
            error_label.configure(
                text='Must Enter a Username and Password')
            guestAcc()

    sign_up_frame = customtkinter.CTkFrame(
        window, width=550, height=650, corner_radius=15)
    sign_up_frame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    # These labels are used for the title and as indicators for the entry boxes
    sign_up_label1 = customtkinter.CTkLabel(sign_up_frame,
                                            text='\n Sign Up to Grafika',
                                            font=('Calibri', 30))
    sign_up_label1.place(relx=0.3)

    # Creates an entry box for the username
    username_entry = customtkinter.CTkEntry(sign_up_frame,
                                            width=220,
                                            placeholder_text='Create Username',
                                            validatecommand=x)
    username_entry.place(relx=0.3, rely=0.3)

    # Creates an entry box for the password
    pass_entry = customtkinter.CTkEntry(sign_up_frame,
                                        show='*',
                                        width=220,
                                        placeholder_text='Create Password',
                                        validatecommand=x)
    pass_entry.place(relx=0.3, rely=0.4)

    # Creates a button which hides/shows the password
    show_btn = customtkinter.CTkButton(sign_up_frame,
                                       text='Show',
                                       width=50,
                                       corner_radius=5,
                                       font=('Calibri', 12),
                                       command=showPass)

    show_btn.place(relx=0.72, rely=0.4)

    # Creates a button which allows the user to submit their new account details

    sign_up_btn = customtkinter.CTkButton(sign_up_frame,
                                          text='Sign Up',
                                          width=220,
                                          corner_radius=5,
                                          font=('Calibri', 16),
                                          command=createUser)

    sign_up_btn.place(relx=0.3, rely=0.53)

    guest_label = customtkinter.CTkLabel(sign_up_frame,
                                         text='Or...',
                                         font=('Calibri', 20))
    guest_label.place(relx=0.47, rely=0.65)

    guest_btn = customtkinter.CTkButton(sign_up_frame,
                                        text='Continue As Guest',
                                        width=100,
                                        height=50,
                                        corner_radius=5,
                                        font=('Calibri', 16),
                                        command=startPage)

    guest_btn.place(relx=0.365, rely=0.7)

    verify_label = customtkinter.CTkLabel(sign_up_frame,
                                          text='',
                                          text_color='#54a175',
                                          font=('Calibri', 16))
    verify_label.place(relx=0.25, rely=0.65)

    error_label = customtkinter.CTkLabel(sign_up_frame,
                                         text='',
                                         text_color='red',
                                         font=('Calibri', 16))
    error_label.place(relx=0.25, rely=0.65)

    back_btn1 = customtkinter.CTkButton(window,
                                        text='<',
                                        width=200,
                                        height=100,
                                        fg_color=('black', '#e14141'),
                                        hover_color='#fb7070',
                                        font=('Calibri', 40, 'bold'),
                                        command=main)

    back_btn1.place(x=50, y=480)


def informingUsers():
    clearWindow()

    def tutorialIntro():

        info_frame = customtkinter.CTkFrame(window, width=800, height=800)
        info_frame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

        back_btn = customtkinter.CTkButton(window,
                                           text='<',
                                           width=200,
                                           height=100,
                                           fg_color=('black', '#e14141'),
                                           hover_color='#fb7070',
                                           font=('Calibri', 40, 'bold'),
                                           command=startPage)
        back_btn.place(x=20, y=480)

        tutorial_tabs = customtkinter.CTkTabview(
            info_frame, width=700, height=700)
        tutorial_tabs.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        tutorial_tabs.pack_propagate(False)

        for i in range(7):
            tutorial_tabs.add(f'TAB {i+1}')

        tutorial_label = customtkinter.CTkLabel(
            tutorial_tabs.tab('TAB 1'),
            text='\nWelcome to Grafika!\n\n\n This is a graphics software where you can \n\ndraw characters, create logos, and more!\n\nThis works similar to apps such as Procreate and Clip Studio drawLine \n\n\n\n\nContinue reading to learn more',
            font=('Calibri', 22),
            width=100,
            height=400)
        tutorial_label.pack(padx=50)

        tutorial_label1 = customtkinter.CTkLabel(
            tutorial_tabs.tab('TAB 2'),
            text='The view projects page will be where you can see and access past projects \n\n\n\nThis is useful for if you want to continue working on a piece\n\n\n When you save your work, it will appear there \n\n\n The closer the drawing is to the top left, the newer it is\n\n\n',
            font=('Calibri', 22),
            width=100,
            height=600)
        tutorial_label1.pack(padx=50)

        tutorial_label2 = customtkinter.CTkLabel(
            tutorial_tabs.tab('TAB 3'),
            text='The canvas dimensions page is where you can create a canvas \n\n\n This can be tailored to your needs\n\n\nA YouTube thumbnail will require different dimensions to a YouTube banner\n\n\nThis is why this feature is important!',
            font=('Calibri', 22),
            width=100,
            height=600)
        tutorial_label2.pack(padx=50)

        tutorial_label3 = customtkinter.CTkLabel(
            tutorial_tabs.tab('TAB 4'),
            text='The creation page is where you can actually draw on the canvas\n\n The creation tools are all located along the top of the window\n\n The brush size slider is located at the left\n\n\nThe canvas will always appear in the middle \n\n',
            font=('Calibri', 22),
            width=100,
            height=600)
        tutorial_label3.pack(padx=50)

        tutorial_label4 = customtkinter.CTkLabel(
            tutorial_tabs.tab('TAB 5'),
            text='The basic tools include:\n\n Brush Colour  - Used to change the brush colour\nUseful as it allows for variety within a user\'s drawing\n\nCanvas Fill - Used to fill the canvas in one entire block of colour\nBoosts efficiency\n\nCustomise Window - Used to change the window colour\nBeneficial for users who want a certain work setting\n\nClear - Used to remove EVERYTHING that is present on the canvas',
            font=('Calibri', 22),
            width=100,
            height=600)
        tutorial_label4.pack(padx=50)

        tutorial_label5 = customtkinter.CTkLabel(
            tutorial_tabs.tab('TAB 6'),
            text='The other tools include:\n\n The Colour Prompt Tool\n\nThis is used to return a colour palette based on input prompts\n\ne.g Input: Ocean -> Shades of Blues\n\n Try this out yourself using the following prompts:\n- Retro\n- Snow \n- Futuristic\n- Blossom\n\nNOTE: This colour prompt system does not work well with more complex prompts\ne.g Arctic biome with polar bears\n\n\nThe Colour History \n\n Used to store your 5 most recent used colours\n\nClicking on it will allow you to use it again',
            font=('Calibri', 20),
            width=100,
            height=600)
        tutorial_label5.pack(padx=50)

        tutorial_label6 = customtkinter.CTkLabel(
            tutorial_tabs.tab('TAB 7'),
            text='DISCLAIMER:\n\n This project is still in beta so there are some features which\nhave yet to be implemented\n\n\n Some areas may also contain bugs\n\n If any are found, please let us know immediately\n\n\n\n Thank you for using Grafika!',
            font=('Calibri', 20),
            width=100,
            height=600)
        tutorial_label6.pack(padx=50)

    tutorialIntro()


def startPage():
    clearWindow()

    frame1 = customtkinter.CTkFrame(window, width=1920, height=1080)
    frame1.pack()

    logo_label = customtkinter.CTkLabel(frame1,
                                        text='GRAFIKA',
                                        font=('Calibri', 70))

    logo_label.place(relx=0.42, rely=0.15)

    new_button = customtkinter.CTkButton(
        frame1,
        text='New',
        height=350,
        width=350,
        font=('Calibri', 60, 'bold'),
        corner_radius=25,
        command=canvasDimensions,
    )
    new_button.place(relx=0.4, rely=0.5)

    view_button = customtkinter.CTkButton(
        frame1,
        text='View \nProjects',
        height=350,
        width=350,
        font=('Calibri', 50, 'bold'),
        corner_radius=25,
        command=viewProject,
    )
    view_button.place(relx=0.15, rely=0.5)

    info_button = customtkinter.CTkButton(frame1,
                                          height=350,
                                          width=350,
                                          text='Tutorial',
                                          font=('Calibri', 60, 'bold'),
                                          corner_radius=25, command=informingUsers)
    info_button.place(relx=0.65, rely=0.5)

    global username1
    user_label = customtkinter.CTkLabel(window, text=f'User: {username1}')
    user_label.place(relx=0.9, rely=0.95)

    log_out_btn = customtkinter.CTkButton(frame1,
                                          text='Log Out',
                                          width=100,
                                          corner_radius=5,
                                          command=loginPage)
    log_out_btn.place(relx=0.05, rely=0.05)


def clearWindow():
    # Destroys all widgets within the window
    for widgets in window.winfo_children():
        widgets.destroy()


def menuBar():
    # Provides a menu bar at the history_win of the screen
    menu1 = Menu(window)
    menu1.configure(bg='blue')

    # Creates the drop-down menu options for the File tab
    file_menu = Menu(menu1, tearoff=0)
    file_menu.add_command(label="New", command=canvasDimensions)
    file_menu.add_command(label="Open", command=x)
    file_menu.add_command(label="Save", command=x)
    file_menu.add_command(label="Save as...", command=x)
    file_menu.add_command(label="Close", command=x)

    # Adds a visual separator in the form of a horizontal line
    file_menu.add_separator()

    # Creates the drop-down menu options for the Edit tab
    file_menu.add_command(label="Exit", command=window.quit)
    menu1.add_cascade(label="File", menu=file_menu)
    edit_menu = Menu(menu1, tearoff=0)
    edit_menu.add_command(
        label="Undo", accelerator='CMD+Z', command=x)
    edit_menu.add_separator()
    edit_menu.add_command(label="Cut", accelerator='CMD+X', command=x)
    edit_menu.add_command(label="Copy", accelerator='CMD+C', command=x)
    edit_menu.add_command(label="Paste", accelerator='CMD+V', command=x)
    edit_menu.add_command(label="Delete", command=x)

    menu1.add_cascade(label="Edit", menu=edit_menu)
    helpmenu = Menu(menu1, tearoff=0)

    # Creates the drop-down menu options for the Help tab
    helpmenu.add_command(label="About...", command=x)
    menu1.add_cascade(label="Help", menu=helpmenu)

    window.config(menu=menu1)


def kbdShortcut(event):

    # Handle keyboard shortcuts

    if event.state == 0 and event.keysym.lower() == 'x':
        cmd = 'Cut'
        return cmd

    elif event.state == 0 and event.keysym.lower() == 'c':
        cmd = 'Copy'
        return cmd
    elif event.state == 0 and event.keysym.lower() == 'v':
        cmd = 'Paste'
        return cmd
    elif event.state == 0 and event.keysym.lower() == 'z':
        cmd = 'Undo'
        return cmd

    # Bind keyboard shortcuts to the window
    window.bind_all('<Command-x>', kbdShortcut)
    window.bind_all('<Command-c>', kbdShortcut)
    window.bind_all('<Command-v>', kbdShortcut)
    window.bind_all('<Command-z>', kbdShortcut)


def validateInput(text):
    # Checks if the input contains only digits and is not an empty string
    return text.isdigit() and text != ''


def validateWidthInput(text):
    return validateInput(text) and int(text) > 299 and int(text) < 1921


def validateHeightInput(text):
    return validateInput(text) and int(text) > 299 and int(text) < 1081


def canvasDimensions():
    clearWindow()
    # window.configure(fg_color='')

    def create_canvas():
        width_error_label.configure(text='')
        height_error_label.configure(text='')

        width = width_entry.get()
        height = height_entry.get()

        if validateWidthInput(width) and validateHeightInput(height):
            newProject(int(width), int(height))

        elif validateWidthInput(width) and not validateHeightInput(height):
            height_error_label.configure(
                text='INVALID HEIGHT \nMUST BE BETWEEN 300 <-> 1080')

        elif not validateWidthInput(width) and validateHeightInput(height):
            width_error_label.configure(
                text='INVALID WIDTH  \nMUST BE BETWEEN 300 <-> 1920')

        else:
            width_error_label.configure(
                text='INVALID WIDTH  \nMUST BE BETWEEN 300 <-> 1920')
            height_error_label.configure(
                text='INVALID HEIGHT \nMUST BE BETWEEN 300 <-> 1080')

    def canvasInfo():
        canvas_tabs = customtkinter.CTkTabview(window, width=50, height=50)
        canvas_tabs.place(x=1150, y=280)

        for i in range(4):
            canvas_tabs.add(f'TAB {i+1}')

        d_label1 = customtkinter.CTkLabel(canvas_tabs.tab('TAB 1'),
                                          text='\n\nCANVAS GUIDE',
                                          font=('Calibri', 45, 'bold'),
                                          width=100,
                                          height=400)
        d_label1.pack(padx=50)

        d_label1 = customtkinter.CTkLabel(
            canvas_tabs.tab('TAB 2'),
            text='\nThe Canvas Is The Area Where You Will Be Able To Draw\n\nThe Size To Use Will Vary Based On Your Needs, So Choose Wisely!\n\nWidth Must Be Between 300->1920\n\n Height Must Be Between 300->1080',
            font=('Calibri', 12, 'bold'),
            width=100,
            height=400)
        d_label1.pack(padx=50)

        d_label2 = customtkinter.CTkLabel(
            canvas_tabs.tab('TAB 3'),
            text='\n\nFor Reference:\n1920x1080 => Canvas Is 1920 Pixels Wide And 1080 Pixels Tall\n',
            font=('Calibri', 14, 'bold'),
            width=100,
            height=400)
        d_label2.pack(padx=50)

        d_label3 = customtkinter.CTkLabel(
            canvas_tabs.tab('TAB 4'),
            text='\nEXAMPLES:\n\n Youtube Thumbnail: 1280x720 \n\n Social Media Profile Picture: 800x800 \n ',
            font=('Calibri', 13, 'bold'),
            width=100,
            height=400)
        d_label3.pack(padx=50)

    global username1
    user_label = customtkinter.CTkLabel(window, text=f'User: {username1}')
    user_label.place(relx=0.9, rely=0.95)

    help_label1 = customtkinter.CTkLabel(
        window,
        text='Need Help?\n Read Through These Tabs. ',
        font=('Calibri', 20, 'bold'))
    help_label1.place(x=1240, y=200)

    canvasInfo()

    # Creates a frame for the entry boxes, text and create canvas button
    entry_frame = customtkinter.CTkFrame(window,
                                         height=600,
                                         width=800,
                                         corner_radius=30)
    entry_frame.place(x=300, y=200)
    entry_frame.pack_propagate(False)

    # These dimension labels are used for the title and extra information regarding canvases
    dimensions_label1 = customtkinter.CTkLabel(window,
                                               text='\nCANVAS DIMENSIONS',
                                               font=('Calibri', 60, 'bold'))
    dimensions_label1.place(x=400)

    width_label = customtkinter.CTkLabel(entry_frame,
                                         text='Canvas Width: ',
                                         font=('Calibri', 13, 'bold'))
    width_label.place(x=120, y=250)

    # Creates an entry box for the canvas width
    width_entry = customtkinter.CTkEntry(entry_frame,
                                         width=200,
                                         validatecommand=(validateWidthInput,
                                                          '%P'))
    width_entry.place(x=240, y=250)

    height_label = customtkinter.CTkLabel(entry_frame,
                                          text='Canvas Height: ',
                                          font=('Calibri', 13, 'bold'))
    height_label.place(x=120, y=350)

    # Creates an entry box for the canvas height
    height_entry = customtkinter.CTkEntry(entry_frame,
                                          width=200,
                                          validatecommand=(validateHeightInput,
                                                           '%P'))
    height_entry.place(x=240, y=350)

    # Creates labels for displaying invalid input messages
    width_error_label = customtkinter.CTkLabel(entry_frame,
                                               text='',
                                               text_color='red',
                                               font=('Calibri', 12))
    width_error_label.place(x=240, y=280)

    height_error_label = customtkinter.CTkLabel(entry_frame,
                                                text='',
                                                text_color='red',
                                                font=('Calibri', 12))
    height_error_label.place(x=240, y=380)

    # Creates a confirm button which allows the user to create their canvas
    confirm_btn = customtkinter.CTkButton(entry_frame,
                                          text='Create Canvas!',
                                          width=200,
                                          #   height=120,
                                          corner_radius=5,
                                          #   fg_color=('black', '#434343'),
                                          #   hover_color='#b0afaf',
                                          font=('Calibri', 16),
                                          command=create_canvas)

    confirm_btn.place(x=240, y=420)

    back_btn1 = customtkinter.CTkButton(window,
                                        text='<',
                                        width=200,
                                        height=100,
                                        fg_color=('black', '#e14141'),
                                        hover_color='#fb7070',
                                        font=('Calibri', 40, 'bold'),
                                        command=startPage)

    back_btn1.place(x=20, y=480)

    # return canvas_width, canvas_height


def newProject(canvas_width, canvas_height):
    global username1

    clearWindow()
    menuBar()

    frame2 = customtkinter.CTkFrame(window,
                                    bg_color='black',
                                    height=100,
                                    width=1920)
    frame2.pack()
    frame2.pack_propagate(False)

    canvas1 = customtkinter.CTkCanvas(window,
                                      width=canvas_width,
                                      height=canvas_height,
                                      bg='white')

    canvas1.pack(anchor=customtkinter.CENTER, expand=True)

    user_label = customtkinter.CTkLabel(window, text=f'User: {username1}')
    user_label.place(relx=0.9, rely=0.95)

    colour_code = ''
    last_colours = ''

    def chooseColour():
        # Store hex colour code
        global colour_code
        colour_code = colorchooser.askcolor()[1]
        if colour_code != None:
            colour_code = colour_code
        else:
            return None

        colourHistory(colour_code)
        return colour_code

    def colourHistory(colour_code):
        global username1
        # Used to store hex colour codes

        # Open the file in append mode (Can read/write)
        with open(os.path.join(base_dir, "colourHistory.txt"), "a+") as f:

            # Write the current color code to the file
            if colour_code is not None and colour_code != '':
                f.write(f'{username1}: {colour_code}\n')

            # Goes to beginning of the file
            f.seek(0)
            # Returns a list using each new line from the file as a list item
            lines = f.readlines()

            # Strip newline characters, split username from colour and store the colour
            account_colours = [line.strip().split()[1]
                               for line in lines if line.strip().split()[0] == f'{username1}:']

            #   Select the last 5 colours from that user
            last_colours = account_colours[-5:]

            # Print the list of the last 5 colours
            print(last_colours)

            return last_colours

    def historyWindow(last_colours):
        # This subroutine creates a pop up window for the colour history
        global username1

        # Returns the x and y positions of the history button widget
        history_x = history_btn.winfo_rootx()
        history_y = history_btn.winfo_rooty()

        # Adjusts x and y values
        win_x = history_x - 45
        win_y = history_y + 70

        history_win = Toplevel(window)
        # 300x50 sets the window dimensions, win_x + win_y sets the position
        history_win.geometry(f'300x50+{win_x}+{win_y}')
        history_win.title(f'{username1.upper()}\'S COLOUR HISTORY')

        # Creates a frame for the colour buttons
        history_frame = customtkinter.CTkFrame(history_win)
        history_frame.pack(fill="both", expand=True)

        history_frame.pack()
        history_frame.pack_propagate(False)

        # Creating buttons for each of the last 5 colours used

        for i, hex_code in enumerate(last_colours):
            colour_btn = customtkinter.CTkButton(
                history_frame, text='', fg_color=hex_code, hover_color=hex_code, width=60, height=50, command=lambda hex_code=hex_code: HistoryBrushColour(hex_code))
            colour_btn.grid(row=0, column=i)

        return last_colours

    def HistoryBrushColour(hex_code):
        # Sets brush colour to colour of button clicked
        brush_colour.set(hex_code)

    def openHistoryWindow():
        global last_colours

        #  Calls colourHistory subbroutine so list can be accessed
        last_colours = colourHistory(colour_code)
        historyWindow(last_colours)

    def promptWindow():
        # This function, 'promptWindow', creates a pop up window for the colour prompt system

        def searched():
            # Stores user propmpt input as a lowercase string
            raw_prompt = (prompt_entry.get()).lower()
            print(raw_prompt)

            res = colourAssociations(raw_prompt)
            if res:
                print(res)
            else:
                print('x')

            return

        def colourAssociations(raw_prompt):

            # def suggestedColour():
            #     # Open the file in append mode (Can read/write)
            #     with open('colourHistory.txt', 'a+') as file:

            #         # Write the current color code to the file
            #         file.write(f'{item}\n')
            #         brush_colour.set(item)

            # return

            # Opens the colour data JSON file in read only format
            with open(os.path.join(base_dir, "colourData.json"), "r") as f:
                colour_associations = json.load(f)
                c_data = colour_associations['colours']
                # print(c_data)

            # Creates a list to store the colours

            prompt_colours = []

            # Iterates through the list of dictionaries under 'colours' from JSON filw
            for colour_group in c_data:

                # Checks if user input appears as a key in any of the colour-based dictionaries
                if raw_prompt in colour_group:

                    # Assigns value associated with prompt key to this variable in the form of a list
                    prompt_colours = colour_group[f'{raw_prompt}']
                    print(prompt_colours)

                    for i, hex_code in enumerate(prompt_colours):
                        colour_btn = customtkinter.CTkButton(prompt_frame1,
                                                             text='',
                                                             fg_color=hex_code,
                                                             hover_color=hex_code,
                                                             width=60,
                                                             height=50,
                                                             command=lambda hex_code=hex_code: HistoryBrushColour(hex_code))
                        colour_btn.grid(row=0, column=i)

        # Returns the x and y positions of the prompt button widget
        prompt_x = prompt_btn.winfo_rootx()
        prompt_y = prompt_btn.winfo_rooty()

        # Adjusts x and y values of where window appears
        win_x = prompt_x - 45
        win_y = prompt_y + 70

        prompt_win = Toplevel(window)
        # 400x400 sets the window dimensions, win_x + win_y sets the position
        prompt_win.geometry(f'400x200+{win_x}+{win_y}')
        prompt_win.title('COLOUR PALETTE PROMPT')

        # Creates frame for entry box and submit button
        prompt_frame = customtkinter.CTkFrame(
            prompt_win,
            width=400,
            height=50,
            bg_color='black')
        prompt_frame.grid(row=0, column=0)

        # Creates frame for colours
        prompt_frame1 = customtkinter.CTkFrame(
            prompt_win,
            width=400,
            height=100,
            bg_color='black')
        prompt_frame1.grid(row=1, column=0)
        prompt_frame1.pack_propagate(False)

        # Creates entry box for user to enter prompt
        prompt_entry = customtkinter.CTkEntry(
            prompt_frame, placeholder_text='Enter Prompt')
        prompt_entry.place(relx=0.05, rely=0.2)

        # Creates button for user to submit prompt
        prompt_submit = customtkinter.CTkButton(
            prompt_frame, text='CREATE PALETTE!', command=searched)
        prompt_submit.place(relx=0.5, rely=0.2)

        return

    def clearCanvas():
        canvas1.delete('all')
        canvas1.configure(bg='white')

    def fillCanvas():
        # Changes the background colour of the canvas
        canvas1.configure(bg=chooseColour())

    def customiseWindow():
        # Changes the background colour of the window and button colours

        # Returns the x and y positions of the prompt button widget
        # custom_x = window_color_btn.winfo_rootx()
        # custom_y = window_color_btn.winfo_rooty()

        # Creates pop-up window
        custom_win = Toplevel(window)
        custom_win.geometry('280x30+615+130')

        def windowColour():
            window.configure(fg_color=chooseColour())
            window.update_idletasks()

        def reverseChanges():
            window.configure(fg_color='#282728')

        reverse_btn = customtkinter.CTkButton(custom_win,
                                              text='Reverse Changes',
                                              command=reverseChanges)

        window_btn = customtkinter.CTkButton(custom_win,
                                             text='Edit Window Colour',
                                             command=windowColour)
        reverse_btn.grid(row=0, column=0)
        window_btn.grid(row=0, column=1)

    def brushColour():
        # Changes the brush colour
        brush_colour.set(chooseColour())

    def brushSize(value):
        # Changes the brush size based on slider
        global current_size

        current_size = int(value)
        brush_size.set(current_size)
        # print(f'Brush size: {current_size}')

    brush_colour = StringVar()
    brush_colour.set('black')

    brush_size = StringVar()
    brush_size.set(4)

    def drawLine(event):

        global prev_x, prev_y
        x = event.x
        y = event.y

        # If the previous position exists, this will draw a line from previous position to current
        if prev_x is not None and prev_y is not None:
            canvas1.create_line(prev_x, prev_y, x, y,
                                fill=brush_colour.get(), width=brush_size.get(), splinesteps=36)

        # Updates previous position to current position
        prev_x = x
        prev_y = y

    def release(event):
        global prev_x, prev_y

        # Resets previous position when the mouse button is released
        prev_x = None
        prev_y = None

    canvas1.bind('<B1-Motion>', drawLine)
    canvas1.bind('<ButtonRelease-1>', release)

    def saveCanvas():

        def saving():

            # Displays a pop-up window where the user can choose a file name and path
            file_path = filedialog.asksaveasfilename(
                defaultextension=file_type_list.get())

            # Saves canvas as postscript file
            ps_file = f'{file_path}.ps'
            canvas1.postscript(file=ps_file, colormode='color')

            # Get the canvas background color
            canvas_bg_color = canvas1.cget('background')

            # Opens the Ps file as an image
            image = Image.open(ps_file)

            # Saves actual image
            image.save(file_path)

            # Removes the Ps file as it is no longer needed
            os.remove(ps_file)

            save_win.destroy()

        save_win = Toplevel(window)
        save_win.geometry('300x50+600+130')
        save_win.title('File Extension')

        file_types = ['.png', '.jpg']

        file_type_list = customtkinter.CTkOptionMenu(
            save_win, values=file_types)
        file_type_list.grid(row=0, column=0)

        save_btn1 = customtkinter.CTkButton(
            save_win, text='Enter', command=saving)
        save_btn1.grid(row=0, column=1)

    brush_slider = customtkinter.CTkSlider(window,
                                           from_=1,
                                           to=20,
                                           height=250,
                                           width=25,
                                           orientation=VERTICAL,
                                           number_of_steps=20,
                                           button_hover_color='black',
                                           command=brushSize)
    brush_slider.place(relx=0.01, rely=0.5)

    # Sets the initial brush size
    brush_slider.set(4)
    current_size = int(brush_slider.get())

    # Button used to go back to canvas dimensions page
    back_btn2 = customtkinter.CTkButton(frame2,
                                        width=200,
                                        height=60,
                                        text='<',
                                        fg_color=('black', '#e14141'),
                                        font=('Calibri', 30, 'bold'),
                                        command=canvasDimensions)
    back_btn2.grid(row=0, column=0)

    # Button used to select the brush colour
    brush_btn1 = customtkinter.CTkButton(frame2,
                                         text='BRUSH COLOUR',
                                         font=('calibri', 18, 'bold'),
                                         command=brushColour,
                                         width=200,
                                         height=60)
    brush_btn1.grid(row=0, column=1)

    # Button used to fill the canvas with one colour
    fill_btn = customtkinter.CTkButton(frame2,
                                       text='FILL CANVAS',
                                       font=('calibri', 18, 'bold'),
                                       command=fillCanvas,
                                       width=200,
                                       height=60)
    fill_btn.grid(row=0, column=2)

    # Button used to customise the window colour
    window_color_btn = customtkinter.CTkButton(frame2,
                                               text='CUSTOMISE WINDOW',
                                               text_color='white',
                                               width=300,
                                               height=60,
                                               font=('calibri', 18, 'bold'),
                                               command=customiseWindow)
    window_color_btn.grid(row=0, column=3)

    # Button used to allow user to enter a prompt for a colour palette
    prompt_btn = customtkinter.CTkButton(frame2,
                                         text='COLOUR PROMPT',
                                         text_color='white',
                                         width=300,
                                         height=60,
                                         font=('calibri', 18, 'bold'),
                                         command=promptWindow)
    prompt_btn.grid(row=0, column=4)

    # Button used to display user's colour history
    history_btn = customtkinter.CTkButton(frame2,
                                          text='COLOUR HISTORY',
                                          text_color='white',
                                          width=200,
                                          height=60,
                                          font=('calibri', 18, 'bold'),
                                          command=openHistoryWindow)
    history_btn.grid(row=0, column=5)

    # Button used to clear EVERYTHING on the canvas
    clear_btn = customtkinter.CTkButton(frame2,
                                        text='CLEAR',
                                        text_color='white',
                                        width=130,
                                        height=60,
                                        font=('calibri', 18, 'bold'),
                                        command=clearCanvas)

    clear_btn.grid(row=0, column=6)

    save_btn = customtkinter.CTkButton(frame2,
                                       text='SAVE',
                                       width=130,
                                       height=60,
                                       font=('calibri', 18, 'bold'),
                                       command=saveCanvas)
    save_btn.grid(row=0, column=7)


def viewProject():
    clearWindow()
    # Indicates that there are currently no projects to view
    empty_label = customtkinter.CTkLabel(window,
                                         height=100,
                                         width=100,
                                         text='No Projects')
    empty_label.pack()

    # Button used to go back to the start page
    back_btn = customtkinter.CTkButton(window,
                                       height=100,
                                       width=200,
                                       text='>',
                                       font=('Calibri', 40, 'bold'),
                                       hover_color='#fb7070',
                                       fg_color=('black', '#e14141'),
                                       command=startPage).place(x=1400, y=480)


def main():
    # Main function used to start the main page
    clearWindow()
    loginPage()


main()

# run
window.mainloop()
