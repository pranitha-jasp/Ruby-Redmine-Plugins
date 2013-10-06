#!/usr/bin/python

MAKE_OPTIONS = ''
DEBUG=False

def run_command(command=None):
    import commands
    if command is None:
        return ['1',"error"]
    response = commands.getstatusoutput(command)
    if DEBUG:
        print response[1]
    return response

def request_parser(param):
    import json
    request = None
    try:
        request = json.loads(param)
    except e:
        print "Error parsing "+ e
    return request

def response_gen(response_obj):
    import json
    response = None
    try:
        response = json.dumps(response_obj)
    except e:
        print "unable to process to json "+ e
    return response

def build(labid,location):
    make_status = run_command('cd '+location+'/src; make'+' '+MAKE_OPTIONS)
    if  make_status[0] != 0 :
        return { 'status' : 0, 'summary' : 'Make failed'}
    
    run_command('rm -rf /var/www/labs/'+labid+'/*')
    run_command('rsync -auvz '+location+'/build/* /var/www/labs/'+labid+'/')    
    run_command('chgrp -R www-data /var/www/labs/'+labid+'/')
    run_command('chmod -R g+w /var/www/labs/'+labid+'/')
    run_command('rm -rf '+ location)
    return { 'status' : 1 , 'summary' : 'Successful'}
	

if __name__ == '__main__':
    import sys
    response_obj = build(sys.argv[1],sys.argv[2])
    response = response_gen(response_obj)
    print response

