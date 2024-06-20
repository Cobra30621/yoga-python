import os
import glob
import cv2
import mediapipe as mp
import json


nodeList = mp.solutions.pose.PoseLandmark
mp_pose = mp.solutions.pose
mp_sample_pose = mp_pose.Pose(static_image_mode=True,
                                        model_complexity=2,
                                        min_detection_confidence=0.5)
mp_result_pose = mp_pose.Pose(static_image_mode=False,
                                        model_complexity=2,
                                        min_detection_confidence=0.5)


# 取的某個資料夾中，所有圖片的路徑
def get_image_files(folder_path):
    return glob.glob(os.path.join(folder_path, '*.jpeg')) + \
        glob.glob(os.path.join(folder_path, '*.jpg')) + \
        glob.glob(os.path.join(folder_path, '*.png'))

# 繪製關節點到圖片中
def draw_skeleton(image, point2d):
    height, width, channels = image.shape

    for node in nodeList:
        point = getLandmarks(point2d[node.value], width, height)
        point_color = (255, 0, 0)
        cv2.circle(image, point, 4, point_color, 4)

    return image


def getLandmarks(landmark, w=None, h=None):
    """Get skeleton landmark x,y,z respectively

    Args:
        landmark (mediapipe landmark): skeleton landmark
        w (int): image w
        h (int): image h

    Returns:
        2D relative coordinates(image) landmark(x,y) || 3D real coordinates landmark(x,y,z)

    """
    if w == None or h == None:
        return landmark.x, landmark.y, landmark.z
    else:
        return int(landmark.x * w), int(landmark.y * h)




def get_Mediapipe_point(image):
    point2d, point3d = getMediapipeResult(image, False)
    if type(point2d) == int and type(point3d) == int:
        print("無法偵測到完整骨架")
        return None, None

    return point2d, point3d

def getMediapipeResult(frame, mode=True):
    """Get mediapipe result of this frame

    Args:
        frame (image array):  process frame
        mode (bool): set mediapipe args [static_image_mode]
            True -> use to different image
            False -> use to video

    Returns:
        2D & 3D result of mediapipe
        (if process error return 0,0)

    """
    try:
        if mode:
            results = mp_sample_pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        else:
            results = mp_result_pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        point2d = results.pose_landmarks.landmark
        point3d = results.pose_world_landmarks.landmark
        return point2d, point3d
    except:
        return 0, 0


# 儲存 json 檔案
def save_json(path, file_name, json_data):
    output_json_path = path + "/" + file_name

    # 檢查路徑是否存在，如果不存在則創建
    if not os.path.exists(path):
        os.makedirs(path)

    with open(output_json_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


