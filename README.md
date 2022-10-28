# Data

Repository to store dummy data and log parsing utilities

## Logging on Solace

`rsyslogd` is the logging utility currently in use on Solace.

`rsyslogd` logs a stored under `/var/log/` in CentOS (the OS used by Solace).

The following format is used for each of the failure and success modes of a login / file copy over `ssh`:

#### Success: correct password

```
<timestamp (m d hh:mm:ss)> <machine name> <system daemon (sshd)>: Accepted password for <user> from <ip address> port <port number> <ssh protocol (ssh2)>
```

#### Failure: wrong password

```
<timestamp (m d hh:mm:ss)> <machine name> <system daemon (sshd)>: Failed password for <user> from <ip address> port <port number> <ssh protocol (ssh2)>
```

#### Failure: invalid / non-existent user

```
<timestamp (m d hh:mm:ss)> <machine name> <system daemon (sshd)>: Failed password for invalid <user> from <ip address> port <port number> <ssh protocol (ssh2)>
```

Attempts by an end user to login with the incorrect port number (but potentially a correct username) will not captured by `rsyslogd`.

Attempts to login to the wrong hostname will also not be captured. 

## Logfile Parsing

`log_parser.py` takes a logfile and timestamp file as input and transmits these results to the database accessible through MongoDB Atlas and the backend API routes ([Dragoffs/SL2/backend/routes](https://github.com/Dragoffs/SL2/tree/main/backend/routes)).

The timestamp file allows the script to determine what should be parsed from the logfile in order to speed up the parsing process.  Correct usage of the API in `log_parser.py` should prevent any duplicate records.

Lines not already parsed are matched against the three login result patterns (success, failure, & invalid user) and login attempts are stored in the following Python dictionary structure:

```
{
	username: [
		{
			datetime: <yyyy-mm-dd>T<hh:mm:ss.uuu>+<HH:MM>,
			result: <"Failure", "Success">
		}
	]
}
```

Where `u` represents one digit in the milliseconds value and `HH:MM` represents a timezone offset of `HH` hours and `MM` minutes.

These objects are "up-serted" (a combination of updating and insertion) into the database, preventing duplicates and inserting new values when appropriate.
