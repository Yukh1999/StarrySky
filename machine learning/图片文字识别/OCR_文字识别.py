import easyocr
import os
import cv2
import re

os.environ["CUDA_VISIBLE_DEVICES"] = "True"
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

values = []


def ocr_res(area, num, isFull=False):
    """
    Ocr result
    """
    img = cv2.imread(f'D:/MLDataSet/0530_reimbursement/{num}.jpg')
    cropped_image = img[area[0]:area[1], area[2]:area[3]]  # Slicing to crop the image
    reader = easyocr.Reader(['ch_sim', 'en'])

    if isFull:
        print(reader.readtext(img))
        return 0

    result = reader.readtext(cropped_image)
    text = result[0][1]
    number = re.search(r"[1-9]\d*\.?\d*", text)

    print(number.group(0))

    return float(number.group(0))


# 1-7
for i in range(7):
    res = ocr_res([1510, 1570, 500, 1005], i + 1)

    values.append(res)

# 8
res = ocr_res([1900, 1955, 782, 1056], 8, isFull=False)
values.append(res)

# 9-15
for i in range(9, 16):
    res = ocr_res([2010, 2070, 895, 1050], i, isFull=False)
    values.append(res)

# 16-71
for i in range(16, 72):
    res = ocr_res(area=[1105, 1162, 620, 1006], num=16, isFull=False)
    values.append(res)
print(values)
