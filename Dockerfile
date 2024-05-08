FROM kbase/sdkpython:3.8.10
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

 RUN apt-get update

# Longer term, we should completely redo the testing rig to allow for running tests without
# kb-sdk. E.g. start up local instances of mongo, minio, auth, blobstore, and the handle service,
# create users in auth, the whole shebang. See the workspace for how do to this.

RUN apt-get install wget

#####################
### install dockerize
#####################

# TODO DOCKERFILE switch from dockerize to rancher env driven config. See collections for an
#                 example.

WORKDIR /opt
RUN wget -q https://github.com/kbase/dockerize/raw/master/dockerize-linux-amd64-v0.6.1.tar.gz \
    && tar xvzf dockerize-linux-amd64-v0.6.1.tar.gz \
    && rm dockerize-linux-amd64-v0.6.1.tar.gz
RUN mkdir -p /kb/deployment/bin/
RUN ln -s /opt/dockerize /kb/deployment/bin/dockerize

###################
### install mongodb
###################

# TODO Set things up so we can test against multiple versions of Mongo in GHA. This might work?
ENV MONGO_VER=mongodb-linux-x86_64-3.6.23

RUN mkdir -p /mongo/tmpdata
WORKDIR /mongo
RUN wget -q http://fastdl.mongodb.org/linux/$MONGO_VER.tgz
RUN tar xfz $MONGO_VER.tgz && rm $MONGO_VER.tgz
ENV MONGO_EXE_PATH=/mongo/$MONGO_VER/bin/mongod
ENV MONGO_TEMP_DIR=/mongo/tmpdata
RUN echo $MONGO_EXE_PATH
RUN echo $MONGO_TEMP_DIR
RUN $MONGO_EXE_PATH --version

#######################
### Install python deps
#######################

RUN conda config --add channels conda-forge
# uwsgi install fails with pip due to some kind of incompatibility with conda
# note this step takes FOREVER
# should probably try to get rid of conda, it's a nightmare to deal with
RUN conda install -y uwsgi=2.0.22

# Conda fails to install these due to what appears to be an overly strict dependency graph solver
RUN pip install \
        cachetools==4.2.2 \
        mock==4.0.3 \
        pymongo==3.8.0 \
        pytest==8.2.0 \
        pytest-cov==5.0.0 \
        requests==2.31.0 \
        semver==3.0.2

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
