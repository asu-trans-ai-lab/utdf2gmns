#!/bin/bash
#SBATCH -N 1                            # number of nodes
#SBATCH -n 1                            # number of "tasks" (cores)   n-total cores; c-each node, MPI require tasks n  > 1
#SBATCH --mem=1G                        # GigaBytes of RAM required  each node
#SBATCH -t 0-1:00:00                    # time in d-hh:mm:ss
#SBATCH -p serial                       # Partition (serial) parallel fn1 fn3 asing250cpu1
#SBATCH -q normal                       # QOS (normal)

#SBATCH -o slurm-%j.out                 # File to save job's STDOUT to (%j = JobId)
#SBATCH -e slurm-%j.err                 # File to save job's STDERR to (%j = JobId)
##SBATCH --mail-type=ALL                # Send a notification when a job starts, stops, or fails
##SBATCH --mail-user=jiaweil9@asu.edu   # Send-to address

# Always purge modules to ensure a consistent environment
module purge

# load required modules for jobs enviromnent
# module load python/3.7.1

# load anaconda
module load anaconda/py3

# activate virtual environment

source activate xluo_civ

# conda install python=3.10.4

# can not install geocoder using conda, pip3 instead
# conda install geocoder

# run function with arguments
python utdf2gmns.py
