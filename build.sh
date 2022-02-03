docker build -f ./Dockerfile -t synodriver/nsfw:v1.1 .

docker run -d -p 9002:9000 -v /home/lighthouse/nsfwlog:/log synodriver/nsfw:v1.1

