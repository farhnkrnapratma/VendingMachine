import random
import string

def generate_qris():
    """Generate kode QRIS dummy"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

def pilih_minuman():
    """Menampilkan menu minuman dan meminta input"""
    print("\n" + "="*50)
    print(" "*15 + "MENU MINUMAN")
    print("="*50)
    menu = {
        "1": {"nama": "Kopi", "harga": 5000},
        "2": {"nama": "Teh", "harga": 3000},
        "3": {"nama": "Jus Jeruk", "harga": 8000},
        "4": {"nama": "Air Mineral", "harga": 3000},
        "5": {"nama": "Susu", "harga": 6000},
        "6": {"nama": "Cappuccino", "harga": 10000},
        "7": {"nama": "Green Tea", "harga": 4000},
        "8": {"nama": "Cokelat Panas", "harga": 7000},
        "9": {"nama": "Lemon Tea", "harga": 4000},
        "10": {"nama": "Smoothie", "harga": 12000}
    }
    
    for key, value in menu.items():
        print(f"  [{key:>2}]  {value['nama']:<20} Rp {value['harga']:>8,}")
    
    print("="*50)
    pilihan = input("Pilih nomor minuman: ")
    return menu.get(pilihan, None)

def input_bayar():
    """Meminta input jumlah bayar dengan validator nominal valid"""
    nominal_valid = [1000, 2000, 5000, 10000, 20000, 50000, 100000]
    
    print("\n" + "="*50)
    print(" "*12 + "NOMINAL YANG DITERIMA")
    print("="*50)
    print("  Rp   1.000  |  Rp   2.000  |  Rp   5.000")
    print("  Rp  10.000  |  Rp  20.000  |  Rp  50.000")
    print("  Rp 100.000")
    print("="*50)
    
    total_bayar = 0
    print("\nMasukkan uang (ketik 0 untuk selesai)")
    print("-"*50)
    
    while True:
        try:
            print(f"\nTotal saat ini: Rp {total_bayar:>10,}")
            jumlah = int(input("Masukkan nominal: Rp "))
            
            if jumlah == 0:
                if total_bayar == 0:
                    print("\n[!] Anda belum memasukkan uang!")
                    continue
                print("-"*50)
                return total_bayar
            
            if jumlah not in nominal_valid:
                print(f"\n[X] Nominal Rp {jumlah:,} tidak valid!")
                print("    Gunakan: 1000, 2000, 5000, 10000, 20000, 50000, 100000")
                continue
            
            total_bayar += jumlah
            print(f"[OK] Uang diterima: Rp {jumlah:,}")
            
        except ValueError:
            print("\n[X] Input tidak valid! Masukkan angka.")

def cek_cukup(bayar, harga):
    """Mengecek apakah pembayaran cukup"""
    return bayar >= harga

def pilih_metode_bayar():
    """Menanyakan metode pembayaran"""
    print("\n" + "="*50)
    print(" "*14 + "METODE PEMBAYARAN")
    print("="*50)
    print("  [1] Tunai")
    print("  [2] QRIS")
    print("="*50)
    while True:
        pilihan = input("Pilih metode pembayaran (1/2): ")
        if pilihan == "1":
            return True  # Tunai
        elif pilihan == "2":
            return False  # QRIS
        else:
            print("[X] Pilihan tidak valid! Pilih 1 atau 2.")

def cek_lebih(bayar, harga):
    """Mengecek apakah pembayaran lebih dari harga"""
    return bayar > harga

def proses_kembalian(bayar, harga):
    """Menghitung dan menampilkan kembalian"""
    kembalian = bayar - harga
    print("\n" + "="*50)
    print(" "*17 + "KEMBALIAN")
    print("="*50)
    print(f"  Total Bayar    : Rp {bayar:>12,}")
    print(f"  Harga          : Rp {harga:>12,}")
    print(f"  Kembalian Anda : Rp {kembalian:>12,}")
    print("="*50)

def generate_qris_payment():
    """Generate dan tampilkan kode QRIS"""
    kode = generate_qris()
    print("\n" + "="*50)
    print(" "*14 + "PEMBAYARAN QRIS")
    print("="*50)
    print(f"\n  Kode QRIS: {kode}")
    print("\n  Silakan scan kode di atas untuk")
    print("  melakukan pembayaran")
    print("\n" + "="*50)

def keluarkan_minuman(minuman):
    """Menampilkan pesan pengambilan minuman"""
    print("\n" + "="*50)
    print(" "*13 + "PESANAN BERHASIL")
    print("="*50)
    print(f"\n  Pesanan Anda: {minuman}")
    print("\n  Silakan ambil minuman Anda")
    print("  Terima kasih!")
    print("\n" + "="*50)

def main():
    """Fungsi utama sesuai flowchart"""
    print("\n" + "="*50)
    print(" "*10 + "VENDING MACHINE MINUMAN")
    print(" "*12 + "Selamat Datang!")
    print("="*50)
    
    # Pilih Minuman
    minuman_data = pilih_minuman()
    if minuman_data is None:
        print("\n[X] Pilihan tidak valid!")
        return
    
    minuman = minuman_data['nama']
    harga = minuman_data['harga']
    
    print("\n" + "="*50)
    print(f"  Minuman dipilih : {minuman}")
    print(f"  Harga           : Rp {harga:,}")
    print("="*50)
    
    # Pilih metode pembayaran
    is_tunai = pilih_metode_bayar()
    
    if is_tunai:
        # Pembayaran Tunai
        # Bayar (loop hingga cukup)
        bayar = 0
        while not cek_cukup(bayar, harga):
            if bayar > 0:
                print("\n" + "="*50)
                print("\n[X] Maaf, uang Anda masih kurang!")
                print(f"    Total saat ini : Rp {bayar:>10,}")
                print(f"    Harga          : Rp {harga:>10,}")
                print(f"    Masih kurang   : Rp {harga - bayar:>10,}")
                print("\n    Silakan masukkan uang lagi")
                print("="*50)
            
            bayar_tambahan = input_bayar()
            bayar += bayar_tambahan
        
        # Cek apakah ada kembalian
        if cek_lebih(bayar, harga):
            proses_kembalian(bayar, harga)
        
        # Keluarkan minuman
        keluarkan_minuman(minuman)
    
    else:
        # Pembayaran QRIS
        generate_qris_payment()
        
        # Simulasi konfirmasi pembayaran
        print("\n" + "="*50)
        konfirmasi = input("Apakah pembayaran sudah selesai? (y/n): ").lower()
        if konfirmasi == 'y':
            # Keluarkan minuman
            keluarkan_minuman(minuman)
        else:
            print("\n" + "="*50)
            print("\n[!] Pembayaran dibatalkan")
            print("\n" + "="*50)
            return
    
    print("\n" + "="*50)
    print(" "*18 + "SELESAI")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()