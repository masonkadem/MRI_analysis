import os
from dipy.io import read_bvals_bvecs
from dipy.core.gradients import gradient_table
from dipy.reconst.dti import TensorModel
import subprocess
from pathlib import Path
import nibabel as nib
from nipype.interfaces import fsl
import matplotlib.pyplot as plt
import argparse


def run_dti(path, input_dir, output_dir, bval_file, bvec_file, TotalReadoutTime):

    """
    This function processes DTI data using dcm2niix, BET, and FSL Eddy, then fits a tensor model
    and generates DTI maps.

    Parameters:
    path (str): Path to the working directory.
    input_dir (str): Path to the input directory containing DICOM files.
    output_dir (str): Path to the output directory for intermediate and final results.
    bval_file (str): Path to the .bval file.
    bvec_file (str): Path to the .bvec file.
    TotalReadoutTime (float): Total readout time in seconds.

    Returns:
    None: This function does not return any values. It generates plots and saves files in the output directory.
    """

    # Change working directory
    cwdir = os.getcwd()
    os.chdir(path)

     # Convert DICOM files to NIfTI format using dcm2niix
    result = subprocess.run(["dcm2niix", "-o", output_dir, input_dir], check=True, capture_output=True, text=True)
    nifti_file = Path(output_dir) / result.stdout.split('->')[1].strip()

    # Skull stripping using BET
    subprocess.run(["bet", str(nifti_file), str(output_dir / "brain"), "-m", "-f", "0.3"], check=True)
    
    # Create acqp file for Eddy
    acq_file = open("acqp.txt", "w")
    acq_file.write(f"0 1 0 {TotalReadoutTime}\n 0 -1 0 {TotalReadoutTime}") 
    acq_file.close()

    # Generate index file for Eddy
    img = nib.load(nifti_file).get_fdata()
    nvolumes = img.shape[-1]
    index_file = open("index.txt", "w")
    for i in range(nvolumes):
        index_file.write("1 ")
    index_file.close()

    # Run FSL Eddy for motion and distortion correction
    eddy = fsl.Eddy()
    eddy.inputs.in_file = nifti_file
    eddy.inputs.in_mask = str(output_dir / "hifi_mask.nii.gz")  # Add mask input
    eddy.inputs.in_bval = bval_file
    eddy.inputs.in_bvec = bvec_file
    eddy.inputs.in_acqp = "acqp.txt"
    eddy.inputs.out_base = "eddy_corrected"
    eddy.cmdline  # This prints the command that will be run
    res = eddy.run()

    # Define new paths for processed data
    dti_file = 'eddy_corrected.nii.gz'
    brainmask_file = 'brain_mask.nii.gz'
    bval = bval_file
    bvec = 'eddy_corrected.eddy_rotated_bvecs'

    # Load data and brainmask
    data = nib.load(dti_file).get_fdata()
    brainmask = nib.load(brainmask_file).get_fdata()
    gradient = gradient_table(*read_bvals_bvecs(bval, bvec))

    # Fit tensor model
    model = TensorModel(gradient).fit(data, brainmask)

    # Create output directory for DTI results
    output_path = os.path.join(path, 'DTI')
    os.makedirs(output_path, exist_ok=True)

    # Calculate metrics and save as NIfTI images
    metrics = {'FA': model.fa, 'MD': model.md, 'RD': model.rd, 'AD': model.ad}
    for metric, data in metrics.items():
        nib.save(nib.Nifti1Image(data, nib.load(dti_file).affine), os.path.join(output_path, f'{metric}.nii.gz'))

    # Set plotting style
    plt.style.use('default')

    # Plot DTI maps
    fig, axs = plt.subplots(2, 2, figsize=(10, 10), subplot_kw={'xticks': [], 'yticks': []})
    fig.suptitle('DTI Maps', fontsize=20)

    # Iterate through metrics and display images
    for i, (metric, data) in enumerate(metrics.items()):
        row = i // 2
        col = i % 2     
        axs[row, col].imshow(data[:, :, 20])
        axs[row, col].set_title(metric, fontsize=12)

    # Show plot
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process DTI data and generate DTI maps")
    parser.add_argument("path", help="Path to the working directory")
    parser.add_argument("input_dir", help="Path to the input directory containing DICOM files")
    parser.add_argument("output_dir", help="Path to the output directory for intermediate and final results")
    parser.add_argument("bval_file", help="Path to the .bval file")
    parser.add_argument("bvec_file", help="Path to the .bvec file")
    parser.add_argument("TotalReadoutTime", type=float, help="Total readout time in seconds")

    args = parser.parse_args()

    run_dti(args.path, args.input_dir, args.output_dir, args.bval_file, args.bvec_file, args.TotalReadoutTime)
