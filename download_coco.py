# -*- coding:utf-8 -*-
# Author: Kedong Xiu
# 
from pycocotools.coco import COCO
import requests
from tqdm import tqdm as tqdm
import concurrent.futures
import os
import argparse

parser = argparse.ArgumentParser(description="Download COCO images by category")
parser.add_argument(
    "--root-dir",
    type=str,
    default="/hub/huggingface/datasets/COCO",
    help="Directory to store the COCO dataset",
)
parser.add_argument(
    "--data-type",
    type=str,
    default="test-dev2017",
    help="Type of the COCO dataset",
)
args = parser.parse_args()

# Define the data directory and type
dataDir = args.root_dir
dataType = args.data_type
annFile = "{}/annotations/instances_{}.json".format(dataDir, dataType)

# Create the data directory if it does not exist
os.makedirs(os.path.join(dataDir, dataType), exist_ok=True)

# Initialize COCO API for instance annotations
coco = COCO(annFile)

catIds = coco.getCatIds()
cats = coco.loadCats(catIds)
catNms = [cat["name"] for cat in cats]


def download_image(im, dataDir):
    """
    Helper function to download a single image
    """
    try:
        img_data = requests.get(im["coco_url"]).content
        img_path = os.path.join(dataDir, dataType, im["file_name"])
        with open(img_path, "wb") as handler:
            handler.write(img_data)
    except Exception as e:
        # print(f"Failed to download {im['file_name']}: {e}")
        print(e)


def download_category_images(catNm, coco, dataDir):
    """
    Download all images for a given category name using the COCO API.
    """
    catIds = coco.getCatIds(catNms=[catNm])
    imgIds = coco.getImgIds(catIds=catIds)
    images = coco.loadImgs(imgIds)

    # Parallelize the download of images for this category
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Pass each image and the dataDir to the download_image function
        futures = [executor.submit(download_image, im, dataDir) for im in images]
        # Ensure all images are downloaded
        for future in tqdm(
            concurrent.futures.as_completed(futures), desc=catNm, total=len(images)
        ):
            future.result()  # Get the result or handle exceptions


# Parallelize the download of images for all categories
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Submit a task for each category
    futures = [
        executor.submit(download_category_images, catNm, coco, dataDir)
        for catNm in catNms
    ]
    # Ensure all categories are processed
    for future in tqdm(
        concurrent.futures.as_completed(futures),
        desc="Downloading categories",
        total=len(catNms),
    ):
        future.result()  # Handle any exceptions during the task execution
