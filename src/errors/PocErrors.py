#!/usr/bin/env python3

class StepError(RuntimeError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)