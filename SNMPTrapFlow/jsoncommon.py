
import base64
import json
import urllib.request
import http
import ssl
import base64
import urllib.request
import requests


class JsonCommon():


    def get_restapitojson(self,url,prism_user,prism_password):


        vm_data = []
        
        nutanix_userpass = (prism_user + ":" + prism_password).replace("\n", "")

        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Basic %s' % (base64.encodebytes(nutanix_userpass.encode("utf8")).decode("ascii")).replace("\n", "")
        }

        try:
            response = requests.request("GET", url, headers=headers,verify=False)
            return response.text
        except Exception as e:
            return false

        




    def post_restapitojson(self,url,prism_user,prism_password,payload):
        vm_data = []
        
        nutanix_userpass = (prism_user + ":" + prism_password).replace("\n", "")
        

        #payload = "{\r\n  \"snapshot_specs\": [\r\n    {\r\n      \"snapshot_name\": \"OK2\",\r\n      \"vm_uuid\": \"566b39d9-4525-480e-a47e-00ce415e0f41\"\r\n    }\r\n  ]\r\n}"
        #headers = {
        #  'Content-Type': 'application/json',
        #  'Authorization': 'Basic %s' % (base64.encodebytes(nutanix_userpass.encode("utf8")).decode("ascii")).replace("\n", "")
        #}


        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Basic %s' % (base64.encodebytes(nutanix_userpass.encode("utf8")).decode("ascii")).replace("\n", "")
        }

        response = requests.request("POST", url, headers=headers, data=payload,verify=False)

        return response.text



    def put_restapitojson(self,url,prism_user,prism_password,payload):
        vm_data = []
        
        nutanix_userpass = (prism_user + ":" + prism_password).replace("\n", "")
        

        #payload = "{\r\n  \"snapshot_specs\": [\r\n    {\r\n      \"snapshot_name\": \"OK2\",\r\n      \"vm_uuid\": \"566b39d9-4525-480e-a47e-00ce415e0f41\"\r\n    }\r\n  ]\r\n}"
        #headers = {
        #  'Content-Type': 'application/json',
        #  'Authorization': 'Basic %s' % (base64.encodebytes(nutanix_userpass.encode("utf8")).decode("ascii")).replace("\n", "")
        #}


        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Basic %s' % (base64.encodebytes(nutanix_userpass.encode("utf8")).decode("ascii")).replace("\n", "")
        }

        response = requests.request("PUT", url, headers=headers, data=payload,verify=False)

        return response.text


    #def __init__(self):
    #    s = "dummy"
