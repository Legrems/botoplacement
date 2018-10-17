from PIL import Image
import numpy as np
from skimage import measure

img = Image.open("PlanP32_approuve_placement.png")

img = np.array(img.getdata()).reshape(img.size[0], img.size[1], 4)

tab = []

r = 0
g = 1
b = 2

r_query = 255
g_query = 223
b_query = 127

tab = np.where((img[:,:,r] == r_query) & (img[:,:,g] == g_query) & (img[:,:,b] == b_query))
print(len(tab[0]))