date
PATH="/usr/ecflow5/bin:/usr/local/ecflow5/bin:$PATH"
TASK_DURATION=$(($(date +%%s) - $TASK_START_TIME))

ecflow_client --msg="$ECF_NAME: duration $TASK_DURATION seconds"
ecflow_client --complete  # Notify ecFlow of a normal end
trap 0                    # Remove all traps
exit 0                    # End the shell
