from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk

starting_width = 960
starting_height = 540
ratio = 1  # The ratio by which the size of the background image changes after rescaling
text_position_x = 0
text_position_y = 0
font_file = 'arial.ttf'
font_size = 60
r = 255
g = 255
b = 255
alpha = 255  # Opacity
background_image = Image.new("RGBA", (1, 1))
text_image = Image.new("RGBA", (1, 1))
center_text = True
fonts_names = ['Arial', 'Calibri', 'Cambria', 'Comic Sans', 'Courier New', 'Georgia',
               'Times New Roman', 'Trebuchet MS', 'Verdana']
fonts_files = {
    'Arial': 'arial.ttf',
    'Arial Italic': 'ariali.ttf',
    'Arial Bold': 'arialbd.ttf',
    'Arial Bold Italic': 'arialbi.ttf',
    'Calibri': 'calibri.ttf',
    'Calibri Italic': 'calibrii.ttf',
    'Calibri Bold': 'calibrib.ttf',
    'Calibri Bold Italic': 'calibriz.ttf',
    'Cambria': 'cambria.ttc',
    'Cambria Italic': 'cambriai.ttf',
    'Cambria Bold': 'cambriab.ttf',
    'Cambria Bold Italic': 'cambriaz.ttf',
    'Comic Sans': 'comic.ttf',
    'Comic Sans Italic': 'comici.ttf',
    'Comic Sans Bold': 'comicbd.ttf',
    'Comic Sans Bold Italic':  'comicz.ttf',
    'Courier New': 'cour.ttf',
    'Courier New Italic': 'couri.ttf',
    'Courier New Bold': 'courbd.ttf',
    'Courier New Bold Italic': 'courbi.ttf',
    'Georgia': 'georgia.ttf',
    'Georgia Italic': 'georgiai.ttf',
    'Georgia Bold': 'georgiab.ttf',
    'Georgia Bold Italic': 'georgiaz.ttf',
    'Times New Roman': 'times.ttf',
    'Times New Roman Italic': 'timesi.ttf',
    'Times New Roman Bold': 'timesbd.ttf',
    'Times New Roman Bold Italic': 'timesbi.ttf',
    'Trebuchet MS': 'trebuc.ttf',
    'Trebuchet MS Italic': 'trebucit.ttf',
    'Trebuchet MS Bold': 'trebucbd.ttf',
    'Trebuchet MS Bold Italic': 'trebucbi.ttf',
    'Verdana': 'verdana.ttf',
    'Verdana Italic': 'verdanai.ttf',
    'Verdana Bold': 'verdanab.ttf',
    'Verdana Bold Italic': 'verdanaz.ttf'
}
colors = {
    'black': (0, 0, 0),
    'brown4': (139, 35, 35),
    'red1': (255, 0, 0),
    'orange': (255, 128, 0),
    'yellow1': (255, 255, 0),
    'green': (0, 128, 0),
    'aqua': (0, 255, 255),
    'blue': (0, 0, 255),
    'purple': (128, 0, 128),
    'violet': (238, 130, 238),
    'lightgrey': (211, 211, 211),
    'white': (255, 255, 255)}

def upload_image():
    """The function is responsible for loading the image and adjusting the size of the window to its size."""
    filename = filedialog.askopenfilename()
    uploaded_img = Image.open(filename)
    global background_image, center_text
    # Saves the original image
    background_image = uploaded_img
    center_text = True
    resize_image()
    # Adjusts the size of the window and Canvas to the loaded image
    new_width = round(background_image.width / ratio)
    new_height = round(background_image.height / ratio)
    root.minsize(width=new_width, height=new_height)
    canvas.configure(width=new_width, height=new_height)

