#!/usr/bin/env python
"""Another DI example using Ooze"""
import ooze
import tkinter as tk
from tkinter import ttk


@ooze.provide('root_window')
class RootWindow:
    def __init__(self, settings, label, button):
        self.window = tk.Tk()
        self.window.title(settings['title'])
        self.window.geometry(self._calculate_geometry(settings['width'], settings['height']))
        self.label = label
        self.button = button

    def _calculate_geometry(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_left = int(screen_width / 2 - width / 2)
        window_top = int(screen_height / 2 - height / 2)
        return f"{width}x{height}+{window_left}+{window_top}"

    def render(self):
        self.add_widgets()
        return self.window

    def add_widgets(self):
        self.label.render(self.window)
        self.button.render(self.window)


@ooze.provide('label')
class LabelWidget:
    def __init__(self, settings):
        self.message = settings['label']['message']

    def render(self, root):
        l = tk.Label(root, text=self.message)
        l.pack()
        return l

    
@ooze.provide('button')
class ButtonWidget:
    root = None

    def quit(self):
        print('Quitting application...')
        self.root.destroy()

    def render(self, root):
        self.root = root
        b = ttk.Button(root, text="Quit", command=self.quit)
        b.pack()
        return b
    
    
@ooze.startup
def main(root_window):
    root_window.render().mainloop()


if __name__ == '__main__':
    ooze.run()
