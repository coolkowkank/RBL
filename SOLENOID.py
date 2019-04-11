# ========== TUJUAN =============
# 1. Mencari besar gaya sesaat dari solenoid actuator berdasarkan posisi plunger terhadap solenoid
# 2. Mencari kombinasi jumlah lilitan pada masing-masing layer solenoid agar didapat actuator yang efisien

# ========== MODULES =============
import matplotlib.pyplot as plt
import numpy as np
from sympy import *

#============ KONSTANTA ============
Up = 1.32 * 10**-6 # permeabilitas neodimium (CONTOH aja)
V = 9 #volt baterai
r_plunger = 1.5 * 10**-2 # jari jari plunger
Ap = pi * r_plunger**2 # luas penampang plunger
r_kawat = 0.5/2 * 10**-3 # m
resistivity = 1.68 * 10**-8 # ohm m
Ro = 1.6 * 10**-2 # m
R = [Ro + i * r_kawat for i in range(20)] # jari-jari solenoid
Uo = 4 * pi * 10**-7 # nyu nol
A_kawat = pi * r_kawat**2 # luas penampang kawat

# ============= FUNGSI ===========
# Kamus
# N = array kombinasi
N = [0 for i in range(800)] # kombinasi : N[a] = b , berarti pada layer ke-a+1 ada b lilitan

def run(a) : # memvariasikan kombinasi
    a[0] += 1
    try :
        while a[0] > 5 :
            for i in range(len(a)) :
                if a[i] > 5 :
                    a[0 : i + 2] = [a[i+1] + 1 for j in range(len(a[0 : i + 2]))]                 
    except :
        print("selesai")
        return;
    return a

def l(N): # panjang kawat
    global R
    y = 0
    for i in range(len(N)):
        y += R[i] * N[i]
    return 2 * pi * y

def R(N): # hambatan
    global resistivity, A_kawat
    y = resistivity * l(N) / A_kawat
    return y

def l_sol(N,no_layer): #panjang solenoid pada layer tertentu
    y = N[no_layer - 1] * r_kawat * 2
    return y

def A_sol(no_layer): # luas solenoid pada layer tertentu
    y = pi * R[no_layer - 1 ]**2
    return y

def I_arus(N,t) : # arus listrik
    global V
    if t == "tunak" :
        return V/R(N)
    else :
        return V/R(N) * (1 - np.e**(-t*R(N)/L(N)))

def B(N,z,no_layer,t = 'tunak') : # medan pada jarak z dari kawat lingkaran
    # no layer menentukan jari2
    global Uo, R 
    denominator = 2 * (R[no_layer]**2 + z**2)**(3/2)
    y = Uo * I_arus(N,t) * R[no_layer]**2 / (denominator)
    return y

def jarak_pusat(N, no_lilitan, no_layer) : # jarak lilitan ke i dari pusat, no_lilitan : 0, 1, 2, 3, 4 ....
    if N[no_layer] % 2 == 0 : # kasus genap
        posisi_yang_dicari = (no_lilitan + 1 -0.5) * 2 * pi * r_kawat
    elif N[no_layer] % 2 != 0 : #kasus ganjil
        posisi_yang_dicari = no_lilitan * 2 * pi * r_kawat
    return posisi_yang_dicari

def B_total(N, no_lilitan) : # Nilai B pada no_lilitan ( posisi lilitan dari pusat ) dengan konfigurasi N
    y = 0
    
    jarak_dicari = jarak_pusat(N,no_lilitan,0)

    for i in range(len(N)) : # pada layer i+1
        for j in range(N[i]//2) : # pada lilitan ke-j
            jarak_lilitan_ke_pusat = jarak_pusat(N, j, i) # jarak lilitan ke-j dari pusat
            z = jarak_dicari - jarak_lilitan_ke_pusat #untuk posisi B (yang dicari) dan lilitan j di bagian yang sama relatif terhadap pusat
            z_sebelah = jarak_dicari + jarak_pusat # untuk posisi B berbeda
            y += B(N,z, i)
            y += B(N,z_sebelah, i)
        if N[i] % 2 != 0 : #untuk kasus ganjil, pada posisi tengah terhitung dua kali
            y -= B(N, jarak_dicari ,i)
    return y

def L(N, x) : #induktansi saat plunger berjarak x dari pusat
    global Ro, Ap
    Ao = pi * Ro**2

# .
# .
# .
# .
# ...... MASIH DALAM PROGRESS
    
