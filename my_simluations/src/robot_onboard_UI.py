#!/usr/bin/env python3

from tkinter import *
import rospy
from my_simluations.srv import ui as _UI
import time
from my_simluations.srv import uiResponse as _UI_resp


root = Tk()
root.geometry("400x200")

class Window(Frame):

    textvar = StringVar()
    textvar.set("")
    cont = IntVar()
    b = Button(root,text = "Press to continue", command =lambda: Window.cont.set(1))

    def return_UI(req):
        _deliver = 3
        print(str(req.text))
        Window.textvar.set(req.text)
        Window.b.wait_variable(Window.cont)
        Window.textvar.set("Thank you")
        time.sleep(1)
        return _UI_resp(_deliver)

    s = rospy.Service("UI", _UI, return_UI)

    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master= master
        self.init_window()

    def init_window(self):
        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)

        #intialsise sections

        l2 =Label(root, textvariable=Window.textvar)
        l1 = Label(root, text="Once finished please press continue to send me on my way")

        l2.pack()
        l1.pack()
        Window.b.pack()

    # def client_exit(self):
    #     exit()


if __name__ == "__main__":
    rospy.init_node("on_board_UI")
    rospy.loginfo("hello from  onboard UI")
    print("UI check")
    app = Window(root)
    root.resizable(True,True)
    root.mainloop()

    #rospy.spin()
