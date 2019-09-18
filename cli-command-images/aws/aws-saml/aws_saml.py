#!/usr/bin/python

import sys
import boto3
from botocore.config import Config
import requests
import getpass
import base64
import logging
import xml.etree.ElementTree as ET
import os
import argparse
import re
import urllib3
from os.path import expanduser
from requests_ntlm import HttpNtlmAuth


# Detect which version of python we are running on.
python_version = sys.version_info[0]

if python_version < 3:
    import ConfigParser
    from StringIO import StringIO
    from bs4 import BeautifulSoup
    from urlparse import urlparse, urlunparse
    configparser = ConfigParser
else:
    import configparser
    from io import StringIO
    from bs4 import BeautifulSoup
    from urllib.parse import urlparse, urlunparse


debug = 0

REGIONS = ["us-east-2", "us-east-1", "us-west-1", "us-west-2", "ca-central-1", "ap-south-1",
           "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-northeast-1",
           "eu-central-1", "eu-west-1", "eu-west-2", "sa-east-1"]

##########################################################################
def write_config_file(filename, configname, outputformat, region, access_id, access_key, token):
    # Create directory if not exists
    dirname = os.path.dirname(filename)

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    # Read in the existing config file
    config = configparser.RawConfigParser()
    config.read(filename)

    # Put the credentials into a specific profile instead of clobbering
    # the default credentials
    if not config.has_section(configname):
        # The "default" section is special for configparser; for some reason we cannot write it
        # with the "add_section" method. So, we do it manually if the '~/.aws/credentials' file is empty.
        if configname is "default":
            with open(filename, 'a') as f:
                f.write('[%s]\n' % configname)
        else:
            config.add_section(configname)

    # Re-read the file so we include the "default" section
    config.read(filename)
    config.set(configname, 'output', outputformat)
    config.set(configname, 'region', region)
    config.set(configname, 'aws_access_key_id', access_id)
    config.set(configname, 'aws_secret_access_key', access_key)
    config.set(configname, 'aws_session_token', token)

    # Write the updated config file
    with open(filename, 'w+') as configfile:
        config.write(configfile)
##########################################################################
# Variables

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-u', '--username', dest='username', help='Your email')
PARSER.add_argument('-p', '--password', dest='password', help='Your password')
PARSER.add_argument('-r', '--region', dest='region', help='the region string e.g us-west-2')
PARSER.add_argument('-i', '--idp-fqdn', default="adfs.example.net", help="The base fqdn of the identity provider url to communicate with for authn/authz.")
PARSER.add_argument('-e', '--export', dest='export', const=True, nargs="?", help='Boolean flag, will print export statements to stdout')
PARSER.add_argument('-d', '--export-docker', dest='export_docker', const=True, nargs="?", help='Boolean flag, will print export statements to stdout for docker')
PARSER.add_argument('-a', '--account', dest='account', help='Human readable name that for the role you want to assume. It may help to run this script and see what options are available before using the flag')
PARSER.add_argument('-t', '--profile', dest='profilename', help='Name of the profile you would like to store the credentails in. Default is the Human readable name of the account in the federated services')

# Parse the above arguments.
ARGS = PARSER.parse_args()

# region: The default AWS region that this script will connect
# to for all API calls
region = ''

# output format: The AWS CLI output format that will be configured in the
# saml profile (affects subsequent CLI calls)
outputformat = 'json'

# awsconfigfile: The file where this script will store the temp
# credentials under the saml profile
awsconfigfile = '~/.aws/credentials'

# Write the AWS STS token into the AWS credential file
filename = os.path.expanduser(awsconfigfile)
dirname = os.path.dirname(filename)

if not os.path.exists(dirname):
    os.makedirs(dirname)

# Fix bug (boto.exception.NoAuthHandlerFound: No handler was ready to authenticate.)
if not os.path.isfile(filename):
    write_config_file(filename, 'default', 'json', 'us-east-1', 'testid', 'testkey', 'testtoken')
