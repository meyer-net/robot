# flink-analysis-py
Used for analysis user behavior based on flink。

setup step 
{
    clean step：
        1：buildout init  #keep dirs of eggs、develop-eggs、bin、parts empty
        2：wget -O bootstrap.py https://bootstrap.pypa.io/bootstrap-buildout.py
        3：wget -O ez_setup.py https://bootstrap.pypa.io/ez_setup.py

    setep step：
        4：python bootstrap.py  #if u see zc.buildout conflict, please input 'pip uninstall zc.buildout' on bash command.
        5：bin/buildout install
}