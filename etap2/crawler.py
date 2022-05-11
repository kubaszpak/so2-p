import tkinter as tk
from tkinter import ttk
from scrollable_frame import ScrollableFrame
from subscription import Subscription

SUPPORTED_COUNTRIES = {
    "Poland": "pl",
    "United States": "us",
    "Ukraine": "ua",
    "United Kingdom": "gb",
    "Germany": "gr",
    "France": "fr"
}

SUPPORTED_CATEGORIES = [
    "entertainment",
    "business",
    "general",
    "health",
    "science",
    "sports",
    "technology"
]


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('News reader')
        self.geometry('1280x800')
        self.resizable(0, 0)
        self.subscriptions = []
        self.layout()

    def layout(self):
        frame_left = tk.Frame(self)
        frame_left.pack(side="left", expand=True, fill="both")
        self.frame_left = frame_left
        self.create_subscriptions_list()

    def create_subscriptions_list(self):
        frame = ScrollableFrame(self, width=200)
        frame.pack(side="right", fill="y")

        button_add = ttk.Button(frame.scrollable_frame,
                                text="+", command=self.add_source_popup, width=20)
        button_add.pack(fill="x", side="top", expand=True, pady=10, padx=10)
        self.frame_right = frame.scrollable_frame

    def add_source(self, name, country_choice, category_choice):
        sep = ttk.Separator(self.frame_right, orient="horizontal")
        sep.pack(fill='x')
        label_new_source = ttk.Label(
            self.frame_right, text=name)
        label_new_source.pack()

        self.subscriptions.append(Subscription(name, country_choice, category_choice))


    def add_source_popup(self):
        popup = tk.Toplevel(self)
        popup.geometry('1280x800')
        popup.resizable(0, 0)
        label_name = ttk.Label(popup, text="Name:")
        label_name.pack()
        text_name = tk.Text(popup, height=1, width=15)
        text_name.pack()

        label_country = ttk.Label(popup, text="Country:")
        label_country.pack()

        country_choice = tk.StringVar(popup, "-1")

        country_options = {}

        for i, country in enumerate(SUPPORTED_COUNTRIES.keys()):
            country_options[country] = str(i)

        for (text, value) in country_options.items():
            ttk.Radiobutton(popup, text=text, variable=country_choice,
                            value=value).pack(ipady=5)

        category_choice = tk.StringVar(popup, "-1")

        category_options = {}

        for i, category in enumerate(SUPPORTED_CATEGORIES):
            category_options[category] = str(i)

        separator = ttk.Separator(popup, orient='horizontal')
        separator.pack(fill='x')

        label_category = ttk.Label(popup, text="Category:")
        label_category.pack()

        for (text, value) in category_options.items():
            ttk.Radiobutton(popup, text=text, variable=category_choice,
                            value=value).pack(ipady=5)

        separator = ttk.Separator(popup, orient='horizontal')
        separator.pack(fill='x')

        def submit_on_click():
            if text_name.get('1.0', 'end') == '\n':
                print("You need to put new subscription name!")
                return
            self.add_source(
                text_name.get('1.0', 'end'), country_choice.get(), category_choice.get())
            popup.destroy()

        button_add_source = ttk.Button(
            popup, text="Add subscription", command=submit_on_click)
        button_add_source.pack(fill="x", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
