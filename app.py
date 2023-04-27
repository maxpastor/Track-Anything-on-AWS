#!/usr/bin/env python3
from aws_cdk import core
from stack import SegmentAnythingStack

app = core.App()
SegmentAnythingStack(app, "SegmentAnythingStack")

app.synth()