def upload_text():
    """The function is responsible for changing the text entered by the user into an image
     and displaying it on the canvas."""
    text = entry_field.get()
    font = ImageFont.truetype(font_file, font_size)

    # Creates a temporary image to calculate text size
    temp_img = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    text_size = temp_img.textbbox((0, 0), text, font)

    # Creates an image of the text based on its actual size
    uploaded_text = Image.new("RGBA", (text_size[2], text_size[3]))
    uploaded_text.putalpha(0)  # Transparent Background
    draw_image = ImageDraw.Draw(uploaded_text)
    draw_image.text((0, 0), text=text, font=font, fill=(r, g, b, alpha))

    # Saves the original image of the text
    global text_image, center_text
    text_image = uploaded_text

    resize_text()

    # Sets the text to the center of the main image
    if center_text:
        x1, y1, x2, y2 = canvas.bbox(text_container)
        text_width = x2 - x1
        text_height = y2 - y1
        half_width = round((canvas.winfo_width()-text_width) / 2)
        half_height = round((canvas.winfo_height()-text_height) / 2)
        canvas.coords(text_container, half_width, half_height)
        center_text = False

def resize_image():
    """Scales the image to the dimensions of the main window."""
    uploaded_image = background_image.copy()
    uploaded_image.thumbnail((canvas.winfo_width(), canvas.winfo_height()), resample=Image.LANCZOS)
    root.p_img = ImageTk.PhotoImage(uploaded_image)
    global ratio
    ratio = background_image.width / root.p_img.width()
    canvas.itemconfig(image_container, image=root.p_img)

def resize_text():
    """Scales the text to fit the size of the scaled image."""
    uploaded_text = text_image.copy()
    new_size = (round(uploaded_text.width / ratio), round(uploaded_text.height / ratio))
    resized_uploaded_text = uploaded_text.resize(new_size)
    root.p_text = ImageTk.PhotoImage(resized_uploaded_text)
    canvas.itemconfig(text_container, image=root.p_text)

def save_image():
    """Combines the original image and original text together and saves it to disk."""
    # Specifies where the text should be.
    if canvas.bbox(text_container) is not None:
        text_x = canvas.bbox(text_container)[0]
        text_y = canvas.bbox(text_container)[1]
    else:
        text_x = 1
        text_y = 1

    image_to_save = background_image.copy()
    image_to_save.paste(text_image, (round(text_x * ratio), round(text_y * ratio)), mask=text_image)
    file_format = background_image.format
    # Checks if the user has uploaded an image before trying to save it.
    if file_format:
        file_format = file_format.lower()
    else:
        messagebox.showerror(title="Empty Image", message="You need to upload an image to save it.")
        return

    filename = filedialog.asksaveasfilename()
    if filename:
        image_to_save.save(filename+'.'+file_format)

def adjust_size(event):
    """Dynamically resizes image and text if the user resizes the main window."""
    if event.widget == root:
        resize_image()
        resize_text()

def button_press(event):
    """Together with the move_text() function, allows to move text with the mouse."""
    global text_position_x, text_position_y
    text_position_x = event.x
    text_position_y = event.y

def move_text(event):
    """Together with the button_press() function, allows to move text with the mouse."""
    if 0 < event.x <= canvas.winfo_width() and 0 < event.y <= canvas.winfo_height():
        global text_position_x, text_position_y
        new_x = event.x - text_position_x
        new_y = event.y - text_position_y
        canvas.move(text_container, new_x, new_y)
        text_position_x = event.x
        text_position_y = event.y

def update_font_type(event):
    """Associated with the tkinter widget OptionMenu. Allows to change the font of the text."""
    global font_file
    bold = bold_var.get()
    italic = italic_var.get()
    if bold == 1 and italic == 1:
        font_file = fonts_files[event + " Bold Italic"]
    elif bold == 1:
        font_file = fonts_files[event + " Bold"]
    elif italic == 1:
        font_file = fonts_files[event + " Italic"]
    else:
        font_file = fonts_files[event]
    upload_text()

def update_font_style():
    """Associated with the tkinter widget Checkbutton. Allows to change the style of the text."""
    font_name = font_var.get()
    update_font_type(font_name)

def update_font_size(event):
    """Associated with the tkinter Scale widget. Allows to change the size of the text."""
    global font_size, center_text
    center_text = False
    font_size = int(event)
    upload_text()

def update_opacity(event):
    """Associated with the tkinter Scale widget. Allows to change the transparency of the text."""
    global alpha, center_text
    center_text = False
    alpha = int(event)
    upload_text()

