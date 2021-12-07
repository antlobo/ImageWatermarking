# Standard library imports
import pathlib
from tkinter import END
from tkinter import filedialog as fd
from tkinter import messagebox as mb

# Third party imports
import PIL
from PIL import Image, ImageDraw, ImageFont

# Local specific imports
from app_ui import AppUI

FONT = 'arial.ttf'


def open_file() -> None:
    """
    Opens a file dialog to select the images to add the watermark
    :return: it doesn't return a value
    """
    filetypes = (
        ('Image files', '*.jpg *.jpeg *.png *.bmp'),
    )

    filenames = fd.askopenfilenames(
        title='Open images file(s)',
        initialdir='/',
        filetypes=filetypes)

    for filename in filenames:
        try:
            file = pathlib.Path(filename)
        except FileNotFoundError:
            mb.showerror("Error", f"The file {filename} wasn't found")
        else:
            if file not in screen.files:
                screen.list.insert(END, file.name)
                screen.files.append(file)

    screen.list.selection_set(0, END)


def text_watermark(photo: Image, watermark_text: str, file_path: str, new_file_name: str) -> bool:
    """
    Given an image and a watermark text, creates a new image with the text watermarked
    :param photo: image to be watermarked. It receives an PIL.Image object
    :param watermark_text: a string with the value to be watermarked inside the image
    :param file_path: a string with the original image's file path
    :param new_file_name: a string with the new name of the image
    :return: 'True' if the watermark process completed, otherwise returns 'False' and a message
    """
    width, height = photo.size

    # makes a blank image for the text, initialized to transparent color
    txt = Image.new('RGBA', photo.size, (255, 255, 255, 0))

    try:
        # get a font
        fnt = ImageFont.truetype(FONT, width // (len(watermark_text)) // 2)
    except OSError:
        mb.showerror("Error acquiring font", f"Couldn't acquire default font: {FONT}")
        return False
    else:
        # get a drawing context
        d = ImageDraw.Draw(txt)

        x = (width // len(watermark_text)) * 1.8
        y = height // 3

        # draw text
        d.text((x, y),
               watermark_text,
               font=fnt,
               fill=(255, 255, 255, 56),
               stroke_width=1, stroke_fill=(255, 255, 255, 128))

        out = Image.alpha_composite(photo, txt)
        try:
            out.save(pathlib.Path(file_path).joinpath(new_file_name).absolute())
        except ValueError and OSError:
            return False
        return True


def image_watermark(photo: Image, watermark: Image, file_path: str, new_file_name: str) -> bool:
    """
    Given an image and a watermark image, creates a new image with the image watermarked
    :param photo: image to be watermarked. It receives an PIL.Image object
    :param watermark: watermark image. It receives an PIL.Image object
    :param file_path: a string with the original image's file path
    :param new_file_name: a string with the new name of the image
    :return: 'True' if the watermark process completed, otherwise returns 'False' and a message
    """
    width, height = photo.size

    # Resizes the watermark image if it's bigger than the original image
    if watermark.size > photo.size:
        watermark.thumbnail(photo.size, Image.ANTIALIAS)

    w_width, w_height = watermark.size

    # put the watermark in the middle of the image
    photo.paste(watermark, ((width//2)-(w_width//2), (height//2)-(w_height//2)), watermark)

    try:
        photo.save(pathlib.Path(file_path).joinpath(new_file_name).absolute())
    except ValueError and OSError:
        return False
    return True


def select_image_watermark() -> Image:
    """
    Selects the watermark image
    :return: an PIL.Image object or None if a file wasn't selected
    """
    filetypes = (
        ('Image files', '*.jpg *.jpeg *.png *.bmp'),
    )

    filename = fd.askopenfilename(
        title='Open an image file',
        initialdir='/',
        filetypes=filetypes)

    if filename:
        try:
            file = pathlib.Path(filename)
            watermark = Image.open(file.absolute())
        except FileNotFoundError:
            mb.showerror("Error", f"The watermark file wasn't found")
        except PIL.UnidentifiedImageError:
            mb.showerror("Image format error", f"The file chosen doesn't correspond to a valid image")
        else:
            # convert the image to RGBA and add alpha channel
            watermark = watermark.convert("RGBA")
            watermark.putalpha(56)
            return watermark
    return None


def apply_watermark() -> None:
    """
    Makes the validation of the files selected, opens the original image and calls the function to apply the watermark
    :return: it doesn't return a value
    """
    if screen.list.curselection():
        watermark_text = screen.ent_watermark_text.get()
        watermark = None
        watermarked_files = []
        not_watermarked_files = []

        if not watermark_text:
            watermark = select_image_watermark()

        if watermark_text or watermark:
            for file_pos in screen.list.curselection():
                file = screen.files[file_pos]
                file_path = str(file.absolute()).replace(file.name, "")

                # create the new file name like: name + _watermarked + png
                file_name = file.name[::-1].split(".", 1)
                file_name[0] = "gnp"
                file_name[1] = str("_watermarked"[::-1]) + file_name[1]
                new_file_name = str(".".join(file_name)[::-1])

                try:
                    # open file and convert it to 'RGBA' to add alpha channel
                    photo = Image.open(file.absolute())
                    photo = photo.convert("RGBA")
                except FileNotFoundError:
                    mb.showerror("Error", f"The file {file.name} wasn't found")
                except PIL.UnidentifiedImageError:
                    mb.showerror("Image format error", f"The file {file.name} doesn't correspond to a valid image")
                else:
                    if watermark_text:
                        result = text_watermark(photo, watermark_text, file_path, new_file_name)
                    else:
                        result = image_watermark(photo, watermark, file_path, new_file_name)

                    if result:
                        watermarked_files.append(new_file_name)
                    else:
                        not_watermarked_files.append(file.name)

            if watermarked_files:
                mb.showinfo("Success",
                            f"It was created the file {', '.join(watermarked_files)} "
                            f"inside the folder of the original file")

            if not_watermarked_files:
                mb.showerror("Error",
                             f"Couldn't create the file {', '.join(not_watermarked_files)}")
        else:
            mb.showerror("Error", f"Write a watermark text or provide a watermark image")


def remove_list() -> None:
    """
    Clears ListBox
    :return: it doesn't return a value
    """
    screen.list.delete(0, END)
    screen.files = []


screen = AppUI(open_file, apply_watermark, remove_list)
screen.mainloop()
