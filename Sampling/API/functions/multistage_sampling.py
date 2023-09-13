import time
from API.functions.sampleSize import dowellSampleSize
from API.functions.simpleRandomSampling import dowellSimpleRandomSampling
from API.functions.stratifiedSampling import dowellStratifiedSampling

def dowellmultistagesampling():
    # Define the number of stages
    S = int(input("Enter the number of stages: "))

    # List to store the selected units at each stage
    sample_values = []

    # Iterate over each stage
    for stage in range(1, S+1):
        print(f"\nStage {stage}:")
        
        # Choose the sampling method for the current stage
        sampling_method = dowellindex()
        
        # Check if the user entered "0" for the current stage
        if sampling_method == 0:
            print("Sampling stopped.")
            break
        
        # Determine the number of units to be selected in the current stage
        si = dowellSampleSize(stage,0.5)
        
        # Check if the selected sampling method is Simple Random Sampling
        if sampling_method == 1:
            sample = dowellSimpleRandomSampling(si)
        # Check if the selected sampling method is Stratified Sampling
        elif sampling_method == 2:
            sample = dowellStratifiedSampling(si)
        else:
            print("Invalid sampling method.")
            continue
        
        # Add the selected sample to the list of sample values
        sample_values.append(sample)
    
    # Process time
    process_time = time.process_time()
    
    # Permutation chosen
    permutation_chosen = None  # Placeholder for permutation chosen
    
    return sample_values, process_time, permutation_chosen

def dowellindex():
    # Display the list of sampling techniques and get user input
    print("Sampling Techniques:")
    print("1. Simple Random Sampling")
    print("2. Stratified Sampling")
    index = int(input("Choose a sampling technique (0 to stop): "))
    return index


# Example usage
sample_values, process_time, permutation_chosen = dowellmultistagesampling()
print("Sample Values:", sample_values)
print("Process Time:", process_time)
print("Permutation Chosen:", permutation_chosen)





# start																									
# 	Call dowellmultistagesampling(Number of Stages,First Stage Units,Second Stage units,...)																								
																									
# 		Define number of stages as variable "S"																							
# 			Input from user																						
# 		Choose sampling method from the list containing all the sampling techniques for First stage units																							
# 			Call dowellindex()																						
# 				input from user or frontend programmer																					
# 		Choose sampling method from the list containing all the sampling techniques for Second stage units																							
# 			Call dowellindex()																						
# 				input from user or frontend programmer																					
# 		Choose sampling method from the list containing all the sampling techniques for Third stage units																							
# 			Call dowellindex()																						
# 				input from user or frontend programmer																					
# 		Continue this depending on number of stages																							
																									
# 		Define number of units to be selected in each stage as variable "si"																							
# 			Call dowellsamplesize() for each stage																						
																									
# 			Check number of stages S																						
# 				if  1<S<=5,then continue																					
# 				if not,prompt " enter adequate number of Stages																					
																									
# 			For first stage,check																						
# 				if user has entered "0",then prompt "not allowed"																					
# 				Choose from 1 to 12																					
																									
# 			If selected sampling method is Simple Random Sampling																						
# 				Call dowellrandomsampling()																					
# 			If selected sampling method is Simple Random Sampling																						
# 				Calldowellstratifiedsampling()																					
# 			Continue this depending on the selections for each stage																						
																									
# 		if for any stage(except first stage) user has entered "0",then the function should stop at that stage only																							
																									
																									
# 	Function output(sample values at each stage,process time,permutation chosen)	