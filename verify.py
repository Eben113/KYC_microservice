import torch
from PIL import Image
import numpy as np
import torch.nn.functional as F
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from deepface import DeepFace
import timm

def extract_face(img_src):
  faces = DeepFace.extract_faces(img_src, detector_backend="retinaface")
  if len(faces) == 0:
    return "No face detected in given image"
  else:
    return faces[0]["face"]

model1 = timm.create_model("hf_hub:gaunernst/vit_small_patch8_gap_112.cosface_ms1mv3", pretrained=True, num_classes=0).eval()

def resize(arr):
  transform = transforms.Compose([
    transforms.Resize((112, 112)),  # Required input size
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])
  img = (Image).fromarray((arr*255).astype(np.uint8))
  img = transform(img)
  return img.unsqueeze(0)

def check_similarity(arr1, arr2):
  input1, input2 = resize(arr1), resize(arr2)
  with torch.no_grad():
    out1, out2 = model1(input1), model1(input2)
  out1, out2 = F.normalize(out1, dim=1), F.normalize(out2, dim=1)
  return F.cosine_similarity(out1, out2, dim=1)

def compare(id_src, selfie_src):
  if check_similarity(plt.imread(id_src), plt.imread("blank-card.jpg")) < 0.6:
    return "Invalid ID submitted"
  else:
    face1, face2 = extract_face(id_src), extract_face(selfie_src)
    score = check_similarity(face1, face2)
    return score.item()
