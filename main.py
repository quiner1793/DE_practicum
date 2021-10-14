import tkinter as tk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib

GRAPH_UPDATE = 1000  # time in ms to update graph


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
        original_graph_button = tk.Checkbutton(left_frame,
                                               text="Original graph",
                                               variable=self.original_graph_flag,
                                               onvalue=True,
                                               offvalue=False).pack(expand=False)

        y0_frame = Frame(left_frame)
        y0_frame.pack()
        y0_text_label = Label(y0_frame, width=3, text="y0=").pack(side="left")
        y0_box = Entry(y0_frame, width=5).pack(side="left")

        plot_button = tk.Button(left_frame, text="Plot", command=self.update_graph_first_page).pack(expand=False)
        self.update_graph_first_page()

    def update_graph_first_page(self):
        plt.clf()  # Clear all graphs drawn in figure
        plt.plot()  # Draw empty graph

        print(self.original_graph_flag.get())
        if self.original_graph_flag.get():
            x = [i for i in range(1, 4)]
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
