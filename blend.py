import click
import cv2
import os

def getUniqueFileName(filename):
    i = 1
    fn = filename.split('.')
    if os.path.isfile(filename):
        while(1):
            newFilename = fn[0]+str(i)+'.'+fn[1]
            if os.path.isfile(newFilename):
                i += 1
            else: 
                break
        filename = newFilename
    return filename

def blendImages(img1_path, img2_path, mask_path):

    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    mask1 = cv2.imread(mask_path)

    dim = (img1.shape[0], img1.shape[1])
    img2 = cv2.resize(img2, dim)
    mask1 = cv2.resize(mask1, dim)

    mask2 = cv2.bitwise_not(mask1)

    a = img1 * (mask1 / 255)
    b = img2 * (mask2 / 255)

    return a + b

@click.command()
@click.option('-o', 'output_filename', default='output.png', help='output file')
@click.argument('image1', type=click.Path(exists=True))
@click.argument('image2', type=click.Path(exists=True))
@click.argument('mask', type=click.Path(exists=True))
def blend(image1, image2, mask, output_filename):
    outputImage = blendImages(image1, image2, mask)
    cv2.imwrite(getUniqueFileName(output_filename), outputImage)

if __name__ == '__main__':
    blend()
