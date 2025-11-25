"""Utilitas tampilan menggunakan library Rich untuk output terminal yang menarik"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree
from rich.layout import Layout
from rich.live import Live
from rich import box
from typing import Dict, Any, List


console = Console()


def print_header():
    """Tampilkan header aplikasi"""
    header = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║           🧋  Vending Machine Minuman Boba  🧋           ║
    ║                                                          ║
    ║         Implementasi Finite State Automata (FSA)         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    console.print(header, style="bold cyan")


def print_welcome():
    """Tampilkan pesan selamat datang"""
    console.print("\n[bold green]Selamat datang di Mesin Vending Boba![/bold green]")
    console.print("[dim]Simulator transaksi interaktif berbasis FSA[/dim]\n")


def print_menu():
    """Tampilkan menu utama"""
    menu = Table(show_header=False, box=box.ROUNDED, border_style="cyan")
    menu.add_column("Opsi", style="cyan bold", width=8)
    menu.add_column("Keterangan", style="white")
    
    menu.add_row("1", "🛒 Mulai Transaksi (Mode Interaktif)")
    menu.add_row("2", "🧪 Uji String Input")
    menu.add_row("3", "📊 Lihat Informasi FSA")
    menu.add_row("4", "📝 Daftar Semua State")
    menu.add_row("5", "🔍 Detail State")
    menu.add_row("6", "✨ Jalankan Contoh Tes")
    menu.add_row("7", "❓ Bantuan & Dokumentasi")
    menu.add_row("0", "🚪 Keluar")
    
    console.print(menu)
    console.print()


def print_success(message: str):
    """Cetak pesan sukses"""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_error(message: str):
    """Cetak pesan error"""
    console.print(f"[bold red]✗[/bold red] {message}")


def print_info(message: str):
    """Cetak pesan info"""
    console.print(f"[bold blue]ℹ[/bold blue] {message}")


def print_warning(message: str):
    """Cetak pesan peringatan"""
    console.print(f"[bold yellow]⚠[/bold yellow] {message}")


def display_fsa_info(info: Dict[str, Any]):
    """Tampilkan informasi konfigurasi FSA"""
    panel_content = f"""
[bold cyan]Tipe FSA:[/bold cyan] {info['type']}
[bold cyan]State Awal:[/bold cyan] {info['initialState']}
[bold cyan]State Akhir:[/bold cyan] {', '.join(info['finalStates'])}
[bold cyan]Jumlah State:[/bold cyan] {info['totalStates']}
[bold cyan]Ukuran Alfabet:[/bold cyan] {info['alphabetSize']}
[bold cyan]Simbol:[/bold cyan] {', '.join(info['alphabet'])}
    """
    console.print(Panel(panel_content, title="Konfigurasi FSA", border_style="cyan"))


def display_states_list(states: List[Dict[str, Any]]):
    """Tampilkan daftar semua state"""
    table = Table(title="Daftar State FSA", box=box.ROUNDED, border_style="cyan")
    table.add_column("State", style="cyan bold", width=10)
    table.add_column("Deskripsi", style="white", width=35)
    table.add_column("Tipe", style="yellow", width=15)
    
    for state in states:
        state_type = []
        if state['isInitial']:
            state_type.append("Awal")
        if state['isFinal']:
            state_type.append("Akhir")
        if not state_type:
            state_type.append("-")
        
        table.add_row(
            state['state'],
            state['description'],
            ", ".join(state_type)
        )
    
    console.print(table)


def display_state_details(details: Dict[str, Any]):
    """Tampilkan informasi detail state"""
    state_info = f"""
[bold cyan]State:[/bold cyan] {details['state']}
[bold cyan]Deskripsi:[/bold cyan] {details['description']}
[bold cyan]State Awal:[/bold cyan] {'Ya' if details['isInitial'] else 'Tidak'}
[bold cyan]State Akhir:[/bold cyan] {'Ya' if details['isFinal'] else 'Tidak'}
    """
    console.print(Panel(state_info, title=f"Detail State {details['state']}", border_style="cyan"))
    
    if details['availableTransitions']:
        table = Table(title="Transisi yang Tersedia", box=box.ROUNDED, border_style="green")
        table.add_column("Simbol", style="yellow bold", width=10)
        table.add_column("State Tujuan", style="cyan", width=12)
        table.add_column("Deskripsi", style="white", width=40)
        
        for trans in details['availableTransitions']:
            table.add_row(trans['symbol'], trans['nextState'], trans['description'])
        
        console.print(table)
    else:
        print_info("Tidak ada transisi dari state ini")


def display_process_result(result: Dict[str, Any]):
    """Tampilkan hasil pemrosesan string input"""
    if result['accepted']:
        console.print(Panel(
            f"[bold green]✓ Transaksi Berhasil Diselesaikan![/bold green]\n\n"
            f"[cyan]String Input:[/cyan] {result['inputString']}\n"
            f"[cyan]State Akhir:[/cyan] {result['finalState']}\n"
            f"[cyan]Total Langkah:[/cyan] {len(result['transitions'])}",
            title="Berhasil",
            border_style="green"
        ))
    else:
        console.print(Panel(
            f"[bold red]✗ Transaksi Gagal[/bold red]\n\n"
            f"[cyan]String Input:[/cyan] {result['inputString']}\n"
            f"[cyan]Berhenti di:[/cyan] {result['finalState']}\n"
            f"[yellow]Alasan:[/yellow] Urutan transisi tidak valid",
            title="Ditolak",
            border_style="red"
        ))
    
    # Tampilkan jalur transisi
    table = Table(title="Jalur Transaksi", box=box.ROUNDED, border_style="cyan")
    table.add_column("Langkah", style="dim", width=6)
    table.add_column("State", style="cyan bold", width=8)
    table.add_column("Simbol", style="yellow", width=8)
    table.add_column("State Tujuan", style="green", width=12)
    table.add_column("Valid", style="white", width=8)
    
    for i, trans in enumerate(result['transitions'], 1):
        valid_str = "✓" if trans['isValid'] else "✗"
        valid_style = "green" if trans['isValid'] else "red"
        
        table.add_row(
            str(i),
            trans['currentState'],
            trans['inputSymbol'],
            trans['nextState'] if trans['nextState'] else "N/A",
            f"[{valid_style}]{valid_str}[/{valid_style}]"
        )
    
    console.print(table)


def display_transaction_state(state: str, description: str, balance: int = 0, price: int = 15000):
    """Tampilkan status transaksi saat ini dalam mode interaktif"""
    panel = Panel(
        f"[bold cyan]State Saat Ini:[/bold cyan] {state}\n"
        f"[bold white]{description}[/bold white]\n\n"
        f"[yellow]Harga Produk:[/yellow] Rp {price:,}\n"
        f"[green]Saldo Saat Ini:[/green] Rp {balance:,}",
        title="🧋 Status Mesin Boba",
        border_style="cyan"
    )
    console.print(panel)


def display_transition_options(transitions: List[Dict[str, str]]):
    """Tampilkan opsi transisi yang tersedia"""
    if not transitions:
        print_warning("Tidak ada aksi yang tersedia dari state ini")
        return
    
    table = Table(title="Aksi yang Tersedia", box=box.ROUNDED, border_style="green")
    table.add_column("Opsi", style="cyan bold", width=10)
    table.add_column("Simbol", style="yellow", width=10)
    table.add_column("Deskripsi", style="white", width=50)
    
    for i, trans in enumerate(transitions, 1):
        table.add_row(str(i), trans['symbol'], trans['description'])
    
    console.print(table)
