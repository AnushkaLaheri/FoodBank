import base64
import io
import pandas as pd
import json
import torch
import torch.nn as nn
from torchvision import models, transforms
from torch.utils.data import DataLoader, Dataset
import numpy as np
from torchvision.models import ResNet50_Weights
from PIL import Image

with open("ml_stuff/num_classes.json", "r") as f:
    data = json.load(f)
    num_classes = data["num_classes"]

with open("ml_stuff/dataset_metadata.json", "r") as f:
    dataset_metadata = json.load(f)
    labels = dataset_metadata["labels"]
    label_to_index = dataset_metadata["label_to_index"]

with open("ml_stuff/device.json", "r") as f:
    device_info = json.load(f)
    device = torch.device(device_info["device"])

model = models.resnet50(weights=None)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, num_classes)
model.load_state_dict(torch.load("ml_stuff/fine_tuned_model.pth"))
model.eval()


def preprocess_image(image):
    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    image = transform(image)
    image = image.unsqueeze(0)
    return image


def add_padding(base64_str):
    padding = len(base64_str) % 4
    if padding != 0:
        base64_str += "=" * (4 - padding)
    return base64_str


def run_prediction(base64_img):
    print("Length of Base64 String:", len(base64_img))

    if base64_img.startswith("data:image"):
        base64_img = base64_img.split(",")[1]

    base64_img = add_padding(base64_img)

    image_data = base64.b64decode(base64_img)
    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    image = preprocess_image(image)
    image = image.to(device)

    with torch.no_grad():
        outputs = model(image)
        top_prob, top_index = torch.max(outputs, 1)

    top_label = labels[top_index.item()]

    result = {"label": top_label, "probability": top_prob.item()}

    return result
