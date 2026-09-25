import streamlit as st

import random



# ==========================================

# 1. ALGORITMA CAESAR CIPHER 

# ==========================================

def jalankan_caesar(pesan, angka_geser, is_enkripsi=True):

    teks_akhir = ""

    catatan_proses = []

    

    # Menentukan arah geser, jika dekripsi maka nilainya dibuat negatif

    nilai_geser = angka_geser % 26 if is_enkripsi else -(angka_geser % 26)

    

    for huruf in pesan:

        # Mengecek apakah karakter adalah alfabet

        if huruf.isalpha():

            # 65 adalah ASCII untuk 'A', 97 untuk 'a'

            batas_ascii = 65 if huruf.isupper() else 97

            

            # Perhitungan posisi huruf baru

            posisi_baru = (ord(huruf) - batas_ascii + nilai_geser) % 26

            huruf_baru = chr(posisi_baru + batas_ascii)

            teks_akhir += huruf_baru

            

            # Mencatat riwayat untuk ditampilkan di web

            catatan_proses.append(f"Huruf '{huruf}' digeser menjadi '{huruf_baru}'")

        else:

            teks_akhir += huruf

            

    return teks_akhir, catatan_proses



# ==========================================

# 2. ALGORITMA VIGENERE CIPHER 

# ==========================================

def jalankan_vigenere(pesan, kata_kunci, is_enkripsi=True):

    teks_akhir = ""

    catatan_proses = []

    kata_kunci = kata_kunci.upper()

    indeks_kunci = 0

    panjang_kunci = len(kata_kunci)

    

    for huruf in pesan:

        if huruf.isalpha():

            # Mengambil nilai pergeseran dari huruf kunci saat ini

            penggeser = ord(kata_kunci[indeks_kunci % panjang_kunci]) - 65

            

            # Balik arah geser jika sedang mode dekripsi

            if not is_enkripsi:

                penggeser = -penggeser

                

            batas_ascii = 65 if huruf.isupper() else 97

            

            # Kalkulasi abjad baru

            huruf_baru = chr((ord(huruf) - batas_ascii + penggeser) % 26 + batas_ascii)

            teks_akhir += huruf_baru

            

            catatan_proses.append(f"'{huruf}' disandikan dengan '{kata_kunci[indeks_kunci % panjang_kunci]}' -> '{huruf_baru}'")

            indeks_kunci += 1 # Pindah ke huruf kunci berikutnya

        else:

            teks_akhir += huruf

            

    return teks_akhir, catatan_proses



# ==========================================

# 3. ALGORITMA RAIL FENCE 

# ==========================================

def enkripsi_jalur_zigzag(pesan, jumlah_baris):

    if jumlah_baris <= 1: return pesan

    # Membuat wadah (list of strings) untuk setiap baris

    wadah_baris = ["" for _ in range(jumlah_baris)]

    baris_sekarang = 0

    arah_turun = False

    

    for karakter in pesan:

        wadah_baris[baris_sekarang] += karakter

        # Balik arah jika mentok di atas atau bawah

        if baris_sekarang == 0 or baris_sekarang == jumlah_baris - 1:

            arah_turun = not arah_turun

        baris_sekarang += 1 if arah_turun else -1

        

    return "".join(wadah_baris)



def dekripsi_jalur_zigzag(pesan_rahasia, jumlah_baris):

    if jumlah_baris <= 1: return pesan_rahasia

    

    # Membangun pola bintang (*) sebagai cetakan

    cetakan = [["" for _ in range(len(pesan_rahasia))] for _ in range(jumlah_baris)]

    baris_sekarang, kolom_sekarang = 0, 0

    arah_turun = False

    

    for _ in range(len(pesan_rahasia)):

        if baris_sekarang == 0 or baris_sekarang == jumlah_baris - 1:

            arah_turun = not arah_turun

        cetakan[baris_sekarang][kolom_sekarang] = "*"

        kolom_sekarang += 1

        baris_sekarang += 1 if arah_turun else -1

        

    # Mengisi cetakan bintang dengan huruf dari pesan rahasia

    penunjuk_huruf = 0

    for b in range(jumlah_baris):

        for k in range(len(pesan_rahasia)):

            if cetakan[b][k] == "*" and penunjuk_huruf < len(pesan_rahasia):

                cetakan[b][k] = pesan_rahasia[penunjuk_huruf]

                penunjuk_huruf += 1

                

    # Membaca ulang isi cetakan secara zigzag

    teks_asli = []

    baris_sekarang, kolom_sekarang = 0, 0

    arah_turun = False

    for _ in range(len(pesan_rahasia)):

        if baris_sekarang == 0 or baris_sekarang == jumlah_baris - 1:

            arah_turun = not arah_turun

        teks_asli.append(cetakan[baris_sekarang][kolom_sekarang])

        kolom_sekarang += 1

        baris_sekarang += 1 if arah_turun else -1

        

    return "".join(teks_asli)



