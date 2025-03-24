import pandas as pd
import json
import torch
import torch.nn as nn
from torchvision import models, transforms
from torch.utils.data import DataLoader, Dataset
import numpy as np
from torchvision.models import ResNet50_Weights

df = pd.read_pickle("images.pkl")

print(df.head())

# num of unique classes
num_classes = len(df["label"].unique())
with open("num_classes.json", "w") as f:
    json.dump({"num_classes": num_classes}, f)

# load pretrained model
model = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
model.eval()

# freeze all layers except final
for param in model.parameters():
    param.requires_grad = False

# replace the last layer so that it matches num_classes
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, num_classes)


class FoodDataset(Dataset):
    def __init__(self, dataframe, transform=None):
        self.dataframe = dataframe
        self.transform = transform
        self.label_to_index = {
            label: idx for idx, label in enumerate(dataframe["label"].unique())
        }

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        row = self.dataframe.iloc[idx]
        label = row["label"]
        pixel_values = row[1:].values.reshape((224, 224, 3)).astype("uint8")
        if self.transform:
            image = self.transform(pixel_values)
        label_tensor = torch.tensor(self.label_to_index[label], dtype=torch.long)
        return image, label_tensor


# preprocessing steps
transform = transforms.Compose(
    [
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

# create dataset and dataloader
dataset = FoodDataset(df, transform=transform)
dataset_metadata = {
    "labels": df["label"].unique().tolist(),
    "label_to_index": dataset.label_to_index,
}

with open("dataset_metadata.json", "w") as f:
    json.dump(dataset_metadata, f)

dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# loss func and optim
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.fc.parameters(), lr=0.001)

# training loop
num_epcochs = 5
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
with open("device.json", "w") as f:
    json.dump({"device": str(device)}, f)
print("Dumped everything")

model = model.to(device)

for epoch in range(num_epcochs):
    model.train()
    running_loss = 0.0
    correct_predictions = 0
    total_predications = 0

    for images, labels in dataloader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)
        _, predicted = torch.max(outputs, 1)
        correct_predictions += (predicted == labels).sum().item()
        total_predications += labels.size(0)

    epoch_loss = running_loss / len(dataloader.dataset)
    epoch_accuracy = correct_predictions / total_predications

    print(
        f"Epoch {epoch+1}/{num_epcochs}, Loss: {epoch_loss:.4f}, Accuracy: {epoch_accuracy:.4f}"
    )

torch.save(model.state_dict(), "fine_tuned_model.pth")
print("Model now finetuned and saved in fine_tuned_model.pth")
