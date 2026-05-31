import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms
import timm

# ---------------- CONFIG ----------------
MODEL_PATH = r"models/gender_best.pth"
IMAGE_PATH = r"test_inputs/image1.jpg"  # preferably face image
IMG_SIZE = 384

# IMPORTANT: confirm this order from training code
GENDER_CLASSES = ['female' , 'male']

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# ----------------------------------------

def build_gender_model(num_classes):
    model = timm.create_model(
        "tf_efficientnetv2_l.in21k",
        pretrained=False,
        num_classes=num_classes
    )
    return model

def load_model():
    model = build_gender_model(len(GENDER_CLASSES))

    checkpoint = torch.load(MODEL_PATH, map_location=DEVICE)

    if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
        model.load_state_dict(checkpoint["model_state_dict"])
    else:
        model.load_state_dict(checkpoint)

    model.to(DEVICE)
    model.eval()
    return model

def get_transform():
    return transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

def predict_gender(model, image_path):
    image = Image.open(image_path).convert("RGB")
    transform = get_transform()
    x = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(x)
        probs = torch.softmax(outputs, dim=1)
        pred_idx = torch.argmax(probs, dim=1).item()
        pred_class = GENDER_CLASSES[pred_idx]
        confidence = probs[0][pred_idx].item()

    return pred_class, confidence

if __name__ == "__main__":
    model = load_model()
    pred_class, confidence = predict_gender(model, IMAGE_PATH)

    print(f"Predicted Gender: {pred_class}")
    print(f"Confidence: {confidence:.4f}")