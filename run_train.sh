#!/usr/bin/env zsh
#SBATCH --job-name=arldm
#SBATCH --partition=research
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=40G
#SBATCH --time=0-24:00:00
#SBATCH --output="arldm-%j.txt"
#SBATCH -G a100:1
cd $SLURM_SUBMIT_DIR
module load anaconda/full
bootstrap_conda
conda activate arldm
python3 /srv/home/kumar256/ARLDM/main.py 