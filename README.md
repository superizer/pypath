# PyPath
Python library for pathology image analysis

This project is part of my PhD thesis to analyse histopathological images. Especially, the breast cancer hematoxylin and eosin-stained images
from [BreCaHAD: a dataset for breast cancer histopathological annotation and diagnosis](https://figshare.com/articles/dataset/BreCaHAD_A_Dataset_for_Breast_Cancer_Histopathological_Annotation_and_Diagnosis/7379186)

## It supports:
- Optical density transform

## Dependencies
- [OpenCV](https://opencv.org)
- [scikit-image](https://scikit-image.org)



## How to run
```shell
$ python demo.py
```


## Basic Usage
#### *Try your first PyPath program*

```python
>>> import pypath as pp
>>> import cv2
>>> I_BGR = cv2.imread('images/he.png')
>>> I_RGB = cv2.cvtColor(I_BGR, cv2.COLOR_BGR2RGB)
>>> I_OD  = pp.convert_RGB_to_OD(I_RGB)
```

![RGB ](./images/od_rgb_convert.png)
## License
[GNU Affero General Public License v3.0](LICENSE)