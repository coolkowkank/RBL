========== TUJUAN =============
1. Mencari besar gaya sesaat dari solenoid actuator berdasarkan posisi plunger terhadap solenoid
2. Mencari kombinasi jumlah lilitan pada masing-masing layer solenoid agar didapat actuator yang efisien

 ========= ASUMSI ==============
1. Pada kawat lingkaran berarus, semua titik pada sisi permukaan lingkaran memiliki nilai B/u yang sama
2. Tidak ada faktor temperatur pada hambatan
3. Solenoid dianggap kumpulan kawat lingkaran berarus listrik

 ======= Perhitungan ===========
 
 F(gaya) = perubahan energi solenoid / perubahan posisi plunger (gaya tarik/ dorong)
 
 U(energi) = 1/2 * L * i**2 , L adalah induktansi dan i adalah arus yang mengalir pada kawat
 
 => dU/dx = (i**2)/2 * dL(x)/dx , x adalah posisi plunger terhadap pusat solenoid
 
 Tinjau mendapatkan fungsi L(x),
 
 L(x) = flux_total(x) / i
 
 flux_total(x) = jumlah (B * A) masing2 kawat lingkaran pada solenoid, dengan B adalah medan magnet pada sisi kawat lingkaran
 dan nilai B bergantung pada posisi yang dicari
 
 untuk daerah sisi yang dililit kawat yang seluruhnya udara, permeabilitasnya relatifnya adalah Ur = 1
 untuk daerah sisi yang dililit kawat yang sebagian dipengaruhi bahan plunger, nilai U relatif dengan Ur != 1
 
 maka pada daerah yang dipengaruhi plunger, flux pada permukaan kawat adalah
 
 flux = B ( Ap * Ur + (Ao - Ap) ) , dengan Ap, Ao, dan Ur masing2 adalah luas permukaan plunger, permukaan gap-udara dengan plunger, 
 permeabilitas relatif
 
 sehingga dapat dicari energi yang tersimpan pada solenoid ketika plunger berjarak x dari pusat solenoid
 
 maka dapat ditentukan aproksimasi untu dU(x) / dx
 
 dan kemudian didapat besar gaya F terhadap untuk setiap posisi plunger x pada pusat solenoid
 
 Untuk perhitungan numerik, digunakan komputer dengan bahasa pemrograman Python di [SOLENOID.py](sini)
