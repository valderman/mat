FROM nginx:latest
RUN echo 'deb https://deb.debian.org/debian/ bullseye main' >> /etc/apt/sources.list
RUN apt-get update && \
    apt-get -y install pandoc python3 python3-bs4 python3-pip libfreetype-dev libfreetype6-dev git wget unzip xz-utils pkg-config && \
    apt-get clean
WORKDIR /mupdf
RUN wget https://www.mupdf.com/downloads/archive/mupdf-1.18.0-source.tar.xz && \
    tar xf mupdf-1.18.0-source.tar.xz && \
    rm mupdf-1.18.0-source.tar.xz
WORKDIR /mupdf/mupdf-1.18.0-source
RUN sh -c 'CFLAGS="-fPIC -std=c99" make HAVE_X11=no HAVE_GLUT=no prefix=/usr/local install' && \
    cd / && \
    rm -rf /mupdf
RUN ln -s /usr/include/freetype2/ft2build.h /usr/include
RUN ln -s /usr/include/freetype2/freetype /usr/include
RUN pip3 install algebraic-data-types pymupdf==1.18.7 requests

COPY . /mat
WORKDIR /mat/web
RUN mv assets /usr/share/nginx/html/

CMD ./run.sh
