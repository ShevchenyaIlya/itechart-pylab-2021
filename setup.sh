#!/bin/bash

DESTINATION=.git/hooks

for hook_name in pre-push commit-msg
do
  cp hooks/$hook_name $DESTINATION
  if [ "$?" -ne "0" ]; then
    echo "Fail when copy file $hook_name"
    exit 1
  fi
  chmod +x $DESTINATION/$hook_name
done

echo "All hooks copied and configured successfully!"