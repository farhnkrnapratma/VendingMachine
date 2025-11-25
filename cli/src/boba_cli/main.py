"""Titik masuk utama aplikasi CLI"""
import sys
from .api_client import FSAClient
from .display import (
    console, print_header, print_welcome, print_menu,
    print_success, print_error, print_info, print_warning
)
from .commands import (
    cmd_interactive_mode, cmd_test_string, cmd_view_info,
    cmd_list_states, cmd_view_state, cmd_run_examples, cmd_help
)


def check_api_connection(client: FSAClient) -> bool:
    """Cek apakah API backend dapat diakses"""
    console.print("[dim]Memeriksa koneksi API...[/dim]")
    
    if client.health_check():
        print_success("Terhubung ke backend API")
        return True
    else:
        print_error("Tidak dapat terhubung ke backend API di http://localhost:3000")
        print_warning("Pastikan server backend sudah berjalan:")
        console.print("  [cyan]cd backend && bun run start[/cyan]\n")
        return False


def main_loop(client: FSAClient):
    """Loop aplikasi utama"""
    commands = {
        '1': cmd_interactive_mode,
        '2': cmd_test_string,
        '3': cmd_view_info,
        '4': cmd_list_states,
        '5': cmd_view_state,
        '6': cmd_run_examples,
        '7': cmd_help,
    }
    
    while True:
        print_menu()
        
        try:
            choice = console.input("[bold cyan]Masukkan pilihan Anda: [/bold cyan]").strip()
            
            if choice == '0':
                console.print("\n[bold green]Terima kasih telah menggunakan Mesin Vending Boba! 👋[/bold green]")
                console.print("[dim]Sampai jumpa lagi! 🧋[/dim]\n")
                break
            elif choice in commands:
                commands[choice](client)
                console.print()
            else:
                print_error("Pilihan tidak valid. Silakan pilih opsi yang tersedia.")
                console.print()
        except KeyboardInterrupt:
            console.print("\n\n[bold yellow]Diinterupsi oleh pengguna[/bold yellow]")
            console.print("[dim]Kembali ke menu utama...[/dim]\n")
        except Exception as e:
            print_error(f"Terjadi kesalahan: {str(e)}")
            console.print()


def main():
    """Titik masuk aplikasi"""
    print_header()
    print_welcome()
    
    client = FSAClient()
    
    if not check_api_connection(client):
        sys.exit(1)
    
    console.print()
    
    try:
        main_loop(client)
    except Exception as e:
        print_error(f"Kesalahan fatal: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
