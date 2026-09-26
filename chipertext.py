import streamlit as st


# ==========================================
# 1. ALGORITMA CAESAR CIPHER
# ==========================================

def jalankan_caesar(pesan, angka_geser, is_enkripsi=True):
    teks_akhir = ""
    catatan_proses = []

    nilai_geser = angka_geser % 26 if is_enkripsi else -(angka_geser % 26)

    catatan_proses.append("=== CAESAR CIPHER ===")
    catatan_proses.append(
        f"Mode: {'Enkripsi' if is_enkripsi else 'Dekripsi'}"
    )
    catatan_proses.append(
        f"Rumus: {'C = (P + K) mod 26' if is_enkripsi else 'P = (C - K) mod 26'}"
    )
    catatan_proses.append(f"Nilai geseran K = {angka_geser}")
    catatan_proses.append("Setiap huruf dihitung pada rentang posisi alfabet 0-25.")
    catatan_proses.append("Spasi, angka, dan tanda baca tidak mengalami pergeseran.")

    for indeks, huruf in enumerate(pesan):
        if huruf.isalpha():
            batas_ascii = 65 if huruf.isupper() else 97

            posisi_awal = ord(huruf) - batas_ascii
            posisi_baru = (posisi_awal + nilai_geser) % 26
            huruf_baru = chr(posisi_baru + batas_ascii)
            teks_akhir += huruf_baru

            catatan_proses.append(
                f"Karakter {indeks + 1}: '{huruf}' "
                f"(ASCII {ord(huruf)}, posisi {posisi_awal}) "
                f"+ geser {nilai_geser} "
                f"-> posisi {posisi_baru} "
                f"-> '{huruf_baru}' (ASCII {ord(huruf_baru)})"
            )
        else:
            teks_akhir += huruf
            catatan_proses.append(
                f"Karakter {indeks + 1}: '{huruf}' tidak berubah "
                f"(bukan huruf alfabet)."
            )

    catatan_proses.append(f"Hasil akhir: {teks_akhir}")

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

    if panjang_kunci == 0:
        return "", ["Kunci Vigenere tidak boleh kosong."]

    catatan_proses.append("=== VIGENERE CIPHER ===")
    catatan_proses.append(
        f"Mode: {'Enkripsi' if is_enkripsi else 'Dekripsi'}"
    )
    catatan_proses.append(
        f"Rumus: {'C = (P + K) mod 26' if is_enkripsi else 'P = (C - K) mod 26'}"
    )
    catatan_proses.append(f"Kunci: {kata_kunci}")
    catatan_proses.append(
        "Kunci hanya berpindah ketika menemukan karakter alfabet."
    )
    catatan_proses.append(
        "Spasi, angka, dan tanda baca tidak mengonsumsi posisi kunci."
    )

    for indeks, huruf in enumerate(pesan):
        if huruf.isalpha():
            karakter_kunci = kata_kunci[indeks_kunci % panjang_kunci]
            nilai_kunci = ord(karakter_kunci) - 65
            batas_ascii = 65 if huruf.isupper() else 97
            posisi_awal = ord(huruf) - batas_ascii

            if is_enkripsi:
                posisi_baru = (posisi_awal + nilai_kunci) % 26
            else:
                posisi_baru = (posisi_awal - nilai_kunci) % 26

            huruf_baru = chr(posisi_baru + batas_ascii)
            teks_akhir += huruf_baru

            operasi = "+" if is_enkripsi else "-"
            catatan_proses.append(
                f"Karakter {indeks + 1}: '{huruf}' "
                f"(posisi {posisi_awal}) {operasi} "
                f"kunci '{karakter_kunci}' (nilai {nilai_kunci}) "
                f"mod 26 = {posisi_baru} "
                f"-> '{huruf_baru}'"
            )

            indeks_kunci += 1
        else:
            teks_akhir += huruf
            catatan_proses.append(
                f"Karakter {indeks + 1}: '{huruf}' tidak berubah "
                f"dan posisi kunci tidak bertambah."
            )

    catatan_proses.append(f"Hasil akhir: {teks_akhir}")

    return teks_akhir, catatan_proses


# ==========================================
# 3. ALGORITMA RC4
# ==========================================

