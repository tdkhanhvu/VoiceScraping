FROM ubuntu:16.04
SHELL [ "/bin/bash", "--login", "-c" ]

ENV HOME /home
ENV PROJECT_DIR $HOME/app
RUN mkdir -p $PROJECT_DIR

COPY . $PROJECT_DIR

RUN apt-get update \
  && apt-get install -y wget

# install miniconda
ENV CONDA_DIR $HOME/miniconda3
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-4.7.12.1-Linux-x86_64.sh -O ~/miniconda.sh && \
    chmod +x ~/miniconda.sh && \
    ~/miniconda.sh -b -p $CONDA_DIR && \
    rm ~/miniconda.sh
# make non-activate conda commands available
ENV PATH=$CONDA_DIR/bin:$PATH
# make conda activate command available from /bin/bash --login shells
RUN echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.profile

# make conda activate command available from /bin/bash --interative shells
RUN conda init bash

WORKDIR $PROJECT_DIR

# build the conda environment
ENV ENV_PREFIX VoiceScraping
RUN conda env create --file $PROJECT_DIR/env.yml && \
	conda env update --file $PROJECT_DIR/env_os_additional.yml

RUN conda activate $ENV_PREFIX
