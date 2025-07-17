
Certainly! rsync is a versatile tool for synchronizing files and directories between different locations. Here's an overview of some of the most commonly used options and commands in rsync:

Basic rsync Command Structure

```
rsync [options] source destination
```

1. source: The file or directory you want to copy.
2. destination: The location where you want to copy the files.


Commonly Used Options

1. Basic Options:
	- -a or --archive: Archive mode; copies files recursively and preserves symbolic links, permissions, timestamps, and ownership.
	- -v or --verbose: Increase verbosity, showing what files are being transferred.
	- -r or --recursive: Recursively copy directories.
	- -z or --compress: Compress file data during the transfer, useful for slow network connections.
	- -h or --human-readable: Output numbers in a human-readable format (e.g., 1K, 1M, 1G).
2. Excluding Files:
	- --exclude='pattern': Exclude files matching the given pattern (e.g., *.log or folder/).
	- --exclude-from='file': Exclude files based on patterns listed in a file.
3. Including Files:
	- --include='pattern': Include only files matching the given pattern.
	- --include-from='file': Include files based on patterns listed in a file.
4. Handling Large Files:
	- --max-size=SIZE: Exclude files larger than the specified size (e.g., 100M).
	- --min-size=SIZE: Exclude files smaller than the specified size.
5. File Deletion:
	- --delete: Delete files in the destination directory that are not present in the source directory.
	- --delete-before: Delete files from the destination before transferring new ones.
6. Dry Run:
	- -n or --dry-run: Show what would have been transferred without actually doing it. Useful for testing your command.
	- --progress: Show progress during transfer.
7. Partial Transfers:
	- --partial: Keep partially transferred files in case the transfer is interrupted, so it can resume later.
	- --partial-dir=.rsync-partial: Store partial files in a specific directory.
8. Synchronization:
	- -u or --update: Skip files that are newer in the destination than the source.
	- --checksum: Skip files based on checksum, rather than the modification time or file size.
	- -c or --checksum: Force file comparison based on checksums instead of just size and timestamp.
9. Network Transfers:
	- -e ssh: Use SSH as the remote shell for the transfer, useful for transferring files between remote machines.
	- --bwlimit=RATE: Limit the bandwidth used during the transfer (e.g., 100K, 1M).


Example Commands

1. Simple File Copy:
```
rsync -av /source/directory/ /destination/directory/
```
This command copies all files from /source/directory/ to /destination/directory/ and preserves file attributes.

Copy Files Over SSH:
```
rsync -av -e ssh /local/directory/ user@remote:/remote/directory/

rsync -varzh -e "ssh -i nodejs.pem -o IdentitiesOnly=yes" dist.zip    ec2-user@13.235.72.194:/var/www/dev
```
This copies files from a local directory to a remote server over SSH.

Synchronize Directories:
```
rsync -av --delete /source/directory/ /destination/directory/
```
This synchronizes the source and destination directories, deleting files in the destination that are not present in the source.

Dry Run to Test the Command:
```
rsync -av --dry-run /source/directory/ /destination/directory/
```
This shows what would happen without actually copying any files.

Copy Files, Exclude Certain Files and Directories:
```
rsync -av --exclude='*.log' --exclude='temp/' /source/directory/ /destination/directory/
```
This copies all files except those with a .log extension and any files in the temp/ directory.

Copy Only New or Modified Files:
```
rsync -av --update /source/directory/ /destination/directory/
```
This copies only the files that are new or modified in the source directory.

rsync is powerful, especially for backups, migrations, and synchronizations, and it can handle complex scenarios with these options.



LSYNCD



```
ssh-keygen -t rsa -b 2048
ssh-copy-id user@host
ssh 'user@host'
```

```
sudo apt update
sudo apt install lsyncd
sudo vim /etc/lsyncd/lsyncd.conf.lua
```

```

settings {
    logfile = "/var/log/lsyncd.log",
    statusFile = "/var/run/lsyncd.status",
    inotifyMode = "CloseWrite",
}

sync {
    default.rsync,
    source = "/path/to/directory",
    target = "user@host:/path/to/directory",
    rsync = {
        binary = "/usr/bin/rsync",
        archive = true,
        compress = true,
    }
}
```

```
tail /var/log/lsyncd.log
```
