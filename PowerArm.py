
import tkinter as tk
import os
from tkinter import ttk
from tkinter import *
import numpy as np
from PIL import ImageTk, Image
from PyPDF4 import PdfFileReader
from PyPDF4 import PdfFileWriter
from pdf_annotate import PdfAnnotator, Appearance, Location
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait
import fitz
from fitz import utils

class PAWcalc():


    def __init__(self):
        root = Tk()
        root.title("PAW Calculator")

        #creating frames

        self.frame1 = Frame(root, width=1000, height=700)
        frame1 = self.frame1
        frame1.grid(row=0, column=0, sticky="nsew")
        self.frame2 = Frame(root, width=1000, height=700)
        frame2 = self.frame2
        self.frame3 = Frame(root, width=1000, height=700)
        frame3 = self.frame3
        self.frame4 = Frame(root, width=1000, height=700)
        frame4 = self.frame4

        #creating labelframes
        self.lf_workpiece = LabelFrame(frame1, text = 'Input Workpiece Information', font="Helvetica 12")
        self.lf_workpiece.grid(row = 1, column =1, columnspan = 13, padx = 20, pady = 20, sticky = W)
        self.lf_install = LabelFrame(frame1, text='Input Installation Information', font="Helvetica 12")
        self.lf_install.grid(row=7, column=1, columnspan=13, padx=20, pady=20, sticky=W)
        self.lf_control_box = LabelFrame(frame1, text='Input Control Box Information', font="Helvetica 12")
        self.lf_control_box.grid(row=11, column=1, columnspan=13, padx=20, pady=20, sticky=W)


        self.lf_end_effector = LabelFrame(frame2, text = 'Input End Effector Information', font="Helvetica 12")
        self.lf_end_effector.grid(row = 11, column =1, columnspan = 13, padx = 20, pady = 20, sticky = W)

        self.lf_app_info = LabelFrame(frame3, text='Input Application Information', font="Helvetica 12")
        self.lf_app_info.grid(row=1, column=1, columnspan=4, padx=20, pady=20, sticky=W)
        self.lf_calculations = LabelFrame(frame3, text='Load Calculations', font="Helvetica 12")
        self.lf_calculations.grid(row=4, column=1, columnspan=7, padx=20, pady=20, sticky=W)
        self.lf_order_info = LabelFrame(frame4, text = 'Order Form Information', font="Helvetica 12")
        self.lf_order_info.grid(row = 1, column =1, columnspan = 12, padx = 20, pady = 20)

        #variables#

        #workpiece variables
        self.h_wp = DoubleVar()
        self.w_wp = DoubleVar()
        self.depth_wp = DoubleVar()
        self.massW = DoubleVar()
        self.type = IntVar()

        #end effector variables

        self.end_manu = IntVar()
        self.grip_meth = IntVar()
        self.massL = DoubleVar()
        self.lengthL = DoubleVar()

        #control box
        self.control_manu = IntVar()
        self.control_meth = IntVar()
        self.rot_tip = IntVar()
        self.lock_mech = IntVar()

        #install information
        self.sup_pres = DoubleVar()
        self.sup_power = IntVar()
        self.install_method = IntVar()
        self.water = IntVar()
        self.dust = IntVar()
        self.daily_freq = IntVar()
        self.monthly_freq = IntVar()
        self.ext_arm = IntVar()


        #application infromation
        self.end = StringVar()
        self.hori = DoubleVar()
        self.vert = DoubleVar()
        self.arm = StringVar()
        self.modelNum = StringVar()
        self.gs_cost = StringVar()
        self.axNum = StringVar()
        self.scara = StringVar()

        #calcloads
        self.vert_load = DoubleVar()
        self.upperMom = DoubleVar()
        self.middleMom = DoubleVar()
        self.lowerMom = DoubleVar()
        self.vert_cap = DoubleVar()
        self.up_cap = DoubleVar()
        self.mid_cap = DoubleVar()
        self.low_cap = DoubleVar()

        #orderform
        self.cust_name = StringVar()
        self.date = StringVar()
        self.work_details = StringVar()
        self.remarks = StringVar()

        #images
        workpiece_img = ImageTk.PhotoImage(Image.open("workpiece1.PNG"))
        wp_img_label = Label(self.lf_workpiece, image=workpiece_img).grid(row=1, column=4, rowspan = 5, padx=30, pady=20, sticky = N)

        endeffector_img = ImageTk.PhotoImage(Image.open("endeffector1.png"))
        ee_img_label = Label(self.lf_end_effector, image=endeffector_img).grid(row=5, column=1, rowspan = 1, columnspan = 8, padx=0, pady=(20, 20), sticky = N)


        # Call Functions

        self.workpiece()
        self.end_effector()
        self.control_box()
        self.install()
        self.app_info()
        self.mass = (self.vert.get())
        self.order_form()


        #ttk.Separator(frame1, orient=HORIZONTAL).place(x=20, y = 310, relwidth = 3)
        #Label(frame1, text="End Effector/Control Box Mass :",
         #     font="Helvetica 12").grid(row=7, column=1, sticky=W)



        Label(self.lf_app_info, text="Model Number:",
              font="Helvetica 12").grid(row=4, column=1,padx = 20, pady = (10,10), sticky=W)

        Label(self.lf_app_info, text="Budgetary Estimate (GS):",
              font="Helvetica 12").grid(row=5, column=1, padx=20, pady=(10, 10), sticky=W)

        # buttons between pages

        Button(frame1, text="End Effector Information",
               command=self.show_frame2,
               font="Helvetica 12",
               justify=RIGHT).grid(row=12, column=13, padx= 620)


        Button(frame2, text="Back",
               command=self.return_frame1,
               font="Helvetica 12",
               justify=LEFT).grid(row=14, column=1)

        Button(frame2, text="Application Information",
               command=self.show_frame3,
               font="Helvetica 12",
               justify=RIGHT).grid(row=14, column=13, padx=0, pady=(15, 15))


        Button(frame3, text="Back",
               command=self.return_frame2,
               font="Helvetica 12",
               justify=LEFT).grid(row=8, column=1)

        Button(frame3, text="Calculate Model Number",
               command=self.showModel,
               font="Helvetica 14 bold",
               justify=RIGHT).grid(row=1, column=7, columnspan = 3, padx=30, pady=(15, 15))

        Button(frame3, text="Create Order Form",
               command=self.show_frame4,
               font="Helvetica 12",
               justify=RIGHT).grid(row=8, column = 9, padx=0, pady=(15, 15))



        Button(frame4, text="Back",
               command=self.return_frame3,
               font="Helvetica 12",
               justify=LEFT).grid(row=11, column=1, padx= 20, sticky = W)

        Button(frame4, text="Generate PAW Order Form",
               command=self.annotate_form,
               font="Helvetica 30",
               justify=RIGHT).grid(row=11, column=11, padx= 0, sticky = E)


        """Button(frame5, text="Back",
               command=self.return_frame4,
               font="Helvetica 12",
               justify=LEFT).grid(row=11, column=1, padx= 20, sticky = W)

        Button(frame5, text="Show PDF",
               command=self.annotate_form,
               font="Helvetica 12",
               justify=RIGHT).grid(row=11, column=8, padx= 20, sticky = W)"""

        root.geometry("900x750")

        root.mainloop()


    def workpiece(self):

        #workpiece labels
        Label(self.lf_workpiece, text="Height (H):",
              font="Helvetica 12").grid(row=1, column=1, padx = 20, pady = (20,10), sticky=W)
        Entry(self.lf_workpiece, textvariable=self.h_wp, width = 15,
              justify=RIGHT).grid(row=1, column=2, padx=(20, 5))
        Label(self.lf_workpiece, text="mm",
              font="Helvetica 12").grid(row=1, column=3, sticky=W)

        Label(self.lf_workpiece, text="Width (W):",
              font="Helvetica 12").grid(row=2, column=1, padx = 20, pady = (10,10), sticky=W)
        Entry(self.lf_workpiece, textvariable=self.w_wp, width = 15,
              justify=RIGHT).grid(row=2, column=2, padx=(20, 5))
        Label(self.lf_workpiece, text="mm",
              font="Helvetica 12").grid(row=2, column=3, sticky=W)

        Label(self.lf_workpiece, text="Depth (L) or Diameter (θ):",
              font="Helvetica 12").grid(row=3, column=1, padx = 20, pady = (10,10), sticky=W)
        Entry(self.lf_workpiece, textvariable=self.depth_wp, width = 15,
              justify=RIGHT).grid(row=3, column=2, padx=(20, 5))
        Label(self.lf_workpiece, text="mm",
              font="Helvetica 12").grid(row=3, column=3, sticky=W)

        Label(self.lf_workpiece, text="Shape:",
              font="Helvetica 12").grid(row=6, column=1, padx = 20, pady = (10,10), sticky=W)
        Radiobutton(self.lf_workpiece, text="Rectangular", font="Helvetica 12 bold", variable=self.type, value=0).grid(
            row=6, column=2, padx=5, sticky = W)
        Radiobutton(self.lf_workpiece, text="Cylindrical", font="Helvetica 12 bold", variable=self.type,
                    value=1).grid(row=6, column=4, padx=5, sticky = W)

    def install(self):

        self.sup_pres.set(0.5)
        Label(self.lf_install, text="Supply Pressure:",
              font="Helvetica 12").grid(row=1, column=1, padx = 20, pady = (10,10), sticky=W)
        Entry(self.lf_install, textvariable=self.sup_pres, width = 15,
              justify=RIGHT).grid(row=1, column=2, padx=(0, 5))
        Label(self.lf_install, text="MPa  (Allowable Range: 0.25 - 0.7 MPa)",
              font="Helvetica 12").grid(row=1, column=3, columnspan = 4, padx = 5, sticky=W)



        Label(self.lf_install, text="Should the tip be able to rotate?:",
              font="Helvetica 12").grid(row=8, column=1, padx = 20, pady = (10,10), sticky=W)
        Radiobutton(self.lf_install, text="Yes", font="Helvetica 12 bold", variable=self.rot_tip, value=0).grid(
            row=8, column=2, padx=5, sticky = W)
        Radiobutton(self.lf_install, text="No", font="Helvetica 12 bold", variable=self.rot_tip,
                    value=1).grid(row=8, column=3, padx=5, sticky = W)

        Label(self.lf_install, text="Rotary Locking Mechanism:",
              font="Helvetica 12").grid(row=9, column=1, padx = 20, pady = (10,10), sticky=W)
        Radiobutton(self.lf_install, text="Yes", font="Helvetica 12 bold", variable=self.lock_mech, value=1).grid(
            row=9, column=2, padx=5, sticky = W)
        Radiobutton(self.lf_install, text="No", font="Helvetica 12 bold", variable=self.lock_mech,
                    value=0).grid(row=9, column=3, padx=5, sticky = W)


    def control_box(self):

        Label(self.lf_control_box, text="Control Box Required:",
              font="Helvetica 12").grid(row=5, column=1, padx = (20), pady = (20,10), sticky=W)
        Radiobutton(self.lf_control_box, text="Required", font="Helvetica 12 bold", variable=self.control_manu, value=0).grid(
            row=5, column=2, padx=5, sticky = W)
        Radiobutton(self.lf_control_box, text="Not Required", font="Helvetica 12 bold", variable=self.control_manu,
                    value=1).grid(row=5, column=3, padx=(5, 20))


        Label(self.lf_control_box, text="Pressure Control Method:",
              font="Helvetica 12").grid(row=6, column=1, padx = 20, pady = (10,10), sticky=W)
        Radiobutton(self.lf_control_box, text="Automatic", font="Helvetica 12 bold", variable=self.control_meth,
                    value=0).grid(row=6, column=2, padx=(5, 5), sticky = W)
        Radiobutton(self.lf_control_box, text="Manual", font="Helvetica 12 bold", variable=self.control_meth, value=1).grid(
            row=6, column=3, padx=(5, 5), sticky = W)

    def end_effector(self):

        Label(self.lf_end_effector, text="End Effector Manufacturer",
              font="Helvetica 12").grid(row=1, column=1, padx = 20, pady = (20,10), sticky=W)
        Radiobutton(self.lf_end_effector, text="CKD", font="Helvetica 12 bold", variable=self.end_manu, value=0).grid(row=1, column=2, padx=5, sticky=W)
        Radiobutton(self.lf_end_effector, text="Customer", font="Helvetica 12 bold", variable=self.end_manu,  value=1).grid(row=1, column=3, padx=5,sticky=W)

        Label(self.lf_end_effector, text="End Effector Grip Method",
              font="Helvetica 12").grid(row=2, column=1, padx = 20, pady = (10,10), sticky=W)
        Radiobutton(self.lf_end_effector, text="Fork", font="Helvetica 12 bold", variable=self.grip_meth, value=0).grid(row=2, column=2, padx=5, sticky=W)
        Radiobutton(self.lf_end_effector, text="Chuck", font="Helvetica 12 bold", variable=self.grip_meth,  value=1).grid(row=2, column=3, padx=5, sticky=W)
        Radiobutton(self.lf_end_effector, text="Vacuum Suction", font="Helvetica 12 bold", variable=self.grip_meth,  value=2).grid(row=2, column=4, padx=5, sticky=W)
        Radiobutton(self.lf_end_effector, text="Other", font="Helvetica 12 bold", variable=self.grip_meth,  value=3).grid(row=2, column=5, padx=(5, 30), sticky=W)

        Label(self.lf_end_effector, text="End Effector Mass (not including operation box):",
              font="Helvetica 12").grid(row=3, column=1, columnspan = 2, padx = 20, pady = (10,10), sticky=W)
        Entry(self.lf_end_effector, textvariable=self.massL,
              justify=RIGHT).grid(row=3, column=3, padx=(0, 5))
        Label(self.lf_end_effector, text="kg",
              font="Helvetica 12").grid(row=3, column=4, sticky=W)

        Label(self.lf_end_effector, text="End Effector Length (as in the figure below):",
              font="Helvetica 12").grid(row=4, column=1, columnspan = 2, padx = 20, pady = (10,10), sticky=W)
        Entry(self.lf_end_effector, textvariable=self.lengthL,
              justify=RIGHT).grid(row=4, column=3, padx=(0, 5))
        Label(self.lf_end_effector, text="mm",
              font="Helvetica 12").grid(row=4, column=4, sticky=W)



    def app_info(self):

        Label(self.lf_app_info, text="Workpiece Mass:",
              font="Helvetica 12").grid(row=1, column=1, padx = 20, pady = (10,10), sticky=W)
        Entry(self.lf_app_info, textvariable=self.massW,
              justify=RIGHT).grid(row=1, column=2, padx=(0, 5))
        Label(self.lf_app_info, text="kg",
              font="Helvetica 12").grid(row=1, column=3, sticky=W)

        Label(self.lf_app_info, text="Vertical Reach:",
              font="Helvetica 12").grid(row=2, column=1,padx = 20, pady = (10,10), sticky=W)
        Entry(self.lf_app_info, textvariable=self.vert,
              justify=RIGHT).grid(row=2, column=2, padx=(0, 5))
        Label(self.lf_app_info, text="mm",
              font="Helvetica 12").grid(row=2, column=3, padx = (0, 10), sticky=W)

        Label(self.lf_app_info, text="Horizontal Reach:",
              font="Helvetica 12").grid(row=3, column=1, padx = 20, pady = (10,10), sticky=W)
        Entry(self.lf_app_info, textvariable=self.hori,
              justify=RIGHT).grid(row=3, column=2, padx=(0, 5))
        Label(self.lf_app_info, text="mm",
              font="Helvetica 12").grid(row=3, column=3, padx=(0, 10), sticky=W)


    def calcReach(self):


        hori = self.hori.get()
        vert = self.vert.get()
        sizeup = 0


        if vert <= 520:
            axNum = "8"
            if (600 < hori <= 1200):
                scara = "S"
            elif (hori > 1200 ):
                sizeup += 1
            else:
                scara = ""

        if 520 < vert <= 580 or sizeup == 1:
            sizeup = 0
            axNum = "X"
            if 700 < hori <= 1400:
                scara = "S"
            elif hori > 1400:
                sizeup += 1
            else:
                scara = ""

        if 580 < vert <= 650 or sizeup == 1:
            sizeup = 0
            axNum = "Z"
            if 800 < hori <= 1600:
                scara = "S"
            elif hori > 1600:
                sizeup += 1
            else:
                scara = ""

        if 650 < vert <= 1100 or sizeup == 1:
            sizeup = 0
            axNum = "8X"
            if 1300 < hori <= 2000:
                scara = "S"
            elif hori > 2000:
                sizeup += 1
            else:
                scara = ""

        if 1100 < vert <= 1230 or sizeup == 1:
            axNum = "XZ"
            if 1500 < hori <= 2300:
                scara = "S"
            elif 2300 < hori <= 3300:
                axNum = "Extension Arm Required"
                scara = ""
            elif hori > 3300:
                axNum = "Horizontal Too High"
                scara = ""
            else:
                scara = ""


        if 1230 < vert <= 1750:
            axNum = "8XZ"
            scara = ""
            if 2100 < hori <= 3100:
                axNum = "Extension Arm Required"
            elif hori > 3100:
                axNum = "Horizontal Too High"

        if (vert > 1750):

            axNum = "Vertical Too High"
            scara = ""


        #self.scara.set(scara)
        #self.axNum.set(axNum)

        if len(axNum)== 2 or len(axNum)==3 or scara == "S":
            prefix = 'PAW-M-'
        elif len(axNum)==1:
            prefix = 'PAW-S-'
        else:
            prefix = ""

        modelNum = (prefix + axNum + scara)

        #self.modelNum.set(str(modelNum))

        return(modelNum)

    def calc_capacity(self, arms):

        pres = self.sup_pres.get()
        manual = self.control_meth.get()
        opbox_est = 9
        m1 = opbox_est + self.massL.get()
        W = self.massW.get()
        load = m1 + W
        overload = 0
        if manual == 1:
            z_boost = 10.5
            x_boost = 6
            e_boost = 4
        else:
            z_boost = 0
            x_boost = 0
            e_boost = 0

        if arms[0] == "8":
            cap = 80 * pres - 13 + e_boost

        elif arms[0] == "X":
            cap = 127 * pres - 20 + x_boost
        elif arms[0] == "Z":
            cap = 195 * pres - 27.5 + z_boost
        else:
            cap = 0

        self.vert_cap.set(cap)
        self.vert_load.set(load)


        if load > cap:

            if arms == "8":
                arms = "X"
                arms = self.calc_loads(arms)
            elif arms == "8X":
                arms = "XZ"

                arms = self.calc_loads(arms)
            elif arms == "X":
                arms = "Z"
                arms = self.calc_loads(arms)
            elif arms == "Z" or arms == "XZ" or arms == "8XZ":
                #print("!!!#####", arms)
                arms = "Too much weight"
                #print("akacho", arms)
            else:
                arms = arms

        cap = self.vert_cap.get()
        load = self.vert_load.get()

        load = '{:.2f}'.format(load)
        cap = '{:.2f}'.format(cap)
        self.vert_cap.set(cap)
        self.vert_load.set(load)

        return (arms)

    def calc_upper_moment(self, arms):

        opbox_est = 9*9.8
        m1 = opbox_est + self.massL.get()*9.8
        W = self.massW.get()*9.8
        L = (self.lengthL.get()/1000)
        L_1 = L/2

        #calculating upper moment from catalog
        upper_moment = m1*L_1 + W*L
        overload = 0



        if arms[0] == "8":
            max_moment_upper = 350
            if max_moment_upper < upper_moment:
                overload += 1
        elif arms[0] == "X":
            max_moment_upper = 550
            if max_moment_upper < upper_moment:
               overload +=1
        elif arms == "Z":
            max_moment_upper = 900
            if max_moment_upper < upper_moment:
                overload += 1
        else:
            max_moment_upper = 0
        if overload == 1:
            if arms == "8":
                arms = "X"
                arms = self.calc_loads(arms)
            elif arms == "8X":
                arms = "XZ"
            elif arms == "X":
                arms = "Z"
                arms = self.calc_loads(arms)
            else:
                arms = "Moment load too high"
                upper_moment = '{:.2f}'.format(upper_moment)
                self.upperMom.set(upper_moment)
                self.up_cap.set(max_moment_upper)
        else:
            upper_moment = '{:.2f}'.format(upper_moment)
            self.upperMom.set(upper_moment)
            self.up_cap.set(max_moment_upper)

        return(arms)

    def calc_middle_moment(self, arms):

        ##print("this is arms at 2nd moment calc", arms)

        opbox_est = 9 * 9.8
        m1 = opbox_est + self.massL.get() * 9.8
        W = self.massW.get() * 9.8
        r = self.rot_tip.get()
        L = (self.lengthL.get() / 1000)
        L_1 = L / 2

        if arms[0] == "8":
            m3 = 14 * 9.8
            m4 = 4*9.8
            X = 600/1000
        elif arms[0] == "X":
            m3 = 23*9.8
            m4 = 5*9.8
            X = 700/1000

        if r == 1:
            m4 =0
        else:
            m4 = m4



        middle_moment =  W*(L_1+X) + m1*(L_1+X) + m3*X/2 + m4*X

        overload = 0

        max_moment_middle = 69
        if arms[0] == "8":
            max_moment_middle = 550
            if max_moment_middle < middle_moment:
                overload += 1

        if arms[0] == "X":
            max_moment_middle = 900
            if max_moment_middle < middle_moment:
                overload += 1

        #print("this is max middle moment", max_moment_middle)
        #print("middle_moment", middle_moment)

        if overload == 1:
            if arms == "8X":
                arms = "XZ"
                #print('recursion two')
                arms = self.calc_loads(arms)
                #print("going to three axes")
            elif arms == "XZ" or arms == "8XZ":
                arms = "Moment load too high"
                middle_moment = '{:.2f}'.format(middle_moment)
                self.middleMom.set(middle_moment)
                self.mid_cap.set(max_moment_middle)
        else:
            middle_moment = '{:.2f}'.format(middle_moment)
            self.middleMom.set(middle_moment)
            self.mid_cap.set(max_moment_middle)
        return(arms)

    def calc_lower_moment(self, arms):

        #print("arms at 3rd", arms)

        opbox_est = 9 * 9.8
        m1 = opbox_est + self.massL.get() * 9.8
        W = self.massW.get() * 9.8
        r = self.rot_tip.get()
        L = (self.lengthL.get() / 1000)
        L_1 = L / 2
        max_moment_middle = 0.0
        overload = 0
        m3 = 14*9.8
        m4 = 4 * 9.8
        m5 = 23*9.8
        m6 = 5 * 9.8
        X = 600 / 1000
        Y = 700 / 1000

        if r == 1:
            m4 =0
        else:
            m4 = m4

        lower_moment = W * (L + X + Y ) + m1*(L_1+X+Y) + m3*(X/2+Y) + m4*(X+Y) +m5*Y/2 +m6*Y

        #print("lower moment", lower_moment)

        if lower_moment > 900:
            arms = "Moment load too high"
            lower_moment = '{:.2f}'.format(lower_moment)
            self.lowerMom.set(lower_moment)
            self.low_cap.set(900)
        else:
            lower_moment = '{:.2f}'.format(lower_moment)
            self.lowerMom.set(lower_moment)
            self.low_cap.set(900)

        return(arms)

    def calc_loads(self, arms):


        arms = self.calc_capacity(arms)
        arms = self.calc_upper_moment(arms)

        if len(arms) == 2 or len(arms) == 3:
            #print("checking middle moment")
            arms = self.calc_middle_moment(arms)

        if len(arms) ==3:
            #print("checking lower moment")
            arms = self.calc_lower_moment(arms)

        #print("after calc load", arms)
        return(arms)

    def price(self, model_num):


        include_z = 0
        assembly_mult = 0
        box_cost = 0
        body_cost = 0
        base_cost = 0
        control_cost = 0
        rot_cost = 0
        lock_cost = 0
        man = self.control_meth.get()
        rot = self.rot_tip.get()
        lock = self.lock_mech.get()

        if model_num[-1] == 'S':
            scara = 1
            arms = model_num[0:-1]
        elif model_num[-1] != 'S':
            scara = 0
            arms = model_num
        else:
            scara = 0

        #print('important', arms)
        ##calculate body cost

        for letter in model_num:
            if letter == "8":
                #print("8 included")
                body_cost +=470
                #print(body_cost)
                #print('rotary 8 ')
                body_cost+=90
                base_cost = 7
                #print(body_cost)
            if letter == "X":
                #print("X inc")
                body_cost += 530
                #print(body_cost)
                base_cost = 7
                #print('rotary x ')
                body_cost+=130
                #print(body_cost)
            if letter == "Z":
                #print("z inc")
                body_cost += 580
                #print(body_cost)
                #print('rotary z ')
                body_cost+=180
                #print(body_cost)
                base_cost = 11
                if scara ==1:
                    #print('scara rot')
                    body_cost+=200
                    #print(body_cost)
                    base_cost = 13


        """if model_num == '8':
            body_cost = 600
        elif model_num == 'X':
            body_cost = 700
        elif model_num == 'Z':
            body_cost = 800
        elif model_num == '8S':
            body_cost = 800
        elif model_num == 'XS':
            body_cost = 900
        elif model_num == 'ZS':
            body_cost = 1200
        elif model_num == '8X':
            body_cost = 1250
        elif model_num == 'XZ':
            body_cost = 1450
        elif model_num == '8XS':
            body_cost = 1450
        elif model_num == 'XZS':
            body_cost = 1850
        elif model_num == '8XZ':
            body_cost = 2000
        else:
            body_cost = 0
        """


        #figuring out which assembly additional pricing to use
        for ax in arms:
            if ax == 'Z':
                include_z = 1


        #calculate assembly additional pricing
        """if include_z == 1:
            assembly_mult = 80
        else:
            assembly_mult = 60

        if len(model_num) < 4:
            assembly_cost = assembly_mult * len(model_num)
        else:
            assembly_cost = 0"""


        #calculate controller cost and automatic box- 2 pressure controls is assumed
        if man == 1:
            box_cost = 0
            if len(arms) == 1:
                control_cost = 500
            elif len(arms) == 2:
                control_cost = 550
            elif len(arms) == 3:
                control_cost = 600
            else:
                control_cost = 0
        elif man == 0:
            box_cost = 350
            if len(arms) == 1:
                control_cost = 470
            elif len(arms) == 2:
                control_cost = 525
            elif len(arms) == 3:
                control_cost = 570
            else:
                control_cost = 0
        else:
            control_cost = 0


        #calc rotary mechanism cost

        if rot == 0:
            if arms[0] == '8':
                rot_cost = 80
            elif arms[0] == 'X':
                rot_cost = 90
            elif arms[0] == 'Z':
                rot_cost = 130
            else:
                rot_cost = 0
        else:
            rot_cost = 0


        #calc locking mechanism cost

        if lock == 1:
            if rot == 0:
                lock_cost = (len(model_num) + 1) * 100
            elif rot == 1:
                lock_cost = len(model_num) * 100
            else:
                lock_cost = 0
        else:
            lock_cost = 0


        #print('GS cost breakdown: body cost = ', body_cost, 'base cost', base_cost,  'control cost = ', control_cost, '  rotary cost = ', rot_cost, "  lock cost = ", lock_cost, "  box cost = ", box_cost )
        #assuming dolly included
        total_cost = box_cost + body_cost + control_cost + rot_cost + lock_cost + base_cost +675

        return(total_cost)

    def showModel(self):

        modelNum = self.calcReach()
        r = self.rot_tip.get()
        l = self.lock_mech.get()
        conversion_rate = 104.6
        last_num = modelNum[-1]

        if r == 1 and l == 0:
            rot_lock = ""
        elif r == 1 and l == 1:
            rot_lock = "-L"
        elif r == 0 and l == 1:
            rot_lock = "-LR"
        elif r ==0 and l == 0:
            rot_lock = "-R"
        else:
            rot_lock = ""


        if last_num == "S":
            scara = last_num
            arms = modelNum[6:-1]
        elif last_num == "8" or last_num =="X" or last_num == "Z":
            scara = ""
            arms = modelNum[6:]
        else:
            scara = ''
            arms = modelNum

        model_arms = self.calc_loads(arms)

        pressure = self.sup_pres.get()

        if pressure < 0.25 or pressure > 0.75:
            model_arms = "Pressure Out of Range"



        if len(model_arms) > 3:
            checked_model = model_arms
        else:
            checked_model = modelNum[0:6] + model_arms + scara + rot_lock



        self.modelNum.set(str(checked_model))
        ###Produces Model Number###
        Label(self.lf_app_info, textvariable=self.modelNum,
              font="Helvetica 18 bold",
              ).grid(row=4, column=2, padx=(0, 5), pady = (10,10))




        Label(self.lf_calculations, text="Calculated",
              font="Helvetica 12 bold",
              justify=RIGHT).grid(row=6, column=3, columnspan = 2, padx=(0, 10), pady=(10, 10))

        Label(self.lf_calculations, text="Max Allowable",
              font="Helvetica 12 bold",
              justify=RIGHT).grid(row=6, column=6, columnspan=2, padx=(75, 10), pady=(10, 10))



        Label(self.lf_calculations, text = "Load:",
              font="Helvetica 12 bold",
              justify=RIGHT).grid(row=7, column=2, padx = (20, 20), pady = (10,10), sticky = W)
        Label(self.lf_calculations, textvariable=self.vert_load,
              font="Helvetica 12 bold",
              justify=RIGHT).grid(row=7, column=3, padx = (10, 0), pady = (10,10), sticky = W)
        Label(self.lf_calculations, text="kg",
              font="Helvetica 12 bold",
              justify=RIGHT).grid(row=7, column=4, padx = (10, 10), pady=(10, 10), sticky = W)
        Label(self.lf_calculations, textvariable=self.vert_cap,
              font="Helvetica 12 bold",
              justify=RIGHT).grid(row=7, column=6, padx=(90, 0), pady=(10, 10), sticky=W)
        Label(self.lf_calculations, text="kg",
              font="Helvetica 12 bold",
              justify=RIGHT).grid(row=7, column=7, padx=(0, 10), pady=(10, 10), sticky=W)


        Label(self.lf_calculations, text = "First Arm Moment Load :",
              font="Helvetica 12 bold",
              justify=RIGHT).grid(row=8, column=2, padx = (20, 20), pady = (10,10), sticky = W)
        Label(self.lf_calculations, textvariable=self.upperMom,
              font="Helvetica 12 bold",
              justify=RIGHT).grid(row=8, column=3, padx = (10, 0), pady=(10, 10), sticky = W)
        Label(self.lf_calculations, text="N-m",
              font="Helvetica 12 bold",
              justify=RIGHT).grid(row=8, column=4, padx = (10, 10), pady=(10, 10), sticky = W)
        Label(self.lf_calculations, textvariable=self.up_cap,
              font="Helvetica 12 bold",
              justify=RIGHT).grid(row=8, column=6, padx=(90, 0), pady=(10, 10), sticky=W)
        Label(self.lf_calculations, text="N-m",
              font="Helvetica 12 bold",
              justify=RIGHT).grid(row=8, column=7, padx=(0, 10), pady=(10, 10), sticky=W)


        if len(model_arms) > 1:

            Label(self.lf_calculations, text = "Second Arm Moment Load :",
                  font="Helvetica 12 bold",
                  justify=RIGHT).grid(row=9, column=2, padx = (20, 20), pady = (10,10), sticky = W)
            Label(self.lf_calculations, textvariable=self.middleMom,
                  font="Helvetica 12 bold",
                  justify=RIGHT).grid(row=9, column=3, padx = (10, 0), pady = (10,10), sticky = W)
            Label(self.lf_calculations, text = "N-m",
                  font="Helvetica 12 bold",
                  justify=RIGHT).grid(row=9, column=4, padx = (10, 10), pady=(10, 10), sticky = W)
            Label(self.lf_calculations, textvariable=self.mid_cap,
                  font="Helvetica 12 bold",
                  justify=RIGHT).grid(row=9, column=6, padx=(90, 0), pady = (10,10), sticky = W)
            Label(self.lf_calculations, text = "N-m",
                  font="Helvetica 12 bold",
                  justify=RIGHT).grid(row=9, column=7, padx=(0, 10), pady=(10, 10), sticky = W)



        if len(model_arms) > 2:

            Label(self.lf_calculations, text = "Third Arm Moment Load :",
                  font="Helvetica 12 bold",
                  justify=RIGHT).grid(row=10, column=2, padx = (20, 20), pady = (10,10), sticky = W)
            Label(self.lf_calculations, textvariable=self.lowerMom,
                  font="Helvetica 12 bold",
                  justify=RIGHT).grid(row=10, column=3, padx = (10, 0), pady = (10,10), sticky = W)
            Label(self.lf_calculations, text = "N-m",
                  font="Helvetica 12 bold",
                  justify=RIGHT).grid(row=10, column=4, padx = (10, 10), pady=(10, 10), sticky = W)
            Label(self.lf_calculations, textvariable=self.low_cap,
                  font="Helvetica 12 bold",
                  justify=RIGHT).grid(row=10, column=6, padx=(90, 0), pady = (10,10), sticky = W)
            Label(self.lf_calculations, text = "N-m",
                  font="Helvetica 12 bold",
                  justify=RIGHT).grid(row=10, column=7, padx=(0, 10), pady=(10, 10), sticky = W)

        arms_cost = model_arms + scara

        #GS cost in yen
        cost = self.price(arms_cost)*1000

        #print('gs in yen', cost)
        #GS cost in USD

        ###cost = cost / conversion_rate
        #FCA cost in USD

        cost = str(cost)

        gs_cost = ('¥ ' + cost[:-6] + ',' + cost[-6:-3] + ',' + cost[-3:])

        if len(model_arms) > 3:
            gs_cost = 'Contact CKD'
        else:
            Label(self.frame3, text="*This price is an unofficial estimate \nplease fill out PAW Order Sheet \n \n *Dolly included, attachment \n not included",
                  justify=LEFT, font="Helvetica 12").grid(row=1, column=7, columnspan=3, padx=(21, 10), pady=(170, 10))
            Label(self.lf_app_info, text="JPY",
                  font="Helvetica 12").grid(row=5, column=3, padx=(0, 10), pady=(15, 10))

        self.gs_cost.set(gs_cost)

        ###Produces Budgetary cost###
        Label(self.lf_app_info, textvariable=self.gs_cost,
              font="Helvetica 18 bold",
              justify=RIGHT).grid(row=5, column=2, padx=(0, 5), pady = (10,10))

    def order_form(self):

        self.sup_power.set(110)
        Label(self.lf_order_info, text="Power:",
              font="Helvetica 12").grid(row=2, column=1, padx=20, pady=(10, 10), sticky=W)
        Entry(self.lf_order_info, textvariable=self.sup_power,
              justify=RIGHT).grid(row=2, column=2, padx=(0, 5))
        Label(self.lf_order_info, text="VAC",
              font="Helvetica 12").grid(row=2, column=3, sticky=W)

        Label(self.lf_order_info, text="Installation Method:",
              font="Helvetica 12").grid(row=3, column=1, padx=20, pady=(10, 10), sticky=W)
        Radiobutton(self.lf_order_info, text="Fixed on Floor", font="Helvetica 12 bold", variable=self.install_method,
                    value=0).grid(
            row=3, column=2, padx=5, sticky=W)
        Radiobutton(self.lf_order_info, text="Movable on Cart", font="Helvetica 12 bold", variable=self.install_method,
                    value=1).grid(row=3, column=3, padx=5)
        Radiobutton(self.lf_order_info, text="Other", font="Helvetica 12 bold", variable=self.install_method,
                    value=2).grid(row=3, column=4, padx=(5, 110))

        Label(self.lf_order_info, text="Water Drops:",
              font="Helvetica 12").grid(row=4, column=1, padx=20, pady=(10, 10), sticky=W)
        Radiobutton(self.lf_order_info, text="Yes", font="Helvetica 12 bold", variable=self.water, value=0).grid(
            row=4, column=2, padx=(5, 5), sticky=W)
        Radiobutton(self.lf_order_info, text="No", font="Helvetica 12 bold", variable=self.water,
                    value=1).grid(row=4, column=3, padx=(5, 5), sticky=W)

        Label(self.lf_order_info, text="Dust:",
              font="Helvetica 12").grid(row=5, column=1, padx=20, pady=(10, 10), sticky=W)
        Radiobutton(self.lf_order_info, text="Yes", font="Helvetica 12 bold", variable=self.dust, value=0).grid(
            row=5, column=2, padx=(5, 5), sticky=W)
        Radiobutton(self.lf_order_info, text="No", font="Helvetica 12 bold", variable=self.dust,
                    value=1).grid(row=5, column=3, padx=(5, 5), sticky=W)

        Label(self.lf_order_info, text="Daily Operating Frequency:",
              font="Helvetica 12").grid(row=6, column=1, padx=20, pady=(10, 10), sticky=W)
        Entry(self.lf_order_info, textvariable=self.daily_freq,
              justify=RIGHT).grid(row=6, column=2, padx=(0, 5))
        Label(self.lf_order_info, text="times/day",
              font="Helvetica 12").grid(row=6, column=3, sticky=W)

        Label(self.lf_order_info, text="Monthly Operating Frequency:",
              font="Helvetica 12").grid(row=7, column=1, padx=20, pady=(10, 10), sticky=W)
        Entry(self.lf_order_info, textvariable=self.monthly_freq,
              justify=RIGHT).grid(row=7, column=2, padx=(0, 5))
        Label(self.lf_order_info, text="days/month",
              font="Helvetica 12").grid(row=7, column=3, sticky=W)

        Label(self.lf_order_info, text="Customer Company Name:",
              font="Helvetica 12").grid(row=8, column=1, padx=20, pady=(10, 10), sticky=W)
        Entry(self.lf_order_info, width = 53, textvariable=self.cust_name,
              justify=RIGHT).grid(row=8, column=2, columnspan=2, padx=(17, 5))

        Label(self.lf_order_info, text="Date: ",
              font="Helvetica 12").grid(row=9, column=1, padx=20, pady=(10, 10), sticky=W)
        Entry(self.lf_order_info, textvariable=self.date,
              justify=RIGHT).grid(row=9, column=2, padx=(0,5))
        Label(self.lf_order_info, text="(MM/DD/YY)",
              font="Helvetica 12").grid(row=9, column=3, sticky=W)

        Label(self.lf_order_info, text="Enter details of work in progress and purpose of use for PAW:",
              font="Helvetica 12").grid(row=10, column=1, columnspan = 3, padx = 20, pady = (10,10), sticky=W)
        Entry(self.lf_order_info, width = 130, textvariable=self.work_details,
              justify= LEFT).grid(row=11, column=1, columnspan =7, padx=(20, 40), pady = (10, 20) )






    def annotate_form(self):
        cust = self.cust_name.get()
        date = self.date.get()

        #part 1
        details = self.work_details.get()

        #part 2
        height = self.h_wp.get()
        width = self.w_wp.get()
        depth = self.depth_wp.get()
        weight = self.massW.get()
        type = self.type.get()

        #part 3

        manu = self.end_manu.get()
        grip = self.grip_meth.get()
        end_weight = self.massL.get()

        #part4
        cont_manu = self.control_manu.get()
        cont_meth = self.control_meth.get()

        #part5
        pres = self.sup_pres.get()
        power = self.sup_power.get()

        install = self.install_method.get()
        water = self.water.get()
        dust = self.dust.get()
        day_freq = self.daily_freq.get()
        monthly_freq = self.monthly_freq.get()



        path = 'PAW_application_order_sheet.pdf'
        doc = fitz.open(path)
        page = doc[0]
        page.cleanContents()
        # the text strings, each having 3 lines

        details_0 = details[0:90]
        details_1 = details[90:180]
        details_2 = details[180:270]
        details_3 = details[270:360]

        black = (0, 0, 0)  # the color for the balck dots


        p_cust = fitz.Point(180, 52)
        p_date = fitz.Point(450, 25)
        p_details_0 = fitz.Point(89, 136)
        p_details_1 = fitz.Point(89, 149)
        p_details_2 = fitz.Point(89, 163)
        p_details_3 = fitz.Point(89, 176)
        p_height = fitz.Point(190, 215)
        p_width = fitz.Point(190, 229)
        if type == 0:
            p_depth = fitz.Point(190, 243)
        else:
            p_depth = fitz.Point(190, 257)
        p_weight = fitz.Point(190, 270)
        p_type = fitz.Point(190, 283)

        if manu == 0:
            p_endman = fitz.Point(205, 387)
            rad_end = 7
        else:
            p_endman = fitz.Point(234, 387)
            rad_end = 10

        if grip == 0:
            p_grip = fitz.Point(205, 400)
            rad_grip = 7
        elif grip == 1:
            p_grip = fitz.Point(230, 400)
            rad_grip = 7
        elif grip == 2:
            p_grip = fitz.Point(260, 400)
            rad_grip = 11

        p_endmass = fitz.Point(240,418)

        if cont_manu == 0:
            p_contmanu = fitz.Point(212,442)
        else:
            p_contmanu = fitz.Point(255, 442)

        if cont_meth == 1:
            p_contmeth = fitz.Point(233, 454)
        else:
            p_contmeth = fitz.Point(375, 454)

        p_pres = fitz.Point(314, 472)
        p_power = fitz.Point(430, 472)

        if install == 0:
            p_install = fitz.Point(208, 496)
            rad_ins = 10
        else:
            p_install = fitz.Point(265, 496)
            rad_ins = 10

        if water == 0:
            p_water = fitz.Point(254, 509)
        else:
            p_water = fitz.Point(272, 509)

        if dust == 0:
            p_dust = fitz.Point(333, 509)
        else:
            p_dust = fitz.Point(354, 509)

        p_day = fitz.Point(208, 528)
        p_month = fitz.Point(291, 528)

        # create a Shape to draw on
        shape = page.newShape()




        shape.drawCircle(p_endman, rad_end)
        shape.drawCircle(p_grip, rad_grip)
        shape.drawCircle(p_contmanu, 10)
        shape.drawCircle(p_contmeth, 10)
        shape.drawCircle(p_install, rad_ins)
        shape.drawCircle(p_water, 8)
        shape.drawCircle(p_dust, 8)
        shape.finish(width=0.8, color=black, fill=None
                     )

        # insert the text strings
        shape.insertText(p_cust, str(cust))
        shape.insertText(p_date, str(date))
        shape.insertText(p_details_0, str(details_0))
        shape.insertText(p_details_1, str(details_1))
        shape.insertText(p_details_2, str(details_2))
        shape.insertText(p_details_3, str(details_3))
        shape.insertText(p_height, str(height))
        shape.insertText(p_width, str(width))
        shape.insertText(p_depth, str(depth))
        shape.insertText(p_weight, str(weight))
        shape.insertText(p_type, str(type+1))
        shape.insertText(p_endmass, str(end_weight))
        shape.insertText(p_pres, str(pres))
        shape.insertText(p_power, str(power))
        shape.insertText(p_day, str(day_freq))
        shape.insertText(p_month, str(monthly_freq))

        # store our work to the page
        shape.commit()
        doc.save('Filled_PAW_Order_Form.pdf')
        os.startfile('Filled_PAW_Order_Form.pdf')


    def show_frame2(self):
        self.frame1.grid_forget()
        self.frame2.grid()

    def return_frame1(self):
        self.frame2.grid_forget()
        self.frame1.grid()

    def show_frame3(self):
        self.frame2.grid_forget()
        self.frame3.grid()

    def return_frame2(self):
        self.frame3.grid_forget()
        self.frame2.grid()

    def show_frame4(self):
        self.frame3.grid_forget()
        self.frame4.grid()

    def return_frame3(self):
        self.frame4.grid_forget()
        self.frame3.grid()


    def show_frame5(self):
        self.frame4.grid_forget()
        self.frame5.grid()

    def return_frame4(self):
        self.frame5.grid_forget()
        self.frame4.grid()

    """ def extArm(self):
        Label(self.window, text="mm",
              font="Helvetica 12").grid(row=10, column=2, sticky=W)"""

PAWcalc()

