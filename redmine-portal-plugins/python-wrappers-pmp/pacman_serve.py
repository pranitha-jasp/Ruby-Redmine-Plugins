#!/usr/bin/python

LABS_HOME='/labs/'

MACHINES = ['test','deploy']


DEBUG=False

def run_command(command=None):
    import commands
    if command is None:
        return ['1',"error"]
    response = commands.getstatusoutput(command)
    if DEBUG:
        print response[1]
    return response

def set_id(lab_id):
	import pwd,os
        gid = pwd.getpwnam(lab_id)[3]
        #uid = pwd.getpwnam('tester')[2]
	os.setgid(gid)
       # os.setuid(uid)    
    
def read_desc(lab_id):
    import json
    try:
	return json.loads(open(LABS_HOME+lab_id+'/desc.json').read().replace('\\',''))
	
    except IOError:
	# desc.json does not exist write empty 
	f = open(LABS_HOME+lab_id+'/desc.json','w')
	f.write(json.dumps("{}"))
	f.close()
	return {}


def write_desc(lab_id,desc):
     f = open(LABS_HOME+lab_id+'/desc.json','w')
     import json
     f.write(json.dumps(desc))
     f.close()
     
def exec_remote(location,command,pack_name):
    import commands
    remote_cmd = 'ssh '+location+' "pacman.py '+command+' '+pack_name+'"'
    print remote_cmd
    response= run_command(remote_cmd)
    import json
    return json.loads(response[1])

def sync_package(locations,pack_name):
    # find current status
    # verify if the package is installed on MACHINES[0]
    print locations 
    response = exec_remote(locations[0],'status',pack_name)
    if response['status'] == "Not Installed":
	for location in locations:
		exec_remote(location,'install',pack_name)
    response = exec_remote(locations[0],'status',pack_name)	
    return response   	



def get_location(lab_id):
    return ['test','deploy']

def run():
    import os	
    
    labs = os.listdir(LABS_HOME)
    for lab in labs:
        td_pair = get_location(lab)
	print lab
	status = read_desc(lab)	
	for pack_name in status:
	    status[pack_name] = sync_package(td_pair,pack_name)
        
	set_id(lab)
        write_desc(lab,status)
    	

if __name__ == '__main__':
    run()
