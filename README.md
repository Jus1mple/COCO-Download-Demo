# COCO2017 Dataset download


This repository is a easy demo & util for download COCO2017 dataset.

Hope this repo could help you in any cases.


## Dependencies


### Install packages for downloading

```bash
pip install pycocotools
pip install requests
```


### Download instance files

```bash
wget -c http://images.cocodataset.org/annotations/annotations_trainval2017.zip # Training set
wget -c http://images.cocodataset.org/annotations/stuff_annotations_trainval2017.zip # Val set
wget -c http://images.cocodataset.org/annotations/image_info_test2017.zip # Test set
```

### Unzip downloaded file on current folder

```bash
unzip annotations_trainval2017.zip
unzip stuff_annotations_trainval2017.zip
unzip image_info_test2017.zip
```


## Easy Usage

```bash
python download_coco.py --root-dir YOUR_COCO_DIR_PATH --data-type train2017 
```
