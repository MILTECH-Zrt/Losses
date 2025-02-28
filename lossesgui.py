import tkinter as tk
from tkinter import ttk

import losscalc as LC

""" Init GUI and its main parameters"""
root = tk.Tk()
root.title('Loss Calculations - MILTECH Co.')
root.iconbitmap(r'./Miliconnew.ico')  # use relat
root.geometry("825x421")  # width * height
lw = 25  # labelwidth
ew = 15  # entrywidth
uw = 5   # unitwidth

""" Tabs """
tabControl = ttk.Notebook(root)

tabRWG = ttk.Frame(tabControl)
tabControl.add(tabRWG, text='Rectangular WG', sticky='NSEW')

tabVSWR = ttk.Frame(tabControl)
tabControl.add(tabVSWR, text='VSWR', sticky='NSEW')

tabControl.grid()  # show tabs


""" Events """


def rwg_changed(event):

    rwgtype = rwgType_combo.get()
    aunit = rwgaunits_combo.get()
    a = LC.WG_types[rwgtype][0] * LC.unit2SI["inch"] / LC.unit2SI[aunit]
    b = LC.WG_types[rwgtype][1] * LC.unit2SI["inch"] / LC.unit2SI[aunit]
    dbRWGa.set(a)
    dbRWGb.set(b)
    rwgRecomFreq.set(LC.WG_types[rwgType_combo.get()][2])


def rwgaunit_changed(event):
    rwgbunit.set(rwgaunits_combo.get())


def rwgMaterial_changed(event):
    dbRWGcond.set(LC.WG_conductivity[rwgMaterial_combo.get()])
    calc_rwg()


def rwgfrequnit_changed(event):
    rwgfcunit.set(rwgfunits_combo.get())


def vswr_changed(event):
    vswr = dbVSWR.get()
    Lmis, refcoeff, fracpowrefl = LC.mismatchloss(vswr)
    dbMismatchLoss.set(Lmis)
    dbReflectionCoeff.set(refcoeff)
    dbFracPowRefl.set(fracpowrefl)


""" Calculations """


def calc_rwg():
    aunit = rwgaunits_combo.get()
    a = dbRWGa.get() * LC.unit2SI[aunit]
    b = dbRWGb.get() * LC.unit2SI[aunit]
    m = intRWGTEm.get()
    n = intRWGTEn.get()
    mur = dbRWGmur.get()
    epsr = dbRWGepsr.get()
    sig = dbRWGcond.get()
    frequnit = rwgfunits_combo.get()
    fr = dbRWGfr.get() * LC.unit2SI[frequnit]
    rwgl = dbRWGlength.get() * LC.unit2SI[rwgLunits_combo.get()]

    fc = LC.rectwaveguide_cutofffreq(a, b, m, n, mur, epsr)
    Alfa, Lrwg = LC.rectwaveguideloss(a, b, sig, fr, fc, rwgl)
    # alfa, Lwg = LC.rectwaveguideloss(0.072136,0.034036,3.767e7, 2.6e9, 2.079406e9)

    rwgRecomFreq.set(LC.WG_types[rwgType_combo.get()][2])
    dbCutoffFreq.set(fc/LC.unit2SI[frequnit])
    dbRWGatten.set(Alfa)
    dbRWGloss.set(Lrwg)


""" VSWR Frame"""

vswframe = ttk.LabelFrame(tabVSWR, text="Parameters")
vswframe.grid(row=0, column=0, sticky='NW')

rc = 0
ttk.Label(vswframe, text='VSWR:', width=lw, anchor='w').grid(row=rc, column=0)
dbVSWR = tk.DoubleVar()
dbVSWR.set(1)
VSWR_entry = tk.Entry(vswframe, textvariable=dbVSWR, width=ew)
VSWR_entry.grid(row=rc, column=1)
VSWR_entry.bind("<Return>", vswr_changed)

rc += 1
ttk.Label(vswframe, text='Reflection coefficient:', width=lw, anchor='w').grid(row=rc, column=0)
dbReflectionCoeff = tk.DoubleVar()
ttk.Label(vswframe, textvariable=dbReflectionCoeff, width=lw, anchor='w').grid(row=rc, column=1)

rc += 1
ttk.Label(vswframe, text='Fraction of power reflected:', width=lw, anchor='w').grid(row=rc, column=0)
dbFracPowRefl = tk.DoubleVar()
ttk.Label(vswframe, textvariable=dbFracPowRefl, width=lw, anchor='w').grid(row=rc, column=1)

rc += 1
ttk.Label(vswframe, text='Mismatch loss:', width=lw, anchor='w').grid(row=rc, column=0)
dbMismatchLoss = tk.DoubleVar()
ttk.Label(vswframe, textvariable=dbMismatchLoss, width=lw, anchor='w').grid(row=rc, column=1)
ttk.Label(vswframe, text='dB', width=uw, anchor='w').grid(row=rc, column=2)

