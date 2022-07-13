#!/usr/bin/env bash
# The name to show in queue lists for this job:
#SBATCH -J 05_run_knn_parallel

# Number of desired cores (can be in any node):
##SBATCH --ntasks=1

# Number of desired cores (can be in any node):
##SBATCH --ntasks=1

# Number of desired cores (all in same node):
#SBATCH --cpus-per-task=10

# Amount of RAM needed for this job:
#SBATCH --mem=2gb

# The time the job will be running:
#SBATCH --time=10:00:00

# To use GPUs you have to request them:
##SBATCH --gres=gpu:1

# If you need nodes with special features uncomment the desired constraint line:
# * to request only the machines with 80 cores and 2TB of RAM
#SBATCH --constraint=sd

# Set output and error files

##SBATCH --error=get_active_constraints_general_MILP.%a.%J.err
##SBATCH --output=get_active_constraints_general_MILP.%a.%J.out

#SBATCH --error=/dev/null
#SBATCH --output=/dev/null

# MAKE AN ARRAY JOB, SLURM_ARRAY_TASK_ID will take values from 1 to 100
#SBATCH --array=1-10

# To load some software (you can show the list with 'module avail'):
module purge
module load cplex/20.1.0

# the program to execute with its parameters:
time python3 05_run_knn_parallel.py
