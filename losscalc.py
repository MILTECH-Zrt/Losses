import numpy as np
import matplotlib.pyplot as plt

eps0 = 8.8541878188e-12  # vacuum permitivity, F/m
mu0 = 1.25663706127e-6  # vacuum permeability, N/A2
c = 299792458  # lightspeed m/s

"""Waveguide material conductivity in Siemens/m"""
WG_conductivity = {
    "Aluminum": 37.67e6,
    "Brass":    15e6,
    "Brass (30% Zn)":   16.7e6,
    "Brass (5% Zn)":    33.4e6,
    "Bronze":   10e6,
    "Chromium": 5.56e6,
    "Copper":   59.6e6,
    "Copper (annealed)":    58e6,
    "Gold": 41.1e6,
    "Nickel":   11.5e6,
    "Silver":   62.9e6,
    "Zinc": 17.6e6
}

"""Waveguide type and a,b sizes in inch, recommended frequency range"""
WG_types = {
    "WR2300": [23, 11.5, '0.32 to 0.45 GHz'],
    "WR2100": [21, 10.5, '0.35 to 0.50 GHz'],
    "WR1800": [18, 9, '0.45 to 0.63 GHz'],
    "WR1500": [15, 7.5, '0.50 to 0.75 GHz'],
    "WR1150": [11.5, 5.75, '0.63 to 0.97 GHz'],
    "WR975": [9.75, 4.875, '0.75 to 1.15 GHz'],
    "WR770": [7.7, 3.85, '0.97 to 1.45 GHz'],
    "WR650": [6.5, 3.25, '1.15 to 1.72 GHz'],
    "WR510": [5.1, 2.55, '1.45 to 2.20 GHz'],
    "WR430": [4.3, 2.15, '1.72 to 2.60 GHz'],
    "WR340": [3.4, 1.7, '2.20 to 3.30 GHz'],
    "WR284": [2.84, 1.34, '2.60 to 3.95 GHz'],
    "WR229": [2.29, 1.145, '3.30 to 4.90 GHz'],
    "WR187": [1.872, 0.872, '3.95 to 5.85 GHz'],
    "WR159": [1.59, 0.795, '4.90 to 7.05 GHz'],
    "WR137": [1.372, 0.622, '5.85 to 8.20 GHz'],
    "WR112": [1.122, 0.497, '7.05 to 10 GHz'],
    "WR102": [1.02, 0.51, '7.00 to 11 GHz'],
    "WR90": [0.9, 0.4, '8.20 to 12.40 GHz'],
    "WR75": [0.75, 0.375, '10.00 to 15 GHz'],
    "WR62": [0.622, 0.311, '12.40 to 18 GHz'],
    "WR51": [0.51, 0.255, '15.00 to 22 GHz'],
    "WR42": [0.42, 0.17, '18.00 to 26.50 GHz'],
    "WR34": [0.34, 0.17, '22.00 to 33 GHz'],
    "WR28": [0.28, 0.14, '26.50 to 40 GHz'],
    "WR22": [0.224, 0.112, '33.00 to 50 GHz'],
    "WR19": [0.188, 0.094, '40.00 to 60 GHz'],
    "WR15": [0.148, 0.074, '50.00 to 75 GHz'],
    "WR12": [0.122, 0.061, '60 to 90 GHz'],
    "WR10": [0.1, 0.05, '75 to 110 GHz'],
    "WR8": [0.08, 0.04, '90 to 140 GHz'],
    "WR6": [0.065, 0.0325, '110 to 170 GHz'],
    "WR7": [0.065, 0.0325, '110 to 170 GHz'],
    "WR5": [0.051, 0.0255, '140 to 220 GHz'],
    "WR4": [0.043, 0.0215, '172 to 260 GHz'],
    "WR3": [0.034, 0.017, '220 to 330 GHz']
    }

""" Unit conversion: Y[in SI unit] = Y * unit2SI[from unit str]"""
unit2SI = {
        'fm': 1e-15,
        'pm': 1e-12,
        'angstrom': 1e-10,
        'nm': 1e-9,
        'um': 1e-6,
        'mm': 1e-3,
        'cm': 1e-2,
        'dm': 1e-1,
        'km': 1000,
        'm': 1,
        'nmi': 1852,
        'mi': 1609.344,
        'ft': 0.3048,
        'kft': 304.8,
        'inch': 0.0254,
        'W': 1,
        'kW': 1000,
        'MW': 1e6,
        'hp': 735.49875,  # horsepower in W
        'GHz': 1e9,
        'MHz': 1e6,
        'kHz': 1000,
        'Hz': 1,
        'ms': 1e-3,
        's': 1,
        'us': 1e-6,
        'm/s': 1,
        'km/h': 0.2778,
        'mph': 0.4470,
        'mach': 340.29,
        'rpm': 60,
        'deg/s': 360,
        'rad/s': 2 * np.pi,
        'm/s2': 1,
        'g': 0.101972,  # 1/9.80665, standard gravity (see Acceleration - Wiki)
        'ft/s2': 3.28084,
        'J': 1,  # Joule
        'kJ': 1000,
        'MJ': 1000000,
        'kWh': 3600000,
        'BTU': 1055.05585262,
        'eV': 1.602176634e-19,
        'keV': 1.602176634e-16,
        'cal': 4.184,  # calorie
        'kcal': 4184,
        'Pa': 1,  # Pascal
        'kPa': 1000,
        'atm': 101325,
        'bar': 1e5,
        'mbar': 100,
        'hPa': 100,
        'psi': 6894.75729,
        'Torr': 133.322368,
        "c": 299792458,  # lightspeed m/s
        "k": 1.3806504e-23  # Boltzmann J/K
    }

