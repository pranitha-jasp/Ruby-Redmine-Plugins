#!/usr/bin/python

LABS_HOME='/labs/'
    
    
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
     f.write(desc)
     f.close()
     

def add(lab_id,package_name):
    status = read_desc(lab_id)
    status[package_name] = {'status' : 'Processing'}	
    import json
    write_desc(lab_id, json.dumps(status))
    print json.dumps({'status' : 1 , 'summary': 'package added to request list'})

def drop(lab_id,package_name):
    status = read_desc(lab_id)
    import json 
    del status[package_name]
    write_desc(lab_id, json.dumps(status))
    print json.dumps({'status' : 1 , 'summary': 'package '+package_name+' is no longer monitored'})

def status(lab_id,package_name):
    import json	
    status = read_desc(lab_id)
    if package_name != 'all':
    	print json.dumps(status[package_name])	
    else:
	print json.dumps(status)


def run(command,package_name,lab_id):
    result = {
        'status' : status,
        'add' : add,
        'drop' : drop,
        }[command](lab_id,package_name)


if __name__ == '__main__':
    import sys
    params = sys.argv
    run(params[1],params[2],params[3])

