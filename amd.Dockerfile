FROM python:3.10-slim-bullseye

# Install TeX Live with proper initialization
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        perl \
        wget \
        && \
    apt-get install -y --no-install-recommends \
        texlive-latex-base \
        texlive-latex-recommended \
        texlive-latex-extra \
        texlive-science \
        texlive-fonts-recommended \
        texlive-extra-utils \
        lmodern \
        dvisvgm \
        ghostscript \
        librsvg2-bin \
        xxd \
        && \
    # Fix permissions and initialize
    chown -R root:root /usr/share/texlive && \
    chmod -R 755 /usr/share/texlive && \
    mktexlsr && \
    fmtutil-sys --all || true && \
    updmap-sys && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY worker /
COPY app.py /

RUN pip install flask flask-cors

EXPOSE 8080
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8080"]