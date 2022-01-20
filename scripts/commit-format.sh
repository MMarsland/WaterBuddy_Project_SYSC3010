#!/bin/bash

Color_Off='\033[0m'
BRed="\033[1;31m"         # Red
BGreen="\033[1;32m"       # Green
BYellow="\033[1;33m"      # Yellow
BBlue="\033[1;34m"        # Blue

MSG_FILE=$1
FILE_CONTENT="$(head -n 1 $MSG_FILE)"

# Initialize constants here
export REGEX='(feat:|fix:|docs:|style:|refactor:|test:|chore:)'
export ERROR_MSG="Commit message format must match regex \"${REGEX}\""
export PERIOD_MSG="Commit Subject must not end with a period"
export CHARACTER_MSG="Commit Subject must be within 50 characters"
export UPPER_MSG="Commit Subject must start with a Capital Letter"

export FILE_ARRAY=(${FILE_CONTENT// / })
TYPE=${FILE_ARRAY[0]}
SUBJECT=${FILE_ARRAY[1]}

if [[ $TYPE =~ $REGEX ]]; then
 if [[ "${SUBJECT: -1}" == "." ]]; then
   printf "${BRed}Bad commit ${BBlue}\"$FILE_CONTENT\"\n"
   printf "${BYellow}$PERIOD_MSG\n"
   exit 1
 elif [[ ${#SUBJECT} -gt 50 ]] || [[ ${#SUBJECT} -lt 1 ]]; then
   printf "${BRed}Bad commit ${BBlue}\"$FILE_CONTENT\"\n"
   printf "${BYellow}$CHARACTER_MSG\n"
   exit 1
 elif [[ ${SUBJECT:0:1} =~ [a:z] ]]; then
   printf "${BRed}Bad commit ${BBlue}\"$FILE_CONTENT\"\n"
   printf "${BYellow}$UPPER_MSG\n"
   exit 1
 fi
 printf "${BGreen}Good commit!\n${Color_Off}"

else
 printf "${BRed}Bad commit ${BBlue}\"$FILE_CONTENT\"\n"
 printf "${BYellow}$ERROR_MSG\n"

 exit 1
fi
exit 0
