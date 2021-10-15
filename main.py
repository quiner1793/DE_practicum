import tkinter as tk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

DEFAULT_X_ZERO = 1
LEFT_LIMIT_X_ZERO = 0
RIGHT_LIMIT_X_ZERO = 100
DEFAULT_Y_ZERO = 1
LEFT_LIMIT_Y_ZERO = -100
RIGHT_LIMIT_Y_ZERO = 100
DEFAULT_X_LIMIT = 7
RIGHT_LIMIT_X_LIMIT = 100
DEFAULT_N = 10
LEFT_LIMIT_N = 0
RIGHT_LIMIT_N = 1000
ORIGINAL_FUNCTION_STEP = 0.1


def get_range(start, stop, step):
    x = []
    temp = start
    while temp + step < stop:
        x.append(temp)
        temp += step

    if temp <= stop:
        x.append(stop)
    return x


def get_original_function_constant(x0, y0):
    return np.log(y0 + 2 * x0 - 1) - x0


def get_original_function_output(x, const):
    return np.exp(x + const) - 2 * x + 1


def get_original_function_slope(x, y):
    return 2 * x + y - 3


def get_euler_method_output(x, y, h_step):
    return y + h_step * get_original_function_slope(x, y)


def get_improved_euler_method_output(x, y, h_step):
    k1 = h_step * get_original_function_slope(x, y)
    k2 = h_step * get_original_function_slope(x + h_step, y + k1)
    return y + (k1 + k2) / 2


def get_runge_kutta_method_output(x, y, h_step):
    k1 = h_step * get_original_function_slope(x, y)
    k2 = h_step * get_original_function_slope(x + h_step / 2, y + k1 / 2)
    k3 = h_step * get_original_function_slope(x + h_step / 2, y + k2 / 2)
    k4 = h_step * get_original_function_slope(x + h_step, y + k3)

    return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()
        self.update_graph()

    def update_graph(self):
        raise NotImplementedError()


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
                       offvalue=False,
                       fg="blue").pack(expand=False)

        self.euler_graph_flag = tk.BooleanVar()
        tk.Checkbutton(left_frame,
                       text="Euler method",
                       variable=self.euler_graph_flag,
                       onvalue=True,
                       offvalue=False,
                       fg="green").pack(expand=False)

        self.improved_euler_graph_flag = tk.BooleanVar()
        tk.Checkbutton(left_frame,
                       text="Improved Euler method",
                       variable=self.improved_euler_graph_flag,
                       onvalue=True,
                       offvalue=False,
                       fg="red").pack(expand=False)

        self.runge_kutta_graph_flag = tk.BooleanVar()
        tk.Checkbutton(left_frame,
                       text="Runge-Kutta method",
                       variable=self.runge_kutta_graph_flag,
                       onvalue=True,
                       offvalue=False,
                       fg="magenta2").pack(expand=False)

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

        tk.Button(left_frame, text="Plot", command=self.update_graph).pack(expand=False)

    def get_x_zero_input(self):
        str_value = self.x_zero_entry_box.get()
        value_to_return = DEFAULT_X_ZERO

        if str_value != "":
            try:
                int_value = int(str_value)
                if LEFT_LIMIT_X_ZERO < int_value < RIGHT_LIMIT_X_ZERO:
                    value_to_return = int_value
            except ValueError:
                print("x0 should be an integer value")

        self.x_zero_entry_box.delete(0, END)
        self.x_zero_entry_box.insert(0, value_to_return)
        return value_to_return

    def get_y_zero_input(self):
        str_value = self.y_zero_entry_box.get()
        value_to_return = DEFAULT_Y_ZERO

        if str_value != "":
            try:
                int_value = int(str_value)
                if LEFT_LIMIT_Y_ZERO < int_value < RIGHT_LIMIT_Y_ZERO:
                    value_to_return = int_value
            except ValueError:
                print("y0 should be an integer value")

        self.y_zero_entry_box.delete(0, END)
        self.y_zero_entry_box.insert(0, value_to_return)
        return value_to_return

    def get_x_limit_input(self):
        str_value = self.x_limit_entry_box.get()
        value_to_return = DEFAULT_X_LIMIT

        if str_value != "":
            try:
                int_value = int(str_value)
                if self.get_x_zero_input() < int_value < RIGHT_LIMIT_X_LIMIT:
                    value_to_return = int_value
            except ValueError:
                print("X should be an integer value")

        self.x_limit_entry_box.delete(0, END)
        self.x_limit_entry_box.insert(0, value_to_return)
        return value_to_return

    def get_n_input(self):
        str_value = self.N_entry_box.get()
        value_to_return = DEFAULT_N

        if str_value != "":
            try:
                int_value = int(str_value)
                if LEFT_LIMIT_N < int_value < RIGHT_LIMIT_N:
                    value_to_return = int_value
            except ValueError:
                print("N should be an integer value")

        self.N_entry_box.delete(0, END)
        self.N_entry_box.insert(0, value_to_return)
        return value_to_return

    def update_graph(self):
        plt.figure(1)  # Activate figure 1
        plt.clf()  # Clear all graphs drawn in figure
        plt.plot()  # Draw empty graph

        x_zero = self.get_x_zero_input()
        y_zero = self.get_y_zero_input()
        x_limit = self.get_x_limit_input()
        n_steps = self.get_n_input()
        h_step = (x_limit - x_zero) / n_steps

        const = get_original_function_constant(x_zero, y_zero)

        x1 = get_range(x_zero, x_limit, h_step)

        if self.original_graph_flag.get():
            x2 = get_range(x_zero, x_limit, ORIGINAL_FUNCTION_STEP)
            y1 = [get_original_function_output(i, const) for i in x2]
            plt.plot(x2, y1, 'b')

        if self.euler_graph_flag.get():
            y2 = []

            if len(x1) > 0:
                y2.append(y_zero)  # y(x0) = y0

            for i in range(1, len(x1)):
                y2.append(get_euler_method_output(x1[i-1], y2[i-1], h_step))

            plt.plot(x1, y2, 'g')

        if self.improved_euler_graph_flag.get():
            y3 = []

            if len(x1) > 0:
                y3.append(y_zero)  # y(x0) = y0

            for i in range(1, len(x1)):
                y3.append(get_improved_euler_method_output(x1[i-1], y3[i-1], h_step))

            plt.plot(x1, y3, 'r')

        if self.runge_kutta_graph_flag.get():
            y4 = []

            if len(x1) > 0:
                y4.append(y_zero)

            for i in range(1, len(x1)):
                y4.append(get_runge_kutta_method_output(x1[i-1], y4[i-1], h_step))

            plt.plot(x1, y4, 'm')

        self.fig.canvas.draw()


