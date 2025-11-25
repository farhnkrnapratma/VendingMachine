#!/usr/bin/env python3
"""Skrip demo untuk menampilkan kemampuan CLI"""
import time
import sys
from src.boba_cli.api_client import FSAClient
from src.boba_cli.display import console, print_success, print_info, print_header


def demo():
    """Jalankan demonstrasi CLI"""
    print_header()
    console.print("\n[bold cyan]Menjalankan demo otomatis...[/bold cyan]\n")
    
    client = FSAClient()
    
    print_info("Memeriksa koneksi API...")
    if not client.health_check():
        console.print("[red]Backend tidak berjalan. Silakan jalankan terlebih dahulu.[/red]")
        sys.exit(1)
    print_success("Terhubung ke backend API\n")
    
    time.sleep(1)
    
    console.print("[bold yellow]Demo 1: Konfigurasi FSA[/bold yellow]")
    info = client.get_info()
    console.print(f"  Jumlah State: {info['totalStates']}")
    console.print(f"  State Awal: {info['initialState']}")
    console.print(f"  State Akhir: {', '.join(info['finalStates'])}")
    console.print(f"  Ukuran Alfabet: {info['alphabetSize']}\n")
    time.sleep(2)
    
    console.print("[bold yellow]Demo 2: Memproses Transaksi Valid[/bold yellow]")
    test_string = "abdgjlrtu"
    console.print(f"  Input: {test_string}")
    result = client.process_string(test_string)
    console.print(f"  Hasil: {'✓ Diterima' if result['accepted'] else '✗ Ditolak'}")
    console.print(f"  Jalur: {' → '.join(result['path'])}\n")
    time.sleep(2)
    
    console.print("[bold yellow]Demo 3: Menampilkan Daftar State[/bold yellow]")
    states = client.get_states()
    console.print(f"  Ditemukan {len(states)} state")
    for state in states[:5]:
        console.print(f"    {state['state']}: {state['description']}")
    console.print("    ...\n")
    time.sleep(2)
    
    console.print("[bold green]Demo selesai! 🎉[/bold green]")
    console.print("\n[dim]Jalankan 'uv run python main.py' untuk menggunakan CLI interaktif[/dim]\n")


if __name__ == '__main__':
    demo()
