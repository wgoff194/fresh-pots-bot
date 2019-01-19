#!/bin/bash
# 
# Written by wbrown 
# install git and config script for personal use
#

#
# install git if not installed
#

if git --version; then
	echo "\ngit is installed" 
else 
	echo "\ngit will now be installed. please authorize\n" 
	sudo apt install git
fi

# 
# set login data
#

echo;read -p "What is the git username?: " user_name
git config --global user.name $user_name
echo "\n git username set to $(git config --global user.name)\n"

echo;read -p "What is the git email?: " email
git config --global user.email $email
echo "\n git email set to $(git config --global user.email)"