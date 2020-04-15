Project 3 Deliverable 1 - Alexandria Leto 


To run either script, simply untar and cd into the directory, then run the command  "python cust.py" or "python rad.py", 
respectively. This will generate the necessary files. 

For every histogram computed in both implementations, 10 bins were used. The histograms were created by adjusting the 
minimum and maximum values and printing the result until the desired (approximate) histogram was obtained. 

In the RAD implementation, the stomach, head, left hand, left foot, right hand, and right foot were used to compute 
relative angles and distances. In my custom algorithm, however, I used the head, right hand, right elbow, right knee, 
right foot, left hand, left elbow, left knee, and left foot. Instead of using relative angles, I computed the difference
between the location of the head and each other joint recorded. The purpose of doing so was to eliminate the more 
rigorous math involved in computing relative angles. In order to replace the information that the angles provided, I 
included the elbow and knee joints. 

