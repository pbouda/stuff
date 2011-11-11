import png

f = png.Reader(filename = "knob1.png")

(width, height, pixels, metadata) = f.asRGBA()

sum = 0;
print "var template_width = {0}".format(width)
print "var template_height = {0}".format(height)
print "var template = new Array(";
for i, row in enumerate(pixels):
    values = list()
    for j, el in enumerate(row):
        if (j % 4) == 0:
            sum = sum + el
            values.append(str(el))
    values[-1] = "0"
    if i == (height - 1):
        print("    {0}".format(", ".join(values)))
    else:
        print("    {0},".format(", ".join(values)))
        
print ");"

print sum-(24*255)