printf "\e[32mRunning all unit tests in the tests dir with file name ending *-test.py\e[m\n"
python -m unittest discover -s tests -p "*-test.py" -v
