#!/bin/bash

set -e

if ! python -c "import coverage" &> /dev/null; then
    printf "\e[32mcoverage package is missing. Installing...\e[m\n"
    python -m pip install coverage
fi

if [ -d htmlcov ]; then
  printf "\e[32mRemoving old coverage reports\e[m\n"
  rm -r htmlcov
fi

if [ -f .coverage ]; then
  printf "\e[32mRemoving old coverage db file\e[m\n"
  rm .coverage
fi

printf "\e[32mRunning tests with coverage report\e[m\n"
python -m coverage run -m unittest discover -s tests

printf "\e[32mDone. Printing coverage report:\e[m\n"
python -m coverage report -m

while true; do
    read -p "Do you want to see html page with test report? (y/n)? " yn
    case $yn in
        [Yy]* ) python -m coverage html; open ./htmlcov/index.html; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

