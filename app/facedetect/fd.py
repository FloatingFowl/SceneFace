import cv2
import numpy as np
import os

def imagetofaces(im, offset, dr, classifier, fr):
    '''
    im => image
    offset => save image from
    dr => save directory
    '''
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    
    faces = classifier.detectMultiScale(gray, 1.3, 5)
    ret = []
    cnt = 0
    for (x,y,w,h) in faces:
        ret.append((offset + cnt, (x,y,w,h,fr)))
        cv2.imwrite(dr + ("%d.png" % (offset + cnt)), im[y:y+h,x:x+w])     # save frame as JPEG file      
        cnt += 1
    return ret

def facedetection(fnm, scenes):
    '''
    scenes => list of (beg, end) of all scenes
    fnm => video file path
    '''
    cnt = 0
    scene_cnt = 0
    frame_cnt = 0
    scene_face_map = [[] for _ in range(len(scenes))]
    vidcap = cv2.VideoCapture(fnm)
    success,image = vidcap.read()
    print("Extracting Faces")

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    while success:
        ls = imagetofaces(image, cnt, 'server/detected/', face_cascade, frame_cnt)
        cnt += len(ls)
        scene_face_map[scene_cnt].extend(ls)

        frame_cnt += 1
        if frame_cnt > scenes[scene_cnt][1]:
            scene_cnt += 1
        success,image = vidcap.read()

    return scene_face_map

def display(scenes, faces, scene_people):
    names = [i for i in os.listdir('server/dataset/') if i[0] != '.']
    names.sort()

    print("saving video")
    scene_cnt = 0 
    frame_cnt = 0
    face_cnt = 0
    vidcap = cv2.VideoCapture('server/video/video.mp4')
    success,image = vidcap.read()
    fourcc = cv2.VideoWriter_fourcc(*'h264')
    eap = cv2.VideoWriter('app/static/video/final.mp4',fourcc, 24, (int(vidcap.get(3)),100+int(vidcap.get(4))))

    while success:
        border = np.array([255,0,0])
        if scene_cnt % 2 == 0:
            border = np.array([0,0,255])
        image[:5,:] = image[-5:,:] = border
        image[:,:5] = image[:,-5:] = border

        while face_cnt < len(faces[scene_cnt]) and faces[scene_cnt][face_cnt][1][4] == frame_cnt:
            (x,y,w,h,fr) = faces[scene_cnt][face_cnt][1]
            cv2.rectangle(image, (x,y), (x+w,y+h), (255,0,0), 2)
            face_cnt += 1

        image_new = np.zeros((image.shape[0]+100,image.shape[1],3),dtype=np.uint8)
        image_new[100:,:image.shape[1],:] = image

        for i, j in enumerate(sorted(list(scene_people[scene_cnt]))):
            cv2.putText(image_new, names[j], ((i+1)*100,50), cv2.FONT_HERSHEY_PLAIN, 2, color=(255,255,255))
            print("DONE", names[j], i)

        eap.write(image_new)

        # changing scene_cnt
        frame_cnt += 1
        if scenes[scene_cnt][1] < frame_cnt:
            face_cnt = 0
            scene_cnt += 1
        success,image = vidcap.read()
    print("done")
