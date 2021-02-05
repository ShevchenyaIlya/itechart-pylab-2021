#!/bin/bash

DESTINATION=.git/hooks

for hook_name in pre-push commit-msg pre-commit
do
  cp hooks/$hook_name $DESTINATION
  if [ "$?" -ne "0" ]; then
    echo "Fail when copy file $hook_name"
    exit 1
  fi
  chmod +x $DESTINATION/$hook_name
done

echo "All hooks copied and configured successfully!"

pip3 install pre-commit
cp hooks/.pre-commit-config.yaml .
if [ "$?" -ne "0" ]; then
    echo "Fail when copy file hooks/.pre-commit-config.yaml"
    exit 1
fi

user_choice_store_path=assignment2/selected_database.json
touch $user_choice_store_path

echo "Choose database for project"
echo "1. PostgreSQL"
echo "2. MongoDB"
read choice

if [[ choice -eq 1 ]]
then
  echo '{"database": "PostgreSQL"}' > $user_choice_store_path
  chmod +x scripts/config_postgersql
  ./scripts/config_postgersql
elif [[ choice -eq 2 ]]
then
  echo '{"database": "MongoDB"}' > $user_choice_store_path
  hmod +x scripts/setup_mongodb
  ./scripts/setup_mongodb
else
  echo "Invalid choice. Try again."
fi
