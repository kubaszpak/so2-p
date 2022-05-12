import tkinter as tk
from tkinter import ttk
from scrollable_frame import ScrollableFrame
from subscription import Subscription

SUPPORTED_COUNTRIES = {
    "Poland": "pl",
    "United States": "us",
    "Ukraine": "ua",
    "United Kingdom": "gb",
    "Germany": "de",
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

NONE_OPTION = "None"


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('News reader')
        self.geometry('1280x800')
        self.resizable(0, 0)
        self.subscriptions = {}
        self.layout()

    def layout(self):
        frame_left = ScrollableFrame(self)
        frame_left.pack(side="left", expand=True, fill="both")
        self.frame_left = frame_left.scrollable_frame
        self.create_subscriptions_list()

    def create_subscriptions_list(self):
        frame = ScrollableFrame(self, width=200)
        frame.pack(side="right", fill="y")

        button_add = ttk.Button(frame.scrollable_frame,
                                text="+", command=self.add_source_popup, width=20)
        button_add.pack(fill="x", side="top", expand=True, pady=10, padx=10)
        self.frame_right = frame.scrollable_frame

    def change_thread_state(self, label_text, thread_name):
        thread = self.subscriptions[thread_name]
        if thread.is_thread_running():
            print(f"Pausing subscription for: {thread_name}")
            thread.pause()
            label_text.set(thread_name + '\nPaused [|]')
        else:
            print(f"Resuming subscription for: {thread_name}")
            thread.resume()
            label_text.set(thread_name + '\nRunning [>]')

    def add_source(self, name, country_choice, category_choice):
        kwargs = {}
        if country_choice != NONE_OPTION:
            kwargs['country_choice'] = country_choice
        if category_choice != NONE_OPTION:
            kwargs['category_choice'] = category_choice
        new_subscription = Subscription(
            name, self.frame_left, **kwargs)
        print(f"Adding new subscription: {name} with parameters {kwargs}")
        new_subscription.start()
        self.subscriptions[name] = new_subscription

        sep = ttk.Separator(self.frame_right, orient="horizontal")
        sep.pack(fill='x')

        label_text = tk.StringVar()
        label_text.set(name + '\nRunning >>')
        label_new_source = ttk.Label(
            self.frame_right, textvariable=label_text)
        label_new_source.pack()

        button_change_thread_state = ttk.Button(self.frame_right,
                                                text="Pause/Resume!",
                                                command=lambda: self.change_thread_state(label_text, name))
        button_change_thread_state.pack()

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

        country_choice = tk.StringVar(popup, NONE_OPTION)
        ttk.Radiobutton(popup, text="All", variable=country_choice,
                        value=NONE_OPTION).pack(ipady=5)
        for (full_name, short_name) in SUPPORTED_COUNTRIES.items():
            ttk.Radiobutton(popup, text=full_name, variable=country_choice,
                            value=short_name).pack(ipady=5)

        category_choice = tk.StringVar(popup, NONE_OPTION)

        separator = ttk.Separator(popup, orient='horizontal')
        separator.pack(fill='x')

        label_category = ttk.Label(popup, text="Category:")
        label_category.pack()
        ttk.Radiobutton(popup, text="All", variable=category_choice,
                        value=NONE_OPTION).pack(ipady=5)
        for category_name in SUPPORTED_CATEGORIES:
            ttk.Radiobutton(popup, text=category_name, variable=category_choice,
                            value=category_name).pack(ipady=5)

        separator = ttk.Separator(popup, orient='horizontal')
        separator.pack(fill='x')

        def submit_on_click():
            if text_name.get('1.0', 'end') == '\n':
                print("You need to put new subscription name!")
                return
            elif text_name.get('1.0', 'end').strip() in self.subscriptions:
                print("Subscription with this name already exists!")
                return

            self.add_source(
                text_name.get('1.0', 'end').strip(), country_choice=country_choice.get(),
                category_choice=category_choice.get())
            popup.destroy()

        button_add_source = ttk.Button(
            popup, text="Add subscription", command=submit_on_click)
        button_add_source.pack(fill="x", expand=True)

    def on_close(self):
        for (subscription_name, subscription) in app.subscriptions.items():
            print(f"Stopping subscription {subscription_name}")
            subscription.stop()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", lambda: app.on_close())
    app.mainloop()