def update_color(color_name):
    """Associated with color buttons. Allows to change the color of the text."""
    global r, g, b
    r, g, b = colors[color_name]
    upload_text()

def enter_confirm(event):
    """Allows to confirm the entered text with the enter key."""
    upload_text()

root = Tk()
root.title("Adding Watermark to Photos")
root.minsize(width=starting_width, height=starting_height)

frame_main_image = Frame(root)
frame_side_bar = Frame(root)
frame_main_image.pack(fill=BOTH, expand=True, side=LEFT, padx=5, pady=5)
frame_side_bar.pack(fill=BOTH, expand=True, side=LEFT, padx=5, pady=10)

canvas = Canvas(frame_main_image, highlightthickness=0)
image_container = canvas.create_image(0, 0, anchor=NW)
text_container = canvas.create_image(0, 0, anchor=NW)
canvas.pack(side=LEFT, expand=True, fill=BOTH)

# Buttons to load and save the image
frame_buttons = Frame(frame_side_bar)
load_button = Button(frame_buttons, text='Upload File', command=upload_image)
save_button = Button(frame_buttons, text='Save File', command=save_image, width=9)
load_button.pack(side=LEFT, padx=20)
save_button.pack(side=LEFT, padx=20)
frame_buttons.pack(ipady=3)

# Field to enter text
frame_entry = Frame(frame_side_bar)
entry_label = Label(frame_entry, text="Enter Text")
entry_field = Entry(frame_entry)
confirm_btn = Button(frame_entry, text="Confirm", command=upload_text)
entry_label.grid(row=0, column=0)
entry_field.grid(row=0, column=1, padx=10)
confirm_btn.grid(row=0, column=2)
frame_entry.pack(pady=10)

# Options to change the font
frame_font_setup = Frame(frame_side_bar)
font_var = StringVar()
font_var.set(fonts_names[0])
bold_var = IntVar()
italic_var = IntVar()
label_text_font = Label(frame_font_setup, text="Font Style")
font_option_menu = OptionMenu(frame_font_setup, font_var, *fonts_names, command=update_font_type)
font_option_menu.configure(width=16)
bold_button = Checkbutton(frame_font_setup, variable=bold_var, text='Bold', command=update_font_style)
italic_button = Checkbutton(frame_font_setup, variable=italic_var, text='Italic', command=update_font_style)
label_text_font.grid(row=1, column=0, padx=10)
font_option_menu.grid(row=1, column=1, columnspan=2)
bold_button.grid(row=0, column=1)
italic_button.grid(row=0, column=2)
frame_font_setup.pack(ipadx=20)

# Scale to change size of the text
frame_text_size = Frame(frame_side_bar)
txt_size_label = Label(frame_text_size, text='Text Size')
text_size_scale = Scale(frame_text_size, from_=30, to=400, orient=HORIZONTAL, showvalue=False, command=update_font_size)
text_size_scale.set(font_size)
txt_size_label.pack(side=LEFT, padx=5)
text_size_scale.pack(side=LEFT, padx=15)
frame_text_size.pack(pady=10)

# Scale to change the transparency of the text
frame_opacity = Frame(frame_side_bar)
opacity_label = Label(frame_opacity, text='Opacity')
opacity_scale = Scale(frame_opacity, from_=0, to=255, orient=HORIZONTAL, showvalue=False, command=update_opacity)
opacity_scale.set(alpha)
opacity_label.pack(side=LEFT, padx=5)
opacity_scale.pack(side=LEFT, padx=15)
frame_opacity.pack()

# Buttons to change the color of the text
frame_buttons = Frame(frame_side_bar)
for color in colors:
    position = list(colors.keys()).index(color)
    color_button = Button(frame_buttons, bg=color, width=2, height=1, command=lambda c=color: update_color(c))
    if position < len(colors)/2:
        rw = 1
        col = position
    else:
        rw = 2
        col = position - int(len(colors)/2)
    color_button.grid(column=col, row=rw, padx=1, pady=1)
frame_buttons.pack(pady=20)

root.bind('<Configure>', adjust_size)
canvas.bind('<Button-1>', button_press)
canvas.bind('<B1-Motion>', move_text)
root.bind("<Return>", enter_confirm)

root.mainloop()
