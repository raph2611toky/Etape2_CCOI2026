on nous a donné un image

![image](./Broken_signal%20qrcode.png)

```powershell
┌──(raph㉿RAPH-PORTABLE)-[F:\PROJET\COMPETITIONS\CYBERSECURITE\CYBERCUP\Etape2_CCOI2026\misc\Broken_signal]
└─# file '.\Broken_signal qrcode.png'
.\Broken_signal qrcode.png: PNG image data, 578 x 648, 8-bit/color RGB, non-interlaced
┌──(raph㉿RAPH-PORTABLE)-[F:\PROJET\COMPETITIONS\CYBERSECURITE\CYBERCUP\Etape2_CCOI2026\misc\Broken_signal]
└─# zsteg  -a '.\Broken_signal qrcode.png' | findstr CCOI
b1,r,lsb,xy         .. text: "CCOI26{0c01_15_w4tch1ng_y0u}"
```

Le flag est donc :
`CCOI26{0c01_15_w4tch1ng_y0u}`
