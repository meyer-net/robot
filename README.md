# PyFlink Framework Osteam Base
This framework base on flink below v1.5, serve for 'oshit team', develop in python3.6。
It is usually used for multi-dimensional data high concurrency analysis scenarios。

- setup step 
```
first-boot:
{
    vim build.sh //edit your flink setup path
    chmod +x build.sh
    ./build.sh
}

start-boot:
{
    $SANDBOX_FILE src/boot.py "$FLINK_DIR/bin/pyflink-stream.sh"
}

build-env:
{
    clean step：
        1：buildout init  #keep dirs of eggs、develop-eggs、bin、parts empty
        2：wget -O bootstrap.py https://bootstrap.pypa.io/bootstrap-buildout.py
        3：wget -O ez_setup.py https://bootstrap.pypa.io/ez_setup.py

    setep step：
        4：python bootstrap.py  #if u see zc.buildout conflict, please input 'pip uninstall zc.buildout' on bash command.
        5：bin/buildout install
}
```