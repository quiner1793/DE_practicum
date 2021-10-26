import math
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
RIGHT_LIMIT_N = 1000
ORIGINAL_FUNCTION_STEP = 0.1


def get_range(start, stop, step):
    x = []
    temp = start
    while temp + step <= stop:
        x.append(temp)
        temp += step

    if temp <= stop:
        x.append(stop)
    return x


def get_original_function_constant(x0, y0):
    if 2*x0 + y0 - 1 == 0:
        return 0
    return (2*x0 + y0 - 1) / math.exp(x0)


def get_original_function_output(x, const):
    output = const * math.exp(x) - 2*x + 1
    return output


def get_original_function_slope(x, y):
    slope = 2 * x + y - 3
    return slope


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

        self.x_zero_entry_box = None
        self.y_zero_entry_box = None
        self.x_limit_entry_box = None
        self.N_entry_box = None
        self.n_zero_entry_box = None
        self.n_limit_entry_box = None

    def show(self):
        self.lift()
        self.update_graph()

    def update_graph(self):
        raise NotImplementedError()

    def get_x_zero_input(self):
        str_value = self.x_zero_entry_box.get()
        value_to_return = DEFAULT_X_ZERO

        if str_value != "":
            try:
                float_value = float(str_value)
                if LEFT_LIMIT_X_ZERO < float_value < RIGHT_LIMIT_X_ZERO:
                    value_to_return = float_value
            except ValueError:
                print("x0 should be an float value")

        self.x_zero_entry_box.delete(0, END)
        self.x_zero_entry_box.insert(0, value_to_return)
        return value_to_return

    def get_y_zero_input(self):
        str_value = self.y_zero_entry_box.get()
        value_to_return = DEFAULT_Y_ZERO

        if str_value != "":
            try:
                float_value = float(str_value)
                if LEFT_LIMIT_Y_ZERO < float_value < RIGHT_LIMIT_Y_ZERO:
                    value_to_return = float_value
            except ValueError:
                print("y0 should be an float value")

        self.y_zero_entry_box.delete(0, END)
        self.y_zero_entry_box.insert(0, value_to_return)
        return value_to_return

    def get_x_limit_input(self):
        str_value = self.x_limit_entry_box.get()
        value_to_return = DEFAULT_X_LIMIT

        if str_value != "":
            try:
                float_value = float(str_value)
                if self.get_x_zero_input() < float_value < RIGHT_LIMIT_X_LIMIT:
                    value_to_return = float_value
            except ValueError:
                print("X should be an float value")

        self.x_limit_entry_box.delete(0, END)
        self.x_limit_entry_box.insert(0, value_to_return)
        return value_to_return

    def get_n_input(self):
        str_value = self.N_entry_box.get()

        x_zero = self.get_x_zero_input()
        x_limit = self.get_x_limit_input()
        left_limit = x_limit - x_zero

        value_to_return = int(left_limit)

        if str_value != "":
            try:
                int_value = int(str_value)

                if left_limit < int_value < RIGHT_LIMIT_N:
                    value_to_return = int_value
            except ValueError:
                print("N should be an integer value")

        self.N_entry_box.delete(0, END)
        self.N_entry_box.insert(0, value_to_return)
        return value_to_return

    def get_n_zero_input(self):
        str_value = self.n_zero_entry_box.get()

        x_zero = self.get_x_zero_input()
        x_limit = self.get_x_limit_input()
        left_limit = x_limit - x_zero

        value_to_return = int(left_limit)

        if str_value != "":
            try:
                int_value = int(str_value)
                if left_limit < int_value < RIGHT_LIMIT_N:
                    value_to_return = int_value
            except ValueError:
                print("n0 should be an integer value")

        self.n_zero_entry_box.delete(0, END)
        self.n_zero_entry_box.insert(0, value_to_return)
        return value_to_return

    def get_n_limit_input(self):
        str_value = self.n_limit_entry_box.get()

        value_to_return = self.get_n_zero_input() + 5

        if str_value != "":
            try:
                int_value = int(str_value)
                if value_to_return < int_value < RIGHT_LIMIT_N:
                    value_to_return = int_value
            except ValueError:
                print("N should be an integer value")

        self.n_limit_entry_box.delete(0, END)
        self.n_limit_entry_box.insert(0, value_to_return)
        return value_to_return


