from PIL import Image, ImageDraw

size = 512
img = Image.new("RGB", (size, size), "#8B5CF6")
draw = ImageDraw.Draw(img)

for y in range(size):
    r = int(139 + (236 - 139) * (y / size))
    g = int(92 + (72 - 92) * (y / size))
    b = int(246 + (153 - 246) * (y / size))
    draw.line([(0, y), (size, y)], fill=(r, g, b))

draw.ellipse((140, 240, 400, 300), fill="#F59E0B")
draw.rectangle((220, 200, 260, 240), fill="#FDE68A")
draw.polygon([(140, 240), (400, 240), (380, 300), (160, 300)], fill="#F59E0B")

for x, y, r in [(120, 130, 8), (390, 110, 6), (410, 200, 7), (100, 210, 6)]:
    draw.ellipse((x-r, y-r, x+r, y+r), fill="white")

img.save("icon.png")
img.save("icon.ico", format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])

print("Icon ban gaya! icon.png aur icon.ico check karein.")