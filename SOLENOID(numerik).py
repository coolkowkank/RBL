# ********************************** DESKRIPSI SINGKAT *********************
# ========== TUJUAN =============
# 1. Mencari besar gaya sesaat dari solenoid actuator berdasarkan posisi plunger terhadap solenoid
# 2. Mencari kombinasi jumlah lilitan pada masing-masing layer solenoid agar didapat actuator yang efisien
#
# ========= ASUMSI ==============
# 1. Permeabilitas relatif plunger (magnet dan kawannya) sudah diketahui
# 2. Pada kawat lingkaran berarus, semua titik pada sisi permukaan lingkaran memiliki nilai B/u yang sama
# 3. Tidak ada faktor temperatur pada hambatan
# 4. Solenoid dianggap kumpulan kawat lingkaran berarus listrik
# *************************************** PROGRAM **********************************
# ========== MODULES =============
import matplotlib.pyplot as plt
import numpy as np
from math import *

#============ KONSTANTA ============
Up = 1.05 # permeabilitas neodimium (CONTOH aja)
n = 1
V = 9*n #volt baterai
r_plunger = 1.5 * 10**-2 # jari jari plunger (m)
Ap = pi * r_plunger**2 # luas penampang plunger (m^2)
r_kawat = 0.5/2 * 10**-3 # (m)
resistivity = 1.68 * 10**-8 # ohm m
Ro = 1.6 * 10**-2 # m
R = [Ro + 2 * i * r_kawat for i in range(20)] # jari-jari solenoid
Uo = 4 * pi * 10**-7 # nyu nol
A_kawat = pi * r_kawat**2 # luas penampang kawat
R_batt = n # asumsi hambatan dalam baterai 1 ohm/baterai

# ============= FUNGSI ===========
# Kamus
# no_layer = 0, 1, 2, 3, 4, ....
# N = array kombinasi
N = [0 for i in range(10)] # kombinasi : N[a] = b , berarti pada layer ke-a+1 ada b lilitan

def run(a,b) : # memvariasikan kombinasi dengan maksimal lilitan b
    a[0] += 1
    try :
        while a[0] > b :
            for i in range(len(a)) :
                if a[i] > b :
                    a[0 : i + 2] = [a[i+1] + 1 for j in range(len(a[0 : i + 2]))]                 
    except :
        print("indeks berlebih")
    return a

def jumlah_kombinasi(x,y) : # mencari jumlah kombinasi maksimum jika lilitan maksimum per layer adalah x, dan jumlah layer maksimum adalah y
    a = [0 for i in range(y)]
    y = 0
    while True :
        a[0] += 1
        try :
            while a[0] > x :
                for i in range(len(a)) :
                    if a[i] > x :
                        a[0 : i + 2] = [a[i+1] + 1 for j in range(len(a[0 : i + 2]))]                 
        except :
            return y
            break
        y += 1   
        
def kombinasi(indeks_yang_dicari, jumlah_layer, maks_lilitan) :
    N = [0 for i in range(jumlah_layer)]
    n = jumlah_kombinasi(maks_lilitan, jumlah_layer)
    for i in range(n) :
        run(N,maks_lilitan)
        if i == indeks_yang_dicari :
            print(N)
            break

def l(N): # panjang kawat
    global R
    y = 0
    for i in range(len(N)):
        if N[i] == 0 :
            break
        y += R[i] * N[i]
    return 2 * pi * y

def R_hambatan(N): # hambatan
    global R_batt
    global resistivity, A_kawat
    y = resistivity * l(N) / A_kawat
    return y + R_batt

def l_sol(N,no_layer): #panjang solenoid pada layer tertentu
    y = N[no_layer] * r_kawat * 2
    return y

def A_sol(no_layer): # luas solenoid pada layer tertentu
    global R
    y = pi * R[no_layer]**2
    return y

def I_arus(N,t = 'tunak') : # arus listrik
    global V
    if t == "tunak" :
        return V/R_hambatan(N)
    else :
        return V/R_hambatan(N) * (1 - np.e**(-t*R(N)/L(N)))
    
