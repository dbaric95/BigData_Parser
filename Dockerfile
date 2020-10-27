# set base image (host OS)
FROM python:3.7

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .
COPY dist/ .
COPY src/ .
# install dependencies
RUN pip install -r requirements.txt
RUN pip install dbaric_parser_gid-0.0.1.tar.gz
# copy the content of the local src directory to the working directory

ARG CHANNEL_INSTANCE
ENV CHANNEL_INSTANCE=$CHANNEL_INSTANCE

ARG PATH_INSTANCES
ENV PATH_INSTANCES=$PATH_INSTANCES

# command to run on container start
CMD ["sh", "-c", "python parse_gid_files.py -c ${CHANNEL_INSTANCE} -p ${PATH_INSTANCES}"]

