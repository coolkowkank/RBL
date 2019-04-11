# TUJUAN
1. Mencari besar gaya sesaat dari solenoid actuator berdasarkan posisi plunger terhadap solenoid
2. Mencari kombinasi jumlah lilitan pada masing-masing layer solenoid agar didapat actuator yang efisien

# ASUMSI
1. Permeabilitas relatif plunger (magnet dan kawannya) sudah diketahui
2. Pada kawat lingkaran berarus, semua titik pada sisi permukaan lingkaran memiliki nilai B/u yang sama
3. Tidak ada faktor temperatur pada hambatan
4. Solenoid dianggap kumpulan kawat lingkaran berarus listrik

# Metode Perhitungan
 
 Gaya = perubahan energi solenoid / perubahan posisi plunger = dU(x)/dx
 
 ```python
 U(energi) = 1/2 * L * i**2 , L adalah induktansi dan i adalah arus yang mengalir pada kawat
 
 => dU/dx = (i**2)/2 * dL(x)/dx , x adalah posisi plunger terhadap pusat solenoid
 ```
 Tinjau suatu fungsi L(x),
 ```python
 L(x) = flux_total(x) / i
 ```
 flux_total(x) = jumlah (B * A) masing2 kawat lingkaran pada solenoid, dengan B adalah medan magnet pada sisi kawat lingkaran
 dan nilai B bergantung pada posisi yang dicari
 
 ``` python
 flux_total(x) = jumlah masing2 flux untuk tiap kawat lingkaran
 ```
 
 untuk daerah sisi yang dililit kawat yang seluruhnya udara, permeabilitasnya relatifnya adalah Ur = 1
 untuk daerah sisi yang dililit kawat yang sebagian dipengaruhi bahan plunger, nilai U relatif dengan Ur != 1
 
 maka pada daerah yang dipengaruhi plunger, flux pada permukaan kawat adalah
 
 ```python
 flux = B * ( Ap * Ur + (Ao - Ap) )
 ```
 dengan Ap, Ao, dan Ur masing2 adalah luas permukaan plunger, permukaan gap-udara dengan plunger, 
 permeabilitas relatif
 
 sehingga dapat dicari energi yang tersimpan pada solenoid ketika plunger berjarak x dari pusat solenoid
 
 maka dapat ditentukan aproksimasi untuk dU(x) / dx
 
 dan kemudian didapat besar gaya F terhadap untuk setiap posisi plunger x pada pusat solenoid
 
 Untuk perhitungan numerik, digunakan komputer dengan bahasa pemrograman Python di [SOLENOID.py](https://github.com/coolkowkank/RBL/blob/master/SOLENOID.py)
 
 # Sistem Kombinasi
Jadi gini, 
```python
N = [0 for i in range(800)] # kombinasi : N[a] = b , berarti pada layer ke-a+1 ada b lilitan
```
Nomor index dari N menunjukkan nomor layer.

No Layer = 0, 1, 2, 3 ,4 , ..... 

Nilai N pada index ke-i menunjukkan jumlah lilitan pada index ke-i

```python
def run(a) : # memvariasikan kombinasi
    a[0] += 1
    try :
        while a[0] > 1000 :
            for i in range(len(a)) :
                if a[i] > 1000 :
                    a[0 : i + 2] = [a[i+1] + 1 for j in range(len(a[0 : i + 2]))]      

```
Fungsi tersebut berfungsi untuk mengubah kombinasi array N.

Contoh :
```python
N = [1,2,3,0,0,0,0, ......] # Kombinasi awal
run(N)
print(N)
```
Output :
```python
[2,2,3,0,0,0,0, ........] # perhatikan nilai index ke-0
```
Notice, nilai maksimal pada masing-masing indeks adalah 1000.
jika ada indeks yang bernilai > 1000, maka indeks setelahnya ditambahkan 1 dan indeks yang >1000 tereduksi sesuai nilai indeks berikutnya.

contoh :
```python
N = [1000,5,3,0,0,0,0, ..........] # Kombinasi awal
run(N)
print(N)
```
output :
```python
[6,6,3,0,0,0,0, .........] # perhatikan nilai indeks ke-0
```
nilai indeks ke-0 tidak menjadi 1, karena lilitan ke-n tidak mungkin < lilitan ke-(n+1)

