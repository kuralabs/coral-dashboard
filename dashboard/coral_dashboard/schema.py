# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 KuraLabs S.R.L
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Daemon communication protocol.
"""

from logging import getLogger as get_logger

from cerberus import Validator


log = get_logger(__name__)


SCHEMA_PUSH = {
    'data': {
        'required': True,
        'type': 'dict',
        'empty': False,
        'nullable': False,
        'keyschema': {
            'type': 'string',
            'regex': '^[a-z][a-z0-9_]*$',
        },
        'valueschema': {
            'percent': {
                'type': 'float',
                'nullable': True,
            },
            'value': {
                'type': 'integer',
                'nullable': True,
            },
            'total': {
                'type': 'integer',
                'nullable': True,
            },
        },
    },
}


SCHEMAS = {
    'push': SCHEMA_PUSH,
}


def validate_schema(schema_id, data):
    """
    Generic schema validation function.

    :param str schema_id: Name of the schema to validate against.
    :param dict data: Data to validate.

    :return: A tuple of a dictionary with validated and coersed data and the
     validation errors found, if any.
    :rtype: tuple
    """
    validator = Validator(SCHEMAS[schema_id])
    validated = validator.validated(data)
    return validated, validator.errors


__all__ = [
    'validate_schema',
]
