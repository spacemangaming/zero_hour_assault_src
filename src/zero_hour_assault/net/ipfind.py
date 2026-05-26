import pyperclip

with open("access.log.4", "r") as f:
    log = f.read()

ips = {}

for line in log.split("\n"):
    if not line.strip():
        continue
    ip = line.split(" - ")[0]
    if ip in ("127.0.0.1", "::1"):
        continue
    ips[ip] = ips.get(ip, 0) + 1  # Daha kısa bir sayaç artırma yöntemi

# IP'leri bağlantı sayısına göre büyükten küçüğe sırala
sorted_ips = sorted(ips.items(), key=lambda x: x[1], reverse=True)

out = "\n".join(f"{ip}, {count}" for ip, count in sorted_ips)
pyperclip.copy(out)
