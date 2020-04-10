# this is where the RAD will be implemented 



# Input:   Training setTrainor testing setTest
# Output:  radd1orradd1.t

# for each instance in Train or Test do
    # for frame t = 1, ..., T do
        # Select joints that form a star skeleton
        # Compute and store distances between body
        # extremities to body center (dt1,...,dt5)
        # Compute and store angles between two adjacent body
        # extremities (θt1,...,θt5)
    # Compute a histogram ofNbins for eachdi={dti}Tt=1, i= 1,...,5
    # Compute a histogram ofMbins for eachθi={θti}Tt=1, i= 1,...,5
    # Normalize the histograms by dividingTto compensatefor different number of frames in a data instance
    # Concatenate all normalized histograms into aone-dimensional vector of length5(M+N)
    # Convert the feature vector as a single line in the radd1orradd1.t file