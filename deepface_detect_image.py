# my_script.py
import sys
import torch
from torch.utils.model_zoo import load_url
from PIL import Image
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
import numpy as np

import sys
sys.path.append('C:\\dfdc\\code\\icpr2020dfdc')



# 获取当前工作目录

# print("当前工作目录:",os.getcwd())

# !%cd icpr2020dfdc/notebook
# print("change")
# print("当前工作目录:",os.getcwd())

from blazeface import FaceExtractor, BlazeFace
from architectures import fornet,weights

from isplutils import utils


def detect(file_name):

    net_model = 'EfficientNetAutoAttB4'
    train_db = 'DFDC'

    device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
    face_policy = 'scale'
    face_size = 224

    model_url = weights.weight_url['{:s}_{:s}'.format(net_model,train_db)]
    net = getattr(fornet,net_model)().eval().to(device)
    net.load_state_dict(load_url(model_url,map_location=device,check_hash=True))

    transf = utils.get_transformer(face_policy, face_size, net.get_normalizer(), train=False)

    facedet = BlazeFace().to(device)
    facedet.load_weights("C:\\dfdc\\code\\icpr2020dfdc\\blazeface\\blazeface.pth")
    facedet.load_anchors("C:\\dfdc\\code\\icpr2020dfdc\\blazeface\\anchors.npy")
    face_extractor = FaceExtractor(facedet=facedet)

    detect_image = Image.open(file_name)

    detect_image_faces = face_extractor.process_image(img=detect_image)

    detect_image_face = detect_image_faces['faces'][0]

    faces_t = torch.stack( [ transf(image=detect_image_face)['image']] )

    with torch.no_grad():
        faces_pred = torch.sigmoid(net(faces_t.to(device))).cpu().numpy().flatten()

    result = '假人' if faces_pred[0] > 0.5 else '真人'
    #print('$Score for face want to detect: {:.4f}'.format(faces_pred[0]))
    print('$接收到的是圖片')
    print('搞笑機器人判定為' + result, end="")





if __name__ == "__main__":
    # 获取命令行参数
    arguments = sys.argv

    # 第一个参数是脚本名称，从第二个参数开始是传递的参数
    if len(arguments) >= 2:
        file_name = arguments[1]
        detect(file_name)
    else:
        print("Please provide a file name as a command-line argument.")
