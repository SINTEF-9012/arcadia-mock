#
# ARCADIA Mocks
#
# Copyright (C) 2017 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

FROM python:2.7-slim

LABEL maintainer "anatoly.vasilevskiy@sintef.no"

# Install
WORKDIR /arcadia-mock
COPY . /arcadia-mock
RUN pip install -r requirements.txt
RUN pip install .

# Make port 1234 available to the world outside this container
EXPOSE 1234

# Define environment variable
ENV NAME arcadia-mock

# Run arcadiamock when the container launches
CMD ["arcadiamock", "--name", "0.0.0.0", "--port", "1234"]
