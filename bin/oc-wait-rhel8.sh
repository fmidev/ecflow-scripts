#!/bin/sh

set -u

job=$1

# wait for completion as background process - capture PID
oc wait --for=condition=complete job/$job &
completion_pid=$!

# wait for failure as background process - capture PID
oc wait --for=condition=failed job/$job && exit 1 &
failure_pid=$! 

# capture exit code of the first subprocess to exit
wait -n $completion_pid $failure_pid

# store exit code in variable
exit_code=$?

if [ $exit_code -eq 0 ]; then
  echo "Job completed"
else
  echo "Job failed with exit code ${exit_code}, exiting..."
fi

exit $exit_code
