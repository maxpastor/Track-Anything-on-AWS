#!/usr/bin/env python3
from aws_cdk import core
from stack import Ec2GpuStack

app = core.App()
Ec2GpuStack(app, "Ec2GpuStack")

app.synth()
