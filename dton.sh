#!/bin/bash

# Check if the number of arguments is correct
if [ $# -ne 1 ]; then
    echo "Usage: $0 participants_file"
    exit 1
fi

# Read participant IDs from file
participants_file=$1
participants=($(cat $participants_file))

# Path to data directory
path='/Users/masonkadem/Downloads/MRI/chickens'

# Loop over participants
for participant in "${participants[@]}"; do
    echo "Converting participant: $participant"

    # Define input directories for anatomical and functional scans
    participant_dir="$path/$participant"
    anatomical_input_dir="$participant_dir/3D"
    functional_input_dir="$participant_dir/fMRI"

    # Run dcm2niix for anatomical scans
    dcm2niix -z y -f "${participant}_3D" -o "$anatomical_input_dir" "$anatomical_input_dir"

    # Run dcm2niix for functional scans
    dcm2niix -z y -f "${participant}_fMRI" -o "$functional_input_dir" "$functional_input_dir"

done

echo "Conversion complete"
