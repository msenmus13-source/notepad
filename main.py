import os
import tkinter as tk
interface = tk.Tk()
interface.geometry("800x500")
interface.title("untitled-notepad")
text = tk.Text(undo=True)
scroll = tk.Scrollbar()
scroll.pack(side=tk.RIGHT, fill=tk.Y)
text.pack(fill=tk.BOTH, expand=1)




scroll.config(command=text.yview)
text.config(yscrollcommand=scroll.set)
undolist = [""]
redolist = []
selectedFont = "Arial"
selectedSize = "8"
ischangeonce = False

file = None
    
#file menu
filemenu = tk.Menu(tearoff=0)
def NewFile(event=None):
    interface.title("untitled-notepad")
    global file
    file = None
    text.delete(1.0,tk.END)
    return "break"
    
filemenu.add_command(label='New                           Ctrl+N' , command=NewFile)

from tkinter.filedialog import *
def Openfile(event=None):
        global file
        path = askopenfilename(defaultextension=".txt",
                               filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if not path:
            return "break"
        else:
            file = path
            interface.title(os.path.basename(file)+"-Notepad")
            text.delete(1.0,tk.END)
            with open(file, 'r', encoding="utf-8") as txtfile:
                text.insert(1.0,txtfile.read())
        return "break"
filemenu.add_command(label='Open                         Ctrl+O',command=Openfile)

def SaveFile(event=None):
    global file
    if file is None:
        file = asksaveasfilename(initialfile="untitled.txt", defaultextension=".txt",
                                 filetypes=[("All Files", "*.*"), ("Textdoc", "*.txt")])
        if file == "":
            file = None
            return
        interface.title(os.path.basename(file) + "-Notepad")
        global ischangeonce
        ischangeonce = False
    with open(file, "w", encoding="utf-8") as txtfile:
        txtfile.write(text.get(1.0, "end-1c"))
filemenu.add_command(label='Save                          Ctrl+S' , command=SaveFile)
def SaveAs(event=None):
    global file
    path = asksaveasfilename(initialfile="untitled.txt", defaultextension=".txt",
                             filetypes=[("All Files", "*.*"), ("Textdoc", "*.txt")])
    if not path:
        return
    else:
        file = path
        with open(file, "w", encoding="utf-8") as txtfile:
            txtfile.write(text.get(1.0, "end-1c"))
        interface.title(os.path.basename(file) + "-Notepad")
        global ischangeonce
        ischangeonce = False
filemenu.add_command(label='Save as            Ctrl_Shift+S', command=SaveAs)
filemenu.add_separator()

def exitapp():
    interface.destroy()
filemenu.add_command(label='Exit', command=exitapp)

menubar = tk.Menu(tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)
#Editmenu
Editmenu = tk.Menu(tearoff=0)
def Undo():
    try:
        text.edit_undo()
    except tk.TclError:
        pass
    ischangeonce = False #global var for prevent put lots of stars ***** untitled-notepad
    def TextChanged(event):
        flag = text.edit_modified()
        print(flag)
        if flag:
            print("text changed")
            global ischangeonce
            undolist.append(text.get(1.0, "end-1c"))
            redulist.clear()
            if not ischangeonce:
                ischangeonce = True
                interface.title("*"+interface.title())
                
    def undo(event=None):
        if undo_stack: #if anything in undo stack
            undo_stack.pop() #pop the last action
            text = undo_stack[-1]
            redu_stack.append(text.get("1.0", tk.END))
            Text.delete("1.0",tk.END)
            Text.insert("1.0", text)
            undolist.pop() #pop the last action from undolist
Editmenu.add_command(label='Undo                  Ctrl+Z', command=Undo) 
text.bind("<Control-z>", Undo)
def Redo(event=None):
    if redo_stack :
        text = redo_stack.pop()
        undo_stack.append(text.get("1.0", tk.END))
        text.delete("1.0",tk.END)
        text.insert("1.0", text)
        undo_stack.pop() #pop the last action from undolist
Editmenu.add_command(label='Redo                  Ctrl+Y', command=Redo)
text.bind("<Control-y>", Redo)                    
                
        
Editmenu.add_command(label='Undo           Ctrl+Z', command=Undo)
Editmenu.add_separator()
def Copy(event = None):
    text.event_generate("<<Copy>>")
Editmenu.add_command(label='Copy           Ctrl+C', command=Copy)
def Cut(event = None):
    text.event_generate("<<Cut>>")
Editmenu.add_command(label='Cut              Ctrl+X', command=Cut)
def Paste(event = None):
    text.event_generate("<<Paste>>")
Editmenu.add_command(label='Paste          Ctrl+V', command=Paste)
def DeleteText():
    sel = text.tag_ranges("sel")
    if sel:
        text.delete(sel[0], sel[1])
Editmenu.add_command(label='Delete               Del' , command=DeleteText)
Editmenu.add_separator()   
def SelectAll(event=None):
    text.tag_add("sel", "1.0", "end")
    return "break" 
Editmenu.add_command(label='Select All    Ctrl+A', command=SelectAll)
def DateTime(event=None):
    import datetime
    text.insert(tk.INSERT,str(datetime.datetime.now()))    

Editmenu.add_command(label='Date/Time          F5', command=DateTime)
menubar.add_cascade(label='Edit', menu=Editmenu)
#Formatmenu
Formatmenu = tk.Menu(tearoff=0)

def FontFunction():
    FontWindow = tk.Toplevel(interface)
    FontWindow.geometry("400x450+200+200")
    interface.attributes("-disabled", True)
    def closeFontWindow():
        interface.attributes("-disabled", False)
        FontWindow.destroy()
    FontWindow.protocol("WM_DELETE_WINDOW", closeFontWindow)   
    FontWindow.wm_attributes("-topmost", True) 
    FontWindow.title("Font")
    #font window frame
    font_frame = tk.Frame(FontWindow)
    font_frame.pack()
    
    fontFrameFont = tk.Frame(font_frame)
    fontFrameFont.pack(side=tk.LEFT,padx=10)
    fontFrameFontSize = tk.Frame(font_frame)
    fontFrameFontSize.pack(side=tk.LEFT,padx=10)
    #addlistbox
    tk.Label(fontFrameFont,text="Select Font:").pack()
    listboxFont = tk.Listbox(fontFrameFont, selectmode=tk.SINGLE,width=40,exportselection=False)
    listboxFont.pack()
    import tkinter.font as tkf
    for f in tkf.families():
        listboxFont.insert(tk.END, f)
    #addsizelistbox
    tk.Label(fontFrameFontSize,text="Select Size:").pack()
    sizeboxList = [8,10,12,14,16,18,20,36,48,72]
    listboxSize = tk.Listbox(fontFrameFontSize, selectmode=tk.SINGLE,width=40,exportselection=False)
    listboxSize.pack()
    for s in sizeboxList:
        listboxSize.insert(tk.END, s)
    #Add Preview Label
    tk.Label(FontWindow,text="Preview:").pack()
    previewLabel = tk.Label(FontWindow,text="AaBb")
    previewLabel.pack()
    #when font or size clicked preview change
    def font_chooser(event):
        global selectedFont
        global selectedSize
        selectedFont = listboxFont.get(listboxFont.curselection())
        previewLabel.config(font=(selectedFont,selectedSize))
    def Size_chooser(event):
        global selectedSize
        selectedSize = listboxSize.get(listboxSize.curselection())
        previewLabel.config(font=(selectedFont,selectedSize))

    listboxFont.bind('<ButtonRelease-1>',font_chooser)
    listboxSize.bind('<ButtonRelease-1>',Size_chooser)
    
    def okclick():
        global selectedSize
        global selectedFont
        text.config(font=(selectedFont, selectedSize))
        closeFontWindow()
    tk.Button(FontWindow,text="OK",command=okclick).pack()
    tk.Button(FontWindow,text="Cancel",command=closeFontWindow).pack()   
    
       
Formatmenu.add_command(label='Font',command=FontFunction)
menubar.add_cascade(label='Format', menu=Formatmenu)
menubar.add_cascade(label='View')
Helpmenu = tk.Menu(tearoff=0)
#Helpmenu
Helpmenu.add_command(label='About Notepad')
menubar.add_cascade(label='Help', menu=Helpmenu)

#menu right click
RightClickMenu = tk.Menu(tearoff=0)
RightClickMenu.add_command(label="undo", command=Undo)
RightClickMenu.add_command(label="cut", command=Cut)
RightClickMenu.add_command(label="Paste", command=Paste)
RightClickMenu.add_command(label="copy", command=Copy)
RightClickMenu.add_command(label="delete", command=DeleteText)
RightClickMenu.add_separator()
RightClickMenu.add_command(label="Select All", command=SelectAll)

def RightClick(event):
    RightClickMenu.tk_popup(event.x_root, event.y_root)
text.bind("<Button-3>", RightClick)
text.bind("<Control-n>", NewFile)
text.bind("<Control-o>", Openfile)
interface.bind("<Control-s>", SaveFile)
interface.bind("<Control-S>", SaveAs)
text.bind("<Control-a>", SelectAll)
interface.bind("<F5>", DateTime)


interface.config(menu=menubar)



interface.mainloop()