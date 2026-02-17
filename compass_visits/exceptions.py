# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

class ValidationError(Exception):
    pass


class OverrideNotPermitted(Exception):
    def __str__(self):
        return "Action not permitted while using admin override"
