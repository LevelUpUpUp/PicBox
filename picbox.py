import os
import rawpy
import exifread
import cv2
import imagehash

# from skimage.measure import compare_ssim
from PIL import Image
from PIL.ExifTags import TAGS


class FileExifInfo:
    def __init__(self, path, focalLength, fNumber, lensModel, imageModel):
        self.Path = path
        self.FocalLength = focalLength
        self.FNumber = fNumber
        self.LensModel = lensModel
        self.ImageModel = imageModel

    def __str__(self):
        return f"{self.Path} | {self.FocalLength} | {self.FNumber} | {self.LensModel} | {self.ImageModel}"



# def compare_images(img1, img2):
#     # 载入两幅图像
#     img1 = cv2.imread(img1)
#     img2 = cv2.imread(img2)
#
#     # 将图片转换为灰度图，因为SSIM取值主要关注的是结构性信息，颜色信息通常会忽略；
#     img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#     img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
#
#     # 计算两幅图像的SSIM指数值
#     ssim = compare_ssim(img1, img2)
#
#     return ssim


def compare_imagesV2(img1, img2):
    # 载入两幅图像
    img1 = Image.open(img1)
    img2 = Image.open(img2)

    # 计算两幅图像的哈希值
    hash1 = imagehash.phash(img1)
    hash2 = imagehash.phash(img2)

    # 计算两个哈希值之间的差异
    diff = hash1 - hash2

    return diff

def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        tag = TAGS.get(key, key)
        labeled[tag] = val

    return labeled


def read_cr2_metadata(filepath):
    with open(filepath, 'rb') as f:
        tags = exifread.process_file(f)
        # print(tags.keys())
        # for key in tags.keys():
            # print(f"{key}={tags[key]}")
            # if key == 'EXIF FNumber':
            #     print(f"FNumber: {tags[key]}")
            # elif key == 'EXIF FocalLength':
            #     print(f"FocalLength: {tags[key]}")
            # elif key == 'EXIF LensModel':
            #     print(f"LensModel: {tags[key]}")

    return FileExifInfo(filepath, tags.get('EXIF FocalLength'), tags.get('EXIF FNumber'), tags.get('EXIF LensModel'), tags.get('Image Model'))

def get_exif_data(image):
    image.verify()
    exif_data = {}
    info = image._getexif()
    if info:
        for (tag, value) in get_labeled_exif(info).items():
            if isinstance(value, (bytes, str)):
                # decode bytes
                try:
                    exif_data[tag] = value.decode('utf-8', 'ignore')
                except:
                    exif_data[tag] = value
            else:
                exif_data[tag] = value

    return exif_data

def print_exif_data(file_path):
    image = Image.open(file_path)
    try:
        exif_data = get_exif_data(image)
        return FileExifInfo(file_path, exif_data.get('FocalLength'), exif_data.get('ApertureValue'), exif_data.get('LensModel'), exif_data.get('Model') )
    except:
        return FileExifInfo(file_path, 0, 0, "未识别到镜头型号", "未识别到相机型号")

    # for key, value in exif_data.items():
    #     print(f"{key}= {value}")


def print_all_exif_data(directory):
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                print(print_exif_data(os.path.join(foldername, filename)))
            if filename.lower().endswith('.cr2'):
                print(read_cr2_metadata(os.path.join(foldername, filename)))


print_all_exif_data("/Users/zhuojianfei/Pictures/柚子")
print(compare_imagesV2("/Users/zhuojianfei/Pictures/柚子/1.jpg","/Users/zhuojianfei/Pictures/柚子/2.jpg"))