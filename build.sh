docker build -f ./Dockerfile -t synodriver/nsfw:v1.2 .

docker run -d -p 9002:9000 synodriver/nsfw:v1.2