def get_approximation_function_graph(func, x_range, y_zero):
    y = []

    if len(x_range) > 0:
        y.append(y_zero)  # y(x0) = y0

    for i in range(1, len(x_range)):
        y.append(func(x_range[i - 1], y[i - 1], x_range[i] - x_range[i - 1]))

    return y


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Numerical methods")
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

    def update_graph(self):
        plt.figure(1)  # Activate figure 1
        plt.clf()  # Clear all graphs drawn in figure
        plt.plot()  # Draw empty graph
        plt.grid()  # Grid for plot

        x_zero = self.get_x_zero_input()
        y_zero = self.get_y_zero_input()
        x_limit = self.get_x_limit_input()
        n_steps = self.get_n_input()
        h_step = (x_limit - x_zero) / n_steps

        const = get_original_function_constant(x_zero, y_zero)

        x_range = get_range(x_zero, x_limit, h_step)

        if self.original_graph_flag.get():
            x2 = get_range(x_zero, x_limit, ORIGINAL_FUNCTION_STEP)
            y1 = [get_original_function_output(i, const) for i in x2]
            plt.plot(x2, y1, 'b')

        if self.euler_graph_flag.get():
            euler_graph = get_approximation_function_graph(get_euler_method_output, x_range, y_zero)

            plt.plot(x_range, euler_graph, '-go')

        if self.improved_euler_graph_flag.get():
            improved_euler_graph = get_approximation_function_graph(get_improved_euler_method_output, x_range, y_zero)

            plt.plot(x_range, improved_euler_graph, '-ro')

        if self.runge_kutta_graph_flag.get():
            runge_kutta_graph = get_approximation_function_graph(get_runge_kutta_method_output, x_range, y_zero)

            plt.plot(x_range, runge_kutta_graph, '-mo')

        self.fig.canvas.draw()


def get_error_graph(func, x_range, y_zero,  const):
    y = []
    error = []  # error values

    if len(x_range) > 0:
        y.append(y_zero)  # y(x0) = y0

    for i in range(1, len(x_range)):
        y.append(func(x_range[i - 1], y[i - 1], x_range[i] - x_range[i - 1]))

    for i in range(0, len(x_range)):
        error.append(abs(y[i] - get_original_function_output(x_range[i], const)))

    return error


class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="LTE")
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

    def update_graph(self):
        plt.figure(2)  # Activate figure 2
        plt.clf()  # Clear all graphs drawn in figure
        plt.plot()  # Draw empty graph
        plt.grid()  # Grid for plot

        x_zero = self.get_x_zero_input()
        y_zero = self.get_y_zero_input()
        x_limit = self.get_x_limit_input()
        n_steps = self.get_n_input()
        h_step = (x_limit - x_zero) / n_steps

        const = get_original_function_constant(x_zero, y_zero)

        x_range = get_range(x_zero, x_limit, h_step)

        if self.euler_error_flag.get():
            euler_error = get_error_graph(get_euler_method_output, x_range, y_zero, const)

            plt.plot(x_range, euler_error, '-go')

        if self.improved_euler_error_flag.get():
            improved_euler_error = get_error_graph(get_improved_euler_method_output, x_range, y_zero, const)

            plt.plot(x_range, improved_euler_error, '-ro')

        if self.runge_kutta_error_flag.get():
            runge_kutta_error = get_error_graph(get_runge_kutta_method_output, x_range, y_zero, const)

            plt.plot(x_range, runge_kutta_error, '-mo')

        self.fig.canvas.draw()


