#!/usr/bin/python

import argparse
import commands
import json
import logging
import os
import sys

""" REQUIREMENTS : A directory system such as /labs/projectname/git , /labs/projectname/svn, /labs/projectname/bazaar already existing
		 : svn ,git, bzr, python  preinstalled 	"""

LOGGER = logging.getLogger(__name__)

LAB_HOME='/labs/'
DEBUG=False


#----------------------------------------------------------------------------------------------------------------------#


# The function run_command takes as input ,a string ,and executes it as a command . For example , if it 	#
# is given a sting { "ls" + "-" + "la" } then it would concatenate it and execute ls -la in the command 	#
# line . This is achieved by usage of a built in method declared in module commands called 			#
# commands.getstatusoutput(command).										#


# USED TO 		: To execute a string in shell.
# USAGE   		: One argument, essentially a string.
# OUTPUT  		: Returns a 2-tuple (status, output) 
# VARIABLES USED	: response [ 2-tuple ] , command [ string ]

def run_command(command=None):
    if command is None:
        return ['1',"error"]
    LOGGER.info('Executing command - %s', command)
    response = commands.getstatusoutput(command)
    LOGGER.debug('Result - %s', response)
    return response

#----------------------------------------------------------------------------------------------------------------------#


# The function response_gen is used to print the response to the screen, it has mainly debugging benefits	#
# For example , if provided with a dictionary that has various datatypes, it would convert all those datatypes  #
# into standard json string format, and can be used later on. json.dumps() is a built in method in python's 	#
# json module , that takes a dictionary and converts it into json strings.					#


# USED TO		: To generate response of the overall process and convert the dictionary datatypes into json string.
# USAGE			: One agrument, essentially a dictionary (hash)
# OUTPUT		: The dictionary with all datatypes changed into json string format.
# VARIABLES USED	: response_obj [ dictionary ], response [ json string formatted dictionary ]

def response_gen(response_obj):
    response = None
    try:
        response = json.dumps(response_obj)
    except e:
        print "unable to process to json "+ e
    return response


#----------------------------------------------------------------------------------------------------------------------#


# The function svncreate is used to create a svn repository , at /labs/project_id/svn/repo  , here project_id would be   	 #
# an argument , which would also be the name of the project in redmine_repos plugin. Basically we create a 	 #
# svn repository and in it copy contents of ldk folder ( lab development kit) , Perform svn add * , and commit	 # 
# run_command fucntion has been used a lot here, whcih has been defined above already				 #


# USED TO 		: To create a svn repository
# USAGE			: Three arguments,repo_location, project_id - project name (string) , repo - repository name (string)
# OUTPUT		: A dictionary with status variable mapped to 1 and summary
# VARIABLES USED	: project_id [string], repo [string]

def svn_create(repo_location,project_id,repo):
	run_command('cd '+ LAB_HOME+project_id +'/'+'svn'+'/' + ';svnadmin create '+repo+' ; sudo chmod -R g+w '+repo)[1]
        run_command('mkdir -p /tmp/ldk')[1]
        run_command('svn co file://'+repo_location+' /tmp/ldk')[1]
        run_command('cp -r ldk/* /tmp/ldk')[1]
        run_command('cd /tmp/ldk ; svn add * ;svn commit -m "LDK committed"')[1]
        run_command('cd /tmp; rm -rf /tmp/ldk')[1]
        run_command('sudo chmod g+w '+repo_location+'/db/rep-cache.db')
	run_command('sudo chown -R www-data:'+project_id+' '+repo_location)
        return {'status' : 1 ,'summary' : 'Repo initialized with ldk' }


#----------------------------------------------------------------------------------------------------------------------#


	
# The function gitcreate is used to create a git repository , at /labs/project_id/git/repo  , here project_id would be   	 #
# an argument , which would also be the name of the project in redmine_repos plugin. Basically we create a 	 #
# git repository and in it copy contents of ldk folder ( lab development kit) , Perform git add * , and commit	 # 
# run_command fucntion has been used a lot here, whcih has been defined above already				 #


# USED TO 		: To create a git repository
# USAGE			: Three arguments,repo_location, project_id - project name (string) , repo - repository name (string)
# OUTPUT		: A dictionary with status variable mapped to 1 and summary
# VARIABLES USED	: project_id [string], repo [string]

def git_create(repo_location, project_id, repo):
    run_command('cd '+ LAB_HOME+project_id +'/'+'git'+ ' ;git init --bare --shared '+repo+' ; sudo chmod -R g+w '+repo)[1]
    run_command('mkdir -p /tmp/ldk')[1]
    run_command('git clone file://'+repo_location+' /tmp/ldk')[1]
    run_command('cp -r ldk/* /tmp/ldk')[1]
    run_command('cd /tmp/ldk ; git add * ;git commit -m "LDK committed"; git push origin master')[1]
    run_command('cd /tmp; rm -rf /tmp/ldk')[1]
    return {'status' : 1 ,'summary' : 'Repo initialized with ldk' }


