# Data

Repository to store dummy data.

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

Attempts by an end user to login with the incorrect port number (but potentially a correct username) are not captured by `rsyslogd`

Attempts to login to the wrong hostname will also not be captured. 

## Logfile Parsing

`log_parser.py` takes a logfile and timestamp file as input and outputs results in JSON format.

The timestamp file allows the script to determine what should be parsed from the logfile and prevents storage of duplicate records in the database.

Lines not already parsed are matched against the three patterns above and login attempts are stored in the following JSON structure:

```
{
    user:
    {
        "Month Day":
        [
            {
                "result": "failure",
                "time": "00:00:00"
            },
            ...
        ],
        ...
    }
}
```

Login attempts (result and time) for each user are stored in a list organized by date.

The results are written to a JSON file, but in the final version of the parser they should transmit the data to the database via the MongoDB API. 
