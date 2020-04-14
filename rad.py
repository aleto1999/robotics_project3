#!/usr/bin/python
import math
import numpy as np 

def increase_action(current): 
    to_return = ""                    
    if current == "": to_return = "a08"             # a08 = cheer up 
    elif current == "a08": to_return = "a10"        # a10 = toss paper
    elif current == "a10": to_return = "a12"        # a12 = lie on sofa 
    elif current == "a12": to_return = "a13"        # a13 = walk 
    elif current == "a13": to_return = "a15"        # a15 = stand up 
    elif current == "a15": to_return = "a16"        # a16 = sit down
    elif current == "a16": to_return = "a08" 
    else: raise Exception('action number should not exceed 16')
    return to_return

def increase_human_subject(current): 
    to_return = ""
    if current == "": to_return = "s01" 
    else: 
        current = current[1:]
        next = int(current) + 1
        if next == 7: to_return = "s01"
        elif next > 7: to_return = "s0" + str(next)
        else: raise Exception('subject number should not exceed 7')
    
    return to_return

def increase_human_trial(current):
    to_return = ""
    if current == "": to_return = "e01"
    elif current == "e01": to_return = "e02"
    elif current == "e02": to_return = "e01"
    else: raise Exception('trial number should not exceed 2')
    return to_return

def get_file_name(action, subject, trial):
    action = increase_action(action)
    subject = increase_human_subject(subject)
    trial = increase_human_trial(trial)
    beginning = "/home/aleto14/robotics/project_3/dataset/train/"
    end = "_skeleton_proj.txt"
    to_return = beginning + action + "_" + subject + "_" + trial + end
    return to_return 

def distance(p1, p2):
    distance = 0 
    d1 = (p1[0] - p2[0]) ** 2
    d2 = (p1[1] - p2[1]) ** 2
    d3 = (p1[2] - p2[2]) ** 2
    distance = math.sqrt(d1 + d2 + d3)
    return distance 

def compute_distances(points):
    distances = []
    center = points[0]
    distances.append(distance(center, points[1]))
    distances.append(distance(center, points[2]))
    distances.append(distance(center, points[3]))
    distances.append(distance(center, points[4]))
    distances.append(distance(center, points[5]))
    return distances 

def angle(b, a, c): 
    angle = ""
    a_2 = a ** 2
    b_2 = b ** 2
    c_2 = c ** 2
    cos_B = (a_2 - b_2 + c_2) / (2 * c * a)
    angle = np.arccos(cos_b)
    return angle 

def compute_angles(points):
    angles = []
    center = points[0]
    angles.append(angle(center, points[1], points[2]))
    angles.append(angle(center, points[1], points[3]))
    angles.append(angle(center, points[2], points[4]))
    angles.append(angle(center, points[3], points[5]))
    angles.append(angle(center, points[4], points[5]))
    return angles 


# this is where the RAD will be implemented 


# Input:   Training setTrainor testing setTest
# Output:  radd1orradd1.t

def main(): 
    # declare input and output files 
    out_file_name = "rad_d1"
    out_file = open(out_file_name, "w")

    # action number, 12 files for each of 6 different actions 
    action_number = ""
    # human subject number, increases every two files 
    subject_number = ""
    # trial number 
    trial_number = ""
      

    for i in range(0, 72): # 72 files 
        in_file_name = get_file_name(action_number, subject_number, trial_number)
        in_file = open(in_file_name, "r")

        # write each file into one line 
        distances = []
        angles = []
        points = []

        # start for loop to go through frames 
        counter = 0 
        temp_points = []
        for line in in_file: 
            line = line.split()
            if(line[1] == 1): 
                point = (line[2], line[3], line[4])
                temp_points.append(point)
            elif line[1] == 4: 
                point = (line[2], line[3], line[4])
                temp_points.append(point)
            elif line[1] == 8:
                point = (line[2], line[3], line[4])
                temp_points.append(point)
            elif line[1] == 12:
                point = (line[2], line[3], line[4])
                temp_points.append(point)
            elif line[1] == 16: 
                point = (line[2], line[3], line[4])
                temp_points.append(point)
            elif line[1] == 20: 
                point = (line[2], line[3], line[4])
                temp_points.append(point)
                distances.append(compute_distances(temp_points))
                angles.append(compute_angles(temp_points))
                temp_points.clear()


    # for each instance in Train or Test do
        # for frame t = 1, ..., T do
            # Select joints that form a star skeleton
            # Compute and store distances between body
            # extremities to body center (dt1,...,dt5)
            # Compute and store angles between two adjacent body
            # extremities (anglet1,...,anglet5)
        # Compute a histogram ofN bins for eachdi={dti}Tt=1, i= 1,...,5
        # Compute a histogram of M bins for eachanglei={angleti}Tt=1, i= 1,...,5
        # Normalize the histograms by dividing T to compensate for different number of frames 
        # in a data instance
        # Concatenate all normalized histograms into aone-dimensional vector of length5(M+N)
        # Convert the feature vector as a single line in the radd1orradd1.t file


if __name__ == "__main__": 
    main()