'''
Sitations to handle:
[x] no cfg directory
[ ] no token_name.json file
[ ] no .jira folder
[ ] given file name is not .pat
[ ] given file name is not in .jira
[ ] loaded file name no longer exists
[ ] loaded file name is not valid

'''

from collections import Counter
from typing import cast

import json
import os
from os.path import isfile
from os.path import isdir
from pathlib import Path

from jira import JIRA
from jira.client import ResultList
from jira.resources import Issue
    
    
class tokenManager(object):
    def __init__(self):
        self.token_info_file = 'token_info.json'
        self.token_name = ''
        self.token = ''
        
        # check if there is a .jira folder
        self.jira_folder_path = os.path.join(Path.home(),'.jira')
        if not isdir(self.jira_folder_path):
            raise Exception(f"'.jira' directory not found in home directory: {Path.home()}\nPlease follow steps for token setup [LINK]")
        
        # get enclosing dir & path to cfg dir
        curr_file = Path(os.path.realpath(__file__))
        enclosing_dir = curr_file.parent.absolute()
        self.cfg_dir_path = os.path.join(enclosing_dir,'.cfg')
        self.token_info_path = os.path.join(self.cfg_dir_path,self.token_info_file)
        
        # check if this folder has had its cfg setup, and if not create it
        if not isdir(os.path.join(enclosing_dir,'.cfg')):
            os.mkdir(cfg_dir_path)

        # check if the token info file exists
        if isfile(self.token_info_path):
            self.load_token_info()
        else:
            print("No token info found.")
            self.update_token_name()
            self.save_token_info()
            
        self.get_token()
            
    def load_token_info(self):
        with open(self.token_info_path) as f:
            info = json.load(f)
        self.token_name = info['token_name']
            
    def get_token(self):
        with open(os.path.join(self.jira_folder_path, self.token_name), 'r') as f:
            self.token =  f.read()
        if self.token[-1] == '\n':
            self.token = self.token[:-1]
        
    def update_token_name(self):
        valid_token_name = False
        while not valid_token_name:
            token_name = input("Please enter the name of your Personal Access Token (PAT) file: ")
            if token_name[-4:] != '.pat':
                print("Invalid file extension. Must be '.pat'")
            elif not isfile(os.path.join(self.jira_folder_path,token_name)):
                print(f"Could not find file token file '{token_name}' in {jira_folder_path}")
            else:
                valid_token_name = True
            
        self.token_name = token_name
        
    def save_token_info(self):
        with open(self.token_info_path,'w') as f:
            json.dump({'token_name':self.token_name}, f)


tMan = tokenManager()

# Some Authentication Methods
jira = JIRA(
    server="https://jira.berkeleyse.org",
    token_auth=tMan.token  # Self-Hosted Jira (e.g. Server): the PAT token
    # basic_auth=("admin", "admin"),  # a username/password tuple [Not recommended]
    # basic_auth=("email", "API token"),  # Jira Cloud: a username/token tuple
    # auth=("admin", "admin"),  # a username/password tuple for cookie auth [Not recommended]
)

# Who has authenticated
myself = jira.myself()

test_issue = jira.issue('AVI-235')

# jira.add_attachment(issue=test_issue, attachment='ship24.png')
# new_description = test_issue.fields.description + '\n!ship24.png|thumbnail!'
# 
# test_issue.update(description = new_description)