""" Rectangular Waveguide Frame """

rwgframe = ttk.LabelFrame(tabRWG, text="Parameters")
rwgframe.grid(row=0, column=0, sticky='NW')

rwgresframe = ttk.LabelFrame(tabRWG, text="Results")
rwgresframe.grid(row=0, column=1, sticky='NW')

rc = 0
ttk.Label(rwgframe, text='Frequency:', width=lw, anchor='w').grid(row=rc, column=0)
dbRWGfr = tk.DoubleVar()
dbRWGfr.set(1)
RWGfr_entry = tk.Entry(rwgframe, textvariable=dbRWGfr, width=ew)
RWGfr_entry.grid(row=rc, column=1)

rwgfunits = ["GHz", "MHz", "kHz", "Hz"]
rwgfunits_combo = ttk.Combobox(rwgframe, values=rwgfunits, width=uw)
rwgfunits_combo.current(0)
rwgfunits_combo.grid(row=rc, column=2)
rwgfunits_combo.bind("<<ComboboxSelected>>", rwgfrequnit_changed)

rc += 1
ttk.Label(rwgframe, text='Waveguide type:', width=lw, anchor='w').grid(row=rc, column=0)
rwgTypes = list(LC.WG_types.keys())
rwgType_combo = ttk.Combobox(rwgframe, values=rwgTypes, width=ew-3)
rwgType_combo.current(0)
rwgType_combo.grid(row=rc, column=1)
rwgType_combo.bind("<<ComboboxSelected>>", rwg_changed)

rc += 1
ttk.Label(rwgframe, text='Cross section a:', width=lw, anchor='w').grid(row=rc, column=0)
dbRWGa = tk.DoubleVar()
dbRWGa.set(3)
RWGa_entry = tk.Entry(rwgframe, textvariable=dbRWGa, width=ew)
RWGa_entry.grid(row=rc, column=1)

rwgaunits = ["mm", "cm", "inch"]
rwgaunits_combo = ttk.Combobox(rwgframe, values=rwgaunits, width=uw)
rwgaunits_combo.current(2)
rwgaunits_combo.grid(row=rc, column=2)
rwgaunits_combo.bind("<<ComboboxSelected>>", rwgaunit_changed)

rc += 1
ttk.Label(rwgframe, text='Cross section b:', width=lw, anchor='w').grid(row=rc, column=0)
dbRWGb = tk.DoubleVar()
dbRWGb.set(2)
RWGb_entry = tk.Entry(rwgframe, textvariable=dbRWGb, width=ew)
RWGb_entry.grid(row=rc, column=1)

rwgbunit = tk.StringVar()
rwgbunit.set(rwgaunits[2])
ttk.Label(rwgframe, textvariable=rwgbunit, width=uw, anchor='w').grid(row=rc, column=2)

rc += 1
ttk.Label(rwgframe, text='Waveguide length:', width=lw, anchor='w').grid(row=rc, column=0)
dbRWGlength = tk.DoubleVar()
dbRWGlength.set(1)
RWGlength_entry = tk.Entry(rwgframe, textvariable=dbRWGlength, width=ew)
RWGlength_entry.grid(row=rc, column=1)

rwgLunits = ["m", "dm", "cm", "mm", "ft", "in"]
rwgLunits_combo = ttk.Combobox(rwgframe, values=rwgLunits, width=uw)
rwgLunits_combo.current(0)
rwgLunits_combo.grid(row=rc, column=2)

rc += 1
ttk.Label(rwgframe, text='Waveguide wall material:', width=lw, anchor='w').grid(row=rc, column=0)
rwgMaterials = list(LC.WG_conductivity.keys())
rwgMaterial_combo = ttk.Combobox(rwgframe, values=rwgMaterials, width=ew-3)
rwgMaterial_combo.current(0)
rwgMaterial_combo.grid(row=rc, column=1)
rwgMaterial_combo.bind("<<ComboboxSelected>>", rwgMaterial_changed)

rc += 1
ttk.Label(rwgframe, text='Waveguide conductivity:', width=lw, anchor='w').grid(row=rc, column=0)
dbRWGcond = tk.DoubleVar()
dbRWGcond.set(LC.WG_conductivity["Aluminum"])
RWGcond_entry = tk.Entry(rwgframe, textvariable=dbRWGcond, width=ew)
RWGcond_entry.grid(row=rc, column=1)
ttk.Label(rwgframe, text='S/m', width=uw, anchor='w').grid(row=rc, column=2)

rc += 1
ttk.Label(rwgframe, text='Waveguide filler material', width=lw, anchor='w').grid(row=rc, column=0)

