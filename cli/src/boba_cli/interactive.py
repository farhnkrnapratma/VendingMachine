"""Mode transaksi interaktif - navigasi FSA langkah demi langkah"""
from typing import Optional, Dict, Any
from .api_client import FSAClient
from .display import (
    console, display_transaction_state, display_transition_options,
    print_success, print_error, print_info, print_warning
)


SYMBOL_MEANINGS = {
    'a': ('Mulai Transaksi', 0),
    'b': ('Pilih Produk', 0),
    'c': ('Pilih Metode Pembayaran', 0),
    'd': ('Pilih Non-Tunai', 0),
    'e': ('Masukkan Uang Rp 5.000', 5000),
    'f': ('Masukkan Uang Rp 10.000', 10000),
    'g': ('Proses Pembayaran Non-Tunai', 0),
    'h': ('Scan Kode QR', 15000),
    'i': ('Tambah Uang Rp 10.000', 10000),
    'j': ('Cek Saldo', 0),
    'k': ('Lanjutkan Pengecekan', 0),
    'l': ('Saldo Cukup, Lanjutkan', 0),
    'm': ('Proses Pembayaran', 0),
    'n': ('Batalkan Transaksi', 0),
    'o': ('Uang Tidak Cukup, Batalkan', 0),
    'p': ('Kembalikan Uang Non-Tunai', 0),
    'q': ('Kembali Input Uang', 0),
    'r': ('Hitung Kembalian', 0),
    's': ('Lanjutkan (Tidak Ada Kembalian)', 0),
    't': ('Ada Kembalian', 0),
    'u': ('Keluarkan Kembalian', 0),
    '1': ('Tambah Uang Rp 5.000', 5000),
    '2': ('Tambah Uang Rp 10.000', 10000)
}


class InteractiveTransaction:
    def __init__(self, client: FSAClient):
        self.client = client
        self.current_state = 'q0'
        self.balance = 0
        self.price = 15000
        self.path = ['q0']
        self.symbols_used = []

    def get_state_description(self) -> str:
        """Dapatkan deskripsi state saat ini"""
        try:
            details = self.client.get_state_details(self.current_state)
            return details['description']
        except:
            return "State Tidak Diketahui"

    def execute_transition(self, symbol: str) -> bool:
        """Eksekusi transisi dan perbarui saldo"""
        try:
            result = self.client.execute_transition(self.current_state, symbol)
            
            if result.get('success'):
                if symbol in SYMBOL_MEANINGS:
                    _, amount = SYMBOL_MEANINGS[symbol]
                    self.balance += amount
                    if symbol == 'h':
                        self.balance = self.price
                
                self.current_state = result['transition']['to']
                self.path.append(self.current_state)
                self.symbols_used.append(symbol)
                
                print_success(f"Berpindah ke {self.current_state}: {result['transition']['toDescription']}")
                return True
            else:
                print_error("Transisi tidak valid")
                return False
        except Exception as e:
            print_error(f"Transisi gagal: {str(e)}")
            return False

    def get_available_actions(self) -> list:
        """Dapatkan transisi yang tersedia dengan deskripsi yang mudah dipahami"""
        try:
            details = self.client.get_state_details(self.current_state)
            transitions = details.get('availableTransitions', [])
            
            actions = []
            for trans in transitions:
                symbol = trans['symbol']
                if symbol in SYMBOL_MEANINGS:
                    description, amount = SYMBOL_MEANINGS[symbol]
                    if amount > 0:
                        description = f"{description} (Saldo +Rp {amount:,})"
                    actions.append({
                        'symbol': symbol,
                        'description': description,
                        'nextState': trans['nextState']
                    })
            
            return actions
        except:
            return []

    def is_final_state(self) -> bool:
        """Cek apakah state saat ini adalah state akhir"""
        return self.current_state == 'q17'

    def display_status(self):
        """Tampilkan status transaksi saat ini"""
        description = self.get_state_description()
        display_transaction_state(self.current_state, description, self.balance, self.price)

    def run(self):
        """Jalankan transaksi interaktif"""
        console.print("\n[bold cyan]═══ Memulai Transaksi Interaktif ═══[/bold cyan]\n")
        print_info(f"Harga Produk: Rp {self.price:,}")
        print_info("Ikuti petunjuk untuk menyelesaikan transaksi Anda\n")

        while not self.is_final_state():
            self.display_status()
            
            actions = self.get_available_actions()
            
            if not actions:
                print_error("Tidak ada aksi yang tersedia. Transaksi tidak dapat dilanjutkan.")
                break
            
            display_transition_options(actions)
            
            console.print()
            try:
                choice = console.input("[bold cyan]Pilih opsi (atau 'q' untuk keluar): [/bold cyan]")
                
                if choice.lower() == 'q':
                    print_warning("Transaksi dibatalkan oleh pengguna")
                    break
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(actions):
                    selected = actions[choice_num - 1]
                    console.print()
                    
                    if not self.execute_transition(selected['symbol']):
                        print_error("Gagal mengeksekusi transisi. Silakan coba lagi.")
                    
                    console.print()
                else:
                    print_error("Opsi tidak valid. Silakan coba lagi.")
            except ValueError:
                print_error("Silakan masukkan angka yang valid atau 'q' untuk keluar.")
            except KeyboardInterrupt:
                print_warning("\nTransaksi dibatalkan oleh pengguna")
                break

        if self.is_final_state():
            console.print("\n[bold green]" + "═" * 60 + "[/bold green]")
            console.print("[bold green]🎉 TRANSAKSI BERHASIL DISELESAIKAN! 🎉[/bold green]")
            console.print("[bold green]" + "═" * 60 + "[/bold green]\n")
            
            print_success(f"Boba Anda sudah siap! Selamat menikmati! 🧋")
            print_info(f"Urutan input: {''.join(self.symbols_used)}")
            print_info(f"State yang dilalui: {' → '.join(self.path)}")
            
            if self.balance > self.price:
                change = self.balance - self.price
                print_success(f"Kembalian: Rp {change:,}")
        
        console.print()
