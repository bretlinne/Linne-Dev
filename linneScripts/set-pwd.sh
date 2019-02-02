#!/bin/bash
# Read Password
echo -n Password: 
read -s password
export PASSWORD=password
# Run Command
echo $password
