FROM nginx:latest
# We need libmupdf-dev <=1.16 or pymupdf won't build
RUN echo 'deb https://deb.debian.org/debian/ bullseye main' >> /etc/apt/sources.list
RUN apt-get update && \
    apt-get -y install pandoc python3 python3-bs4 python3-pip libfreetype6-dev git && \
    apt-get clean
WORKDIR /mupdf
RUN git clone --recursive git://git.ghostscript.com/mupdf.git . && \
    git submodule update --init
RUN make HAVE_X11=no HAVE_GLUT=no prefix=/usr/local install
RUN pip3 install algebraic-data-types pymupdf requests

COPY . /mat
WORKDIR /mat/web
RUN mv assets /usr/share/nginx/html/

CMD ./run.sh
