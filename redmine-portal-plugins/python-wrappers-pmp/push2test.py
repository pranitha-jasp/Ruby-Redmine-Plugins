#!/usr/bin/python

"""
Push repositories from development server to test server
"""

import commands
import logging
import os
import sys
import time

LOGGER = logging.getLogger(__name__)

LAB_ROOT = '/labs'
MAKE_OPTIONS = 'theme=maroon-grid'


def run_command(command=None):
    """Execute a given command"""
    if command is None:
        return ['1', "error"]
    LOGGER.info('Executing command - %s', command)
    response = commands.getstatusoutput(command)
    LOGGER.debug('Reponse - %s', response)
    return response


def format_path(repository_type, project_id, repo):
    """Return a path created by combining the components"""
    return '{0}/{1}/{2}/{3}/'.format(LAB_ROOT, project_id, repository_type,
                                     repo)


def check_url(url, repository_type):
    """Check if given URL is valid repository directory"""
    if repository_type == 'svn':
        svn_url = '{0}conf/'.format(url)
        return os.path.isdir(svn_url)
    elif repository_type == 'git':
        git_url = os.system('cd {0}; git rev-parse'.format(url))
        return (bool(not git_url))
    elif repository_type == 'bzr':
        bazaar_url = os.system('cd {0}; bzr info >/dev/null 2>&1'.format(url))
        return (bool(not bazaar_url))


def clear_repo(repository_type, path):
    """Remove the repository information from given directory"""
    if repository_type == 'svn':
        run_command('find {0} -type d -name .svn -delete'.format(path))
    elif repository_type == 'git':
        run_command('find {0} -type d -name .git -delete'.format(path))
    elif repository_type == 'bzr':
        run_command('find {0} -type d -name .bzr -delete'.format(path))


def svn_checkout(path, revision, directory):
    """Checkout SVN repository"""
    result = run_command('svn co file://{0} -r {1} {2}'.format(path, revision,
                                                               directory))
    if result[1].find('No such revision') > 0:
        raise Exception('Revision not found')


def git_checkout(path, revision, directory):
    """Checkout Git repository"""
    if revision == "":
        result = run_command('git clone file://{0} {1}'.format(path,
                                                               directory))
        if result[1].find('No such revision') > 0:
            raise Exception('Directory not found')
    else:
        run_command('git clone file://{0} {1}'.format(path, directory))
        result = run_command('cd {0}; git checkout {1}'.format(directory,
                                                               revision))
        if result[1].find('No such revision') > 0:
            raise Exception('Directory not found')


def bzr_checkout(path, revision, directory):
    """Checkout Bazaar repository"""
    result = run_command('bzr checkout file://{0}trunk -r {1} {2}'
                         .format(path, revision, directory))
    if result[1].find('No such revision') > 0:
        raise Exception('Revision not found')


def push_to_test(repository_type, project_id, repo, revision):
    """Push a repository to the testing server"""
    path = format_path(repository_type, project_id, repo)
    if not check_url(path, repository_type):
        raise Exception('Repository does not exist')

    transaction_id = str(int(time.time() * 1000000))
    directory = '/tmp{0}{1}'.format(path, transaction_id)

    run_command('mkdir -p {0}'.format(directory))
    if repository_type == "svn":
        svn_checkout(path, revision, directory)
    elif repository_type == "git":
        git_checkout(path, revision, directory)
    elif repository_type == "bzr":
        bzr_checkout(path, revision, directory)

    final_build_path = '/home/{0}/public_html/final-build'.format(project_id)
    command = 'ssh tester@test "rm -rf {0}/*"'.format(final_build_path)
    run_command(command)

    command = 'rsync -auvz {0} tester@test:/tmp/{1}'.format(directory, project_id)
    run_command(command)

    command = 'ssh tester@test "/home/tester/build.py {0} /tmp/{1}/{2}"'.format(project_id, project_id, transaction_id)
    result = run_command(command)
    return result[1]


def main():
    """Parse arguments and invoke required methods"""
    logging.basicConfig(level='INFO')

    params = sys.argv
    if len(sys.argv) == 4:
        params.append('')

    try:
        print push_to_test(params[1], params[2], params[3], params[4])
    except Exception, exception:
        print {'status': 0, 'summary': 'Not successful',
               'error': exception.message}


if __name__ == '__main__':
    main()
