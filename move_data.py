import os
import shutil

# to check if file exist
# os.path.isfile(path)

old_dir = '/home/yoel/Desktop/SL/data_structed/kids/vsl/'
new_dir = '/home/yoel/Desktop/SL/data_from_server/data_stim_added/vsl_kids/'

old_files = os.listdir(old_dir)
for f in old_files:
    if not os.path.isfile(os.path.join(new_dir, f)):
        shutil.move(os.path.join(old_dir, f), os.path.join(new_dir, f))