rc += 1
ttk.Label(rwgframe, text='  Rel. permittivity:', width=lw, anchor='w').grid(row=rc, column=0)
dbRWGepsr = tk.DoubleVar()
dbRWGepsr.set(1)
RWGepsr_entry = tk.Entry(rwgframe, textvariable=dbRWGepsr, width=ew)
RWGepsr_entry.grid(row=rc, column=1)

rc += 1
ttk.Label(rwgframe, text='  Rel. permeability:', width=lw, anchor='w').grid(row=rc, column=0)
dbRWGmur = tk.DoubleVar()
dbRWGmur.set(1)
RWGmur_entry = tk.Entry(rwgframe, textvariable=dbRWGmur, width=ew)
RWGmur_entry.grid(row=rc, column=1)

rc += 1
ttk.Label(rwgframe, text='TEmn modes', width=lw, anchor='w').grid(row=rc, column=0)

rc += 1
ttk.Label(rwgframe, text='  m:', width=lw, anchor='w').grid(row=rc, column=0)
intRWGTEm = tk.IntVar()
intRWGTEm.set(1)
RWGTEm_entry = tk.Entry(rwgframe, textvariable=intRWGTEm, width=ew)
RWGTEm_entry.grid(row=rc, column=1)

rc += 1
ttk.Label(rwgframe, text='  n:', width=lw, anchor='w').grid(row=rc, column=0)
intRWGTEn = tk.IntVar()
intRWGTEn.set(0)
RWGTEn_entry = tk.Entry(rwgframe, textvariable=intRWGTEn, width=ew)
RWGTEn_entry.grid(row=rc, column=1)

rc += 1
rwgCalc_button = tk.Button(rwgframe, text="Calculate", command=calc_rwg, width=14)
rwgCalc_button.grid(row=rc, column=0)

rc = 0
ttk.Label(rwgresframe, text='Recommended frequency:', width=lw, anchor='w').grid(row=rc, column=0)
rwgRecomFreq = tk.StringVar()
ttk.Label(rwgresframe, textvariable=rwgRecomFreq, width=lw, anchor='w').grid(row=rc, column=1)

rc += 1
ttk.Label(rwgresframe, text='Cut-off frequency:', width=lw, anchor='w').grid(row=rc, column=0)
dbCutoffFreq = tk.DoubleVar()
ttk.Label(rwgresframe, textvariable=dbCutoffFreq, width=lw, anchor='w').grid(row=rc, column=1)
rwgfcunit = tk.StringVar()
rwgfcunit.set("GHz")
ttk.Label(rwgresframe, textvariable=rwgfcunit, width=uw, anchor='w').grid(row=rc, column=2)

rc += 1
ttk.Label(rwgresframe, text='Spec. attenuation:', width=lw, anchor='w').grid(row=rc, column=0)
dbRWGatten = tk.DoubleVar()
ttk.Label(rwgresframe, textvariable=dbRWGatten, width=lw, anchor='w').grid(row=rc, column=1)
ttk.Label(rwgresframe, text='dB/m', width=uw, anchor='w').grid(row=rc, column=2)

rc += 1
ttk.Label(rwgresframe, text='Loss:', width=lw, anchor='w').grid(row=rc, column=0)
dbRWGloss = tk.DoubleVar()
ttk.Label(rwgresframe, textvariable=dbRWGloss, width=lw, anchor='w').grid(row=rc, column=1)
ttk.Label(rwgresframe, text='dB', width=uw, anchor='w').grid(row=rc, column=2)


# alfa, Lwg = LC.rectwaveguideloss(0.072136,0.034036,3.767e7, 2.6e9, 2.079406e9)

""" MENUS """


def plotrwgatten():
    aunit = rwgaunits_combo.get()
    a = dbRWGa.get() * LC.unit2SI[aunit]
    b = dbRWGb.get() * LC.unit2SI[aunit]
    m = intRWGTEm.get()
    n = intRWGTEn.get()
    mur = dbRWGmur.get()
    epsr = dbRWGepsr.get()
    sig = dbRWGcond.get()
    frequnit = rwgfunits_combo.get()
    fr = dbRWGfr.get() * LC.unit2SI[frequnit]
    rwgl = dbRWGlength.get() * LC.unit2SI[rwgLunits_combo.get()]

    fc = LC.rectwaveguide_cutofffreq(a, b, m, n, mur, epsr)
    LC.plotrectwgatten(a, b, sig, fc, rwgType_combo.get())


main_menu = tk.Menu(root)
root.config(menu=main_menu)

plot_menu = tk.Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Plot", menu=plot_menu)
plot_menu.add_command(label="Rectangular waveguide attenuation", command=plotrwgatten)

root.mainloop()
