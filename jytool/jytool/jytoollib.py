#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 timger
#    +Author timger
#    +Gtalk&Email yishenggudou@gmail.com
#    +Msn yishenggudou@msn.cn
#    +Weibo @timger http://t.sina.com/zhanghaibo
#    +twitter @yishenggudou http://twitter.com/yishenggudou
#    Licensed under the MIT License, Version 2.0 (the "License");
__author__ = 'timger'
import os
import sys
DIR_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
import shutil

class Jython(object):

    _jython_home = "/usr/local/Cellar/jython/2.5.3/libexec"
    def __init__(self,
                model_dirs=[],
                jars = [],
                main = ("example.py","main"),
                outjarname = "output.jython.jar",
                project_home='./',
                jython_home = None):
        self.jython_home = jython_home or self._jython_home
        self.project_home = os.path.abspath(project_home)
        self.package_dir_name = "Package"
        self.package_dir = os.path.join(self.project_home,self.package_dir_name)
        self.package_home = self.package_dir
        os.path.isdir(self.package_dir) and shutil.rmtree(self.package_dir)
        (not os.path.isdir(self.package_dir) ) and os.makedirs(self.package_dir)
        self.model_dirs = model_dirs
        self.jars = jars
        self.jython_jar = os.path.join(self.jython_home, 'jython.jar')
        self.jars.append(self.jython_jar)
        self.main_path = main[0]
        self.main_name = self.main_path.split('.')[0]
        print self.main_name
        self.main_fun = main[1]
        self.outjarname = outjarname
        self.outjarpath = os.path.join(self.project_home, outjarname)

    def copytree(self, src, dst, symlinks=False, ignore=None):
        import shutil
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)


    def shell_exec(self, cmd):
        print  cmd
        os.system(cmd)


    def package_py2_jar(self):
        """
        https://wiki.python.org/jython/JythonFaq/DistributingJythonScripts#Using_the_Jar_Method
        """
        import shutil
        from zipfile import ZipFile
        self.copytree(os.path.join(self.jython_home,'Lib'),
                    self.package_dir
                    )
        for jar in self.jars:
            cmd = """
            cd {0}
            unzip {1}
            """.format(self.package_dir,os.path.abspath(jar))
            #zipf = ZipFile(os.path.abspath(jar))
            #zipf.extractall(path=self.package_dir)
            self.shell_exec(cmd)
        try:
            os.makedirs(os.path.join(self.package_dir,'Lib'))
        except:
            pass

        for m in self.model_dirs:
            self.copytree(m, os.path.join(self.package_dir,'Lib'))
        with open(os.path.join(self.project_home, "Main.java"), 'wb') as fw:
            main_str = r"import {fname} \n {fname}.{fun}()".format(fname=self.main_name, fun=self.main_fun)
            JAVA = open(os.path.join(DIR_PATH,'Main.java')).read().replace("MAINSTRMATCH", main_str)
            fw.write(JAVA)
        shutil.copy(self.main_path, self.package_home)
        cmd = """
        cd {package_home}
        javac {project_home}/Main.java -d .
        jar -cfe {outname} Main *
        """.format(package_home=self.package_home,
                   outname=self.outjarpath,
                   project_home=self.project_home
                   )
        self.shell_exec(cmd)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='jytool is tool package py code to jar')
    parser.add_argument('entrypoint', metavar='main_file',
                        type=str,
                        help='the main script')
    parser.add_argument('main', metavar='mian_fun',
                        type=str,
                        help='the main fun')
    parser.add_argument('--models', metavar='models',
                        type=str, default="",
                        help='the py models model1:model2:model3')
    parser.add_argument('--jars', dest='jars',
                        default="",
                        help='the dep jars like jar1.jar:jar2.jar:jar3.jar')
    parser.add_argument('-O', dest='outjarname',
                        default="output.jython.jar",
                        help='the output jar name')
    parser.add_argument('-P', dest='project_home',
                        default='./',
                        help='the project_home')
    parser.add_argument('-J', dest='jython_home',
                        default=None,
                        help='the jython_home')
    args = parser.parse_args()
    print args
    model_dirs = args.models.split(":")
    model_dirs = filter(lambda x:x, model_dirs)
    main_file = args.entrypoint
    main_fun = args.main
    main = (main_file, main_fun)
    outjarname = args.outjarname
    project_home = args.project_home
    jython_home = args.jython_home
    jars = args.jars.split(":")
    print jars
    J = Jython(model_dirs=model_dirs,
            jars = jars,
            main = main,
            outjarname = outjarname,
            project_home=project_home,
            jython_home = jython_home)
    J.package_py2_jar()
