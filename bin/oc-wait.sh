#!/bin/bash

set -u

job=$1

shift

rest=$*

# wait for completion as background process - capture PID
oc wait --for=condition=complete job/$job $rest &
completion_pid=$!

# wait for failure as background process - capture PID
#oc wait --for=condition=failed job/$job $rest && exit 1 &
oc wait --for=condition=failed job/$job $rest && exit 1 &
failure_pid=$! 

# capture exit code of the first subprocess to exit
# need bash 4.3

#wait -n $completion_pid $failure_pid

while [ 1 ]; do
  if ! ps $completion_pid > /dev/null; then
    echo "completion completed"
    # get exit code of process
    wait $completion_pid
    exit_code=$?
    kill $failure_pid
    break
  fi
  if ! ps $failure_pid > /dev/null; then
    echo "failure completed"
    wait $failure_pid
    exit_code=$?
    kill $completion_pid
    break
  fi
  sleep 2
done

wait >/dev/null 2>&1

if [ $exit_code -eq 0 ]; then
  echo "Job completed"
else
  echo "Job failed with exit code ${exit_code}"
fi

exit $exit_code
