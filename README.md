# DTI Processing Pipeline

This repository contains a Python-based DTI (Diffusion Tensor Imaging) processing pipeline that processes DICOM data, corrects for motion and distortions using FSL, fits a tensor model, and generates Fractional Anisotropy (FA), Mean Diffusivity (MD), Radial Diffusivity (RD), and Axial Diffusivity (AD) maps.

## Dependencies

- Python 3
- Dipy
- NiBabel
- Nipype
- FSL
- Matplotlib

## Usage

1. Clone this repository and navigate to the project folder.

2. Install the required dependencies.

3. Update the `path`, `input_dir`, `output_dir`, `bval_file`, `bvec_file`, and `TotalReadoutTime` variables in the `if __name__ == "__main__":` block of the `dti_processing.py` script to match your local setup.

4. Run the `dti_processing.py` script:

```bash
python dti_processing.py
