docker run --name gpu-mongodb -d \
    --restart always \
    -v /gpfs01/bethge/home/bveliqi/gpu-mongodb:/data/db \
    -p 27017:27017 \
    mongo:3.7.7-jessie