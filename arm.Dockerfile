FROM python:3.10-slim-bullseye

# Install minimal TeX Live with chemfig and dvisvgm
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        texlive-latex-base \
        texlive-latex-recommended \
        texlive-latex-extra \
        texlive-extra-utils \
        texlive-fonts-recommended \
        texlive-science \
        lmodern \
        dvisvgm \
        ghostscript \
        librsvg2-bin \
        xxd \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY worker /
COPY app.py /

RUN pip install flask flask-cors

EXPOSE 8080
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8080"]

