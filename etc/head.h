#!/bin/bash
%manual
https://wiki.fmi.fi/display/PROD/ecFlow-suitet
%end

set -e # stop the shell on first error
set -u # fail when using an undefined variable
set -x # echo script lines as they are executed

# Defines the variables that are needed for any communication with ECF
export ECF_PORT=%ECF_PORT%    # The server port number
export ECF_HOST=%ECF_HOST%    # The name of ecf host that issued this task
export ECF_NAME=%ECF_NAME%    # The name of this current task
export ECF_PASS=%ECF_PASS%    # A unique password
export ECF_TRYNO=%ECF_TRYNO%  # Current try number of the task
export ECF_RID=$$
export ECF_SSL=1              # Enable SSL

PATH="/usr/ecflow5/bin:/usr/local/ecflow5/bin:$PATH"

# Tell ecFlow we have started
ecflow_client --init=$$

# Defined a error handler
ERROR() {
    set +e                      # Clear -e flag, so we don't fail
    ecflow_client --abort=trap  # Notify ecFlow that something went wrong, using 'trap' as the reason
    trap 0                      # Remove the trap
    exit 0                      # End the script
}

# Trap any calls to exit and errors caught by the -e flag
trap ERROR 0

# Trap any signal that may cause the script to fail
trap '{ echo "Killed by a signal"; ERROR ; }' 1 2 3 4 5 6 7 8 10 12 13 15

# Sleep for a while, if this is an automatic retry
if [ %ECF_TRYNO% -gt 1 -a %ECF_TRYNO% -le %ECF_TRIES% ]; then
    echo "This is try number %ECF_TRYNO%, and it is an automatic retry. Sleeping for 10 seconds."
    sleep 10
fi

TASK_START_TIME=$(date +%%s)

date
