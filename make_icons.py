#!/usr/bin/env python3
"""Generate simple hinomaru (Japan flag) PNG icons — pure stdlib, no Pillow."""
import struct, zlib, math

def png(path, size, bg=(247, 243, 233), fg=(188, 0, 45), radius_frac=0.32):
    cx = cy = (size - 1) / 2
    r = size * radius_frac
    rows = bytearray()
    for y in range(size):
        rows.append(0)  # filter type 0 for each scanline
        for x in range(size):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                rows += bytes(fg)
            else:
                rows += bytes(bg)
    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data +
                struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)  # 8-bit RGB
    idat = zlib.compress(bytes(rows), 9)
    with open(path, "wb") as f:
        f.write(sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b""))
    print("wrote", path)

if __name__ == "__main__":
    import os
    d = os.path.join(os.path.dirname(__file__), "icons")
    png(os.path.join(d, "icon-180.png"), 180)
    png(os.path.join(d, "icon-192.png"), 192)
    png(os.path.join(d, "icon-512.png"), 512)
    # maskable: smaller circle so safe-zone cropping keeps the sun whole
    png(os.path.join(d, "icon-512-maskable.png"), 512, radius_frac=0.26)
