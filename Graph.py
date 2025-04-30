# graf_random_jarak.py

import networkx as nx
import matplotlib.pyplot as plt
import random

class RuteDaerah:
    def __init__(self):
        self.G = nx.Graph()

    def tambah_jalan(self, u, v, jarak=None):
        if jarak is None:
            jarak = random.randint(1, 20)  # Random jarak antara 1 dan 20
        self.G.add_edge(u, v, weight=jarak)

    def cari_rute_terpendek(self, asal, tujuan):
        try:
            rute = nx.dijkstra_path(self.G, asal, tujuan, weight='weight')
            jarak = nx.dijkstra_path_length(self.G, asal, tujuan, weight='weight')
            return rute, jarak
        except nx.NetworkXNoPath:
            return None, None

    def cari_rute_terpanjang(self, asal, tujuan):
        semua_rute = list(nx.all_simple_paths(self.G, source=asal, target=tujuan))
        max_jarak = 0
        rute_terpanjang = None
        for rute in semua_rute:
            jarak = sum(self.G[rute[i]][rute[i + 1]]['weight'] for i in range(len(rute) - 1))
            if jarak > max_jarak:
                max_jarak = jarak
                rute_terpanjang = rute
        return rute_terpanjang, max_jarak

    def tampilkan_graf(self, highlight=None, judul="Graf Daerah"):
        pos = nx.spring_layout(self.G, seed=42)
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        warna_node = ['orange' if highlight and n in highlight else 'skyblue' for n in self.G.nodes()]
        plt.figure(figsize=(10, 6))
        nx.draw(self.G, pos, with_labels=True, node_color=warna_node,
                node_size=1600, font_size=11, font_weight='bold', edge_color='gray')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        plt.title(judul)
        plt.show()

# --- Main Program ---

if __name__ == "__main__":
    graf = RuteDaerah()

    edge_list = [
        ("A", "B"),
        ("A", "D"),
        ("A", "E"),
        ("B", "C"),
        ("C", "Z"),
        ("C", "D"),
        ("D", "Z"),
        ("D", "G"),
        ("D", "E"),
        ("E", "F"),
        ("F", "G"),
        ("G", "Z"),
    ]

    for u, v in edge_list:
        graf.tambah_jalan(u, v)

    graf.tampilkan_graf(judul="Graf Daerah (Jarak Random)")

    asal = input("Masukkan titik asal (misal: A): ").strip().upper()
    while asal not in graf.G.nodes():
        print(f"Titik asal '{asal}' tidak valid.")
        asal = input("Masukkan titik asal (misal: A): ").strip().upper()
    tujuan = input("Masukkan titik tujuan (misal: Z): ").strip().upper()
    while tujuan not in graf.G.nodes():
        print(f"Titik tujuan '{tujuan}' tidak valid.")
        tujuan = input("Masukkan titik tujuan (misal: Z): ").strip().upper()

    rute_pendek, jarak_pendek = graf.cari_rute_terpendek(asal, tujuan)
    print(f"🔵 Rute Terpendek {asal} → {tujuan}: {' -> '.join(rute_pendek)} ({jarak_pendek} km)")
    graf.tampilkan_graf(highlight=rute_pendek, judul=f"Rute Terpendek ({jarak_pendek} km)")

    rute_panjang, jarak_panjang = graf.cari_rute_terpanjang(asal, tujuan)
    print(f"🔴 Rute Terpanjang {asal} → {tujuan}: {' -> '.join(rute_panjang)} ({jarak_panjang} km)")
    graf.tampilkan_graf(highlight=rute_panjang, judul=f"Rute Terpanjang ({jarak_panjang} km)")
