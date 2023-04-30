#!/bin/bash

# List of participant IDs
participants=("chicken2" "chicken3" "chicken4" "chicken5" "chicken6" "chicken7" "chicken8")

path='/Users/masonkadem/Downloads/MRI/chickens'

# Loop over participants
for participant in "${participants[@]}"; do
    echo "Removing .feat directories for participant: $participant"

    # Define directory
    participant_dir="$path/$participant"

    # Change directory
    cd "$participant_dir"


    # Create 3D for anat
    to3d -epan -time:tz 1 96 12 altplus -prefix 3D/output_dataset "E*.*" 
    # Create 3D for func
    to3d -epan -time:tz 1 96 12 altplus -prefix fMRI/output_func "E*.*" 

    #standardize
    @auto_tlrc -base //Users/masonkadem/abin/TT_N27+tlrc -input 3D/output_dataset+orig

    align_epi_anat.py -anat 3D/output_dataset+orig -epi fMRI/output_func+orig -epi_base 6 -epi2anat -suffix _ALIGNED \
    -volreg_method 3dWarpDrive -epi_strip 3dSkullStrip -tlrc_apar 3D/output_dataset+tlrc

done


