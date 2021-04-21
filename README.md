# PyPath

![build fail](./images/build_pass.svg)
[![PyPI version](https://badge.fury.io/py/python-patho.svg)](https://badge.fury.io/py/python-patho)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)

Python library for pathology image analysis



This project is part of my PhD thesis to analyse histopathological images. Especially, the breast cancer hematoxylin and eosin-stained images
from [BreCaHAD: a dataset for breast cancer histopathological annotation and diagnosis](https://figshare.com/articles/dataset/BreCaHAD_A_Dataset_for_Breast_Cancer_Histopathological_Annotation_and_Diagnosis/7379186)

## It supports:
- Optical density transform
- Color deconvolution

## Dependencies
- [OpenCV](https://opencv.org)
- [scikit-image](https://scikit-image.org)
- [spams](http://spams-devel.gforge.inria.fr)
- [numpy](https://numpy.org)

## Installation
```shell
$ pip install python-patho
```

## How to run
```shell
$ python demo.py
```


## Basic Usage
#### *Try your first PyPath program*

```python
>>> from pypath.transform import convert_RGB_to_OD
>>> import cv2
>>> I_BGR = cv2.imread('images/he.png')
>>> I_RGB = cv2.cvtColor(I_BGR, cv2.COLOR_BGR2RGB)
>>> I_OD  = convert_RGB_to_OD(I_RGB)
```

![RGB](./images/od_rgb_convert.png)

```python
>>> I_H, I_E = color_decon(I_RGB)
```

![CD](./images/color_decon.png)

## License
[GNU Affero General Public License v3.0](LICENSE)