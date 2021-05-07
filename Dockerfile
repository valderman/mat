FROM nginx:latest
# We need g++-10 or pymupdf won't build
RUN echo 'deb https://deb.debian.org/debian/ bullseye main non-free contrib' >> /etc/apt/sources.list
RUN apt-get update && \
    apt-get -y install pandoc python3 python3-bs4 python3-pip libmupdf-dev libfreetype6-dev && \
    apt-get clean
RUN pip3 install algebraic-data-types pymupdf requests

COPY . /mat
WORKDIR /mat/web
RUN mv assets /usr/share/nginx/html/

CMD ./run.sh