# ==========================================

# 4. ALGORITMA RC4 

# ==========================================

def hitung_rc4(data_teks, kata_kunci_str):

    # Tahap Inisialisasi Kunci (KSA)

    kotak_s = [angka for angka in range(256)]

    indeks_j = 0

    # Mengubah string kunci menjadi deretan angka ASCII

    kunci_ascii = [ord(huruf) for huruf in kata_kunci_str]

    panjang_k = len(kunci_ascii)

    

    # Pengacakan kotak S

    for indeks_i in range(256):

        indeks_j = (indeks_j + kotak_s[indeks_i] + kunci_ascii[indeks_i % panjang_k]) % 256

        # Menukar elemen array

        kotak_s[indeks_i], kotak_s[indeks_j] = kotak_s[indeks_j], kotak_s[indeks_i]

        

    # Tahap Pembuatan Cipher (PRGA)

    pointer_i = pointer_j = 0

    teks_akhir = ""

    catatan_proses = []

    

    for karakter in data_teks:

        pointer_i = (pointer_i + 1) % 256

        pointer_j = (pointer_j + kotak_s[pointer_i]) % 256

        kotak_s[pointer_i], kotak_s[pointer_j] = kotak_s[pointer_j], kotak_s[pointer_i]

        

        # Mendapatkan nilai keystream acak

        aliran_kunci = kotak_s[(kotak_s[pointer_i] + kotak_s[pointer_j]) % 256]

        

        # Meng-XOR-kan nilai ASCII karakter asli dengan aliran kunci

        karakter_baru = chr(ord(karakter) ^ aliran_kunci)

        teks_akhir += karakter_baru

        catatan_proses.append(f"Teks Asli ({ord(karakter)}) XOR Keystream ({aliran_kunci}) = Sandi ({ord(karakter_baru)})")

        

    return teks_akhir, catatan_proses



# ==========================================

# 5. ALGORITMA VERNAM XOR (MODERN SEDERHANA)

def hitung_vernam(data_teks, kata_kunci_str):
    if not kata_kunci_str:
        return "", []

    teks_akhir = ""
    catatan_proses = []

    for indeks, karakter in enumerate(data_teks):
        kunci = kata_kunci_str[indeks % len(kata_kunci_str)]
        nilai_teks = ord(karakter)
        nilai_kunci = ord(kunci)
        nilai_xor = nilai_teks ^ nilai_kunci
        teks_akhir += chr(nilai_xor)
        catatan_proses.append(
            f"ASCII {nilai_teks} XOR ASCII {nilai_kunci} = {nilai_xor}"
        )

    return teks_akhir, catatan_proses


def vernam_ke_hex(teks):
    return "".join(format(ord(c), "02x") for c in teks)


# 5. ALGORITMA RSA 

# ==========================================

def hitung_fpb(bil1, bil2):

    while bil2 != 0:

        bil1, bil2 = bil2, bil1 % bil2

    return bil1



def hitung_invers_modulo(eksponen, nilai_phi):

    # Menggunakan algoritma Euclidean yang diperluas

    r_lama, r_baru = eksponen, nilai_phi

    s_lama, s_baru = 1, 0

    while r_baru != 0:

        hasil_bagi = r_lama // r_baru

        r_lama, r_baru = r_baru, r_lama - hasil_bagi * r_baru

        s_lama, s_baru = s_baru, s_lama - hasil_bagi * s_baru

    return s_lama % nilai_phi



def cek_bilangan_prima(angka):

    if angka <= 1: return False

    for pembagi in range(2, int(angka ** 0.5) + 1):

        if angka % pembagi == 0: return False

    return True



