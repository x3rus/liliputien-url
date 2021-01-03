#!/usr/bin/python3
#
# Client for liliputien cmd
#
########################################

import requests
import argparse


class liliputienClient():
    """ Create liliputien client """
    def __init__(self, liliputien_url="http://127.0.0.1:5000/"):
        """ liliputien_client"""
        self.host_url = liliputien_url

    def health_check(self):
        response = requests.get(self.host_url + "/health")
        print(response.status_code)
        print(response.content)
        print(self.host_url + "/health")
        if response.status_code >= 200 and response.status_code < 300:
            return True
        return False

# #######
# MAIN #
# #######


if __name__ == '__main__':

    # #######################
    # Command Line Arguments
    parser = argparse.ArgumentParser(description='script to create GitLab issue\
                                     and create my directory structure')
    parser.add_argument('--verbose', '-v', help='Verbose mode',
                        action='store_true', default=False)

    args = parser.parse_args()

    lili_cli = liliputienClient()
