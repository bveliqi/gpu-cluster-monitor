nvidia-smi --query-gpu=index,timestamp,name,temperature.gpu,utilization.gpu,utilization.memory,memory.total,memory.free,memory.used,pstate --format=csv > ../data/gpu.csv