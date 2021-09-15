import tkinter as tk

#  A cheezy thing to make a green screen to superimpose images onto

root = None

def destroy(event=None):
    global root
    root.destroy()

if "__main__" == __name__:
    root = tk.Tk()
    root.title("Green")
    frame = tk.Frame(root, cursor="none", bg="green")
    frame.pack(fill=tk.BOTH, expand=1)
    root.bind("<Escape>", destroy)
    root.attributes("-fullscreen", True)
    root.mainloop()