def ciptakan_pasangan_kunci_rsa():

    # Mencari dua bilangan prima acak p dan q

    prima_p = random.choice([x for x in range(11, 50) if cek_bilangan_prima(x)])

    prima_q = random.choice([x for x in range(51, 99) if cek_bilangan_prima(x)])

    

    modulus_n = prima_p * prima_q

    euler_phi = (prima_p - 1) * (prima_q - 1)

    

    # Memilih eksponen publik (e) yang relatif prima dengan phi

    kunci_publik = 3

    while hitung_fpb(kunci_publik, euler_phi) != 1:

        kunci_publik += 2

        

    kunci_privat = hitung_invers_modulo(kunci_publik, euler_phi)

    return kunci_publik, kunci_privat, modulus_n, prima_p, prima_q



def enkripsi_dengan_rsa(pesan_asli, pub_key, mod_n):

    blok_sandi = []

    catatan_proses = []

    for huruf in pesan_asli:

        nilai_ascii = ord(huruf)

        angka_sandi = pow(nilai_ascii, pub_key, mod_n) # Rumus: (m^e) mod n

        blok_sandi.append(str(angka_sandi))

        catatan_proses.append(f"Huruf '{huruf}' -> ASCII {nilai_ascii}^{pub_key} mod {mod_n} -> {angka_sandi}")

    return " ".join(blok_sandi), catatan_proses



def dekripsi_dengan_rsa(pesan_sandi, priv_key, mod_n):

    teks_asli = ""

    catatan_proses = []

    daftar_angka = pesan_sandi.split()

    

    for angka_str in daftar_angka:

        try:

            angka_sandi = int(angka_str)

            angka_asli = pow(angka_sandi, priv_key, mod_n) # Rumus: (c^d) mod n

            teks_asli += chr(angka_asli)

            catatan_proses.append(f"Sandi {angka_sandi} -> {angka_sandi}^{priv_key} mod {mod_n} -> ASCII {angka_asli} ('{chr(angka_asli)}')")

        except:

            teks_asli += "?"

    return teks_asli, catatan_proses



# ==========================================

# ANTARMUKA PENGGUNA STREAMLIT

# ==========================================

st.set_page_config(page_title="Tugas Kripto", layout="wide", page_icon="🛡️")



st.sidebar.header("📁 Daftar Menu Kriptografi")

pilihan_menu = st.sidebar.selectbox(

    "Silakan pilih fitur di bawah ini:",

    ["Profil Kelompok", "Algoritma 1: Caesar", "Algoritma 2: Vigenere", "Algoritma 3: RC4", "Algoritma 4: Vernam XOR", "Super Enkripsi (Kombinasi)"]

)

st.sidebar.divider()

st.sidebar.caption("Sistem Keamanan Data - IF D")



if pilihan_menu == "Profil Kelompok":

    st.title("🛡️ Aplikasi Keamanan Data Kriptografi")

    st.write("Dibuat khusus untuk memenuhi evaluasi Tugas 4 Mata Kuliah Kriptografi.")

    st.info("Dosen Pengampu: Bagus Muhammad Akbar, S.T., M.T.")

    

    st.markdown("### Daftar Anggota (Kelompok)")

    st.markdown("""

    - **Afiq Fathurrahman** (123240010)

    - **Radja Azhara I.K.** (123240012)

    - **Muhammad Afif P.N.** (123240031)

    - **Munadhil Mutawakkil** (123240145)

    """)



elif pilihan_menu == "Algoritma 1: Caesar":

    st.header("Metode Klasik: Caesar Cipher")

    mode_operasi = st.radio("Tentukan Tindakan:", ("Enkripsi Teks", "Dekripsi Teks"), horizontal=True)

    

    panel_kiri, panel_kanan = st.columns(2)

    with panel_kiri:

        masukan_teks = st.text_area("Ketik teks di sini:")

        angka_kunci = st.number_input("Besaran geseran (0-25):", min_value=0, max_value=25, value=3)

        tombol_proses = st.button("Mulai Proses")

        

    if tombol_proses and masukan_teks:

        status_enkripsi = True if mode_operasi == "Enkripsi Teks" else False

        hasil_teks, daftar_log = jalankan_caesar(masukan_teks, angka_kunci, status_enkripsi)

        

        with panel_kanan:

            tab_hasil, tab_log = st.tabs(["Teks Hasil", "Log Perhitungan"])

            with tab_hasil:

                st.code(hasil_teks)

            with tab_log:

                for log in daftar_log: st.text(log)



