import tkinter as tk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib

GRAPH_UPDATE = 100  # time in ms to update graph


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


def update_graph():
    plt.clf()  # Clear all graphs drawn in figure
    plt.plot()  # Draw empty graph

    if original_graph_flag.get():
        x = [i for i in range(1, 4)]
        y = [i ** 2 for i in x]
        plt.plot(x, y)

    fig.canvas.draw()
    root.after(GRAPH_UPDATE, update_graph)  # Periodic event


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Page 1")
        label.pack(side="top", fill="both", expand=True)

        fig = plt.figure(1)

        canvas = FigureCanvasTkAgg(fig, master=self)  # Matplotlib graphing canvas
        plot_widget = canvas.get_tk_widget()

        plot_widget.pack(side="right")  # Add the plot to the tkinter widget

        left_frame = Frame(self)
        left_frame.pack(side="left")

        original_graph_flag = tk.BooleanVar()
        original_graph_flag.set(True)
        original_graph_button = tk.Checkbutton(left_frame,
                                               text="Original graph",
                                               variable=original_graph_flag,
                                               onvalue=True,
                                               offvalue=False).pack(side="top")

        y0_text_label = Label(left_frame, width=3, text="y0=").pack(side="left")
        y0_box = Entry(left_frame, width=5).pack(side="right")

        root.after(GRAPH_UPDATE, update_graph)


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
    root.wm_geometry("900x900")

    root.mainloop()
