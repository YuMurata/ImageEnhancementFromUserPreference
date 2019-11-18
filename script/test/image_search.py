import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageStat, ImageChops
import matplotlib.pyplot as plt
from io import BytesIO
import math
from tqdm import tqdm


org_image = Image.open(
    r'C:\Users\init\Documents\PythonScripts\EnhanceImageFromUserPreference\script\test\a.PNG').convert('RGB')

url = 'https://data.csail.mit.edu/graphics/fivek/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')


def make_image(image_path):
    re = requests.get(image_path)
    return Image.open(BytesIO(re.content)).convert('RGB')


def match(item: tuple):
    web_image = item[1]
    image = org_image.resize(web_image.size)

    diff_img = ImageChops.difference(web_image, image)
    stat = ImageStat.Stat(diff_img)
    mse = sum(stat.sum2) / len(stat.count) / stat.count[0]
    return 10 * math.log10(255 ** 2 / mse)


def part_search(min_index, max_index):
    image_path_list = [url+image_path['src']
                       for image_path in soup.find_all('img')]

    image_dict = {image_path: make_image(image_path) for image_path in tqdm(
        image_path_list[min_index:max_index])}

    image_item = min(image_dict.items(), key=match)

    return image_item


max_image_num = 5000
part_size = 50

item_list = []
for i in range(max_image_num//part_size):
    item = part_search(i*part_size, (i+1)*part_size)
    item_list.append(item)

    image_path=item[0]
    print(f'{i}th similar: {image_path}')

best_item = min(item_list, key=match)

best_image = best_item[1]
best_path = best_item[0]

print(best_path)
plt.imshow(best_image)
plt.show()
