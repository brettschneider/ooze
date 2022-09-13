#!/usr/bin/env python
"""Another DI example using Ooze"""
import ooze
import tkinter as tk
from tkinter import ttk


@ooze.provide('root_window')
class RootWindow:
    def __init__(self, settings, label, button):
        self.title = settings['title']
        self.width = settings['width']
        self.height = settings['height']
        self.window = r = tk.Tk()
        self.label = label
        self.button = button

    def initialize_window(self):
        self.window.title(self.title)
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_left = int(screen_width / 2 - self.width / 2)
        window_top = int(screen_height / 2 - self.height / 2)
        self.window.geometry(f"{self.width}x{self.height}+{window_left}+{window_top}")

    def add_widgets(self):
        self.label.render(self.window)
        self.button.render(self.window)

    def render(self):
        self.initialize_window()
        self.add_widgets()
        return self.window


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
