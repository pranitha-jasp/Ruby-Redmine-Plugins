#!/usr/bin/python

def run_command(command=None):
    import commands
    if command is None:
        return ['1',"error"]
    response = commands.getstatusoutput(command)
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

def add_key(username, key):
    key_file = open('keys/'+username,'w')
    key_file.write(key)
    key_file.close()
    return { 'status' : 1 , 'summary' : 'key added'}


if __name__ == '__main__':
    import sys
    params = sys.argv
    key = ""
    key_length = len(sys.argv) -2 
    for i in range(0,key_length):
	key = key+params[i+2]+' '
    response_obj = add_key(params[1],key.strip())
    print response_gen(response_obj)
