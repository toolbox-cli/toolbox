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
import urllib3
from os.path import expanduser

##########################################################################
# Requirements
# These commands may need to be updated; sorry, I forgot to fully document as I went along.

# python -m pip install --upgrade pip
# python 3:
#       unix based: pip3 install --user boto3 requests configparser BeautifulSoup4 urlparse lxml
#       windows based: pip3 install --user boto3 requests configparser BeautifulSoup4 lxml
# python 2:
#       unix based: pip install --user boto3 requests configparser BeautifulSoup4 urlparse lxml
#       windows based: pip install --user boto3 requests configparser BeautifulSoup4 lxml


##########################################################################
# Variables

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

# output format: The AWS CLI output format that will be configured in the
# saml profile (affects subsequent CLI calls)
outputformat = 'json'

# awsconfigfile: The file where this script will store the temp
# credentials under the saml profile
awsconfigfile = '~/.aws/credentials'

# This is a hash mapping the account name to the aws account ids.
# Todo: Continue to append to this list.
aws_account_name_to_id = {

                        }

# Get the account names from the above hash.
if python_version < 3:
    aws_account_name_keys = aws_account_name_to_id.keys()
    aws_account_name_values = aws_account_name_to_id.values()
else:
    aws_account_name_keys = list(aws_account_name_to_id.keys())
    aws_account_name_values = list(aws_account_name_to_id.values())

# Parse the CLI arguments passed in.
parser = argparse.ArgumentParser(description='Use SAML auth to get AWS temporary credentials.')
account_details = parser.add_mutually_exclusive_group(required=True)
account_details.add_argument('--environment', help="The AWS Environment name.")
account_details.add_argument('--account-id', help="The AWS Account ID.")
parser.add_argument('--region', default="us-east-1", help="The AWS region to log in to.")
parser.add_argument('--role', help="The AWS role to assume.")
parser.add_argument('--idp-url', default="https://adfs.example.com/adfs/ls/IdpInitiatedSignOn.aspx?loginToRp=urn:amazon:webservices", help="The identity provider url to communicate with for authn/authz.")
parser.add_argument('--profile', default="default", help="The aws credential profile to use; defaults to 'default' credential profile.")
parser.add_argument('--duration', default=3600, type=int, help="The duration (in seconds) of the temporary role credentials.")
parser.add_argument('--no-verify-ssl', action='store_false', help="(Optional) Add this argument to disable strict SSL verification. Use only if you are seeing SSL validation issues due to our network config :(")

options = parser.parse_args()

if not options.idp_url:
    print("The '--idp-url' argument is required!")
    sys.exit(1)

if options.account_id:  # if environment is not given
    if not (options.account_id in aws_account_name_values): # If invalid account ID
        print("{} not found in {}".format(options.account_id, aws_account_name_values))
        sys.exit(1)

    for account_name, account_id in aws_account_name_to_id.items():
        if account_id == options.account_id:
            options.environment = account_name

if not (options.environment in aws_account_name_keys): # If invalid account name
    print("{} not found in {}".format(options.environment, aws_account_name_keys))
    sys.exit(1)

# Suppress the "InsecureRequestWarning: Unverified HTTPS request is being made" messages when not verifying ssl cert
if not options.no_verify_ssl:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Uncomment to enable low level debugging
#logging.basicConfig(level=logging.DEBUG)

##########################################################################

# Get the federated credentials from the user
print("Username (@example.com email):"),
if python_version < 3:
    username = raw_input()
else:
    username = input()

password = getpass.getpass()
print ('')

# Ensure that "@example.com" is appended if missing.
username = username.split("@")[0] + "@example.com"

# Initiate session handler
session = requests.Session()

# Build a dictionary of all of the form values the IdP expects
payload = {}
payload["UserName"] = username
payload["Email"] = username
payload["Password"] = password

# Debug the parameter payload if needed
# Use with caution since this will print sensitive output to the screen
#print payload

# Performs the submission of the IdP login form with the above post data
response = session.post(options.idp_url, data=payload, verify=options.no_verify_ssl)

# Debug the response if needed
#print (response.text)

# Overwrite and delete the credential variables, just for safety
username = '##############################################'
password = '##############################################'
del username
del password

