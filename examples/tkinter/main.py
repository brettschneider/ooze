#!/usr/bin/env python
"""Another DI example using Ooze"""
import ooze
import tkinter as tk
from tkinter import ttk


@ooze.provide
class Root:
    def __init__(self, window_settings):
        self.title = window_settings['title']
        self.width = window_settings['width']
        self.height = window_settings['height']

    def generate(self):
        r = tk.Tk()
        r.title(self.title)
        screen_width = r.winfo_screenwidth()
        screen_height = r.winfo_screenheight()
        window_left = int(screen_width / 2 - self.width / 2)
        window_top = int(screen_height / 2 - self.height / 2)
        r.geometry(f"{self.width}x{self.height}+{window_left}+{window_top}")
        return r


@ooze.provide
class Label:
    def __init__(self, window_settings):
        self.message = window_settings['label']['message']

    def generate(self, root):
        l = tk.Label(root, text=self.message)
        l.pack()
        return l

    
@ooze.provide
class Button:
    def quit(self):
        print('Quitting application...')
        self.root.destroy()

    def generate(self, root):
        self.root = root
        b = ttk.Button(root, text="Quit", command=self.quit)
        b.pack()
        return b
    
    
@ooze.startup
def main(root, label, button):
    r = root.generate()
    l = label.generate(r)
    b = button.generate(r)
    r.mainloop()


if __name__ == '__main__':
    ooze.run()