def pow2db(xpow):
    """
    :param xpow: quantity to convert into dB
    :return:  value in dB
    """
    # We want to guarantee that the result is an integer. if y is a negative power of 10.  To do so, we force some
    # rounding of precision by adding 300 - 300.
    ydB = (10 * np.log10(xpow) + 300) - 300
    return ydB


def rectwaveguide_cutofffreq(a, b, m=1, n=0, mur=1, epsr=1):
    """
    Calculates the cut-off frequency of rectangular waveguide
    :param a: waveguide cross-section longer side length, in m
    :param b: waveguide cross-section shorter side length, in m
    :param m: TEmn mode m, integer value of 0,1,2...
    :param n: TEmn mode n, integer value of 0,1,2...
    :param mur: relative permeability
    :param epsr: relative permittivity
    :return: fc: cut-off frequency of rectangular waveguide, in Hz
    """
    kc = np.sqrt((m * np.pi/a)**2 + (n * np.pi/b)**2)  # cutoff wavenumber
    fc = c * kc / (2 * np.pi * np.sqrt(mur * epsr))  # cutoff frequency in Hz
    return fc


def rectwaveguideloss(a, b, sig, f, fc, waveguidelength=1):
    """
    Calculates the specific and total loss of a rectangular waveguide
    :param a: waveguide cross-section longer side length, in m
    :param b: waveguide cross-section shorter side length, in m
    :param sig: sigma conductivity of waveguide inner wall material, in Siemens/m
    :param f: wave frequency, in Hz
    :param fc: waveguide cut-off frequency, in Hz
    :param waveguidelength: length of the waveguide, in m
    :return:
    alfa - loss per meter, in dB/m
    Lwg - loss on waveguide, in dB
    Ref.: H.Meikle, Modern Radar Systems (2nd.ed.) p.87, eq.(4.4)
    """

    fr = f/fc  # frequency ratio
    # attenuation of waveguide in dB/m:
    if fr**2 >= 1:
        alfa = np.sqrt((np.pi/(2*sig)) * np.sqrt(eps0/mu0)) * (1/a**1.5) * ((2 * fr**-0.5 + (a/b)*(fr**1.5)) /
                                                                        np.sqrt(fr**2 - 1)) * 20 * np.log10(np.e)

        # total loss of waveguide:
        Lwg = waveguidelength * alfa
    else:
        alfa = np.nan
        Lwg = np.nan
    return alfa, Lwg


def mismatchloss(vswr):
    """
    :param vswr: VSWR value, e.g.: 1.2
    :return: mismatch loss in dB, reflection coefficient
    """
    if vswr > 1:
        reflcoeff = (vswr - 1)/(vswr + 1)
    else:
        reflcoeff = (1 - vswr) / (vswr + 1)

    Lmismatch = (vswr + 1)**2 / (4 * vswr)
    LmismatchdB = pow2db(Lmismatch)
    fractionOfPowerReclected = reflcoeff**2
    return LmismatchdB, reflcoeff, fractionOfPowerReclected


def polarizationloss(TxP, RxP):

    if TxP == "Horizontal":
        if RxP == "Vertical":
            Lpol = 10
        elif RxP == "Horizontal":
            Lpol = 0
        else:  # RHC or LHC
            Lpol = 3
    elif TxP == "Vertical":
        if RxP == "Vertical":
            Lpol = 0
        elif RxP == "Horizontal":
            Lpol = 10
        else:  # RHC or LHC
            Lpol = 3
    elif TxP == "RHC":
        if RxP == "RHC":
            Lpol = 3
        elif RxP == "LHC":
            Lpol = 0
        else:  # Horizontal or Vertical
            Lpol = 3
    elif TxP == "LHC":
        if RxP == "RHC":
            Lpol = 0
        elif RxP == "LHC":
            Lpol = 3
        else:  # Horizontal or Vertical
            Lpol = 3
    else:
        Lpol = None

    return Lpol

def plotrectwgatten(a, b, sig, fc, WGname):
    """ Plot rectangular waveguide attenuation vs. frequency"""
    fr = np.arange(1, 10.1, 0.1)*1e9
    fig = plt.figure()
    for m in list(WG_conductivity.keys()):
        attr = []
        sig = WG_conductivity[m]
        for f in fr:
            att, L = rectwaveguideloss(a, b, sig, f, fc)
            attr.append(att)
        fig = plt.plot(fr/1e9, attr, label=WGname + ", " + m)

    plt.xlabel('Frequency [GHz]')
    plt.ylabel('Attenuation [dB/m]')
    plt.title("Rect. Waveguide Attenuation")
    plt.legend(draggable=True)
    plt.show()

