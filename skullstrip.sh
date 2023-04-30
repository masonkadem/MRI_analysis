#!/bin/bash

# List of participant IDs
participants=("chicken2" "chicken3" "chicken4" "chicken5" "chicken6" "chicken7" "chicken8")

path='/Users/masonkadem/Downloads/MRI/chickens'

# Loop over participants
for participant in "${participants[@]}"; do
    echo "Skull-stripping participant: $participant"

    # Define input directories for anatomical and functional scans
    participant_dir="$path/$participant"
    anatomical_input_dir="$participant_dir/3D"
    functional_input_dir="$participant_dir/fMRI"
    
    # Check for skull-stripped brain files
    if [ ! -f "$anatomical_input_dir/"*brain.nii.gz ]; then
        echo "No brain found"
        
        input_file = "$anatomical_input_dir/"*.nii.gz
        output_file = "$anatomical_input_dir/_brain.nii.gz"

        bet2 $input_file $output_file -f 0.3
    fi
done

echo "Skull-stripped for all participants."
