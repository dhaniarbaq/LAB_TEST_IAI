import streamlit as st
import torch
from torchvision import models, transforms
from PIL import Image
import requests

st.title("Real-Time Image Classification")

labels_url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
labels = requests.get(labels_url).text.splitlines()

model = models.resnet18(pretrained=True)
model.eval()

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225])
])

image_file = st.camera_input("Capture an image")

if image_file:
    image = Image.open(image_file)
    st.image(image, caption="Captured Image")

    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)

    top5 = torch.topk(probabilities, 5)

    st.subheader("Top 5 Predictions")
    for i in range(5):
        st.write(labels[top5.indices[i]], float(top5.values[i]))
