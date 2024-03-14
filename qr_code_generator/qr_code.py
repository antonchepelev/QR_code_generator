# basic_qrcode.py
from urllib.request import urlopen
import segno


qr_code = segno.make_qr("Hello, World")
nirvana_url = urlopen("https://media1.tenor.com/images/1f973d6fffa5b779bd5352fecb9eccb7/tenor.gif?itemid=15635897")
#qr_code.save("my_qr.png",scale = 10,border = 2,light = "red",dark = "blue", quiet_zone ="yellow")
qr_code.to_artistic(
    background=nirvana_url,
    target="animated_qrcode.gif",
    scale=5,
    light = "lightblue",
    dark = "black"
)