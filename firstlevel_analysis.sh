#!/bin/bash


#This script performs 1st level analysis across all particpants with the assumptions that dicom to nifti conversion and skull stripping were performed, in addition to a first participant run


# List of participant IDs
participants=("chicken2" "chicken3" "chicken4" "chicken5" "chicken6" "chicken7" "chicken8")

path='/Users/masonkadem/Downloads/MRI/chickens'

# Loop over participants
for participant in "${participants[@]}"; do
    echo "Analyzing participant: $participant"

    # Define directory
    participant_dir="$path/$participant"

    # Change directory
    cd "$participant_dir" 
    # Already copied the design files into subjects' directory
    cp ../design.fsf .

    # change subject path in design.fsf file
    sed -i '' "s|chicken1|${participant}|g" design.fsf
    
    # sed -i '' "s|3D_4BF3-LAB3_20141015164644_3_brain.nii.gz|_brain.nii.gz|g" design.fsf
    # run feat
    feat design.fsf

    # Repeat loop
    cd ..
done