elif pilihan_menu == "Algoritma 2: Vigenere":

    st.header("Metode Klasik: Vigenere Cipher")

    mode_operasi = st.radio("Tentukan Tindakan:", ("Enkripsi Teks", "Dekripsi Teks"), horizontal=True)

    

    panel_kiri, panel_kanan = st.columns(2)

    with panel_kiri:

        masukan_teks = st.text_area("Ketik teks di sini:")

        kata_kunci = st.text_input("Gunakan kata kunci (huruf):", value="KUNCI")

        tombol_proses = st.button("Mulai Proses")

        

    if tombol_proses and masukan_teks:

        kunci_valid = ''.join([huruf for huruf in kata_kunci if huruf.isalpha()])

        if not kunci_valid:

            st.error("Gagal! Kata kunci wajib berisi huruf abjad.")

        else:

            status_enkripsi = True if mode_operasi == "Enkripsi Teks" else False

            hasil_teks, daftar_log = jalankan_vigenere(masukan_teks, kunci_valid, status_enkripsi)

            

            with panel_kanan:

                tab_hasil, tab_log = st.tabs(["Teks Hasil", "Log Perhitungan"])

                with tab_hasil:

                    st.code(hasil_teks)

                with tab_log:

                    for log in daftar_log: st.text(log)



elif pilihan_menu == "Algoritma 3: RC4":

    st.header("Metode Modern: Stream Cipher RC4")

    mode_operasi = st.radio("Tentukan Tindakan:", ("Enkripsi Teks", "Dekripsi Teks"), horizontal=True)

    

    panel_kiri, panel_kanan = st.columns(2)

    with panel_kiri:

        masukan_teks = st.text_area("Ketik teks di sini (Wajib Heksadesimal untuk Dekripsi):")

        kata_kunci = st.text_input("Kata Kunci (Bebas):")

        tombol_proses = st.button("Mulai Proses")

        

    if tombol_proses and masukan_teks and kata_kunci:

        if mode_operasi == "Enkripsi Teks":

            hasil_proses, daftar_log = hitung_rc4(masukan_teks, kata_kunci)

            # Konversi hasil ASCII berantakan ke Hex

            hasil_visual = "".join(format(ord(c), "02x") for c in hasil_proses)

        else:

            try:

                # Konversi Hex kembali ke ASCII

                teks_awal = "".join(chr(int(masukan_teks[i:i+2], 16)) for i in range(0, len(masukan_teks), 2))

                hasil_visual, daftar_log = hitung_rc4(teks_awal, kata_kunci)

            except:

                st.error("Data dekripsi tidak sesuai format heksadesimal!")

                hasil_visual = None

                

        if hasil_visual:

            with panel_kanan:

                tab_hasil, tab_log = st.tabs(["Teks Hasil", "Log Proses (XOR)"])

                with tab_hasil:

                    st.code(hasil_visual)

                with tab_log:

                    for log in daftar_log: st.text(log)



elif pilihan_menu == "Algoritma 4: Vernam XOR":

    st.header("Metode Modern: Vernam Cipher (XOR)")

    mode_operasi = st.radio("Tentukan Tindakan:", ("Enkripsi Teks", "Dekripsi Teks"), horizontal=True)

    panel_kiri, panel_kanan = st.columns(2)

    with panel_kiri:

        masukan_teks = st.text_area("Ketik teks di sini:")

        kata_kunci = st.text_input("Kata Kunci (Bebas):")

        tombol_proses = st.button("Mulai Proses")



    if tombol_proses and masukan_teks and kata_kunci:

        if mode_operasi == "Enkripsi Teks":

            hasil_proses, daftar_log = hitung_vernam(masukan_teks, kata_kunci)

            hasil_visual = vernam_ke_hex(hasil_proses)

        else:

            try:

                teks_awal = "".join(
                    chr(int(masukan_teks[i:i+2], 16))
                    for i in range(0, len(masukan_teks), 2)
                )

                hasil_proses, daftar_log = hitung_vernam(teks_awal, kata_kunci)

                hasil_visual = hasil_proses

            except:

                st.error("Data dekripsi tidak sesuai format heksadesimal!")

                hasil_visual = None



        if hasil_visual is not None:

            with panel_kanan:

                tab_hasil, tab_log = st.tabs(["Teks Hasil", "Log Proses (XOR)"])

                with tab_hasil:

                    st.code(hasil_visual)

                with tab_log:

                    for log in daftar_log: st.text(log)