# Decode the response and extract the SAML assertion
soup = BeautifulSoup(response.text, features="lxml")
assertion = ''

# Look for the SAMLResponse attribute of the input tag (determined by
# analyzing the debug print lines above)
for inputtag in soup.find_all('input'):
    if(inputtag.get('name') == 'SAMLResponse'):
        #print(inputtag.get('value'))
        assertion = inputtag.get('value')

# Better error handling is required for production use.
if (assertion == ''):
    #TODO: Insert valid error checking/handling
    print ('Response did not contain a valid SAML assertion')
    sys.exit(1)

# Debug only
#print(base64.b64decode(assertion))

# Parse the returned assertion and extract the authorized roles
awsroles = []
root = ET.fromstring(base64.b64decode(assertion))
for saml2attribute in root.iter('{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'):
    if (saml2attribute.get('Name') == 'https://aws.amazon.com/SAML/Attributes/Role'):
        for saml2attributevalue in saml2attribute.iter('{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue'):
            # Let's trim the list of roles availabe to just the environment specified
            if options.environment:
                role_account_id = saml2attributevalue.text.split(':')[4]
                if role_account_id == aws_account_name_to_id[options.environment]:
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

# If I have more than one role, ask the user which one they want,
# otherwise just proceed
print ("")

if len(awsroles) > 1:
    # if role is given, assume the role name exists; use the same saml provider.
    if options.role:
        role_arn = awsroles[0].split(',')[0].split('/')[0] + "/" + options.role
        principal_arn = awsroles[0].split(',')[1]
    else:
        i = 0
        print ("Please choose the role you would like to assume:")
        for awsrole in awsroles:
            print ("[ {} ] - ".format(i) + awsrole.split(',')[0])
            i += 1
        print("Selection: "),
        if python_version < 3:
            selectedroleindex = raw_input()
        else:
            selectedroleindex = input()

        # Basic sanity check of input
        if int(selectedroleindex) > (len(awsroles) - 1):
            print ('You selected an invalid role index, please try again')
            sys.exit(0)

        role_arn = awsroles[int(selectedroleindex)].split(',')[0]
        principal_arn = awsroles[int(selectedroleindex)].split(',')[1]
else:
    role_arn = awsroles[0].split(',')[0]
    principal_arn = awsroles[0].split(',')[1]

#print "role_arn: " + role_arn
#print "principal_arn: " + principal_arn

# Use the assertion to get an AWS STS token using Assume Role with SAML
client = boto3.client('sts', region_name=options.region, verify=options.no_verify_ssl)

token = client.assume_role_with_saml(RoleArn=role_arn,
                                     PrincipalArn=principal_arn,
                                     SAMLAssertion=assertion,
                                     DurationSeconds=options.duration)

# Write the AWS STS token into the AWS credential file
filename = os.path.expanduser(awsconfigfile)
dirname = os.path.dirname(filename)

if not os.path.exists(dirname):
    os.makedirs(dirname)

# Read in the existing config file
config = configparser.ConfigParser()
config.read(filename)

# Put the credentials into a saml specific section as defined through the CLI argument "--profile"
credential_profile = options.profile

config.set(credential_profile, 'output', outputformat)
config.set(credential_profile, 'region', options.region)
config.set(credential_profile, 'aws_access_key_id', token['Credentials']['AccessKeyId'])
config.set(credential_profile, 'aws_secret_access_key', token['Credentials']['SecretAccessKey'])
config.set(credential_profile, 'aws_session_token', token['Credentials']['SessionToken'])

# Write the updated config file
with open(filename, 'w+') as configfile:
    config.write(configfile)

# Give the user some basic info as to what has just happened
print ('\n----------------------------------------------------------------')
print ('Your new access key pair has been stored in the AWS configuration file {} under the default profile.'.format(filename))
print ('Note that it will expire at {}.'.format(token['Credentials']['Expiration']))
print ('After this time, you may safely rerun this script to refresh your access key pair.')
print ('To use this credential, call the AWS CLI with the --profile option (e.g. aws --profile default ec2 describe-instances).')
print ('----------------------------------------------------------------\n\n')

sys.exit(0)
