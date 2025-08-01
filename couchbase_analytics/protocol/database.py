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

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

from couchbase_analytics.protocol._core.client_adapter import _ClientAdapter
from couchbase_analytics.protocol.scope import Scope

if TYPE_CHECKING:
    from couchbase_analytics.protocol.cluster import Cluster


class Database:
    def __init__(self, cluster: Cluster, database_name: str) -> None:
        self._database_name = database_name
        self._cluster = cluster

    @property
    def client_adapter(self) -> _ClientAdapter:
        """
        **INTERNAL**
        """
        return self._cluster.client_adapter

    @property
    def name(self) -> str:
        """
        str: The name of this :class:`~couchbase_analytics.protocol.database.Database` instance.
        """
        return self._database_name

    @property
    def threadpool_executor(self) -> ThreadPoolExecutor:
        """
        **INTERNAL**
        """
        return self._cluster.threadpool_executor

    def scope(self, scope_name: str) -> Scope:
        return Scope(self, scope_name)