def get_max_errors_graph(func, x_zero, x_limit, y_zero, n_range, const):
    max_errors = [0 for _ in n_range]

    for n in n_range:
        h_step = (x_limit - x_zero) / n
        j = n - n_range[0]

        x1 = get_range(x_zero, x_limit, h_step)
        y1 = []

        if len(x1) > 0:
            y1.append(y_zero)  # y(x0) = y0

        for i in range(1, len(x1)):
            y1.append(func(x1[i - 1], y1[i - 1], x1[i] - x1[i - 1]))

        for i in range(0, len(x1)):
            if (abs(y1[i] - get_original_function_output(x1[i], const))) > max_errors[j]:
                max_errors[j] = abs(y1[i] - get_original_function_output(x1[i], const))

    return max_errors


class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="GTE")
        label.pack(side="top", fill="both", expand=True)

        self.fig = plt.figure(3)

        canvas = FigureCanvasTkAgg(self.fig, master=self)  # Matplotlib graphing canvas
        plot_widget = canvas.get_tk_widget()

        plot_widget.pack(side=RIGHT)  # Add the plot to the tkinter widget

        left_frame = Frame(self)
        left_frame.pack(side=LEFT, fill=Y, expand=False)

        self.euler_errors_flag = tk.BooleanVar()
        tk.Checkbutton(left_frame,
                       text="Euler error",
                       variable=self.euler_errors_flag,
                       onvalue=True,
                       offvalue=False,
                       fg="green").pack(expand=False)

        self.improved_euler_errors_flag = tk.BooleanVar()
        tk.Checkbutton(left_frame,
                       text="Improved Euler error",
                       variable=self.improved_euler_errors_flag,
                       onvalue=True,
                       offvalue=False,
                       fg="red").pack(expand=False)

        self.runge_kutta_errors_flag = tk.BooleanVar()
        tk.Checkbutton(left_frame,
                       text="Runge-Kutta error",
                       variable=self.runge_kutta_errors_flag,
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

        n_zero_frame = Frame(left_frame)
        n_zero_frame.pack()
        Label(n_zero_frame, width=3, text="n0=").pack(side="left")
        self.n_zero_entry_box = Entry(n_zero_frame, width=5)
        self.n_zero_entry_box.pack(side="left")

        n_limit_frame = Frame(left_frame)
        n_limit_frame.pack()
        Label(n_limit_frame, width=3, text="N=").pack(side="left")
        self.n_limit_entry_box = Entry(n_limit_frame, width=5)
        self.n_limit_entry_box.pack(side="left")

        tk.Button(left_frame, text="Plot", command=self.update_graph).pack(expand=False)

    def update_graph(self):
        plt.figure(3)  # Activate figure 2
        plt.clf()  # Clear all graphs drawn in figure
        plt.plot()  # Draw empty graph
        plt.grid()  # Grid for plot

        x_zero = self.get_x_zero_input()
        y_zero = self.get_y_zero_input()
        x_limit = self.get_x_limit_input()
        n_zero = self.get_n_zero_input()
        n_limit = self.get_n_limit_input()

        const = get_original_function_constant(x_zero, y_zero)

        n_range = get_range(n_zero, n_limit, 1)

        if self.euler_errors_flag.get():
            euler_max_errors = get_max_errors_graph(get_euler_method_output, x_zero, x_limit, y_zero, n_range, const)
            plt.plot(n_range, euler_max_errors, '-go')

        if self.improved_euler_errors_flag.get():
            improved_euler_max_errors = get_max_errors_graph(get_improved_euler_method_output, x_zero, x_limit,
                                                             y_zero, n_range, const)
            plt.plot(n_range, improved_euler_max_errors, '-ro')

        if self.runge_kutta_errors_flag.get():
            runge_kutta_max_errors = get_max_errors_graph(get_runge_kutta_method_output, x_zero, x_limit,
                                                          y_zero, n_range, const)
            plt.plot(n_range, runge_kutta_max_errors, '-mo')

        self.fig.canvas.draw()


class MainView(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        page1 = Page1(self)
        page2 = Page2(self)
        page3 = Page3(self)

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
