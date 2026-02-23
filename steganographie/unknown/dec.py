import re

with open("challengefile-toprovide.pdf", "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

unicode_vals = re.findall(r'\\u(-?\d+)\?', content)

bit_map = {
    8204: "00",  # U+200C ZWNJ
    8205: "01",  # U+200D ZWJ
    8236: "10",  # U+202C PDF
    65279: "11", # U+FEFF BOM  
}

bit_string = ""
for val_str in unicode_vals:
    val = int(val_str)
    if val < 0:
        val = 65536 + val 
    if val in bit_map:
        bit_string += bit_map[val]

print(f"[*] Bits extraits ({len(bit_string)}) : {bit_string[:64]}...")

flag = ""
for i in range(0, len(bit_string) - 7, 8):
    byte = bit_string[i:i+8]
    char = chr(int(byte, 2))
    if char.isprintable():
        flag += char

print(f"[+] Message caché : {flag}")