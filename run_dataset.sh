#!/usr/bin/env zsh
#SBATCH --job-name=arldm
#SBATCH --partition=research
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --time=0-15:00:00
#SBATCH --output="arldm-%j.txt"
#SBATCH -G 2
cd $SLURM_SUBMIT_DIR
module load anaconda/full
bootstrap_conda
conda activate arldm
python3 /srv/home/kumar256/ARLDM/data_script/ssid_hdf5.py --ssid_json_dir /srv/home/kumar256/ARLDM/SSID/SSID_Annotations --img_dir /srv/home/kumar256/ARLDM/SSID/SSID_Images --save_path /srv/home/kumar256/ARLDM/ssid.hdf5