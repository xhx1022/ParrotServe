#!/bin/sh

rm -rf log

echo "Run benchmark: Parrot"

pwd=$PWD
log_path=$pwd/log/

echo $log_path

# Launch cluster
cd cluster_1_vicuna_13b_shared
bash launch.sh $log_path os.log engine.log

# Run benchmark
cd ..
python3 bench_hack_parrot.py cache > result_parrot.txt # > log/program.log

# Kill cluster
bash ../../scripts/kill_all_servers.sh