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

import sys
from typing import Awaitable, overload

if sys.version_info < (3, 11):
    from typing_extensions import Unpack
else:
    from typing import Unpack

from acouchbase_analytics.protocol._core.client_adapter import _AsyncClientAdapter
from acouchbase_analytics.protocol.database import AsyncDatabase as AsyncDatabase
from couchbase_analytics.options import QueryOptions, QueryOptionsKwargs
from couchbase_analytics.result import AsyncQueryResult

class AsyncScope:
    def __init__(self, database: AsyncDatabase, scope_name: str) -> None: ...
    @property
    def client_adapter(self) -> _AsyncClientAdapter: ...
    @property
    def name(self) -> str: ...
    @overload
    def execute_query(self, statement: str) -> Awaitable[AsyncQueryResult]: ...
    @overload
    def execute_query(self, statement: str, options: QueryOptions) -> Awaitable[AsyncQueryResult]: ...
    @overload
    def execute_query(self, statement: str, **kwargs: Unpack[QueryOptionsKwargs]) -> Awaitable[AsyncQueryResult]: ...
    @overload
    def execute_query(
        self, statement: str, options: QueryOptions, **kwargs: Unpack[QueryOptionsKwargs]
    ) -> Awaitable[AsyncQueryResult]: ...
    @overload
    def execute_query(
        self, statement: str, options: QueryOptions, *args: str, **kwargs: Unpack[QueryOptionsKwargs]
    ) -> Awaitable[AsyncQueryResult]: ...
    @overload
    def execute_query(
        self, statement: str, options: QueryOptions, *args: str, **kwargs: str
    ) -> Awaitable[AsyncQueryResult]: ...
    @overload
    def execute_query(self, statement: str, *args: str, **kwargs: str) -> Awaitable[AsyncQueryResult]: ...
