import sys
import configparser
import os
import getpass
import setting
import paramiko
import logging
import subprocess
import shlex

# Tag for make sure whether entering FTP username and password
sftp_credentials_entered = False

def read_config(file_path):
    parser = configparser.ConfigParser(allow_no_value=True)
    parser.optionxform = str # disable "default translate all section to lower case"
    parser.read(file_path)
    return parser

def getLogger(name=None):
    """
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.
    """
    if not name or isinstance(name, str) and name == root.name:
        return root
    return Logger.manager.getLogger(name)

def run_bash(cmd: str, silent: bool=False, ignore_err: bool=False):
    logger = logging.getLogger()
    if not silent:
        logger.info(f'Executing bash commands: {cmd}')
    cmds = shlex.split('/bin/sh -c')
    cmds.append(cmd)
    process = subprocess.Popen(cmds, stdout=subprocess.PIPE)
    output, error = process.communicate()
    stdout = output.decode('utf-8') if output else ""
    stderr = error.decode('utf-8') if error else ""
    # ret = subprocess.run(cmd, stdout=subprocess.PIPE)
    # stdout = ret.stdout.decode()
    # stderr = ret.stderr.decode()
    if not silent:
        logger.info(f'stdout: {stdout}')
        logger.info(f'stderr: {stderr}')
    # if ret.returncode != 0 and not ignore_err:
    if process.returncode != 0 and not ignore_err:
        raise RuntimeError(f'Failed to execute command, stderr={stderr}')
    else:
        if not silent:
            logger.info(f'Successfully executed bash commands.')
        return stdout, stderr

def check_packages_exist(version, packages):
    global sftp_credentials_entered

    for package in packages:
        package_path = os.path.join(setting.check_the_folder, package)

        if os.path.exists(package_path):
            print(f"\nPackage name:'{package}' exists.")
        else:
            print(f"\nPackage name:'{package}' does not exist. Looking for SFTP server ... ")
            
            # Check 是不是第一次登入 ftp
            if not sftp_credentials_entered:
                print(f"\nPlease provide SFTP username and password to download the packages")
                sftp_username = input("Enter SFTP username: ")
                sftp_credentials_entered = True

            # 如果沒有找到 package 就到 FTP 下載
            src_p = os.path.join(setting.remote_install_resources_path, package)
            dst_p = os.path.join(setting.local_install_resources_path, package)

            cmd = f'scp -r {sftp_username}@{setting.sftp_host}:{src_p} {dst_p}'
            run_bash(cmd)

def main():
    parser = read_config(setting.config_file)

    # Check if a command-line argument is provided
    if len(sys.argv) < 2:
        print("Add the VERSION in the autoDLpack.sh")
        sys.exit(1)

    version = sys.argv[1]

    if parser.has_section(version):
        packages = parser.options(version)
        print(f"Preparing packages for the version {version}:\n {', '.join(packages)}")

        check_packages_exist(version, packages)
    else:
        print(f"Error version of {version}, enter the available version in the autoDLpack.sh")

if __name__ == "__main__":
    main()