elif pilihan_menu == "Super Enkripsi (Kombinasi)":

    st.header("Metode Lapis Baja: Super Enkripsi")

    st.caption("Penyandian berantai: Caesar -> Vigenere -> RC4 (Stream) -> Vernam XOR")

    mode_operasi = st.radio("Tentukan Tindakan:", ("Enkripsi Data", "Dekripsi Data"), horizontal=True)



    panel_kiri, panel_kanan = st.columns(2)

    with panel_kiri:

        masukan_teks = st.text_area("Ketik pesan rahasia di sini:")

        st.markdown("**Atur Kombinasi Kunci Anda:**")

        geseran_c = st.number_input("Kunci Caesar (Angka):", 0, 25, 3)

        teks_v = st.text_input("Kunci Vigenere (Huruf):", "RAHASIA")

        teks_rc4 = st.text_input("Kunci RC4 (Bebas):", "RAHASIA")

        teks_vernam = st.text_input("Kunci Vernam (Bebas):", "RAHASIA")

        tombol_proses = st.button("Jalankan Keamanan Berlapis")



    if tombol_proses:

        kunci_v_valid = ''.join([h for h in teks_v if h.isalpha()])
        kunci_rc4_valid = teks_rc4
        kunci_vernam_valid = teks_vernam

        if masukan_teks and kunci_v_valid and kunci_rc4_valid and kunci_vernam_valid:

            with panel_kanan:

                st.write("### Riwayat Proses Berlapis:")

                if mode_operasi == "Enkripsi Data":

                    # Plainteks -> Caesar -> Vigenere -> RC4 -> Vernam XOR -> Cipherteks
                    lapis1, _ = jalankan_caesar(masukan_teks, geseran_c, True)

                    st.info(f"**Lapis 1 (Caesar):** {lapis1}")



                    lapis2, _ = jalankan_vigenere(lapis1, kunci_v_valid, True)

                    st.info(f"**Lapis 2 (Vigenere):** {lapis2}")



                    # Modern 3: RC4 Stream Cipher
                    lapis3, _ = hitung_rc4(lapis2, kunci_rc4_valid)

                    lapis3_hex = vernam_ke_hex(lapis3)

                    st.info(f"**Lapis 3 (RC4 - Stream):** {lapis3_hex}")



                    # Modern 4: Vernam XOR
                    # Kunci Vernam memakai input yang sama agar tampilan tetap.
                    lapis4, _ = hitung_vernam(lapis3, kunci_vernam_valid)

                    st.success(f"**Lapis 4 Final (Vernam XOR):**")

                    st.code(vernam_ke_hex(lapis4))



                else: # Dekripsi

                    # Dekripsi membalik urutan:
                    # Cipherteks -> Vernam XOR -> RC4 -> Vigenere -> Caesar
                    try:

                        cipher_bytes = "".join(
                            chr(int(masukan_teks[i:i+2], 16))
                            for i in range(0, len(masukan_teks), 2)
                        )

                        lapis1, _ = hitung_vernam(cipher_bytes, kunci_vernam_valid)

                        st.info(f"**Lapis 1 Buka Vernam (XOR):** {vernam_ke_hex(lapis1)}")



                        lapis2, _ = hitung_rc4(lapis1, kunci_rc4_valid)

                        st.info(f"**Lapis 2 Buka RC4 (Stream):** {vernam_ke_hex(lapis2)}")



                        lapis3, _ = jalankan_vigenere(lapis2, kunci_v_valid, False)

                        st.info(f"**Lapis 3 Buka Vigenere:** {lapis3}")



                        lapis4, _ = jalankan_caesar(lapis3, geseran_c, False)

                        st.success(f"**Lapis 4 Final (Pesan Asli):**")

                        st.code(lapis4)

                    except:

                        st.error("Data dekripsi tidak sesuai format heksadesimal!")
