#!/usr/bin/python
import math
import numpy as np 

def increase_action(current): 
    to_return = ""                    
    if current == "0": to_return = "a08"             # a08 = cheer up 
    elif current == "a08": to_return = "a10"        # a10 = toss paper
    elif current == "a10": to_return = "a12"        # a12 = lie on sofa 
    elif current == "a12": to_return = "a13"        # a13 = walk 
    elif current == "a13": to_return = "a15"        # a15 = stand up 
    elif current == "a15": to_return = "a16"        # a16 = sit down
    elif current == "a16": to_return = "a08" 
    else: raise Exception('action number should not exceed 16')
    return to_return

def increase_human_subject(mode, current): 
    to_return = ""
    if mode == 1: 
        if current == "": to_return = "s01" 
        else: 
            current = current[1:]
            next = int(current) + 1
            if next == 7: to_return = "s01"
            elif next < 7: to_return = "s0" + str(next)
            else: raise Exception('subject number should not exceed 7')
    elif mode == 2: 
        if current == "": to_return = "s07" 
        else: 
            current = current[1:]
            next = int(current) + 1
            if next == 11: to_return = "s07"
            elif next == 10: to_return = "s10"
            elif next < 10: to_return = "s0" + str(next)
            else: raise Exception('subject number should not exceed 7')    
    return to_return

def increase_human_trial(current):
    to_return = ""
    if current == "": to_return = "e01"
    elif current == "e01": to_return = "e02"
    elif current == "e02": to_return = "e01"
    else: raise Exception('trial number should not exceed 2')
    return to_return

def get_file_name(action, subject, trial, beginning, end ):
    
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

def angle(a, b, c): 
    angle = ""
    a_2 = a ** 2
    b_2 = b ** 2
    c_2 = c ** 2
    cos_B = (a_2 - b_2 + c_2) / (2 * c * a)
    angle = np.degrees(np.arccos(cos_B))
    return angle 

def compute_angles(distances, points):
    angles = []
    angles.append(angle(distances[0],distance(points[1], points[2]),distances[1]))
    angles.append(angle(distances[1],distance(points[2], points[4]),distances[3]))
    angles.append(angle(distances[3],distance(points[4], points[5]),distances[4]))
    angles.append(angle(distances[4],distance(points[5], points[3]),distances[2]))
    angles.append(angle(distances[2],distance(points[1], points[3]),distances[0]))
    return angles 

def make_histo(num_bins, min_, max_, data_set):
    histogram = []
    step = (max_ - min_) / float(num_bins)
    for k in range(0, num_bins): 
        histogram.append(0)
    # print(histogram) # check for correct number of bins 
    for i in range(0, len(data_set)):
        current = data_set[i]
        temp = min_ 
        for j in range (0, num_bins):
            temp = temp + step 
            # print(temp)
            if current <= temp: 
                histogram[j] = histogram[j] + 1 
                break
            elif j == (num_bins - 1): histogram[j] = histogram[j] + 1

    return histogram 

def normalize(histogram, num_frames):

    for i in range(0, len(histogram)): 
        histogram[i] = histogram[i] / float(num_frames) 
        histogram[i] = round(histogram[i], 4)
    return histogram  


def run(mode):

    if mode == 1: 
        in_file_prefix = "dataset/train/"
        in_file_suffix = "_skeleton_proj.txt"
        out_file_name = "rad_d1"
        num_files = 72
        change_action = 12
    elif mode == 2: 
        in_file_prefix = "dataset/test/"
        in_file_suffix = "_skeleton_proj.txt"
        out_file_name = "rad_d1.t"
        num_files = 48
        change_action = 8
    else: raise Exception('mode number not valid')

        
    out_file = open(out_file_name, "w")


    action_number = "0"
    subject_number = "" 
    trial_number = ""
      

    for i in range(0, num_files): 
        if i % change_action == 0: action_number = increase_action(action_number)
        if i % 2 == 0: subject_number = increase_human_subject(mode, subject_number)
        trial_number = increase_human_trial(trial_number)
        in_file_name = get_file_name(action_number, subject_number, trial_number, in_file_prefix, in_file_suffix)
        in_file = open(in_file_name, "r")
        # print(in_file_name)

        # write each file into one line 
        distances_0 = []
        distances_1 = []
        distances_2 = []
        distances_3 = []
        distances_4 = []
        angles_0 = []
        angles_1 = []
        angles_2 = []
        angles_3 = []
        angles_4 = []

        frames = 0 

        # start for loop to go through frames 
        temp_points = []
        for line in in_file: 
            line = line.split()
            joint = int(line[1])
            if(joint == 1 or joint == 4 or joint == 8 or joint == 12 or joint == 16): 
                point = (float(line[2]), float(line[3]), float(line[4]))
                temp_points.append(point)
            elif joint == 20: 
                frames = frames + 1 
                point = (float(line[2]), float(line[3]), float(line[4]))
                temp_points.append(point)

                # add distances 
                temp_distances = compute_distances(temp_points)
                distances_0.append(temp_distances[0])
                distances_1.append(temp_distances[1])
                distances_2.append(temp_distances[2])
                distances_3.append(temp_distances[3])
                distances_4.append(temp_distances[4])

                # add angles 
                temp_angles = compute_angles(temp_distances, temp_points)
                angles_0.append(temp_angles[0])
                angles_1.append(temp_angles[1])
                angles_2.append(temp_angles[2])
                angles_3.append(temp_angles[3])
                angles_4.append(temp_angles[4])

                # clear temporary vectors 
                temp_points = []
                temp_distances = []

        # make histogram for each set of angles 
        hist_angles = []

        hist_angles_0 = make_histo(10, 10, 160, angles_0)
        hist_angles.extend(hist_angles_0)
        
        hist_angles_1 = make_histo(10, 5, 160, angles_1)
        hist_angles.extend(hist_angles_1)

        hist_angles_2 = make_histo(10, 0, 75, angles_2)
        hist_angles.extend(hist_angles_2)

        hist_angles_3 = make_histo(10, 5, 150, angles_3)
        hist_angles.extend(hist_angles_3)

        hist_angles_4 = make_histo(10, 5, 160, angles_4)
        hist_angles.extend(hist_angles_4)

        # make histogram for lengths 
        hist_distances = []

        hist_dist_0 = make_histo(10, 0.2, .7, distances_0)
        hist_distances.extend(hist_dist_0)

        hist_dist_1 = make_histo(10, 0.2, .7, distances_1)
        hist_distances.extend(hist_dist_1)

        hist_dist_2 = make_histo(10, 0.1, .6, distances_2)
        hist_distances.extend(hist_dist_2)

        hist_dist_3 = make_histo(10, 0.2, .9, distances_3)
        hist_distances.extend(hist_dist_3)

        hist_dist_4 = make_histo(10, 0.3, .9, distances_4)
        hist_distances.extend(hist_dist_4)

        total_histogram = hist_angles
        total_histogram.extend(hist_distances)
        total_histogram = normalize(total_histogram, frames)

        for i in range(0, len(total_histogram)): 
            out_file.write(str(total_histogram[i]))
            out_file.write(" ")

        out_file.write("\n")

    out_file.close()

def main():

    run(1) # run algorithm on training files
    run(2) # run algorithm on testing files 

if __name__ == "__main__": 
    main()