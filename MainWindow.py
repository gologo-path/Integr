from tkinter import messagebox

import numpy as np

from Integr import Integr
from WindowPattern import WindowPattern
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.offsetbox import AnchoredText


class MainWindow(WindowPattern):
    limits = [0, 0]

    def __init__(self):
        super().__init__("Integr")

    def _new_command(self):
        super()._clean_frame()

        line1 = tk.Frame(self.window)
        line2 = tk.Frame(self.window)
        line3 = tk.Frame(self.window)
        line3.pack(side=tk.BOTTOM)
        line2.pack(side=tk.BOTTOM)
        line1.pack(side=tk.BOTTOM)

        tmp = tk.Label(line1, text="f(x) = ")
        super()._destroy_objects.append(tmp)
        tmp.pack(side=tk.LEFT)

        self.inp_str = tk.StringVar()
        tmp = tk.Entry(line1, textvariable=self.inp_str, width=35)
        super()._destroy_objects.append(tmp)
        tmp.pack(side=tk.BOTTOM)

        tmp = tk.Label(line2, text="left lim = ")
        super()._destroy_objects.append(tmp)
        tmp.pack(side=tk.LEFT)

        self.left_lim_field = tk.StringVar()
        tmp = tk.Entry(line2, textvariable=self.left_lim_field)
        super()._destroy_objects.append(tmp)
        tmp.pack(side=tk.LEFT)

        tmp = tk.Label(line2, text="right lim = ")
        super()._destroy_objects.append(tmp)
        tmp.pack(side=tk.LEFT)

        self.right_lim_field = tk.StringVar()
        tmp = tk.Entry(line2, textvariable=self.right_lim_field)
        super()._destroy_objects.append(tmp)
        tmp.pack(side=tk.LEFT)

        tmp = tk.Label(line2, text="n = ")
        super()._destroy_objects.append(tmp)
        tmp.pack(side=tk.LEFT)

        self.n_field = tk.StringVar()
        tmp = tk.Entry(line2, textvariable=self.n_field)
        super()._destroy_objects.append(tmp)
        tmp.pack(side=tk.LEFT)

        tmp = tk.Button(line3, text="Расчитать", command=self._get_values)
        super()._destroy_objects.append(tmp)
        tmp.pack(side=tk.BOTTOM)

        super()._destroy_objects.append(line1)
        super()._destroy_objects.append(line2)
        super()._destroy_objects.append(line3)

    def _get_values(self):
        try:
            self.limits[0] = float(self.left_lim_field.get())
            self.limits[1] = float(self.right_lim_field.get())
            self.str_eval = self.inp_str.get()
            self.n = int(self.n_field.get())
        except Exception:
            messagebox.showerror("Ошибка", "Ожидается ввод числа")
            return  # Fix 15.03
        self.str_eval = self.str_eval.replace('^', '**').replace(',', '.')
        self._start_calculation()

    def _start_calculation(self):
        step = abs(self.limits[1] - self.limits[0]) / self.n
        x = [x for x in np.arange(self.limits[0], self.limits[1] + step, step)]
        # print(x)
        integr = Integr(self.str_eval, x, step)

        #print(integr.rectangle())
        #print(integr.trapezoid())
        #print(integr.simpson())

        self._build_plot(integr)
    def _open_command(self):
        super()._open_command()
        self.limits = [0, 0]
        with open(self.file, "r") as f:
            file = f.readlines()
            self.str_eval = file[0]
            tmp = file[1].strip().split(',')
            self.limits[0] = float(tmp[0])
            self.limits[1] = float(tmp[1])
            self.n = int(tmp[2])
        self._start_calculation()

    def _build_plot(self, integr):
        super()._clean_frame()
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot()
        a.plot(integr.start_x, integr.start_y, "b")

        #a.spines['left'].set_position('zero')
        #a.spines['bottom'].set_position('zero')
        #a.spines['top'].set_visible(False)
        #a.spines['right'].set_visible(False)
        str_answ = "rectangle = {0}\ntrapezoid = {1}\nsimpson = {2}".format(
            integr.rectangle(), integr.trapezoid(), integr.simpson())
        a.add_artist(AnchoredText(str_answ, loc=2))

        canvas = FigureCanvasTkAgg(f)
        super()._destroy_objects.append(canvas._tkcanvas)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