def hitung_rc4(data_teks, kata_kunci_str):
    if not kata_kunci_str:
        return "", ["Kunci RC4 tidak boleh kosong."]

    kotak_s = [angka for angka in range(256)]
    indeks_j = 0

    kunci_ascii = [ord(huruf) for huruf in kata_kunci_str]
    panjang_k = len(kunci_ascii)

    catatan_proses = []

    catatan_proses.append("=== RC4 - KEY SCHEDULING ALGORITHM (KSA) ===")
    catatan_proses.append(f"Kunci: {kata_kunci_str}")
    catatan_proses.append(
        f"ASCII kunci: {kunci_ascii}"
    )
    catatan_proses.append(
        "S-box awal berisi nilai 0 sampai 255."
    )
    catatan_proses.append(
        "KSA mengacak S-box menggunakan nilai kunci."
    )

    # KSA
    for indeks_i in range(256):
        indeks_j = (
            indeks_j
            + kotak_s[indeks_i]
            + kunci_ascii[indeks_i % panjang_k]
        ) % 256

        kotak_s[indeks_i], kotak_s[indeks_j] = (
            kotak_s[indeks_j],
            kotak_s[indeks_i]
        )

        # Agar log tidak terlalu besar, tetap mencatat semua langkah
        # tetapi bagian S-box hanya ditampilkan dalam bentuk ringkas.
        catatan_proses.append(
            f"KSA i={indeks_i:3d}, j={indeks_j:3d}, "
            f"swap S[{indeks_i}] <-> S[{indeks_j}]"
        )

    catatan_proses.append(
        f"S-box setelah KSA (16 nilai pertama): {kotak_s[:16]}"
    )
    catatan_proses.append("=== RC4 - PSEUDO-RANDOM GENERATION ALGORITHM (PRGA) ===")
    catatan_proses.append(
        "PRGA menghasilkan keystream, kemudian setiap byte data di-XOR "
        "dengan byte keystream."
    )

    pointer_i = 0
    pointer_j = 0
    teks_akhir = ""

    for indeks, karakter in enumerate(data_teks):
        pointer_i = (pointer_i + 1) % 256
        pointer_j = (pointer_j + kotak_s[pointer_i]) % 256

        kotak_s[pointer_i], kotak_s[pointer_j] = (
            kotak_s[pointer_j],
            kotak_s[pointer_i]
        )

        posisi_keystream = (
            kotak_s[pointer_i] + kotak_s[pointer_j]
        ) % 256

        aliran_kunci = kotak_s[posisi_keystream]

        nilai_teks = ord(karakter)
        nilai_hasil = nilai_teks ^ aliran_kunci
        karakter_baru = chr(nilai_hasil)
        teks_akhir += karakter_baru

        catatan_proses.append(
            f"Byte {indeks + 1}: "
            f"data ASCII {nilai_teks} (Hex {nilai_teks:02x}) "
            f"XOR keystream {aliran_kunci} (Hex {aliran_kunci:02x}) "
            f"= {nilai_hasil} (Hex {nilai_hasil:02x}) | "
            f"i={pointer_i}, j={pointer_j}"
        )

    catatan_proses.append(
        "Karena RC4 menggunakan XOR, proses dengan kunci yang sama "
        "dapat digunakan kembali untuk dekripsi."
    )

    return teks_akhir, catatan_proses


# ==========================================
# 4. ALGORITMA VERNAM XOR
# ==========================================

def hitung_vernam(data_teks, kata_kunci_str):
    if not kata_kunci_str:
        return "", ["Kunci Vernam tidak boleh kosong."]

    teks_akhir = ""
    catatan_proses = []

    catatan_proses.append("=== VERNAM XOR ===")
    catatan_proses.append(
        "Rumus: Hasil = Data XOR Kunci"
    )
    catatan_proses.append(
        "Untuk membalik hasil digunakan operasi XOR dengan kunci yang sama."
    )
    catatan_proses.append(
        "Kunci diulang dari awal apabila panjang data melebihi panjang kunci."
    )

    for indeks, karakter in enumerate(data_teks):
        kunci = kata_kunci_str[indeks % len(kata_kunci_str)]

        nilai_teks = ord(karakter)
        nilai_kunci = ord(kunci)
        nilai_xor = nilai_teks ^ nilai_kunci

        teks_akhir += chr(nilai_xor)

        catatan_proses.append(
            f"Byte {indeks + 1}: "
            f"data {nilai_teks} (Hex {nilai_teks:02x}) "
            f"XOR kunci '{kunci}' {nilai_kunci} (Hex {nilai_kunci:02x}) "
            f"= {nilai_xor} (Hex {nilai_xor:02x})"
        )

    catatan_proses.append(
        f"Hasil Hex: {vernam_ke_hex(teks_akhir)}"
    )

    return teks_akhir, catatan_proses


