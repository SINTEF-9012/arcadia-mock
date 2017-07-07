
# ARCADIA Mock

[![wercker status](https://app.wercker.com/status/7afc51aae94fd1a3ab97518535e7c9eb/s/master "wercker status")](https://app.wercker.com/project/byKey/7afc51aae94fd1a3ab97518535e7c9eb)
[![CodeCov](https://img.shields.io/codecov/c/github/SINTEF-9012/arcadia-mock/master.svg)](https://codecov.io/gh/SINTEF-9012/arcadia-mock)
[![Codacy grade](https://img.shields.io/codacy/grade/5c06860e96d54742937e4bcbbc946f08.svg)](https://www.codacy.com/app/fchauvel/arcadia-mock)
[![License](https://img.shields.io/github/license/SINTEF-9012/arcadia-mock.svg)]()

This is a mock of the ARCADIA services, used for testing the TOSCA
Arcadia plugin. It includes a set of REST services that mimics the
ARCADIA ones, and a client API that eases integration with Python 2.7.

## End-points

In the current version (v0.0.3), requests can specify the type of content they would like to receive in the `accept` header field.

 * GET `/service_graphs`, returns the service graphs currently registered.
 * POST `/register`, submit a new service_graphs. So far XML is expected, as follows:
 
````xml
	 <?xml version="1.0" encoding="UTF-8"?>
	 <ServiceGraph>
		 <DescriptiveSGMetadata>
			<SGID>wordpress_mysql_service_graph_id</SGID>
			<SGName>SimpleWordPressServiceGraph</SGName>
			<SGDescription>SGDescription</SGDescription>
		</DescriptiveSGMetadata>
		<GraphNodeDescriptor>
			<GraphNode>
				<NID>graph_node_mysql_id</NID>
				<CNID>mysql_id</CNID>
			</GraphNode>
			<GraphNode>
				<NID>graph_node_wordpress_id</NID>
				<CNID>wordpress_id</CNID>
				<GraphDependency>
					<CEPCID>mysqltcp_cepcid</CEPCID>
					<ECEPID>mysqltcp</ECEPID>
					<NID>NID</NID>
				</GraphDependency>
			</GraphNode>
		</GraphNodeDescriptor>
		<RuntimePolicyDescriptor>
			<RuntimePolicy>
				<RPID>RPID</RPID>
				<RPName>RPName</RPName>
			</RuntimePolicy>
		</RuntimePolicyDescriptor>
	</ServiceGraph>
````

* GET `/components` returns the list of components registered so far

* POST `/components` register a new component, described by an XML snippet as follow:
````xml
<Component>
	<CID>1</CID>
	<CNID>2</CNID>
	<CEPNID>3</CEPNID>
	<ECEPCNID>4</ECEPCNID>\
</Component>\
````

 * GET `/about`, returns some debug info, such as version number and license.

## Installation & Usage

This is a Python 2.7 application. To install it, run the followings commands (assuming you are running Linux-like OS):

	$> cd my-working-directory
	$> git clone git@github.com:SINTEF-9012/arcadia-mock.git
	$> cd arcadiamock
	$> pip install .
	$> arcadiamock

Note that if you want to develop or modify the code, you may want to install it using the `-e` option of pip, as:

	$> pip install -e .

## Testing

ARCADIA mocks comes with a test suite that checks whether its basic
functionalities. You can run it with the following commands:

	$> tox -e py27

or

	$> python setup.py test

In addition, you can measure the code coverage by running this test
suite inside the 'coverage' tool.

	$> coverage run setup.py test
	$> coverage combine
	$> coverage report -m

The test suite includes some acceptance tests that take some time to
run because they spawn an HTTP server in the background and then
request specific pages.

For coverage to account for these integration tests, you must define
the environment variable `COVERAGE_PROCESS_START` as follows:

	$> export COVERAGE_PROCESS_START=".coveragerc"

You must as well include the following lines in the `sitecustomize.py`
of your virtual environment, as follows:

	$> echo "import coverage; coverage.process_startup()" > venv/lib/python2.7/site-packages/sitecustomize.py 

## Releasing

You can release and deploy automatically by two shell scripts located
in `etc/`, namely `release.sh`and `deploy.sh`. `release.sh` tests the
application, fetches the version number from
`arcadia-mock/__init__.py`, tags the repository, and finally builds
and pushes a new docker image in the
[`fchauvel/arcadia-mock`](https://hub.docker.com/r/fchauvel/arcadia-mock/tags/)
repository. `deploy.sh` is meant to be run on the remote host. It
stops and delete the current container, fetches the latest docker
image and restarts a container with it.

After editing the version number as desired, you can release and
deploy as follows:

	$> source etc/release.sh
	$> ssh -i path/to/my/key.pem ec2-user@W.X.Y.Z "bash -s" < etc/deploy.sh

