## TexBox Server

Docker container for a flask app to generate SVG and PNG files from LaTeX.

## Usage

    docker run -i codingdesires/texbox:amd64

THe origianl texbox can be found at:
[dmoj/texbox](https://github.com/DMOJ/texbox.git)

The original texbox solution above does not work as is. This repository introduces modifications to the dockerfile and changes it to a flask application that takes in latex code and parses it to svg.

`\begin{document}` and `\end{document}` are required.