def vernam_ke_hex(teks):
    return "".join(format(ord(c), "02x") for c in teks)


def hex_ke_teks(teks_hex):
    """
    Mengubah Hex menjadi karakter/byte string.
    Dipakai sebelum Vernam atau RC4 agar Hex tidak diproses
    sebagai karakter '0'-'9' dan 'a'-'f'.
    """
    teks_hex = "".join(teks_hex.split())

    if not teks_hex:
        raise ValueError("Input Hex tidak boleh kosong.")

    if len(teks_hex) % 2 != 0:
        raise ValueError("Jumlah digit Hex harus genap.")

    try:
        return "".join(
            chr(int(teks_hex[i:i + 2], 16))
            for i in range(0, len(teks_hex), 2)
        )
    except ValueError:
        raise ValueError(
            "Input mengandung karakter yang bukan format Hex."
        )


# ==========================================
# ANTARMUKA PENGGUNA STREAMLIT
# ==========================================

st.set_page_config(
    page_title="Tugas Kripto",
    layout="wide",
    page_icon="🛡️"
)

st.sidebar.header("📁 Daftar Menu Kriptografi")

pilihan_menu = st.sidebar.selectbox(
    "Silakan pilih fitur di bawah ini:",
    [
        "Profil Kelompok",
        "Algoritma 1: Caesar",
        "Algoritma 2: Vigenere",
        "Algoritma 3: RC4",
        "Algoritma 4: Vernam XOR",
        "Super Enkripsi (Kombinasi)"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Sistem Keamanan Data - IF D")


# ==========================================
# PROFIL
# ==========================================

if pilihan_menu == "Profil Kelompok":

    st.title("🛡️ Aplikasi Keamanan Data Kriptografi")
    st.write(
        "Dibuat khusus untuk memenuhi evaluasi Tugas 4 "
        "Mata Kuliah Kriptografi."
    )
    st.info(
        "Dosen Pengampu: Bagus Muhammad Akbar, S.T., M.T."
    )

    st.markdown("### Daftar Anggota (Kelompok)")

    st.markdown("""
    - **Afiq Fathurrahman** (123240010)
    - **Radja Azhara I.K.** (123240012)
    - **Muhammad Afif P.N.** (123240031)
    - **Munadhil Mutawakkil** (123240145)
    """)


# ==========================================
# MENU 1 - CAESAR
# ==========================================

elif pilihan_menu == "Algoritma 1: Caesar":

    st.header("Metode Klasik: Caesar Cipher")

    mode_operasi = st.radio(
        "Tentukan Tindakan:",
        ("Enkripsi Teks", "Dekripsi Teks"),
        horizontal=True
    )

    panel_kiri, panel_kanan = st.columns(2)

    with panel_kiri:

        masukan_teks = st.text_area("Ketik teks di sini:")

        angka_kunci = st.number_input(
            "Besaran geseran (0-25):",
            min_value=0,
            max_value=25,
            value=3
        )

        tombol_proses = st.button("Mulai Proses")

    if tombol_proses and masukan_teks:

        status_enkripsi = mode_operasi == "Enkripsi Teks"

        hasil_teks, daftar_log = jalankan_caesar(
            masukan_teks,
            angka_kunci,
            status_enkripsi
        )

        with panel_kanan:

            tab_hasil, tab_log = st.tabs(
                ["Teks Hasil", "Log Perhitungan"]
            )

            with tab_hasil:
                st.code(hasil_teks)

            with tab_log:

                st.markdown("""
**Penjelasan proses Caesar:**

1. Setiap huruf diubah menjadi posisi alfabet 0-25.
2. Enkripsi menggunakan rumus **C = (P + K) mod 26**.
3. Dekripsi menggunakan rumus **P = (C - K) mod 26**.
4. Jika hasil melewati Z, operasi modulo 26 mengembalikannya ke awal alfabet.
5. Spasi, angka, dan tanda baca tidak digeser.
6. Log di bawah memperlihatkan perhitungan setiap karakter.
""")

                st.caption(
                    f"Mode: {mode_operasi} | "
                    f"Kunci geseran: {angka_kunci}"
                )

                for log in daftar_log:
                    st.text(log)


# ==========================================
# MENU 2 - VIGENERE
# ==========================================

elif pilihan_menu == "Algoritma 2: Vigenere":

    st.header("Metode Klasik: Vigenere Cipher")

    mode_operasi = st.radio(
        "Tentukan Tindakan:",
        ("Enkripsi Teks", "Dekripsi Teks"),
        horizontal=True
    )

    panel_kiri, panel_kanan = st.columns(2)

    with panel_kiri:

        masukan_teks = st.text_area("Ketik teks di sini:")

        kata_kunci = st.text_input(
            "Gunakan kata kunci (huruf):",
            value="KUNCI"
        )

        tombol_proses = st.button("Mulai Proses")

    if tombol_proses and masukan_teks:

        kunci_valid = "".join(
            [huruf for huruf in kata_kunci if huruf.isalpha()]
        )

        if not kunci_valid:

            st.error(
                "Gagal! Kata kunci wajib berisi huruf abjad."
            )

        else:

            status_enkripsi = mode_operasi == "Enkripsi Teks"

            hasil_teks, daftar_log = jalankan_vigenere(
                masukan_teks,
                kunci_valid,
                status_enkripsi
            )

            with panel_kanan:

                tab_hasil, tab_log = st.tabs(
                    ["Teks Hasil", "Log Perhitungan"]
                )

                with tab_hasil:
                    st.code(hasil_teks)

                with tab_log:

                    st.markdown("""
**Penjelasan proses Vigenere:**

1. Setiap huruf plaintext diubah menjadi nilai 0-25.
2. Huruf pada kunci juga diubah menjadi nilai 0-25.
3. Enkripsi menggunakan **C = (P + K) mod 26**.
4. Dekripsi menggunakan **P = (C - K) mod 26**.
5. Kunci diulang dari awal apabila karakter teks lebih panjang dari kunci.
6. Spasi, angka, dan tanda baca tidak menggunakan posisi kunci.
7. Log memperlihatkan pasangan karakter teks dengan karakter kuncinya.
""")

                    st.caption(
                        f"Mode: {mode_operasi} | "
                        f"Kunci: {kunci_valid.upper()}"
                    )

                    for log in daftar_log:
                        st.text(log)


# ==========================================
# MENU 3 - RC4
# ==========================================

elif pilihan_menu == "Algoritma 3: RC4":

    st.header("Metode Modern: Stream Cipher RC4")

    mode_operasi = st.radio(
        "Tentukan Tindakan:",
        ("Enkripsi Teks", "Dekripsi Teks"),
        horizontal=True
    )

    panel_kiri, panel_kanan = st.columns(2)

    with panel_kiri:

        masukan_teks = st.text_area(
            "Ketik teks di sini "
            "(Wajib Heksadesimal untuk Dekripsi):"
        )

        kata_kunci = st.text_input(
            "Kata Kunci (Bebas):"
        )

        tombol_proses = st.button("Mulai Proses")

    if tombol_proses and masukan_teks and kata_kunci:

        if mode_operasi == "Enkripsi Teks":

            hasil_proses, daftar_log = hitung_rc4(
                masukan_teks,
                kata_kunci
            )

            hasil_visual = vernam_ke_hex(hasil_proses)

        else:

            try:

                teks_awal = hex_ke_teks(masukan_teks)

                hasil_proses, daftar_log = hitung_rc4(
                    teks_awal,
                    kata_kunci
                )

                hasil_visual = hasil_proses

                daftar_log.insert(
                    0,
                    "Input Hex berhasil dikonversi kembali "
                    "menjadi byte asli sebelum RC4."
                )

            except ValueError as error:

                st.error(str(error))
                hasil_visual = None

        if hasil_visual is not None:

            with panel_kanan:

                tab_hasil, tab_log = st.tabs(
                    ["Teks Hasil", "Log Proses (XOR)"]
                )

                with tab_hasil:
                    st.code(hasil_visual)

                with tab_log:

                    st.markdown("""
**Penjelasan proses RC4:**

**1. KSA (Key Scheduling Algorithm)**  
S-box berisi angka 0-255 kemudian diacak berdasarkan kunci.

**2. PRGA (Pseudo-Random Generation Algorithm)**  
S-box yang telah diacak digunakan untuk menghasilkan keystream.

**3. XOR**  
Setiap byte data di-XOR dengan byte keystream:

**Ciphertext = Plaintext XOR Keystream**

Pada dekripsi, operasi RC4 yang sama dengan kunci yang sama digunakan kembali.

Hasil enkripsi ditampilkan dalam bentuk **Hex** agar byte yang tidak terbaca dapat ditampilkan dan disalin dengan aman.
""")

                    st.caption(
                        f"Mode: {mode_operasi} | "
                        f"Kunci RC4: {kata_kunci}"
                    )

                    for log in daftar_log:
                        st.text(log)


# ==========================================
# MENU 4 - VERNAM
# ==========================================

elif pilihan_menu == "Algoritma 4: Vernam XOR":

    st.header("Metode Modern: Vernam Cipher (XOR)")

    mode_operasi = st.radio(
        "Tentukan Tindakan:",
        ("Enkripsi Teks", "Dekripsi Teks"),
        horizontal=True
    )

    panel_kiri, panel_kanan = st.columns(2)

    with panel_kiri:

        masukan_teks = st.text_area(
            "Ketik teks di sini:"
        )

        kata_kunci = st.text_input(
            "Kata Kunci (Bebas):"
        )

        tombol_proses = st.button("Mulai Proses")

    if tombol_proses and masukan_teks and kata_kunci:

        if mode_operasi == "Enkripsi Teks":

            # Jika input merupakan Hex hasil RC4, konversikan
            # kembali menjadi byte sebelum XOR Vernam.
            input_hex_rc4 = (
                len(masukan_teks.strip()) % 2 == 0
                and len(masukan_teks.strip()) > 0
                and all(
                    karakter in "0123456789abcdefABCDEF"
                    for karakter in masukan_teks.strip()
                )
            )

            try:

                if input_hex_rc4:

                    teks_byte = hex_ke_teks(masukan_teks)

                    hasil_proses, daftar_log = hitung_vernam(
                        teks_byte,
                        kata_kunci
                    )

                    daftar_log.insert(
                        0,
                        "Input terdeteksi sebagai Hex hasil RC4."
                    )

                    daftar_log.insert(
                        1,
                        f"Hex {masukan_teks.strip()} "
                        "dikonversi menjadi byte sebelum XOR Vernam."
                    )

                else:

                    hasil_proses, daftar_log = hitung_vernam(
                        masukan_teks,
                        kata_kunci
                    )

                hasil_visual = vernam_ke_hex(hasil_proses)

            except ValueError as error:

                st.error(str(error))
                hasil_visual = None

        else:

            try:

                teks_awal = hex_ke_teks(masukan_teks)

                hasil_proses, daftar_log = hitung_vernam(
                    teks_awal,
                    kata_kunci
                )

                hasil_visual = hasil_proses

                daftar_log.insert(
                    0,
                    "Input Hex berhasil dikonversi kembali "
                    "menjadi byte asli sebelum XOR Vernam."
                )

            except ValueError as error:

                st.error(str(error))
                hasil_visual = None

        if hasil_visual is not None:

            with panel_kanan:

                tab_hasil, tab_log = st.tabs(
                    ["Teks Hasil", "Log Proses (XOR)"]
                )

                with tab_hasil:
                    st.code(hasil_visual)

                with tab_log:

                    st.markdown("""
**Penjelasan proses Vernam XOR:**

1. Data dan kunci dikonversi menjadi nilai byte.
2. Setiap byte data di-XOR dengan byte kunci.
3. Rumus enkripsi adalah **C = P XOR K**.
4. Karena sifat XOR, dekripsi menggunakan **P = C XOR K**.
5. Kunci diulang dari awal apabila panjang data melebihi panjang kunci.
6. Hasil ditampilkan dalam bentuk Hex.
7. Jika input berasal dari RC4, Hex harus dikonversi kembali ke byte asli terlebih dahulu. Dengan cara ini, operasi Vernam pada Menu 4 dan lapisan Vernam pada Menu 5 menggunakan data byte yang sama.
""")

                    st.caption(
                        f"Mode: {mode_operasi} | "
                        f"Kunci Vernam: {kata_kunci}"
                    )

                    for log in daftar_log:
                        st.text(log)


# ==========================================
# MENU 5 - SUPER ENKRIPSI
# ==========================================

elif pilihan_menu == "Super Enkripsi (Kombinasi)":

    st.header("Metode Lapis Baja: Super Enkripsi")

    st.caption(
        "Penyandian berantai: Caesar -> Vigenere -> RC4 (Stream) -> Vernam XOR"
    )

    mode_operasi = st.radio(
        "Tentukan Tindakan:",
        ("Enkripsi Data", "Dekripsi Data"),
        horizontal=True
    )

    panel_kiri, panel_kanan = st.columns(2)

    with panel_kiri:

        masukan_teks = st.text_area(
            "Ketik pesan rahasia di sini:"
        )

        st.markdown(
            "**Atur Kombinasi Kunci Anda:**"
        )

        geseran_c = st.number_input(
            "Kunci Caesar (Angka):",
            0,
            25,
            3
        )

        teks_v = st.text_input(
            "Kunci Vigenere (Huruf):",
            "KUNCI"
        )

        teks_rc4 = st.text_input(
            "Kunci RC4 (Bebas):",
            "KUNCI"
        )

        teks_vernam = st.text_input(
            "Kunci Vernam (Bebas):",
            "KUNCI"
        )

        tombol_proses = st.button(
            "Jalankan Keamanan Berlapis"
        )

    if tombol_proses:

        kunci_v_valid = "".join(
            [h for h in teks_v if h.isalpha()]
        )

        kunci_rc4_valid = teks_rc4
        kunci_vernam_valid = teks_vernam

        if (
            masukan_teks
            and kunci_v_valid
            and kunci_rc4_valid
            and kunci_vernam_valid
        ):

            with panel_kanan:

                st.write(
                    "### Riwayat Proses Berlapis:"
                )

                if mode_operasi == "Enkripsi Data":

                    # --------------------------------------
                    # LAPIS 1 - CAESAR
                    # --------------------------------------

                    lapis1, log_caesar = jalankan_caesar(
                        masukan_teks,
                        geseran_c,
                        True
                    )

                    st.info(
                        f"**Lapis 1 (Caesar):** {lapis1}"
                    )

                    # --------------------------------------
                    # LAPIS 2 - VIGENERE
                    # --------------------------------------

                    lapis2, log_vigenere = jalankan_vigenere(
                        lapis1,
                        kunci_v_valid,
                        True
                    )

                    st.info(
                        f"**Lapis 2 (Vigenere):** {lapis2}"
                    )

                    # --------------------------------------
                    # LAPIS 3 - RC4
                    # --------------------------------------

                    lapis3, log_rc4 = hitung_rc4(
                        lapis2,
                        kunci_rc4_valid
                    )

                    lapis3_hex = vernam_ke_hex(lapis3)

                    st.info(
                        f"**Lapis 3 (RC4 - Stream):** {lapis3_hex}"
                    )

                    # --------------------------------------
                    # LAPIS 4 - VERNAM
                    # --------------------------------------

                    lapis4, log_vernam = hitung_vernam(
                        lapis3,
                        kunci_vernam_valid
                    )

                    hasil_final = vernam_ke_hex(lapis4)

                    st.success(
                        "**Lapis 4 Final (Vernam XOR):**"
                    )

                    st.code(hasil_final)

                    # --------------------------------------
                    # LOG SUPER ENKRIPSI
                    # --------------------------------------

                    st.subheader(
                        "Log Super Enkripsi"
                    )

                    st.markdown("""
### Penjelasan alur enkripsi

**Plaintext**  
↓  
**Caesar** → menggeser huruf  
↓  
**Vigenere** → menggeser berdasarkan kunci huruf  
↓  
**RC4** → menghasilkan keystream dan melakukan XOR  
↓  
**Vernam XOR** → melakukan XOR kembali terhadap byte RC4  
↓  
**Ciphertext Final dalam Hex**

Log berikut menampilkan proses dari masing-masing lapisan secara berurutan.
""")

                    with st.expander(
                        "Lihat Log Caesar",
                        expanded=False
                    ):
                        for log in log_caesar:
                            st.text(log)

                    with st.expander(
                        "Lihat Log Vigenere",
                        expanded=False
                    ):
                        for log in log_vigenere:
                            st.text(log)

                    with st.expander(
                        "Lihat Log RC4",
                        expanded=False
                    ):
                        for log in log_rc4:
                            st.text(log)

                    with st.expander(
                        "Lihat Log Vernam",
                        expanded=False
                    ):
                        for log in log_vernam:
                            st.text(log)

                else:

                    # --------------------------------------
                    # DEKRIPSI - VALIDASI HEX
                    # --------------------------------------

                    try:

                        cipher_bytes = hex_ke_teks(
                            masukan_teks
                        )

                        # ----------------------------------
                        # BALIK LAPIS 4 - VERNAM
                        # ----------------------------------

                        lapis1, log_vernam = hitung_vernam(
                            cipher_bytes,
                            kunci_vernam_valid
                        )

                        st.info(
                            "**Lapis 1 Buka Vernam (XOR):** "
                            f"{vernam_ke_hex(lapis1)}"
                        )

                        # ----------------------------------
                        # BALIK LAPIS 3 - RC4
                        # ----------------------------------

                        lapis2, log_rc4 = hitung_rc4(
                            lapis1,
                            kunci_rc4_valid
                        )

                        st.info(
                            "**Lapis 2 Buka RC4 (Stream):** "
                            f"{vernam_ke_hex(lapis2)}"
                        )

                        # ----------------------------------
                        # BALIK LAPIS 2 - VIGENERE
                        # ----------------------------------

                        lapis3, log_vigenere = jalankan_vigenere(
                            lapis2,
                            kunci_v_valid,
                            False
                        )

                        st.info(
                            f"**Lapis 3 Buka Vigenere:** {lapis3}"
                        )

                        # ----------------------------------
                        # BALIK LAPIS 1 - CAESAR
                        # ----------------------------------

                        lapis4, log_caesar = jalankan_caesar(
                            lapis3,
                            geseran_c,
                            False
                        )

                        st.success(
                            "**Lapis 4 Final (Pesan Asli):**"
                        )

                        st.code(lapis4)

                        # ----------------------------------
                        # LOG SUPER DEKRIPSI
                        # ----------------------------------

                        st.subheader(
                            "Log Super Dekripsi"
                        )

                        st.markdown("""
### Penjelasan alur dekripsi

**Ciphertext Final dalam Hex**  
↓  
**Vernam XOR** → mengembalikan hasil RC4  
↓  
**RC4** → mengembalikan hasil Vigenere  
↓  
**Vigenere** → mengembalikan hasil Caesar  
↓  
**Caesar** → mengembalikan plaintext asli

Urutan dekripsi harus merupakan kebalikan dari urutan enkripsi.
Kunci setiap algoritma juga harus sama dengan kunci yang digunakan
saat enkripsi.
""")

                        with st.expander(
                            "Lihat Log Buka Vernam",
                            expanded=False
                        ):
                            for log in log_vernam:
                                st.text(log)

                        with st.expander(
                            "Lihat Log Buka RC4",
                            expanded=False
                        ):
                            for log in log_rc4:
                                st.text(log)

                        with st.expander(
                            "Lihat Log Buka Vigenere",
                            expanded=False
                        ):
                            for log in log_vigenere:
                                st.text(log)

                        with st.expander(
                            "Lihat Log Buka Caesar",
                            expanded=False
                        ):
                            for log in log_caesar:
                                st.text(log)

                    except ValueError as error:

                        st.error(str(error))
