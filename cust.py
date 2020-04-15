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
    head = points[0]
    distances.append(distance(head, points[1]))
    distances.append(distance(head, points[2]))
    distances.append(distance(head, points[3]))
    distances.append(distance(head, points[4]))
    distances.append(distance(head, points[5]))
    distances.append(distance(head, points[6]))
    distances.append(distance(head, points[7]))
    distances.append(distance(head, points[8]))
    return distances 

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
        out_file_name = "cust_d1"
        num_files = 72
        change_action = 12
    elif mode == 2: 
        in_file_prefix = "dataset/test/"
        in_file_suffix = "_skeleton_proj.txt"
        out_file_name = "cust_d1.t"
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

        distances_0 = [] # head / right elbow
        distances_1 = [] # head / right hand 
        distances_2 = [] # head / left elbow
        distances_3 = [] # head / left hand 
        distances_4 = [] # head / right knee
        distances_5 = [] # head / right foot 
        distances_6 = [] # head / left knee
        distances_7 = [] # head / left foot 

        frames = 0 



        # start for loop to go through frames 
        temp_points = []
        for line in in_file: 
            line = line.split()
            joint = int(line[1])
            if(joint == 4 or joint == 6 or joint == 8 or joint == 10 or joint == 12 or joint == 14 or joint == 16 or joint == 18): 
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
                distances_5.append(temp_distances[5])
                distances_6.append(temp_distances[6])
                distances_7.append(temp_distances[7])

                # clear temporary vectors 
                temp_points = []
                temp_distances = []

        

        # make histogram for lengths 
        hist_distances = []

        # head / right elbow
        hist_dist_0 = make_histo(10, 0.2, .7, distances_0)
        hist_distances.extend(hist_dist_0)

        # head / right hand
        hist_dist_1 = make_histo(10, 0.1, 1.1, distances_1)
        hist_distances.extend(hist_dist_1)

        # head / left elbow
        hist_dist_2 = make_histo(10, 0.2, .7, distances_2)
        hist_distances.extend(hist_dist_2)

        # head / left hand 
        hist_dist_3 = make_histo(10, 0.1, 1.1, distances_3)
        hist_distances.extend(hist_dist_3)

        # head / right knee
        hist_dist_4 = make_histo(10, 0.3, 1.2, distances_4)
        hist_distances.extend(hist_dist_4)
        
        # head / right foot 
        hist_dist_5 = make_histo(10, 0.6, 1.6, distances_5)
        hist_distances.extend(hist_dist_5)
        
        # head / left knee
        hist_dist_6 = make_histo(10, 0.3, 1.2, distances_6)
        hist_distances.extend(hist_dist_6)
        
        # head / left foot 
        hist_dist_7 = make_histo(10, 0.6, 1.6, distances_7)
        hist_distances.extend(hist_dist_7)        

        hist_distances = normalize(hist_distances, frames)

        for i in range(0, len(hist_distances)): 
            out_file.write(str(hist_distances[i]))
            out_file.write(" ")

        out_file.write("\n")

    out_file.close()

def main(): 

    run(1) # run for training files
    run(2) # run for testing files

if __name__ == "__main__": 
    main()