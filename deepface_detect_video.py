import os

# print(os.getcwd())
#os.chdir("icpr2020dfdc/notebook")

import torch
from torch.utils.model_zoo import load_url
import matplotlib.pyplot as plt
from scipy.special import expit

import sys
sys.path.append('C:\\dfdc\\code\\icpr2020dfdc')

# print(sys.path)

from blazeface import FaceExtractor, BlazeFace, VideoReader
from architectures import fornet,weights
#sys.path.append('C:\\Users\\yingda\\deepfake\\albumentations')
#print(sys.path)
from isplutils import utils

"""
Choose an architecture between
- EfficientNetB4
- EfficientNetB4ST
- EfficientNetAutoAttB4
- EfficientNetAutoAttB4ST
- Xception
"""
net_model = 'EfficientNetAutoAttB4'

"""
Choose a training dataset between
- DFDC
- FFPP
"""
train_db = 'DFDC'
def detect(file_name):

    device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
    face_policy = 'scale'
    face_size = 224
    frames_per_video = 50

    model_url = weights.weight_url['{:s}_{:s}'.format(net_model,train_db)]
    net = getattr(fornet,net_model)().eval().to(device)
    net.load_state_dict(load_url(model_url,map_location=device,check_hash=True))

    transf = utils.get_transformer(face_policy, face_size, net.get_normalizer(), train=False)

    facedet = BlazeFace().to(device)
    facedet.load_weights("C:\\dfdc\\code\\icpr2020dfdc\\blazeface\\blazeface.pth")
    facedet.load_anchors("C:\\dfdc\\code\\icpr2020dfdc\\blazeface\\anchors.npy")
    videoreader = VideoReader(verbose=False)
    video_read_fn = lambda x: videoreader.read_frames(x, num_frames=frames_per_video)
    face_extractor = FaceExtractor(video_read_fn=video_read_fn,facedet=facedet)

    vid_faces = face_extractor.process_video(file_name)
    

    faces_t = torch.stack( [ transf(image=frame['faces'][0])['image'] for frame in vid_faces if len(frame['faces'])] )


    with torch.no_grad():
        faces_real_pred = net(faces_t.to(device)).cpu().numpy().flatten()


    """
    Print average scores.
    An average score close to 0 predicts REAL. An average score close to 1 predicts FAKE.
    """

    result = '假人' if expit(faces_real_pred.mean()) > 0.5 else '真人'
    #print('$Score for the video want to detect: {:.4f}'.format(expit(faces_real_pred.mean())))
    print('$接收到的是影片')
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
