import cv2
import numpy as np

imgn = cv2.imread('binary_matrix.jpg') #insert the image name file
img1 = cv2.resize(imgn,(int(imgn.shape[1]*1),int(imgn.shape[0]*1))) #resize if needed
gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) #convert to gray scale
ret, binary = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV) #convert to binary


labels = set()
shapes = np.zeros((img1.shape[0], img1.shape[1])) 
k=1

for i in range(shapes.shape[0]):
    for j in range(shapes.shape[1]):
        A = binary [i][j]
        if i == 0:   #corner cases
            b=0
            if j!=0:
                c = shapes[i][j-1]
            else:
                d=0
                c=0
        elif j==0:
            d=0
            c=0
            b = shapes[i-1][j]
        else:
            b = shapes[i-1][j]
            c = shapes[i][j-1]
            d = shapes[i-1][j-1]
        
        if A == 0:
            shapes[i][j] = 0
        else: # A == 255
            # 1. Gather all valid, non-zero neighbors into a list
            neighbors = [x for x in (b, c, d) if x != 0]
            
            # 2. If no neighbors have a label, create a new one
            if not neighbors:
                shapes[i][j] = k
                labels.add(k)
                k += 1
            else:
                # 3. If neighbors exist, ALWAYS take the smallest label
                min_label = min(neighbors)
                shapes[i][j] = min_label
                
                # 4. Handle collisions (Merging)
                for n in neighbors:
                    if n != min_label and n in labels:
                        for x in range(shapes.shape[0]):
                            for y in range(shapes.shape[1]):
                                if shapes[x][y] == n:
                                    shapes[x][y] = min_label
                        labels.discard(n)
                        
print(len(labels))

#cv2.imshow('show', binary)
#cv2.waitKey(0)