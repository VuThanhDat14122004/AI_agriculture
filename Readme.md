<div align="center">
        <h1>Cattle Detection and Counting in Images</h1>
            <p>The type of livestock considered in this work is dairy cattle</p>
            <p>
            <a href="https://github.com/VuThanhDat14122004/AI_agriculture/graphs/contributors">
                <img src="https://img.shields.io/github/contributors/VuThanhDat14122004/AI_agriculture" alt="Contributors" />
            </a>
            <a href="">
                <img src="https://img.shields.io/github/last-commit/VuThanhDat14122004/AI_agriculture" alt="last update" />
            <a href="https://github.com/VuThanhDat14122004/AI_agriculture/network/members">
		        <img src="https://img.shields.io/github/forks/VuThanhDat14122004/AI_agriculture" alt="forks" />
	        </a>
	        <a href="https://github.com/VuThanhDat14122004/AI_agriculture/stargazers">
		        <img src="https://img.shields.io/github/stars/VuThanhDat14122004/AI_agriculture" alt="stars" />
	        </a>
</div>

# Description
This project addresses the problem of detecting and counting dairy cattle in images. I use a model from the YOLO family, specifically YOLOv11, to solve this task. The YOLOv11 model used is a pretrained object detection model, which I fine-tuned on a custom dataset. The dataset was sourced from Kaggle, and I manually processed and reformatted it to fit the required structure for training and validation with YOLOv11

# Dataset
- I use the <a href="https://www.kaggle.com/datasets/trainingdatapro/cows-detection-dataset/data">cow dataset</a>
- Train: 40 images
- Val: 11 images

# Parameters and Hyperparameters
- Img size: 640
- Epochs: 200
- Batch size: 8
- Initial learning rate: 5e-3
- Optimizer: AdamW
- weight_decay: 10e-2
- [detail parameters](file_work/runs/detect/train/args.yaml)
# Result
After training the model on Google Colab, the best model achieved the following results (validation set):
| Class | Images | Instances | Precision (P) | Recall (R) | mAP@0.5 | mAP@0.5:0.95 |
|-------|--------|-----------|---------------|------------|---------|--------------|
| cow   | 11     | 190       | 0.745         | 0.595      | 0.694   | 0.377        |

- Images: The number of images used for evaluation.

- Instances: Total number of labeled objects (bounding boxes) across all images.

- Precision (P): The proportion of correctly predicted bounding boxes out of all predicted boxes. High precision means few false positives.

- Recall (R): The proportion of correctly predicted bounding boxes out of all ground truth boxes. High recall means few false negatives.

- mAP@0.5: Mean Average Precision at IoU threshold 0.5. A commonly used object detection metric.

- mAP@0.5:0.95: Mean Average Precision averaged over IoU thresholds from 0.5 to 0.95 (step 0.05). A stricter and more comprehensive metric for model performance.

# References
Here are the blogs I referenced for the implementation.

Blog: <a href="https://docs.ultralytics.com/vi/tasks/detect/">
        blog1
       </a>,
       <a href="https://docs.ultralytics.com/vi/datasets/detect/">
        blog2
       </a>
