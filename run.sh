 #!/bin/sh
#cd ./Dockerfile
#docker build --platform linux/amd64 .
#docker build -t facial_decognition:v2 .

docker run -it  --rm --privileged \
         -v /tmp/.X11-unix:/tmp/.X11-unix \
         -v /etc/localtime:/etc/localtime \
         -v $HOME/code//DL_YouTube:/home/shu_docker/ws:rw \
         -e DISPLAY=$DISPLAY \
         --name dl_youtube \
         dl_youtube:v1 bash