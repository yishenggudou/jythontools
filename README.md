#  tool for package python to jar with jar

### usage
用法

```

timger-mac:test timger$ python ../jytool/jytoollib.py -h
usage: jytoollib.py [-h] [--models models] [--jars JARS] [-O OUTJARNAME]
                    [-P PROJECT_HOME] [-J JYTHON_HOME]
                    main_file mian_fun

jytool is tool package py code to jar

positional arguments:
  main_file        the main script
  mian_fun         the main fun

optional arguments:
  -h, --help       show this help message and exit
  --models models  the py models model1:model2:model3
  --jars JARS      the dep jars like jar1.jar:jar2.jar:jar3.jar
  -O OUTJARNAME    the output jar name
  -P PROJECT_HOME  the project_home
  -J JYTHON_HOME   the jython_home

```