def jumlah_luas(N, z) : # jumlah lilitan kawat pada jarak z (dijumlahkan vertikal)
    global r_kawat, R
    y = 0 # luas total
    n = 0 # banyak lilitan
    d = 2 * r_kawat
    if z/d - z//d <=0.2 : #kasus ganjil
        indeks = int((z/d)-0.1) #indeks lilitan
        for i in range(len(N)):
            if N[i] == 0 :
                break
            if ( N[i]%2 != 0 and indeks+1<=N[i]//2 ):
                y += R[i]**2
                n += 1
    else : #kasus genap
        indeks = (z-r_kawat)/d #indeks lilitan
        for i in range(len(N)):
            if N[i] == 0 :
                break
            if ( N[i]%2 == 0 and indeks+1<=N[i]/2 ):
                y += R[i]**2
                n += 1
    return pi * y , n #jumlah_luas(N,z)[0] = jumlah luas, jumlah_luas(N,z)[1] = banyak lilitan
    
# def jumlah_luas(N,n): #jumlah luas secara vertikal dengan n sebagai jumlah lilitan
#     global r_kawat,Ro
#     r = r_kawat
#     n = jumlah_lilitan_vertikal(N, z) - 1
#     if n < 0 :
#         return 0
#     # kemudian dengan menggunakan penjumlahan bilangan natural berpangkat
#     return pi*(Ro**2 + 4/3 * n**3 * r**2 + n**2 * (2*r*Ro + r**2) + n(Ro**2 + 2*r*Ro + 2/3 * r**2))
    
def jarak_pusat(N, no_lilitan, no_layer) : # jarak lilitan ke i dari pusat, no_lilitan : 0, 1, 2, 3, 4 ....
    if N[no_layer] % 2 == 0 : # kasus genap
        posisi_yang_dicari = (no_lilitan + 1 -0.5) * 2 * pi * r_kawat
    elif N[no_layer] % 2 != 0 : #kasus ganjil
        posisi_yang_dicari = no_lilitan * 2 * pi * r_kawat
    return posisi_yang_dicari

def B(N,z,no_layer,t = 'tunak') : # medan pada jarak z dari kawat lingkaran
    # no_layer menentukan jari2
    global Uo, R 
    return Uo * I_arus(N,t) * R[no_layer]**2 / (2 * (R[no_layer]**2 + z**2)**(3/2))

def B_total(N, z) : # Nilai B total pada jarak z dari pusat, dengan konfigurasi N
    y = 0
    if z < 0 :
        return B_total(N,-z)
    
    jarak_dicari = z

    for i in range(len(N)) : # pada layer i+1
        if N[i] == 0 : #berhenti jika tidak ada lilitan pada layer selanjutnya
            break
        for j in range(N[i]//2) : # pada lilitan ke-j
            jarak_lilitan_ke_pusat = jarak_pusat(N, j, i) # jarak lilitan ke-j dari pusat
            z = jarak_dicari - jarak_lilitan_ke_pusat #untuk posisi B (yang dicari) dan lilitan j di bagian yang sama relatif terhadap pusat
            z_sebelah = jarak_dicari + jarak_lilitan_ke_pusat # untuk posisi B berbeda
            y += B(N,z, i) + B(N,z_sebelah, i) # B akibat lilitan pada jarak z dan z_sebelah
        if N[i] % 2 != 0 : #untuk kasus ganjil, pada posisi tengah terhitung dua kali
            y -= B(N, jarak_dicari ,i)
    return y

# def B_total(N, z) : # Nilai B total pada jarak z dari pusat, dengan konfigurasi N
#     y = 0
#     for i in range(len(N)) :
#         if N[i] == 0 :
#             break
#         for j in range(N[i]) :
#             if N[i]%2 != 0 : #kasus ganjil
#                 xo = -(N[i]//2 *2 * r_kawat)
#             elif N[i]%2 == 0 : #kasus genap
#                 xo  = -((N[i]/2 -0.5) *2 *r_kawat)
#             x = xo + j*2*r_kawat
#             selisih_jarak = x - z
#             y += B(N, selisih_jarak, i)
#     return y

# def flux(N,z,no_layer,x) : # flux(dengan luas A) di posisi z, pada kombinasi N dan plunger di x 
#     # note : z dihitung berdasarkan jarak lilitan dari pusat
#     global Ap, R, Up
#     Ao = pi * R[no_layer]**2
#     if z < x :
#         return B_total(N,z) * Ao
#     elif z >= x :
#         return B_total(N,z) * (Ap * (Up-1) +Ao)

# def flux_total(N,x) : #flux total pada konfigurasi N, ketika plunger berjarak x dari pusat
#     y = 0
#     for i in range(len(N)) : # kalkulasi pada layer i, sebanyak jumlah layer
#         if N[i] == 0 :
#             break
#         for j in range(N[i]) : # kalkulasi pada layer i, sebanyak jumlah lilitan
#             if N[i]%2 != 0 : #kasus ganjil
#                 Zo = -(N[i]//2 *2 * r_kawat)
#             elif N[i]%2 == 0 : #kasus genap
#                 Zo  = -((N[i]/2 -0.5) *2 *r_kawat)
#             z = Zo + j * 2 * r_kawat 
#             y += flux(N,z,i,x)
#     return y

def flux(N,z,x) : # flux pada posisi z kanan dan kiri
    # note : z dihitung berdasarkan jarak lilitan dari pusat (menghitung setengah bagian solenoid)
    #        flux yang dihitung total terhadap vertikal
    global Ap, R, Up
    luas_total = jumlah_luas(N,z)[0]
    n_lilitan = jumlah_luas(N,z)[1]
    kiri = luas_total #bagian kiri
    kanan = 0
    if z > x :
        kanan = ( luas_total + (Up*Ap - Ap) * n_lilitan ) #bagian kanan
    else :
        kanan = kiri # jika posisi plunger masih jauh dari pusat
    return B_total(N,z) * (kiri + kanan)

def flux_total(N,x) : #flux total pada konfigurasi N, ketika plunger berjarak x dari pusat
    global r_kawat
    y = 0
    ujung = l_sol(N,0)/2
    n = int(ujung / r_kawat)
    for i in range(n) :
        z = i*r_kawat
        y += flux(N,z,x)
    return y

def L(N, x) : #induktansi saat plunger berjarak x dari pusat
    return flux_total(N,x) / I_arus(N)

def U(N,x) :
    return (L(N,x) * I_arus(N)**2)/2

def F(N,x,dx = r_kawat) :
    y = U(N,x) - U(N, x+dx)
    return y/dx
