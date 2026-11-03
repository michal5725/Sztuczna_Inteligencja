from collections import deque
import time
import random
import matplotlib.pyplot as plt

def pobierz_sasiadow(stan, wiersze, kolumny, labirynt):
    w, k = stan
    kierunki = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    sasiedzi = []
    
    for dw, dk in kierunki:
        nw, nk = w + dw, k + dk
        if 0 <= nw < wiersze and 0 <= nk < kolumny:
            if labirynt[nw][nk] == 0:
                sasiedzi.append((nw, nk))
                
    return sasiedzi

def rozwiaz_labirynt(labirynt, start, cel, algorytm='BFS'):
    wiersze = len(labirynt)
    kolumny = len(labirynt[0])
    
    czas_start = time.perf_counter()
    
    odwiedzone = set()
    rodzic = {start: None}
    
    if algorytm == 'BFS':
        struktura_otwartych = deque([start])
    else:
        struktura_otwartych = [start]
        
    zbior_otwartych = {start}
    maks_rozmiar_otwartych = len(struktura_otwartych)
    
    znaleziono = False
    stan_celu = None
    
    while struktura_otwartych:
        maks_rozmiar_otwartych = max(maks_rozmiar_otwartych, len(struktura_otwartych))
        
        if algorytm == 'BFS':
            obecny = struktura_otwartych.popleft()
        else:
            obecny = struktura_otwartych.pop()
            
        zbior_otwartych.remove(obecny)
        
        if obecny == cel:
            znaleziono = True
            stan_celu = obecny
            break
            
        odwiedzone.add(obecny)
        
        for sasiad in pobierz_sasiadow(obecny, wiersze, kolumny, labirynt):
            if sasiad not in odwiedzone and sasiad not in zbior_otwartych:
                rodzic[sasiad] = obecny
                struktura_otwartych.append(sasiad)
                zbior_otwartych.add(sasiad)
                
    czas_koniec = time.perf_counter()
    czas_wykonania = czas_koniec - czas_start
    
    sciezka = []
    if znaleziono:
        biezacy = stan_celu
        while biezacy is not None:
            sciezka.append(biezacy)
            biezacy = rodzic[biezacy]
        sciezka.reverse()
        
    statystyki = {
        'algorytm': algorytm,
        'znaleziono': znaleziono,
        'dlugosc_sciezki': len(sciezka) if znaleziono else 0,
        'rozmiar_zamknietych': len(odwiedzone),
        'rozmiar_otwartych_koniec': len(zbior_otwartych),
        'maks_rozmiar_otwartych': maks_rozmiar_otwartych,
        'czas_wykonania': czas_wykonania,
        'sciezka': sciezka
    }
    
    return statystyki

def generuj_losowy_labirynt(wiersze, kolumny, gestosc_przeszkod):
    while True:
        labirynt = [[1 if random.random() < gestosc_przeszkod else 0 for _ in range(kolumny)] for _ in range(wiersze)]
        start = (0, 0)
        cel = (wiersze - 1, kolumny - 1)
        
        labirynt[start[0]][start[1]] = 0
        labirynt[cel[0]][cel[1]] = 0
        
        wynik_testu = rozwiaz_labirynt(labirynt, start, cel, 'BFS')
        if wynik_testu['znaleziono']:
            return labirynt, start, cel

