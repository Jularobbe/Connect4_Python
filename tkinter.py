from tkinter import *

class HelloWorld:
    def __init__(self):
        self.root = Tk()
        self.msg = Label(self.root, text = "Welcome!")
        self.msg.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 5)
        self.bt_show = Button(self.root, text = "Click here!",
                              command = self.bt_show_cmd)
        self.bt_show.grid(row = 1, column = 0, padx = 10, pady = 5)
        self.bt_reset = Button(self.root, text = "Reset",
                              command = self.bt_reset_cmd)
        self.bt_reset.grid(row = 1, column = 1, padx = 10, pady = 5)
        self.bt_exit = Button(self.root, text = "Exit",
                              command = self.root.destroy)
        self.bt_exit.grid(row = 2, column = 1, sticky = E)
        self.root.mainloop()

    def bt_show_cmd(self):
        self.msg.config(text = "Hello World")

    def bt_reset_cmd(self):
        self.msg.config(text = "Welcome")


hw = HelloWorld()
