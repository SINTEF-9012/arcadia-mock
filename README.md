
# ARCADIA Mock

[![wercker status](https://app.wercker.com/status/7afc51aae94fd1a3ab97518535e7c9eb/s/master "wercker status")](https://app.wercker.com/project/byKey/7afc51aae94fd1a3ab97518535e7c9eb)
[![CodeCov](https://img.shields.io/codecov/c/github/SINTEF-9012/arcadia-mock/master.svg)](https://codecov.io/gh/SINTEF-9012/arcadia-mock)
[![Codacy grade](https://img.shields.io/codacy/grade/5c06860e96d54742937e4bcbbc946f08.svg)](https://www.codacy.com/app/fchauvel/arcadia-mock)
[![License](https://img.shields.io/github/license/SINTEF-9012/arcadia-mock.svg)]()

This is a mock of the ARCADIA services, used for testing the TOSCA
Arcadia plugin. It includes a set of REST services that mimics the
ARCADIA ones, and a client API that eases integration with Python 2.7.

# Installation & Usage

This is a Python 2.7 application. To install it, run the followings commands (assuming you are running Linux-like OS):

	$> cd my-working-directory
	$> git clone git@github.com:SINTEF-9012/arcadia-mock.git
	$> cd arcadiamock
	$> pip install .
	$> arcadiamock
	
Note that if you want to develop or modify the code, you may want to install it using the `-e` option of pip, as:
	
	$> pip install -e .

# Testing

ARCADIA mocks comes with a test suite that checks whether its basic
functionalities. You can run it with the following commands:

	$> python setup.py test
	
In addition, you can measure the code coverage by running this test
suite inside the 'coverage' tool.

	$> coverage run setup.py test
	$> coverage report -m

The test suite includes some acceptance tests that take some time to
run because they start an HTTP server in the background and then
request specific pages.


# Work Plan

1. GET /about should returns the version, copyright and license
   
   1. Package and release as 0.0.1 
   
   2. Tests in place
    
   3. Coverage in place

2. Make a map on the existing ARCADIA API
