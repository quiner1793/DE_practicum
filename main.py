import tkinter as tk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib

DEFAULT_X_ZERO = 1
LEFT_LIMIT_X_ZERO = -100
RIGHT_LIMIT_X_ZERO = 100
DEFAULT_Y_ZERO = 1
LEFT_LIMIT_Y_ZERO = -100
RIGHT_LIMIT_Y_ZERO = 100
DEFAULT_X_LIMIT = 7
RIGHT_LIMIT_X_LIMIT = 100
DEFAULT_N = 10
LEFT_LIMIT_N = 1
RIGHT_LIMIT_N = 1000


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Page 1")
        label.pack(side="top", fill="both", expand=True)

        self.fig = plt.figure(1)

        canvas = FigureCanvasTkAgg(self.fig, master=self)  # Matplotlib graphing canvas
        plot_widget = canvas.get_tk_widget()

        plot_widget.pack(side=RIGHT)  # Add the plot to the tkinter widget

        left_frame = Frame(self)
        left_frame.pack(side=LEFT, fill=Y, expand=False)

        self.original_graph_flag = tk.BooleanVar()
        self.original_graph_flag.set(True)
        tk.Checkbutton(left_frame,
                       text="Original graph",
                       variable=self.original_graph_flag,
                       onvalue=True,
                       offvalue=False).pack(expand=False)

        self.runge_kutta_graph_flag = tk.BooleanVar()
        tk.Checkbutton(left_frame,
                       text="Runge-Kutta method",
                       variable=self.runge_kutta_graph_flag,
                       onvalue=True,
                       offvalue=False).pack(expand=False)

        self.euler_graph_flag = tk.BooleanVar()
        tk.Checkbutton(left_frame,
                       text="Euler method",
                       variable=self.euler_graph_flag,
                       onvalue=True,
                       offvalue=False).pack(expand=False)

        self.improved_euler_graph_flag = tk.BooleanVar()
        tk.Checkbutton(left_frame,
                       text="Improved Euler method",
                       variable=self.improved_euler_graph_flag,
                       onvalue=True,
                       offvalue=False).pack(expand=False)

        x0_frame = Frame(left_frame)
        x0_frame.pack()
        Label(x0_frame, width=3, text="x0=").pack(side="left")
        self.x_zero_entry_box = Entry(x0_frame, width=5)
        self.x_zero_entry_box.pack(side="left")

        y0_frame = Frame(left_frame)
        y0_frame.pack()
        Label(y0_frame, width=3, text="y0=").pack(side="left")
        self.y_zero_entry_box = Entry(y0_frame, width=5)
        self.y_zero_entry_box.pack(side="left")

        x_limit_frame = Frame(left_frame)
        x_limit_frame.pack()
        Label(x_limit_frame, width=3, text="X=").pack(side="left")
        self.x_limit_entry_box = Entry(x_limit_frame, width=5)
        self.x_limit_entry_box.pack(side="left")

        n_frame = Frame(left_frame)
        n_frame.pack()
        Label(n_frame, width=3, text="N=").pack(side="left")
        self.N_entry_box = Entry(n_frame, width=5)
        self.N_entry_box.pack(side="left")

        tk.Button(left_frame, text="Plot", command=self.update_graph_first_page).pack(expand=False)
        self.update_graph_first_page()

    def get_x_zero_input(self):
        str_value = self.x_zero_entry_box.get()
        if str_value == "":
            return DEFAULT_X_ZERO
        try:
            int_value = int(str_value)
            if not (LEFT_LIMIT_X_ZERO < int_value < RIGHT_LIMIT_X_ZERO):
                return DEFAULT_X_ZERO
            return int_value
        except ValueError:
            print("x0 should be an integer value")
            return DEFAULT_X_ZERO

    def get_y_zero_input(self):
        str_value = self.y_zero_entry_box.get()
        if str_value == "":
            return DEFAULT_Y_ZERO
        try:
            int_value = int(str_value)
            if not (LEFT_LIMIT_Y_ZERO < int_value < RIGHT_LIMIT_Y_ZERO):
                return DEFAULT_Y_ZERO
            return int_value
        except ValueError:
            print("y0 should be an integer value")
            return DEFAULT_Y_ZERO

    def get_x_limit_input(self):
        str_value = self.x_limit_entry_box.get()
        if str_value == "":
            return DEFAULT_X_LIMIT
        try:
            int_value = int(str_value)
            if not (self.get_x_zero_input() < int_value < RIGHT_LIMIT_X_LIMIT):
                return DEFAULT_X_LIMIT
            return int_value
        except ValueError:
            print("X should be an integer value")
            return DEFAULT_X_LIMIT

    def get_n_input(self):
        str_value = self.N_entry_box.get()
        if str_value == "":
            return DEFAULT_N
        try:
            int_value = int(str_value)
            if not (LEFT_LIMIT_N < int_value < RIGHT_LIMIT_N):
                return DEFAULT_N
            return int_value
        except ValueError:
            print("N should be an integer value")
            return DEFAULT_N

    def update_graph_first_page(self):
        plt.clf()  # Clear all graphs drawn in figure
        plt.plot()  # Draw empty graph

        x_zero = self.get_x_zero_input()
        y_zero = self.get_y_zero_input()
        x_limit = self.get_x_limit_input()
        n_steps = self.get_n_input()

        print(x_zero)

        if self.original_graph_flag.get():
            x = [i for i in range(-2, 4)]
            y = [i ** 2 for i in x]
            plt.plot(x, y)

        self.fig.canvas.draw()


class MainView(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        page1 = Page1(self)
        page2 = Page(self)  # TODO replace
        page3 = Page(self)

        button_frame = tk.Frame(self)
        container = tk.Frame(self)
        button_frame.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        page1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        page2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        page3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        page1_button = tk.Button(button_frame, text="Page 1", command=page1.show)
        page2_button = tk.Button(button_frame, text="Page 2", command=page2.show)
        page3_button = tk.Button(button_frame, text="Page 3", command=page3.show)

        page1_button.pack(side="left")
        page2_button.pack(side="left")
        page3_button.pack(side="left")

        page1.show()


if __name__ == '__main__':
    matplotlib.use('TkAgg')  # Redefine Python GUI backend to use matplotlib

    root = tk.Tk()  # Initialize an instance of tkinter
    root.title("GUI for computational practicum")

    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x600")

    root.mainloop()
