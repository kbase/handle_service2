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

# install pipenv
RUN pip install --upgrade pip && \
    pip install pipenv

# install deps
COPY Pipfile* ./
RUN pipenv sync

# activate virtual env
RUN pipenv shell

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
