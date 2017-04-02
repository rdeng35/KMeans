#!/usr/bin/python
# Student sections: s1=1-18 s2 = 19-37 s3 = 38-60

import os
import sys
import subprocess
import glob
import re

# TODO change output format for k-means

# RUN FROM DIR pa6-calendar-student
utestfile = 'src/edu/wit/cs/comp1000/tests/PA6aTestCase.java'
studentcode = 'src/edu/wit/cs/comp1000/'
compile = "javac " + utestfile + ' -classpath src:src/junit-4.12.jar'
run = 'java -cp src/junit-4.12.jar:src/hamcrest-core-1.3.jar:src org.junit.runner.JUnitCore edu.wit.cs.comp1000.tests.PA6aTestCase'
resultsDict = {}

# Run to get the number of tests
out = subprocess.Popen([run], stdout=subprocess.PIPE, shell=True)
output = out.stdout.read()

# Case if unit test results return OK
total_num_tests = output[output.find("(") + 1:output.find(")")].split(" ")[0]
# Case for checking if the compiled unit test has failures
if total_num_tests is "":
    temp = output[output.find("Tests run:"):].split("Tests run: ")[1]
    total_num_tests = temp.split(",")[0]


# # Parses the output from running the unit tests
# # Appends it into a dictionary with results
def checkTests(out):
    if "OK (" in out:
        return []
    else:
        # print "SOMETHING FAILED !!"
        list = []
        r = re.compile(r"\) |\(")
        for line in out.split('\n'):
            if ") test" in line:
                failure = r.split(line)
                list.append(failure[1])
        return list


i = 1
print "Running unit tests"
for file in glob.glob(studentcode + '*.java'):
    print i,
    file_name_with_extension = file.split("src/edu/wit/cs/comp1000/PA6a")
    file_name = file_name_with_extension[1][:-5]
    try:
        f = open(utestfile, 'r')
    except IOError, e:
        print "Could not open file."
        sys.exit()
    filedata = f.read()
    f.close()

    # Changes the class used to run the unit tests
    newtest = "    private static edu.wit.cs.comp1000.PA6a" + file_name + " testClass;"

    # Search and replace the old class for the one set to newtest
    for line in filedata.split('\n'):
        if "private static edu.wit.cs.comp1000.PA6a" in line:
            oldtest = line
            newdata = filedata.replace(oldtest, newtest)

            f = open(utestfile, 'w')
            f.write(newdata)
            f.close()

    os.system(compile)
    out = subprocess.Popen([run], stdout=subprocess.PIPE,
                           shell=True)  # run java file via subprocess to fix stdout and stderr
    out = out.stdout.read()

    # print "\nCHECKING", i
    check = checkTests(out)
    # print check

    resultsDict[i] = check

    i += 1
print "\nCOMPLETE\n"
# print resultsDict

for index, results in resultsDict.items():
    print index, results, "Failed: ", len(results), "/", total_num_tests