class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Page 2")
        label.pack(side="top", fill="both", expand=True)

        self.fig = plt.figure(2)

        canvas = FigureCanvasTkAgg(self.fig, master=self)  # Matplotlib graphing canvas
        plot_widget = canvas.get_tk_widget()

        plot_widget.pack(side=RIGHT)  # Add the plot to the tkinter widget

        left_frame = Frame(self)
        left_frame.pack(side=LEFT, fill=Y, expand=False)

        self.euler_error_flag = tk.BooleanVar()
        tk.Checkbutton(left_frame,
                       text="Euler error",
                       variable=self.euler_error_flag,
                       onvalue=True,
                       offvalue=False,
                       fg="green").pack(expand=False)

        self.improved_euler_error_flag = tk.BooleanVar()
        tk.Checkbutton(left_frame,
                       text="Improved Euler error",
                       variable=self.improved_euler_error_flag,
                       onvalue=True,
                       offvalue=False,
                       fg="red").pack(expand=False)

        self.runge_kutta_error_flag = tk.BooleanVar()
        tk.Checkbutton(left_frame,
                       text="Runge-Kutta error",
                       variable=self.runge_kutta_error_flag,
                       onvalue=True,
                       offvalue=False,
                       fg="magenta2").pack(expand=False)

        tk.Button(left_frame, text="Plot", command=self.update_graph).pack(expand=False)

    def update_graph(self):
        plt.figure(2)
        plt.clf()  # Clear all graphs drawn in figure
        plt.plot()  # Draw empty graph

        x_zero = DEFAULT_X_ZERO
        y_zero = DEFAULT_Y_ZERO
        x_limit = DEFAULT_X_LIMIT
        n_steps = DEFAULT_N
        h_step = (x_limit - x_zero) / n_steps

        const = get_original_function_constant(x_zero, y_zero)

        x = get_range(x_zero, x_limit, h_step)
        original_func = [get_original_function_output(i, const) for i in x]

        if self.euler_error_flag.get():
            y1 = []
            e1 = []  # error values

            if len(x) > 0:
                y1.append(y_zero)  # y(x0) = y0

            for i in range(1, len(x)):
                y1.append(get_euler_method_output(x[i-1], y1[i-1], h_step))

            for i in range(0, len(x)):
                e1.append(abs(y1[i] - original_func[i]))

            plt.plot(x, e1, 'g')

        if self.improved_euler_error_flag.get():
            y2 = []
            e2 = []

            if len(x) > 0:
                y2.append(y_zero)  # y(x0) = y0

            for i in range(1, len(x)):
                y2.append(get_improved_euler_method_output(x[i-1], y2[i-1], h_step))

            for i in range(0, len(x)):
                e2.append(abs(y2[i] - original_func[i]))

            plt.plot(x, e2, 'r')

        if self.runge_kutta_error_flag.get():
            y3 = []
            e3 = []

            if len(x) > 0:
                y3.append(y_zero)

            for i in range(1, len(x)):
                y3.append(get_runge_kutta_method_output(x[i-1], y3[i-1], h_step))

            for i in range(0, len(x)):
                e3.append(abs(y3[i] - original_func[i]))

            plt.plot(x, e3, 'm')

        self.fig.canvas.draw()


class MainView(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        page1 = Page1(self)
        page2 = Page2(self)
        page3 = Page(self)  # TODO replace

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
    root.wm_geometry("800x500")

    root.mainloop()
