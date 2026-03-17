import os
import time
import sys

# --- ANSI Color Codes untuk Terminal ---
RESET = '\033[0m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
GRAY = '\033[90m'

# Simbol untuk visualisasi
WALL_CHAR = '█'
OPEN_CHAR = ' '
PATH_CHAR = f'{YELLOW}*{RESET}'
BACKTRACK_CHAR = f'{GRAY}x{RESET}'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_maze(maze, step, action):
    """Menampilkan labirin ke terminal dengan animasi"""
    clear_screen()
    print(f"{CYAN}=== BACKTRACKING MAZE SOLVER ==={RESET}")
    print(f"Langkah : {step}")
    print(f"Status  : {action}\n")
    
    for row in maze:
        line = ""
        for cell in row:
            if cell == '#':
                line += WALL_CHAR * 2
            elif cell == '.':
                line += OPEN_CHAR * 2
            elif cell == 'S':
                line += f"{GREEN}SS{RESET}"
            elif cell == 'E':
                line += f"{RED}EE{RESET}"
            elif cell == '*':
                line += PATH_CHAR * 2
            elif cell == 'x':
                line += BACKTRACK_CHAR * 2
            else:
                line += cell * 2
        print(line)
    print("\n" + "="*32)

def solve_maze(maze, r, c, end_r, end_c, speed, step_counter):
    """Fungsi rekursif backtracking"""
    # Base Case: Jika mencapai End
    if r == end_r and c == end_c:
        return True

    # Tandai jalur saat ini (kecuali posisi Start)
    if maze[r][c] not in ('S', 'E'):
        maze[r][c] = '*'
    
    step_counter[0] += 1
    print_maze(maze, step_counter[0], f"Mencoba rute di ({r}, {c})")
    time.sleep(speed)

    # 4 Arah: Atas, Bawah, Kiri, Kanan
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        
        # Cek batas dan apakah sel bisa dilewati (bukan tembok '#', bukan jalur '*', bukan backtrack 'x')
        if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]):
            if maze[nr][nc] in ('.', 'E'):
                if solve_maze(maze, nr, nc, end_r, end_c, speed, step_counter):
                    return True # Solusi ditemukan

    # JIKA JALAN BUNTU -> BACKTRACK
    if maze[r][c] not in ('S', 'E'):
        maze[r][c] = 'x' # Tandai sebagai jalan buntu
    
    step_counter[0] += 1
    print_maze(maze, step_counter[0], f"{RED}JALAN BUNTU! Backtrack dari ({r}, {c}){RESET}")
    time.sleep(speed)
    
    return False

def get_preset_maze(level):
    if level == 1: # Easy (5x5)
        return [
            list("S...#"),
            list("###.#"),
            list("#...#"),
            list("#.###"),
            list("#...E")
        ]
    elif level == 2: # Medium (9x9)
        return [
            list("S.......#"),
            list("#######.#"),
            list("#.......#"),
            list("#.#######"),
            list("#...#...#"),
            list("###.#.#.#"),
            list("#...#.#.#"),
            list("#.###.###"),
            list("#.......E")
        ]
    else: # Hard (13x13)
        return [
            list("S...#.......#"),
            list("###.#.#####.#"),
            list("#...#.#...#.#"),
            list("#.###.#.#.#.#"),
            list("#.......#...#"),
            list("#######.###.#"),
            list("#.....#.#...#"),
            list("#.###.###.###"),
            list("#.#.........#"),
            list("#.#.#######.#"),
            list("#.#.......#.#"),
            list("#.#######.#.#"),
            list("#.........#.E")
        ]

def input_custom_maze():
    print("\nMasukkan Custom Maze Anda.")
    print("Gunakan format:")
    print("  'S' untuk Start")
    print("  'E' untuk End")
    print("  '#' untuk Tembok")
    print("  '.' untuk Jalan")
    print("Ketik 'DONE' di baris baru jika sudah selesai.\n")
    
    maze = []
    while True:
        line = input()
        if line.strip().upper() == 'DONE':
            break
        maze.append(list(line.strip()))
    
    # Validasi sederhana
    if not maze or len(maze[0]) == 0:
        print("Maze kosong! Menggunakan maze default.")
        return get_preset_maze(1)
    return maze

def main():
    clear_screen()
    print("=== SETUP VISUALISASI MAZE ===")
    print("1. Pilih Kompleksitas:")
    print("   [1] Mudah (5x5)")
    print("   [2] Sedang (9x9)")
    print("   [3] Sulit (13x13)")
    print("   [4] Masukkan Custom Maze")
    
    try:
        choice = int(input("Pilihan Anda (1-4): "))
    except:
        choice = 1

    if choice == 4:
        maze = input_custom_maze()
    else:
        maze = get_preset_maze(choice if choice in [1, 2, 3] else 1)

    print("\n2. Pilih Kecepatan Animasi:")
    print("   [1] Cepat (0.05 detik/langkah)")
    print("   [2] Normal (0.2 detik/langkah)")
    print("   [3] Lambat (0.5 detik/langkah)")
    
    try:
        speed_choice = int(input("Pilihan Anda (1-3): "))
    except:
        speed_choice = 2

    speeds = {1: 0.05, 2: 0.2, 3: 0.5}
    speed = speeds.get(speed_choice, 0.2)

    # Cari koordinat Start (S) dan End (E)
    start_pos = end_pos = None
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == 'S': start_pos = (r, c)
            if maze[r][c] == 'E': end_pos = (r, c)

    if not start_pos or not end_pos:
        print("Error: Maze harus memiliki karakter 'S' dan 'E'.")
        return

    input("\nTekan ENTER untuk memulai visualisasi...")
    
    step_counter = [0]
    is_solved = solve_maze(maze, start_pos[0], start_pos[1], end_pos[0], end_pos[1], speed, step_counter)

    print_maze(maze, step_counter[0], "SELESAI")
    if is_solved:
        print(f"{GREEN}Solusi Ditemukan!{RESET}")
    else:
        print(f"{RED}Tidak ada jalan menuju End.{RESET}")

if __name__ == "__main__":
    main()
    