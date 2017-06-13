
# ARCADIA Mock

This is a mock of the ARCADIA services, used for testing the TOSCA
Arcadia plugin. It includes a set of REST services that mimics the
ARCADIA ones, and a client API that eases integration with Python 2.7.

# Installation & Usage

This is a Python 2.7 application. To install it, run the followings commands (assuming you are running Linux-like OS):

	$> cd my-working-directory
	$> git clone arcadia-mock.git
	$> cd arcadiamock
	$> pip install .
	$> arcadiamock
	
Note that if you want to develop or modify the code, you may want to install it using the `-e` option of pip, as:
	
	$> pip install -e .


# Work Plan


1. GET /about should returns the version, copyright and license
   
   1. Package and release as 0.0.1 
   
   2. Tests in place
    
   3. Coverage in place

2. Make a map on the existing ARCADIA API
