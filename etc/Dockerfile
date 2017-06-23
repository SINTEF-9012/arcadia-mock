#
# ARCADIA Mocks
#
# Copyright (C) 2017 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

LABEL maintainer "franck.chauvel@sintef.no"

FROM python:2.7-slim

# Install required tools
RUN apt-get -qq update
RUN apt-get install -qq -y git=1:2.1.4-2.1+deb8u3 curl=7.38.0-4+deb8u5

# Fetch and ARCADIA-mock sources from Github
RUN curl -L -o arcadia-mock_v0.0.1.tar.gz https://github.com/SINTEF-9012/arcadia-mock/archive/v0.0.1.tar.gz
RUN tar -xzf arcadia-mock_v0.0.1.tar.gz

# Install
WORKDIR /arcadia-mock-0.0.1
RUN pip install -r requirements.txt
RUN pip install .

# Make port 1234 available to the world outside this container
EXPOSE 1234

# Define environment variable
ENV NAME arcadia-mock

# Run arcadiamock when the container launches
CMD ["arcadiamock", "--name", "0.0.0.0", "--port", "1234"]
