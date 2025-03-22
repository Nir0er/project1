from scapy.all import rdpcap, IP
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

pcap_file = "traffic1.pcapng"

packets = rdpcap(pcap_file)

data = []
for pkt in packets:
    if IP in pkt:
        data.append({
            "src_ip": pkt[IP].src,
            "dst_ip": pkt[IP].dst,
            "size": len(pkt)
        })

traffic_df = pd.DataFrame(data)

plt.figure(figsize=(10, 5))
plt.hist(traffic_df["size"], bins=30, edgecolor="black", alpha=0.7)
plt.xlabel("Размер пакетов (байты)")
plt.ylabel("Частота")
plt.title("Распределение размеров пакетов")
plt.grid(True)
plt.show()

G = nx.DiGraph()
for index, row in traffic_df.iterrows():
    G.add_edge(row["src_ip"], row["dst_ip"], weight=row["size"])

plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)  # Упорядоченное расположение
nx.draw(G, pos, with_labels=True, node_size=700, node_color="lightblue", edge_color="gray", font_size=8, alpha=0.7)
plt.title("Граф соединений между IP-адресами")
plt.show()

traffic_by_ip = traffic_df.groupby("src_ip")["size"].sum().sort_values(ascending=False)

plt.figure(figsize=(12, 6))
traffic_by_ip.plot(kind="bar", color="royalblue", alpha=0.7)
plt.xlabel("IP-адрес")
plt.ylabel("Суммарный объем трафика (байты)")
plt.title("Распределение трафика по IP-адресам")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()