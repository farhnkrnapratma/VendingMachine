"""Handler perintah untuk aplikasi CLI"""
from .api_client import FSAClient
from .display import (
    console, display_fsa_info, display_states_list, display_state_details,
    display_process_result, print_success, print_error, print_info, print_warning
)
from .interactive import InteractiveTransaction


def cmd_interactive_mode(client: FSAClient):
    """Mulai mode transaksi interaktif"""
    transaction = InteractiveTransaction(client)
    transaction.run()


def cmd_test_string(client: FSAClient):
    """Uji string input"""
    console.print("\n[bold cyan]Uji String Input[/bold cyan]\n")
    console.print("[dim]Masukkan string simbol untuk diuji (contoh: 'abdgjlrtu')[/dim]")
    console.print("[dim]Kosongkan untuk membatalkan[/dim]\n")
    
    input_str = console.input("[bold]String input: [/bold]").strip()
    
    if not input_str:
        print_warning("Dibatalkan")
        return
    
    try:
        console.print(f"\n[cyan]Memproses string: {input_str}[/cyan]\n")
        result = client.process_string(input_str)
        display_process_result(result)
    except Exception as e:
        print_error(f"Error saat memproses string: {str(e)}")


def cmd_view_info(client: FSAClient):
    """Lihat informasi FSA"""
    console.print()
    try:
        info = client.get_info()
        display_fsa_info(info)
    except Exception as e:
        print_error(f"Error saat mengambil info FSA: {str(e)}")


def cmd_list_states(client: FSAClient):
    """Daftar semua state"""
    console.print()
    try:
        states = client.get_states()
        display_states_list(states)
    except Exception as e:
        print_error(f"Error saat mengambil daftar state: {str(e)}")


def cmd_view_state(client: FSAClient):
    """Lihat detail state"""
    console.print("\n[bold cyan]Lihat Detail State[/bold cyan]\n")
    
    state = console.input("[bold]Masukkan nama state (contoh: q0): [/bold]").strip()
    
    if not state:
        print_warning("Dibatalkan")
        return
    
    try:
        console.print()
        details = client.get_state_details(state)
        display_state_details(details)
    except Exception as e:
        print_error(f"Error saat mengambil detail state: {str(e)}")


def cmd_run_examples(client: FSAClient):
    """Jalankan contoh tes yang telah didefinisikan"""
    console.print("\n[bold cyan]═══ Contoh Tes ═══[/bold cyan]\n")
    
    examples = [
        ("abdgjlrtu", "Pembayaran non-tunai, saldo cukup"),
        ("abcehkmstu", "Pembayaran tunai (5K), nominal pas"),
        ("abcfikmstu", "Pembayaran tunai (10K), ada kembalian"),
        ("abdgjknpgjlrtu", "Non-tunai dengan percobaan ulang karena saldo kurang"),
        ("abcehkmoqehkmstu", "Tunai 5K dengan percobaan ulang"),
        ("abcfikmoqfikmstu", "Tunai 10K dengan percobaan ulang"),
    ]
    
    from rich.table import Table
    from rich import box
    
    table = Table(title="Kasus Tes yang Tersedia", box=box.ROUNDED, border_style="cyan")
    table.add_column("#", style="cyan bold", width=6)
    table.add_column("String Input", style="yellow", width=20)
    table.add_column("Deskripsi", style="white", width=40)
    
    for i, (input_str, desc) in enumerate(examples, 1):
        table.add_row(str(i), input_str, desc)
    
    table.add_row("0", "Jalankan Semua", "Eksekusi semua kasus tes")
    
    console.print(table)
    console.print()
    
    try:
        choice = console.input("[bold cyan]Pilih kasus tes (atau 'q' untuk batal): [/bold cyan]")
        
        if choice.lower() == 'q':
            print_warning("Dibatalkan")
            return
        
        choice_num = int(choice)
        
        if choice_num == 0:
            for i, (input_str, desc) in enumerate(examples, 1):
                console.print(f"\n[bold cyan]═══ Kasus Tes {i}: {desc} ═══[/bold cyan]\n")
                result = client.process_string(input_str)
                display_process_result(result)
                console.print()
        elif 1 <= choice_num <= len(examples):
            input_str, desc = examples[choice_num - 1]
            console.print(f"\n[bold cyan]═══ {desc} ═══[/bold cyan]\n")
            result = client.process_string(input_str)
            display_process_result(result)
        else:
            print_error("Pilihan tidak valid")
    except ValueError:
        print_error("Silakan masukkan angka yang valid")
    except Exception as e:
        print_error(f"Error saat menjalankan tes: {str(e)}")


def cmd_help(client: FSAClient):
    """Tampilkan bantuan dan dokumentasi"""
    from rich.panel import Panel
    
    help_text = """
[bold cyan]Vending Machine Minuman Boba[/bold cyan]

[bold yellow]Apa ini?[/bold yellow]
Ini adalah simulator interaktif untuk mesin vending minuman boba yang berbasis
teori Finite State Automata (FSA). Program ini mendemonstrasikan bagaimana FSA
dapat memodelkan sistem transaksi di dunia nyata.

[bold yellow]Cara menggunakan:[/bold yellow]

[bold]1. Mode Interaktif[/bold] - Cocok untuk pengguna pertama kali!
   Ikuti transaksi langkah demi langkah dengan panduan yang jelas.
   Pilih opsi untuk berpindah antar state.

[bold]2. Mode Uji String[/bold] - Untuk pengguna yang sudah terbiasa
   Masukkan urutan simbol secara langsung (misalnya: 'abdgjlrtu')
   Lihat jalur transaksi lengkap sekaligus.

[bold yellow]Simbol yang Tersedia:[/bold yellow]
  a = Mulai transaksi                n = Batalkan transaksi
  b = Pilih produk                   o = Uang tidak cukup, batalkan
  c = Pilih metode pembayaran        p = Kembalikan uang non-tunai
  d = Pembayaran non-tunai           q = Kembali input uang
  e = Masukkan Rp 5.000              r = Hitung kembalian
  f = Masukkan Rp 10.000             s = Lanjutkan (tidak ada kembalian)
  g = Proses pembayaran non-tunai    t = Ada kembalian
  h = Scan kode QR                   u = Keluarkan kembalian
  i = Tambah Rp 10.000               1 = Tambah Rp 5.000 (tambahan)
  j = Cek saldo                      2 = Tambah Rp 10.000 (tambahan)
  k = Lanjutkan pengecekan
  l = Saldo cukup, lanjutkan
  m = Proses pembayaran

[bold yellow]Tips:[/bold yellow]
• Harga produk selalu Rp 15.000
• Mulai dengan Mode Interaktif untuk memahami alurnya
• Gunakan Mode Uji String untuk validasi urutan tertentu
• Lihat contoh untuk jalur transaksi yang valid

[bold yellow]State FSA:[/bold yellow]
Mesin memiliki 18 state (q0 sampai q17), dimulai dari q0 (State Awal) 
dan berakhir di q17 (Transaksi Selesai).
    """
    
    console.print(Panel(help_text, border_style="cyan", padding=(1, 2)))
