"""
Purpose of this code is to define an object
that represents the physical properties of one
gamma-emitting radioisotopes
Attributes include: Atomic number, Mass number,
Symbol, Half life [s], Decay constant [1/s], list
of significant gamma emission energies, list of
significant gamma emission branching ratios.
"""


class Isotope(object):
    def __init__(self, symbol, atomic_number, mass_number, half_life,
                 decay_constant, list_sig_g_e, list_sig_g_b_r):
        self.symbol = symbol
        self.atomic_number = atomic_number
        self.mass_number = mass_number
        self.half_life = half_life
        self.decay_constant = decay_constant
        self.list_sig_g_e = list_sig_g_e
        self.list_sig_g_b_r = list_sig_g_b_r

Ac_228_g_e = [338.32, 911.204, 964.766, 968.971]
Ac_228_b_r = [11.27, 25.8, 5, 15.8]
actinium_228 = Isotope("Ac", 89, 228, 22140, 3.13E-05, Ac_228_g_e, Ac_228_b_r)

Bi_214_g_e = [609.31, 1120.29, 1764.49]
Bi_214_b_r = [45.49, 14.91, 15.28]
bismuth_214 = Isotope("Bi", 83, 214, 1194, 5.81E-4, Bi_214_g_e, Bi_214_b_r)

Cs_134_g_e = [604.72]
Cs_134_b_r = [97.62]
caesium_134 = Isotope("Cs", 55, 134, 6.51E+7, 1.065E-8, Cs_134_g_e, Cs_134_b_r)

caesium_137 = Isotope("Cs", 55, 137, 9.483E+8, 7.31E-10, [661.657], [85.1])

Co_60_g_e = [1173.24, 1332.5]
Co_60_b_r = [99.974, 99.986]
cobalt_60 = Isotope("Co", 27, 60, 1.66E+8, 4.17E-9, Co_60_g_e, Co_60_b_r)

lead_210 = Isotope("Pb", 82, 210, 7E9, 9.9E-10, [46.54], [4.3])

lead_212 = Isotope("Pb", 82, 212, 38304, 1.81E-5, [238.63], [43.6])

Pb_214_g_e = [295.22, 351.93]
Pb_214_b_r = [18.5, 35.6]
lead_214 = Isotope("Pb", 82, 214, 1608, 4.31E-4, Pb_214_g_e, Pb_214_b_r)

potassium_40 = Isotope("K", 19, 40, 4.02E+16, 1.72E-17, [1460.83], [11])

Tl_208_g_e = [583.19, 2614.51]
Tl_208_b_r = [30.6, 35.9]
thallium_208 = Isotope("Tl", 81, 208, 183.18, 0.003784, Tl_208_g_e, Tl_208_b_r)

thorium_234 = Isotope("Th", 90, 234, 2.08E6, 3.33E-7, [92.58], [5.58])