else:
    config = configparser.RawConfigParser()
    config.read(filename)
    if not config.has_section('default'):
        write_config_file(filename, 'default', 'json', 'us-east-1', 'testid', 'testkey', 'testtoken')


# SSL certificate verification: Whether or not strict certificate
# verification is done, False should only be used for dev/test
sslverification = True

# idpentryurl: The initial URL that starts the authentication process.
idpentryurl = 'https://{}/adfs/ls/IdpInitiatedSignOn.aspx?loginToRp=urn:amazon:webservices'.format(ARGS.idp_fqdn)

##########################################################################

# Get the federated credentials from the user
if not ARGS.username:
    print("Username: ")
    if python_version < 3:
        username = raw_input()
    else:
        username = input()
else:
    username = ARGS.username

if not ARGS.password:
    password = getpass.getpass()
    print('')
else:
    password = ARGS.password

# Initiate session handler
session = requests.Session()

# Programatically get the SAML assertion
# Set up the NTLM authentication handler by using the provided credential
session.auth = HttpNtlmAuth(username, password, session)

# Opens the initial AD FS URL and follows all of the HTTP302 redirects
response = session.request('GET', idpentryurl, verify=sslverification)

#determine the Input fields for the POST request
soup = BeautifulSoup(response.text, "html.parser")
payload = {}
for inputtag in soup.find_all(re.compile('(INPUT|input)')):
    name = inputtag.get('name','')
    value = inputtag.get('value','')
    if "user" in name.lower():
        #Make an educated guess that this is correct field for username
        payload[name] = username
    elif "email" in name.lower():
        #Some IdPs also label the username field as 'email'
        payload[name] = username
    elif "pass" in name.lower():
        #Make an educated guess that this is correct field for password
        payload[name] = password
    else:
        #Populate the parameter with existing value (picks up hidden fields in the login form)
        payload[name] = value

#make post request
response = session.post(
    idpentryurl, data=payload, verify=sslverification)


# Overwrite and delete the credential variables, just for safety
username = '##############################################'
password = '##############################################'
del username
del password

# Look for the SAMLResponse attribute of the input tag (determined by
# analyzing the debug print lines above)
assertion = ''
soup = BeautifulSoup(response.text, "html.parser")

#Error Checking
try:
    if soup.label.attrs.get('id') == 'errorText':
        for c in soup.label.contents:
            print(c)
except:
    pass # we don't care if this isn't here
#get SAML Response
for inputtag in soup.find_all('input'):
    if(inputtag.get('name') == 'SAMLResponse'):
        assertion = inputtag.get('value')
if assertion == '':
    print("No SAMLResponse Found")

# Parse the returned assertion and extract the authorized roles
awsroles = []
root = None
try:
    root = ET.fromstring(base64.b64decode(assertion))
except: # TODO put a specific exception here
    print("Error Parsing the SAML response. Please check your credentials. If the problem persists, contact your administrator")
    sys.exit(1)

for saml2attribute in root.iter('{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'):
    if (saml2attribute.get('Name') == 'https://aws.amazon.com/SAML/Attributes/Role'):
        for saml2attributevalue in saml2attribute.iter('{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue'):
            awsroles.append(saml2attributevalue.text)

# Note the format of the attribute value should be role_arn,principal_arn
# but lots of blogs list it as principal_arn,role_arn so let's reverse
# them if needed
for awsrole in awsroles:
    chunks = awsrole.split(',')
    if'saml-provider' in chunks[0]:
        newawsrole = chunks[1] + ',' + chunks[0]
        index = awsroles.index(awsrole)
        awsroles.insert(index, newawsrole)
        awsroles.remove(awsrole)

# If region not provided by user, prompt for selected region after authenticating via SAML
if not ARGS.region:
    for i,region in enumerate(REGIONS):
        print("[" , i , "] ", region)
    print("Region: ")
    region = REGIONS[int(input())]
    print("Selected:", region)
else:
    region = ARGS.region

