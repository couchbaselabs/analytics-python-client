#  Copyright 2016-2024. Couchbase, Inc.
#  All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from enum import Enum
from typing import AsyncGenerator, Generator, Optional, TypeVar

T = TypeVar('T')
AsyncYieldFixture = AsyncGenerator[T, None]
YieldFixture = Generator[T, None, None]


class SyncQueryType(Enum):
    NORMAL = 'normal'
    LAZY = 'lazy'
    CANCELLABLE = 'cancellable'


class AnalyticsTestEnvironmentError(Exception):
    """Raised when something with the test environment is incorrect."""

    def __init__(self, message: Optional[str] = None) -> None:
        super().__init__(message)

    def __repr__(self) -> str:
        return f'{type(self).__name__}({super().__repr__()})'

    def __str__(self) -> str:
        return self.__repr__()
