import base64, re, io
from PIL import Image

with open("/Users/xingxiu/Desktop/Fluxium网站/logo.svg", "r") as f:
    text = f.read()

matches = re.findall(r"base64,([A-Za-z0-9+/=]+)", text)

mask_b64 = matches[0]
rgb_b64 = matches[1]

mask_img = Image.open(io.BytesIO(base64.b64decode(mask_b64))).convert("L")
rgb_img = Image.open(io.BytesIO(base64.b64decode(rgb_b64))).convert("RGBA")

rgb_img.putalpha(mask_img)

pixels = rgb_img.load()
for y in range(rgb_img.height):
    for x in range(rgb_img.width):
        r, g, b, a = pixels[x, y]
        if a > 10:
            if r < 120 and g < 120 and b < 120:
                pixels[x, y] = (255, 255, 255, a)

rgb_img.save("/Users/xingxiu/Desktop/Fluxium网站/logo_processed.png")
print("Saved transparent PNG")
