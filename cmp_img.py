from PIL import Image
import os
import argparse

folder = 'dev_dataset'


def image_comparison(folder):
    """Compares images in the folder"""

    Images = []
    for img in os.listdir(folder + "/."):
        # resize and greyshade
        i = Image.open(folder + '/' + img).resize((8, 8)).convert('L')
        # calc avarage pixel value
        pixel_map = i.load()
        pixel_sum = 0
        for x in range(i.size[0]):
            for y in range(i.size[1]):
                pixel_sum += pixel_map[x, y]

        avarage = pixel_sum / i.size[0] / i.size[1]

        # paint black or white
        ihash = ''
        for x in range(i.size[0]):
            for y in range(i.size[1]):
                if pixel_map[x, y] <= avarage:
                    pixel_map[x, y] = 255
                    ihash += '0'
                else:
                    pixel_map[x, y] = 0
                    ihash += '1'

        Images.append((img, ihash))


    def Hamming_dist(h0, h1):
        """Calculates the Hamming distance between 2 hashes"""

        d = 0
        for i in range(len(h0)):
            if h0[i] != h1[i]:
                d += 1
        return d


    i = 1
    for img in Images:
        results = {'image': img[0], 'identical': [], 'modified': [], 'similar': []}
        for compared in Images:
            if compared != img:
                d = Hamming_dist(img[1], compared[1])
                if d == 0:
                    results['identical'].append(compared[0])
                elif 1 <= d <= 5:
                    results['modified'].append((compared[0], d))
                elif 6 <= d <= 12:
                    results['similar'].append((compared[0], d))

        print(f'{i})Image = {results["image"]}')
        print(f'identical = {results["identical"]}')
        print(f'modified = {results["modified"]}')
        print(f'similar = {results["similar"]}')
        print('\n')
        i += 1


parser = argparse.ArgumentParser(description='Compare images')
parser.add_argument('--path', dest='PATH', action='store', help='Write your path to the photos directory')

args = parser.parse_args()

if args.PATH is not None:
    image_comparison(args.PATH)
