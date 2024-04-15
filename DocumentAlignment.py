import os
import cv2
import numpy as np
import argparse

def resize(frame, fx=0.5, fy=0.5):
    image = cv2.resize(frame, (0, 0), fx=fx, fy=fy)
    return image

def grayImage(path):
    image = cv2.cvtColor(path, cv2.COLOR_BGR2GRAY)
    return image

def getORBpoint(grayImg1, grayImg2, MAX_FEATURES):
    orb = cv2.ORB_create(nfeatures=MAX_FEATURES)
    kp1, d1 = orb.detectAndCompute(grayImg1, None)
    kp2, d2 = orb.detectAndCompute(grayImg2, None)
    return kp1, d1, kp2, d2

def Homography(srcImg, dstImg, img1Points, img2Points):
    # Find homography
    h, mask = cv2.findHomography(img1Points, img2Points, cv2.RANSAC)
    # Use homography
    height, width, channels = dstImg.shape
    finalImg = cv2.warpPerspective(srcImg, h, (width, height))
    return finalImg

def process_image(sourceImage, dstImage, output_dir):
    sourceImg = cv2.imread(sourceImage, cv2.IMREAD_COLOR)
    dstImg = cv2.imread(dstImage, cv2.IMREAD_COLOR)
    srcGray = grayImage(sourceImg)
    dstGray = grayImage(dstImg)

    kp1, d1, kp2, d2 = getORBpoint(grayImg1=srcGray, grayImg2=dstGray, MAX_FEATURES=500)

    matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)
    matches = list(matcher.match(d1, d2, None))

    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * 0.15)
    matches = matches[:numGoodMatches]

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = kp1[match.queryIdx].pt
        points2[i, :] = kp2[match.trainIdx].pt

    finalImg = Homography(srcImg=sourceImg, dstImg=dstImg, img1Points=points1, img2Points=points2)


    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    cv2.imwrite(f"{output_dir}/final_{os.path.basename(sourceImage)}", finalImg)

    cv2.imshow("Warped Image", resize(finalImg))
    cv2.waitKey(0)

    cv2.destroyAllWindows()

def main(sourceFolder, dstImage,outputdir):
    if os.path.isdir(sourceFolder):
        for filename in os.listdir(sourceFolder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                sourceImage = os.path.join(sourceFolder, filename)
                process_image(sourceImage, dstImage, output_dir=outputdir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Alignment")
    parser.add_argument("--sourceFolder", type=str,default="input", help="Path to the source folder containing images")
    parser.add_argument("--dstImage", type=str,default="ref-image/reference.jpg", help="Path to the destination image")
    parser.add_argument("--outputdir", type=str, default="output", help="Path to the Save images")
    args = parser.parse_args()

    main(sourceFolder=args.sourceFolder, dstImage=args.dstImage, outputdir=args.outputdir)