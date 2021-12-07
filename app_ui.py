import tkinter as tk

# ---------------------------- CONSTANTS ------------------------------- #
BLUE = "#145da0"
WHITE = "#fff"
BLACK = "#000"
FONT_NAME = "Courier"


class AppUI(tk.Tk):
    def __init__(self, open_func, watermark_func, remove_func):
        super().__init__()
        self.title("aWatermark")
        self.config(padx=50, pady=50, bg=WHITE)

        self.lbl_title = tk.Label(text="aWatermark\nCreator", fg=BLUE, font=(FONT_NAME, 45), bg=WHITE)
        self.lbl_title.grid(column=0, columnspan=3, row=0)

        self.lbl_explanation_text = tk.Label(text="Write a watermark text, if none provided "
                                                  "it will open a file dialog\n"
                                                  "to open an image file as watermark",
                                             fg=BLACK, font=(FONT_NAME, 8), bg=WHITE)
        self.lbl_explanation_text.grid(column=0, row=1, columnspan=3, pady=20)

        self.lbl_watermark_text = tk.Label(text="Watermark text: ",
                                           fg=BLACK, font=(FONT_NAME, 8), bg=WHITE)
        self.lbl_watermark_text.grid(column=0, row=2)

        self.ent_watermark_text = tk.Entry(fg=BLACK, bg=WHITE, width=40)
        self.ent_watermark_text.grid(column=1, columnspan=2, row=2)

        self.list = tk.Listbox(self, selectmode="extended", width=80, setgrid=True)
        self.list.grid(column=0, columnspan=3, row=3, pady=20)

        self.btn_open = tk.Button(text="1. Open files", highlightthickness=0, command=open_func)
        self.btn_open.grid(column=0, row=4)

        self.btn_apply = tk.Button(text="2. Apply watermark", highlightthickness=0, command=watermark_func)
        self.btn_apply.grid(column=1, row=4)

        self.btn_remove = tk.Button(text="Clear list", highlightthickness=0, command=remove_func)
        self.btn_remove.grid(column=2, row=4)

        self.files = []