#----------------------------------------------------------------------------------------------------------------------#


# The function bzrcreate is used to create a bzr repository , at /labs/project_id/bzr/repo  , here project_id     #
# is an argument , which would also be the name of the project in redmine_repos plugin. Basically we create a 	 #
# bzr repository and in it copy contents of ldk folder ( lab development kit) , Perform bzr add * , and 	 # 
# commit . "run_command" function has been used a lot here, whcih has been defined above already		 #


# USED TO 		: To create a bzr repository
# USAGE			: Three arguments, repo_location,project_id - project name (string) , repo - repository name (string)
# OUTPUT		: A dictionary with status variable mapped to 1 and summary
# VARIABLES USED	: repo_location [string], project_id [string], repo [string]

def bzr_create(repo_location, project_id, repository_name):
    shared_location = os.path.join(LAB_HOME, project_id, 'bzr', repository_name)
    trunk_location = os.path.join(shared_location, 'trunk')
    template_location = os.path.join(os.path.dirname(__file__), 'ldk-bzr')

    run_command('bzr init-repo --no-trees {0}'.format(shared_location))
    run_command('bzr branch {0} {1}'.format(template_location, trunk_location))
    run_command('sudo chmod -R g+w {0}'.format(shared_location))
    run_command('sudo chown -R www-data:{0} {1}'.format(project_id, shared_location))

    return {'status': 1 ,'summary': 'Repo initialized with ldk'}


#----------------------------------------------------------------------------------------------------------------------#


# The function create calls either of svncreate,gitcreate or bzrcreate depending on typeofrepo, it additionally #
# checks if repo path exists already or not , by running a function inbuilt in the python os module os.path.exists #
# if it returns true then funtions returns a dictionary with status mapped to 0 and summary that repo exists       #
# otherwise calls either of the three functions. 								   #


# USED TO 		: To select which [repo]create function to call according to typeofrepo			   
# USAGE			: three arguments, typeofrepo , project_id - project name, repo - repository name
# OUTPUT		: Same as [repo]create functions
# VARIABLES USED	: repo_location - full path to server's repository location [string] , rest are same as [repo]create functions.

def create(typeofrepo,project_id,repo):
    LOGGER.debug('Creating repository - %s, %s, %s', typeofrepo, project_id, repo)
    repo_location = LAB_HOME+project_id+'/'+typeofrepo+'/'+repo
    if os.path.exists(LAB_HOME+project_id+'/'+typeofrepo+'/'+repo):		
        return {'status' : 0 , 'summary' : 'repo exists'}
    elif typeofrepo == 'svn':
        return svn_create(repo_location,project_id,repo)
    elif typeofrepo == 'git':
        return git_create(repo_location,project_id,repo)
    elif typeofrepo == 'bzr':
        return bzr_create(repo_location,project_id,repo)
    run_command('sudo chown -R www-data:'+project_id+' '+repo_location)

#----------------------------------------------------------------------------------------------------------------------#


# The function is used to delete the repository completely , rest of the things about it are same as create function #

def discard(typeofrepo,project_id,repo):
	run_command('rm -rf '+LAB_HOME+project_id+'/'+typeofrepo+'/'+repo)
	return {'status' : 1,'summary' : 'Repo removed' }


def main():
    parser = argparse.ArgumentParser(description='Virtual Labs repoistory administration tool')
    parser.add_argument('method', choices=['create', 'discard'], help='Operation to perform')
    parser.add_argument('repository_type', choices=['bzr', 'git', 'svn'], help='Type of the repository')
    parser.add_argument('project_id', help='ID of the project')
    parser.add_argument('repository_name', help='Name of the repository')
    parser.add_argument('--default-log-level', choices=['DEBUG', 'INFO',
                                                        'WARNING', 'ERROR',
                                                        'CRITICAL'],
                        default='INFO', help='Operation to perform, Default: INFO')
    arguments = parser.parse_args()

    logging.basicConfig(level=arguments.default_log_level)

    if arguments.method == 'create':
    	response_obj = create(arguments.repository_type, arguments.project_id,
                              arguments.repository_name)
    elif arguments.method == 'discard': 
    	response_obj = discard(arguments.repository_type, arguments.project_id,
                               arguments.repository_name)

    print response_gen(response_obj)


#----------------------------------------------------------------------------------------------------------------------#


# The main function block, where we pass arguments to create or discard functions as system arguments (params) .     #
# If the first system argument happens to be 'add', then create function is called with rest of the system arguments #
# as arguments to create function. Same is the case with discard function , the only difference being the first system
# argument , if it happens to be 'discard', then the repository is deleted.					     #


# VARIABLES USED 	: response_obj , which is output of create/discard function, look at create/discard for more info
#			: params - system arguments
		
if __name__ == '__main__':
    main()

