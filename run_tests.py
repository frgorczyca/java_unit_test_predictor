from subprocess import run

command = ["java",
           "-jar",
           ".\\bin\\junit-platform-console-standalone-1.10.1.jar",
           "discover",
           "-cp", ".\\TargetSource\\target\\classes\\",
           "-cp", ".\\TargetSource\\target\\test-classes\\",
           "-m",  "org.dtu.analysis.arrays.NaiveArraysTest#sum_elements"]

run(command)
