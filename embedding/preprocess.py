from torchvision import transforms
from PIL import Image

transform = transforms.Compose([
    transforms.Resize((256)),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406], 
        std=[0.229, 0.224, 0.225]
        )
])

def load_image(path):
    image = Image.open(path).convert("RGB")
    return transform(image).unsqueeze(0)