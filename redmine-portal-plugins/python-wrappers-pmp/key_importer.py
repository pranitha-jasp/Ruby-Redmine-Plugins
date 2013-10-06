#!/usr/bin/python

# To be Run as root , looks for <username.pub> in KEYS_HOME and
# updates the key accordingly in /home/<username>/.ssh/authorized_keys

KEYS_HOME = '/home/importer/keys/'


def run_command(command=None):
    import commands
    if command is None:
        return ['1',"error"]
    response = commands.getstatusoutput(command)
    return response




    
def update_key(key_file):
    
    # check if dir '/home/' + user + '/.ssh/authorized_keys' exists 
    username = filter_username(key_file)
    # make sure home dir exists
    import subprocess	
    p = subprocess.Popen(["su", "-",username])
    location = '/home/' + username + '/.ssh'
    # Read the new key 
    key = open(KEYS_HOME + key_file).read()
    # Write to the auth_keys file
    import pwd, os
    gid = pwd.getpwnam(username)[3]
    #os.setgid(gid)
    uid = pwd.getpwnam(username)[2]
    #os.setuid(uid)
    
    if not os.path.exists(location):
        os.mkdir(location)
	os.chown(location,uid,gid)
	os.chmod(location,0700)


    authorized_keys = open(location+'/authorized_keys','w')
    authorized_keys.write(key)
    authorized_keys.close()
    os.chown(location+'/authorized_keys',uid,gid)
    os.chmod(location+'/authorized_keys',0644)
    

def filter_username(key_file):
    # return the name of the file removing the extension .pub
    return key_file

def is_new(key_file):
    # find if the existing key is new to the one in USER_HOME
    username = filter_username(key_file)
    keypath = KEYS_HOME+key_file
    user_keydir = '/home/'+username+'/.ssh'
    user_keypath = user_keydir+'/authorized_keys'
    import os
    if not os.path.exists(user_keydir) or not os.path.exists(user_keypath):
        return True
    elif os.stat(user_keypath).st_mtime < os.stat(keypath).st_mtime:
        return True
    else: 
        return False


def update_keys():
    # Iter all the key files and update as necessary 
    import os
    key_files = os.listdir(KEYS_HOME)
    for key_file in key_files:
        if is_new(key_file):
            update_key(key_file)


if __name__ == '__main__':
    update_keys()

