FROM andrewosh/binder-base

MAINTAINER Boris Leistedt <boris.leistedt@gmail.com>

USER root

# Add dependency
RUN apt-get update
RUN apt-get install -qy texlive-full

USER main
