# set base image (host OS)
FROM python:3.7

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .
COPY dist/ .
# install dependencies
RUN pip install -r requirements.txt
RUN pip install dbaric_parser_gid-0.0.1.tar.gz
# copy the content of the local src directory to the working directory
COPY src/ .
COPY setup.py .

ARG INSTANCE_NUM
ENV INSTANCE_NUM=$INSTANCE_NUM

#ARG TOTAL_INSTANCES
#ENV TOTAL_INSTANCES=$TOTAL_INSTANCES
# command to run on container start
CMD ["sh", "-c", "python setup.py $INSTANCE_NUM"]
#CMD ["sh", "-c", "python  parse_gid_files.py $INSTANCE_NUM $TOTAL_INSTANCES"]


