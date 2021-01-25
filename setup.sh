#!/bin/bash

DESTINATION=.git/hooks

cp hooks/pre-push $DESTINATION
cp hooks/commit-msg $DESTINATION

chmod +x $DESTINATION/pre-push
chmod +x $DESTINATION/commit-msg