def uruchom_eksperyment():
    random.seed(42)
    
    gestosci = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    powtorzenia = 20
    
    czas_bfs, czas_dfs = [], []
    odwiedzone_bfs, odwiedzone_dfs = [], []
    dl_sciezki_bfs, dl_sciezki_dfs = [], []
    maks_otwarte_bfs, maks_otwarte_dfs = [], []
    
    for g in gestosci:
        cz_bfs, cz_dfs = 0, 0
        odw_bfs, odw_dfs = 0, 0
        dl_bfs, dl_dfs = 0, 0
        mo_bfs, mo_dfs = 0, 0
        
        for _ in range(powtorzenia):
            labirynt, start, cel = generuj_losowy_labirynt(15, 15, g)
            
            wynik_bfs = rozwiaz_labirynt(labirynt, start, cel, 'BFS')
            wynik_dfs = rozwiaz_labirynt(labirynt, start, cel, 'DFS')
            
            cz_bfs += wynik_bfs['czas_wykonania']; cz_dfs += wynik_dfs['czas_wykonania']
            odw_bfs += wynik_bfs['rozmiar_zamknietych']; odw_dfs += wynik_dfs['rozmiar_zamknietych']
            dl_bfs += wynik_bfs['dlugosc_sciezki']; dl_dfs += wynik_dfs['dlugosc_sciezki']
            mo_bfs += wynik_bfs['maks_rozmiar_otwartych']; mo_dfs += wynik_dfs['maks_rozmiar_otwartych']
            
        czas_bfs.append(cz_bfs / powtorzenia); czas_dfs.append(cz_dfs / powtorzenia)
        odwiedzone_bfs.append(odw_bfs / powtorzenia); odwiedzone_dfs.append(odw_dfs / powtorzenia)
        dl_sciezki_bfs.append(dl_bfs / powtorzenia); dl_sciezki_dfs.append(dl_dfs / powtorzenia)
        maks_otwarte_bfs.append(mo_bfs / powtorzenia); maks_otwarte_dfs.append(mo_dfs / powtorzenia)
        
    plt.figure(figsize=(12, 10))
    
    plt.subplot(2, 2, 1)
    plt.plot(gestosci, czas_bfs, label='BFS', marker='o')
    plt.plot(gestosci, czas_dfs, label='DFS', marker='s')
    plt.title('Czas wykonania')
    plt.xlabel('Gęstość przeszkód'); plt.ylabel('Czas [s]')
    plt.legend(); plt.grid(True)
    
    plt.subplot(2, 2, 2)
    plt.plot(gestosci, odwiedzone_bfs, label='BFS', marker='o')
    plt.plot(gestosci, odwiedzone_dfs, label='DFS', marker='s')
    plt.title('Liczba stanów odwiedzonych (Closed)')
    plt.xlabel('Gęstość przeszkód'); plt.ylabel('Liczba stanów')
    plt.legend(); plt.grid(True)
    
    plt.subplot(2, 2, 3)
    plt.plot(gestosci, dl_sciezki_bfs, label='BFS', marker='o')
    plt.plot(gestosci, dl_sciezki_dfs, label='DFS', marker='s')
    plt.title('Długość znalezionej ścieżki')
    plt.xlabel('Gęstość przeszkód'); plt.ylabel('Liczba kroków')
    plt.legend(); plt.grid(True)
    
    plt.subplot(2, 2, 4)
    plt.plot(gestosci, maks_otwarte_bfs, label='BFS', marker='o')
    plt.plot(gestosci, maks_otwarte_dfs, label='DFS', marker='s')
    plt.title('Maksymalny rozmiar Open (Pamięć)')
    plt.xlabel('Gęstość przeszkód'); plt.ylabel('Rozmiar Open')
    plt.legend(); plt.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    wiersze, kolumny = 20, 20
    gestosc = 0.2
    
    print(f"Generowanie labiryntu {wiersze}x{kolumny} (gęstość ścian: {gestosc*100}%)...")
    labirynt, start, cel = generuj_losowy_labirynt(wiersze, kolumny, gestosc)
    
    statystyki_bfs = rozwiaz_labirynt(labirynt, start, cel, 'BFS')
    statystyki_dfs = rozwiaz_labirynt(labirynt, start, cel, 'DFS')
    
    for statystyki in [statystyki_bfs, statystyki_dfs]:
        print(f"\n--- Wyniki dla {statystyki['algorytm']} ---")
        if statystyki['znaleziono']:
            print("Znaleziono rozwiązanie!")
            print(f"Długość ścieżki (kroki): {statystyki['dlugosc_sciezki']}")
            print(f"Liczba odwiedzonych stanów (Closed): {statystyki['rozmiar_zamknietych']}")
            print(f"Maksymalny rozmiar Open (pamięć): {statystyki['maks_rozmiar_otwartych']}")
            print(f"Czas wykonania: {statystyki['czas_wykonania']:.6f} s")
            
            print(f"Ścieżka: {statystyki['sciezka']}")
        else:
            print("Nie znaleziono ścieżki do celu!")
            
    print("\nRozpoczynanie eksperymentu z wykresami...")
    uruchom_eksperyment()