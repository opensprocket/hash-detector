# hash-detector

`cleanup.py` was originally written for a simulated blueteam lab for ITC-344. The objective was to find and remove all malicious programs, known and unknown while preserving the functionality of the server. No firewall or useraccess rules were allowed to be modified, so threat hunting coupled with active scanning was used to defend the machine. 

## How it Works

The script takes a list of known `md5` hashes and then scans the system for them. The `md5` hashes represent "malware" on the system and are to be removed when found. In addition to scanning for malware, the system checks for file integrity on the local webserver which hosts `index.php` in `/var/wwww/html`. A `md5` hash of the unaltered index file is used to check if there are changes to the file. One of the "malware" programs also uninstalls `apache2` and masks the service, which the script also remediates automatically. 

The `cleanup.py` is run every minute using crontab, which runs the `check_apache()` and `scan_and_remove()` functions. 

`hash.py` was used to get the hashes of files on the system as part of threat hunting. 

## Retrospective

Since this lab was timed, this script was written so that it would work and accomplish the objective of the lab within the short timeframe allotted. Here's some of the improvements I would make if I were to rewrite it: 
- Improve the `apache2` recovery process by breaking it out into more granular pieces
  - Separate reinstalling, service unmasking and `index.php` recovery
  - Implement a health check using `curl` to check for HTTP `200 OK` status
- Log the things that were removed to a database (likely a local SQLite DB) for additional postmortem analysis
- Use alternate approaches for comparing hash values on the system
  - Hash at the directory level to detect if there are any changes inside the directory (faster scanning)
  - Create a database of all hashes on the system and use that as a baseline for detecting changes 
  - Write a multi-threaded hash checking function to improve scanning time
