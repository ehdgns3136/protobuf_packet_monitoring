from fabric.api import *

@task
def build_proto():
    c = r"protoc -I=. --java_out=. network.proto"

    with settings(warn_only=True):
        local(c)