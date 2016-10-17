RUN apt-get update -q
RUN apt-get install -qy texlive-full 

docker pull jupyter/notebook
docker pull jupyter/nbviewer
docker run -p 8080:8080 jupyter/nbviewer
