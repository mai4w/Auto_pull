import os

# Path of folder
check_the_folder = "install_resources"
config_file = os.path.join(check_the_folder, "config.ini")

# 使用範例
sftp_host = "192.168.xxx.xxx"
remote_install_resources_path = "/mnt/xxx/xxx/xxx/xxx"
local_install_resources_path = os.path.join(os.getcwd(), check_the_folder)
