#!/usr/bin/python

def publish(labid):
        import commands
        commands.getstatusoutput('ssh deployer@deploy "~/publish '+ labid+'"')

if __name__ == '__main__':
        import sys
        params = sys.argv
        publish(params[1])
