import sys
import os
import commands

IGNORE_EXTENSIONS = (
    '.bak',
    '.exe',
    '.zip',
    '.rar',
    '.jpg',
    '.gif',
    '.png',
    '.swf',
    '.mp3',
    '.wav',
    '.wma',
    'r.gz',
)

def remove_from_paths(parent_path, pattern, subst, ignore):
    for path in os.listdir(parent_path):
        path = os.path.join(parent_path, path)
        if os.path.isdir(path):
            remove_from_paths(path, pattern, subst, ignore)

        # If file is in ignore list
        # If extension is in ignored extensions
        if path in ignore \
                or path[-4:] in IGNORE_EXTENSIONS:
            continue      

        # If file is file... it's great!
        if os.path.isfile(path):
            backup_path = "%s.bak" % path
            fsize = os.path.getsize(path)
            content = open(path, 'r').read()
            # If file is blank, ignore
            if not content:
                continue

            pos = content.rfind(pattern)
            # If pattern is in file, replace!
            if pos > 0:
                # Getting permissions from infected file
                perms = commands.getoutput('stat --format=%%a %s' % path)

                if '<script>' in content[(pos - 8):]:
                    pos -= 8

                print 'Infected file: %s @ %s' % (path, pos)
                cleaned_content = content[:pos]
                print 'Copying to a backup file: %s' % backup_path
                open(backup_path, 'w').write(content)
                print 'Overwriting original file: %s' % path
                open(path, 'w').write(cleaned_content.strip())
                print

                # Setting permissions to the cleaned file
                commands.getoutput('chmod %s %s' % (perms, path))


if __name__ == "__main__":
    try:
        path_to_find = sys.argv[1]
    except:
        path_to_find = False
        print 'Using: %s <directory>' % sys.argv[0]

    if path_to_find:
        remove_from_paths(
            parent_path=path_to_find,
            pattern="""try{window.onload=function(){""",
            subst="",
            ignore=(
                'cgi-bin',
                'remove_trojan.py',
            ),
        )

        print 'Done!'