humannames = []
i = 0
selectedroleindex = None
if not ARGS.account:
    # If I have more than one role, ask the user which one they want,
    print("")
    print("Please choose the role you would like to assume:")
    for awsrole in awsroles:
        humanname = awsrole.split(',')[0].split('/')[1].strip()
        print("[ {} ] - ".format(i) + awsrole.split(',')[0] + " (" + humanname + ")")
        humannames.append(humanname)
        i += 1

    print("Selection: ")
    selectedroleindex = input()

    # Basic sanity check of input
    if int(selectedroleindex) > (len(awsroles) - 1):
        print('You selected an invalid role index, please try again')
        sys.exit(0)
else:
    for awsrole in awsroles:
        humanname = awsrole.split(',')[0].split('/')[1].strip()
        humannames.append(humanname)
        if str(ARGS.account) == str(humanname):
            selectedroleindex = i
            break
        i += 1
    # if we get here the cli input was probabaly wrong
    if selectedroleindex is None:
        print('Youve entered an invalid role')
        sys.exit(0)

role_arn = awsroles[int(selectedroleindex)].split(',')[0]
principal_arn = awsroles[int(selectedroleindex)].split(',')[1]

if debug > 0:
    print( 'role_arn =' )
    print(role_arn)
    print( '\n')


#Trim off before the slash of the role
selected_env = role_arn.split(',')[0].split('/')[1]

#Trim down to the environment and role type
if selected_env.find("_") > 0:
    selected_env = selected_env.split(',')[0].split('_')[1]

#Trim off role type leaving environment
if selected_env.find("-") > 0:
    selected_env = selected_env.split(',')[0].split('-')[0]


#Determine if non-production
if selected_env in ['TST','DEV','STG','DMO','EXP','SUP']:
    if debug > 0: print('Non-Production')
    cli_duration = 14400
else:
    if debug > 0: print('Production')
    cli_duration = 3600

if debug > 0:
    print( 'selected_env =' )
    print(selected_env)


if ARGS.profilename:
    configname = ARGS.profilename
else:
    configname = humannames[int(selectedroleindex)]

# Use the assertion to get an AWS STS token using Assume Role with SAML
client = boto3.client('sts', region_name=region, verify=sslverification)

token = client.assume_role_with_saml(RoleArn=role_arn,
                                     PrincipalArn=principal_arn,
                                     SAMLAssertion=assertion,
                                     DurationSeconds=cli_duration)

if not (ARGS.export or ARGS.export_docker):
    # Write the AWS STS token into the AWS credential file
    write_config_file(filename,
                        configname,
                        outputformat,
                        region,
                        token['Credentials']['AccessKeyId'],
                        token['Credentials']['SecretAccessKey'],
                        token['Credentials']['SessionToken'])

    # Give the user some basic info as to what has just happened
    print('\n\n----------------------------------------------------------------')
    print( 'Your new access key pair has been stored in the AWS configuration file {0} under the {1} profile.'.format(filename, configname))
    print( 'Note that it will expire at {0}.'.format(token['Credentials']['Expiration']))
    print( 'After this time you may safely rerun this script to refresh your access key pair.')
    print( 'To use this credential call the AWS CLI with the --profile option (e.g. aws --profile {0} ec2 describe-instances).'.format(configname))
    print( '----------------------------------------------------------------\n\n')
elif ARGS.export_docker:
    print( 'docker run -e AWS_ACCESS_KEY_ID="{0}" -e AWS_SECRET_ACCESS_KEY="{1}" -e AWS_SESSION_TOKEN="{2}"'.format(token.credentials.access_key, token.credentials.secret_key, token.credentials.session_token))
else:
    print( 'export AWS_ACCESS_KEY_ID="{0}"\nexport AWS_SECRET_ACCESS_KEY="{1}"\nexport AWS_SESSION_TOKEN="{2}"'.format(token.credentials.access_key, token.credentials.secret_key, token.credentials.session_token))
