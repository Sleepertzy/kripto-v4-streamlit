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

def _kunci_bytes(kata_kunci):
    return kata_kunci.encode("utf-8")


def hitung_rc4_bytes(data_bytes, kata_kunci_str):
    """RC4 bekerja pada byte, sehingga aman untuk teks UTF-8."""
    kunci = _kunci_bytes(kata_kunci_str)
    if not kunci:
        return b"", ["Kunci RC4 tidak boleh kosong."]

    s_box = list(range(256))
    j = 0
    logs = [
        "=== RC4 - KEY SCHEDULING ALGORITHM (KSA) ===",
        f"Kunci: {kata_kunci_str}",
        f"Byte kunci UTF-8: {list(kunci)}",
        "S-box awal berisi nilai 0 sampai 255.",
        "KSA mengacak S-box menggunakan nilai kunci."
    ]
    for i in range(256):
        j = (j + s_box[i] + kunci[i % len(kunci)]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
        logs.append(f"KSA i={i:3d}, j={j:3d}, swap S[{i}] <-> S[{j}]")

    logs.append(f"S-box setelah KSA (16 nilai pertama): {s_box[:16]}")
    logs.append("=== RC4 - PSEUDO-RANDOM GENERATION ALGORITHM (PRGA) ===")
    out = bytearray()
    i = j = 0
    for pos, byte_data in enumerate(data_bytes):
        i = (i + 1) % 256
        j = (j + s_box[i]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
        keystream = s_box[(s_box[i] + s_box[j]) % 256]
        result = byte_data ^ keystream
        out.append(result)
        logs.append(
            f"Byte {pos + 1}: data {byte_data} (Hex {byte_data:02x}) "
            f"XOR keystream {keystream} (Hex {keystream:02x}) "
            f"= {result} (Hex {result:02x}) | i={i}, j={j}"
        )
    logs.append("RC4 menggunakan XOR; kunci yang sama dipakai kembali saat dekripsi.")
    return bytes(out), logs


def hitung_vernam_bytes(data_bytes, kata_kunci_str):
    kunci = _kunci_bytes(kata_kunci_str)
    if not kunci:
        return b"", ["Kunci Vernam tidak boleh kosong."]
    hasil = bytes(byte ^ kunci[i % len(kunci)] for i, byte in enumerate(data_bytes))
    logs = [
        "=== VERNAM XOR ===",
        "Rumus: Hasil = Data XOR Kunci",
        "Untuk dekripsi, XOR kembali dengan kunci yang sama.",
        "Kunci UTF-8 diulang dari awal apabila data lebih panjang dari kunci."
    ]
    for i, byte in enumerate(data_bytes):
        key_byte = kunci[i % len(kunci)]
        logs.append(
            f"Byte {i + 1}: data {byte} (Hex {byte:02x}) "
            f"XOR kunci {key_byte} (Hex {key_byte:02x}) "
            f"= {hasil[i]} (Hex {hasil[i]:02x})"
        )
    logs.append(f"Hasil Hex: {hasil.hex()}")
    return hasil, logs


def hitung_rc4(data_teks, kata_kunci_str):
    """Kompatibilitas dengan pemanggilan lama; hasil disimpan sebagai byte-string Latin-1."""
    hasil, logs = hitung_rc4_bytes(data_teks.encode("utf-8"), kata_kunci_str)
    return hasil.decode("latin-1"), logs


def hitung_vernam(data_teks, kata_kunci_str):
    """Kompatibilitas dengan pemanggilan lama untuk teks UTF-8."""
    hasil, logs = hitung_vernam_bytes(data_teks.encode("utf-8"), kata_kunci_str)
    return hasil.decode("latin-1"), logs


def vernam_ke_hex(teks):
    # Byte-string Latin-1 dipakai untuk merepresentasikan byte hasil cipher.
    try:
        return teks.encode("latin-1").hex()
    except UnicodeEncodeError:
        return teks.encode("utf-8").hex()


def hex_ke_teks(teks_hex):
    """Mengubah Hex menjadi byte-string Latin-1 agar setiap byte tetap utuh."""
    teks_hex = "".join(teks_hex.split())
    if not teks_hex:
        raise ValueError("Input Hex tidak boleh kosong.")
    if len(teks_hex) % 2 != 0:
        raise ValueError("Jumlah digit Hex harus genap.")
    try:
        return bytes.fromhex(teks_hex).decode("latin-1")
    except ValueError:
        raise ValueError("Input mengandung karakter yang bukan format Hex.")


# ==========================================
# ANTARMUKA PENGGUNA STREAMLIT
# ==========================================

st.set_page_config(
    page_title="Poly-Cipher",
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
    st.markdown("## KRIPTOCOY")
    
    st.markdown("### Daftar Anggota")

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

            hasil_proses, daftar_log = hitung_rc4_bytes(
                masukan_teks.encode("utf-8"),
                kata_kunci
            )

            hasil_visual = hasil_proses.hex()

        else:

            try:

                teks_awal = bytes.fromhex("".join(masukan_teks.split()))

                hasil_proses, daftar_log = hitung_rc4_bytes(
                    teks_awal,
                    kata_kunci
                )

                try:
                    hasil_visual = hasil_proses.decode("utf-8")
                except UnicodeDecodeError:
                    hasil_visual = hasil_proses.hex()

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
            input_bersih = masukan_teks.strip()
            input_hex = (
                len(input_bersih) > 0
                and len(input_bersih) % 2 == 0
                and all(c in "0123456789abcdefABCDEF" for c in input_bersih)
            )
            try:
                # Input Hex (misalnya keluaran RC4) diproses sebagai byte.
                # Selain itu, input dianggap sebagai teks UTF-8 biasa.
                data_bytes = (
                    bytes.fromhex(input_bersih)
                    if input_hex
                    else masukan_teks.encode("utf-8")
                )
                hasil_bytes, daftar_log = hitung_vernam_bytes(data_bytes, kata_kunci)
                hasil_visual = hasil_bytes.hex()
                if input_hex:
                    daftar_log.insert(0, "Input terdeteksi sebagai Hex dan dikonversi menjadi byte sebelum XOR Vernam.")
            except ValueError as error:
                st.error(str(error))
                hasil_visual = None
        else:
            try:
                data_bytes = bytes.fromhex("".join(masukan_teks.split()))
                hasil_bytes, daftar_log = hitung_vernam_bytes(data_bytes, kata_kunci)
                try:
                    hasil_visual = hasil_bytes.decode("utf-8")
                except UnicodeDecodeError:
                    hasil_visual = hasil_bytes.hex()
                daftar_log.insert(0, "Input Hex dikonversi menjadi byte sebelum XOR Vernam.")
            except ValueError as error:
                st.error("Input harus berupa Hex dengan jumlah digit genap.")
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

                    lapis3_bytes, log_rc4 = hitung_rc4_bytes(
                        lapis2.encode("utf-8"),
                        kunci_rc4_valid
                    )

                    lapis3_hex = lapis3_bytes.hex()

                    st.info(
                        f"**Lapis 3 (RC4 - Stream):** {lapis3_hex}"
                    )

                    # --------------------------------------
                    # LAPIS 4 - VERNAM
                    # --------------------------------------

                    lapis4_bytes, log_vernam = hitung_vernam_bytes(
                        lapis3_bytes,
                        kunci_vernam_valid
                    )

                    hasil_final = lapis4_bytes.hex()

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

                        cipher_bytes = bytes.fromhex(
                            "".join(masukan_teks.split())
                        )

                        # ----------------------------------
                        # BALIK LAPIS 4 - VERNAM
                        # ----------------------------------

                        lapis1, log_vernam = hitung_vernam_bytes(
                            cipher_bytes,
                            kunci_vernam_valid
                        )

                        st.info(
                            "**Lapis 1 Buka Vernam (XOR):** "
                            f"{lapis1.hex()}"
                        )

                        # ----------------------------------
                        # BALIK LAPIS 3 - RC4
                        # ----------------------------------

                        lapis2, log_rc4 = hitung_rc4_bytes(
                            lapis1,
                            kunci_rc4_valid
                        )

                        st.info(
                            "**Lapis 2 Buka RC4 (Stream):** "
                            f"{lapis2.hex()}"
                        )

                        # ----------------------------------
                        # BALIK LAPIS 2 - VIGENERE
                        # ----------------------------------

                        lapis2_teks = lapis2.decode("utf-8")
                        lapis3, log_vigenere = jalankan_vigenere(
                            lapis2_teks,
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
