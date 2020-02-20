import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
matplotlib.use("TkAgg")
from tkinter import filedialog
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import csv


LARGE_FONT= ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Heat Map Generator")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        #for F in (StartPage, PageOne, PageTwo, PageThree):
        for F in (StartPage, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageThree)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        # label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        # label.pack(pady=10,padx=10)

        # button = ttk.Button(self, text="Visit Page 1",
        #                     command=lambda: controller.show_frame(PageOne))
        # button.pack()

        # button2 = ttk.Button(self, text="Visit Page 2",
        #                     command=lambda: controller.show_frame(PageTwo))
        # button2.pack()

        # button3 = ttk.Button(self, text="Graph Page",
        #                     command=lambda: controller.show_frame(PageThree))
        # button3.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


class PageThree(tk.Frame):

    def browse_file_path(self):
        filename = filedialog.askopenfilename()
        self.E1.delete(0,'end')
        self.E1.insert(0,filename)
    def create_graph(self):
        f = Figure(figsize=(7,7), dpi=100)
        a = f.add_subplot(111)
        x = []
        y = []
        temp = []

        csv_path = self.E1.get()
        if csv_path == "":
            csv_path = "ExampleData3.csv"
        ar1 = self.array1.get()
        ar2 = self.array2.get()
        if ar1=="" or ar2=="":
            ar1=1
            ar2=1
        else:
            ar1 = int(ar1)
            ar2 = int(ar2)
        try:
            temp_min = float(self.mintemp.get())
            temp_max = float(self.maxtemp.get())
        except:
            temp_min = 20
            temp_max = 40
        try:
            size_pixel = int(self.pixelsize.get())
        except:
            size_pixel = 20
        with open(csv_path,encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                        for index in range(0,ar1*ar2):
                            try:
                                t1=abs(float(row[0]))
                                t2=abs(float(row[1]))
                                t3=float(row[2+index])
                                x.append(float(row[0]))
                                y.append(float(row[1]))
                                temp.append(float(row[2+index]))
                            except:
                                print("error")
        a.scatter( x, y, c=temp, s=size_pixel, vmin=temp_min, vmax=temp_max, alpha=0.6, cmap='jet' )
        #a.scatter([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5],c=[5,6,1,3,8,9,3,5], s=50, alpha=1,cmap='viridis')

        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        #canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().grid(row=1,column=6,rowspan=8,columnspan=8)
        toolbar_frame = tk.Frame(self)
        toolbar_frame.grid(row=0,column=6,columnspan=2)
        toolbar = NavigationToolbar2Tk( canvas, toolbar_frame)
        #toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        #canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.grid(row=1,column=6)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # label = tk.Label(self, text="", font=LARGE_FONT)
        # #label.pack(pady=10,padx=10)
        # label.grid(row=0,column=0)

        # button1 = ttk.Button(self, text="Back to Home",
        #                     command=lambda: controller.show_frame(StartPage))
        # button1.pack()
        # L1 = tk.Label(self, text="CSV Path   ")
        # #L1.pack(pady=10,padx=30,side = tk.TOP)
        # L1.grid(row=1,column=0)
        self.E1 = tk.Entry(self, bd =5)
        self.E1.grid(row=1,column=0)
        #self.E1.pack(side = tk.TOP)
        button1 = ttk.Button(self, text="Browse File",command=self.browse_file_path)
        #button1.pack(in_=self,side = tk.TOP)
        button1.grid(row=1,column=1)


        button2 = ttk.Button(self, text="Create Graph",command=self.create_graph)
        #button2.pack(in_=self,side = tk.TOP)
        button2.grid(row=1,column=2, sticky=tk.W)


        # Array
        # L2 = tk.Label(self, text="Array")
        # L2.grid(row=4,column=0)
        
        self.array1 = tk.Entry(self, bd =3)
        self.array1.grid(row=4,column=0)

        L3 = tk.Label(self, text="X(Array)")
        L3.grid(row=4,column=1)

        self.array2 = tk.Entry(self, bd =3)
        self.array2.grid(row=4,column=2)
        #self.E1.pack(side = tk.TOP)
        

        # Temperature range
        # L4 = tk.Label(self, text="Temperature Range")
        # L4.grid(row=6,column=0)
        
        L5 = tk.Label(self, text="Min(Temp.)")
        L5.grid(row=5,column=0)

        self.mintemp = tk.Entry(self, bd =3)
        self.mintemp.grid(row=5,column=1)

        L6 = tk.Label(self, text="Max(Temp.)")
        L6.grid(row=5,column=2)

        self.maxtemp = tk.Entry(self, bd =3)
        self.maxtemp.grid(row=5,column=3)


        # Pixel Size
        L7 = tk.Label(self, text="Pixel Size")
        L7.grid(row=6,column=0)

        self.pixelsize = tk.Entry(self, bd=3)
        self.pixelsize.grid(row=6,column=1)


        # f = Figure(figsize=(5,5), dpi=100)
        # a = f.add_subplot(111)
        # x = []
        # y = []
        # temp = []
        # with open('ExampleData3.csv',encoding='utf-8') as csv_file:
        #         csv_reader = csv.reader(csv_file, delimiter=',')
        #         for row in csv_reader:
        #             try:
        #                 x.append(float(row[0]))
        #                 y.append(float(row[1]))
        #                 temp.append(float(row[2]))
        #             except:
        #                 print("error")
        # a.scatter( x, y, c=temp, s=50, alpha=0.8, cmap='jet' )
        # #a.scatter([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5],c=[5,6,1,3,8,9,3,5], s=50, alpha=1,cmap='viridis')

        

        # canvas = FigureCanvasTkAgg(f, self)
        # canvas.draw()
        # canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        

app = SeaofBTCapp()
app.mainloop()