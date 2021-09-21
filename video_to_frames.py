# This is a simple Python script for downloading youtube videos and extract video frames
import os
import youtube_dl
import cv2
from tqdm import tqdm

def createFolder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("[folder created] " + path)

def downloadVideo(url, folder):
    ydl_opts = {'outtmpl': folder + '/%(id)s.%(ext)s'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def getFolderContent(path):
    content = []
    for (dirPath, dirNames, fileNames) in os.walk(path):
        content.extend(fileNames)
        break
    return content

def extractVideoFrames(videoName, inputFolder, outputFolder, imageFormat):
    capture = cv2.VideoCapture(inputFolder + "/" + videoName)
    fps = int(capture.get(cv2.CAP_PROP_FPS))
    totalFrames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # Creates the selected frame indexes
    frames_idx = range(fps, totalFrames, fps)
    frame_nr = 1

    print("[extracting frames] " + videoName + ":")
    for idx in tqdm(frames_idx):
        imagePath = outputFolder + "/" + videoName[:(videoName.rfind('.'))] + "_" + str(frame_nr) + imageFormat

        # Check if the frame is already extracted
        if os.path.isfile(imagePath):
            continue

        # Set which frame index to read
        capture.set(cv2.CAP_PROP_POS_FRAMES, idx)
        # Reads the fame index
        ret, frame = capture.read()
        # Writes the frame to an image file
        cv2.imwrite(imagePath, frame)
        # Increment frame number
        frame_nr += 1

def deleteVideo(path):
    if os.path.isfile(path):
        os.remove(path)
        print("[removed] " + path)

def main():
    # Video url to download
    videos = ["https://www.youtube.com/watch?v=y8Kyi0WNg40",
              "https://www.youtube.com/watch?v=XgvR3y5JCXg",
              "https://www.youtube.com/watch?v=KmtzQCSh6xk",
              "https://www.youtube.com/watch?v=PfYnvDL0Qcw",
              "https://www.youtube.com/watch?v=HsvA7p0LYUk",
              "https://www.youtube.com/watch?v=HPPj6viIBmU",
              "https://www.youtube.com/watch?v=J---aiyznGQ",
              "https://www.youtube.com/watch?v=lrzKT-dFUjE",
              "https://www.youtube.com/watch?v=QH2-TGUlwu4",
              "https://www.youtube.com/watch?v=QH2-TGUlwu4",
              "https://www.youtube.com/watch?v=gNgXP4HII_4",
              "https://www.youtube.com/watch?v=EIyixC9NsLI",
              "https://www.youtube.com/watch?v=P5ex69c_dAs"]

    videoFolder = "videos"
    createFolder(videoFolder)

    # Downloading the youtube video
    print("Download of videos started")
    for video_url in videos:
        downloadVideo(video_url, videoFolder)

    # Get the video file names in the video folder
    downloaded_videos = getFolderContent(videoFolder)

    # Extracting 1 frame pr. second in the videos and deleting the video files afterward
    print("Video extration of frames started")

    for video in downloaded_videos:
        videoNameFolder = videoFolder + "/" + video[:(video.rfind('.'))]
        createFolder(videoNameFolder)
        extractVideoFrames(video, videoFolder, videoNameFolder, ".png")
        deleteVideo(videoFolder + "/" + video)

    print("Frames extrated from videos")

if __name__ == '__main__':
    main()

