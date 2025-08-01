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

import sys
from typing import TYPE_CHECKING

if sys.version_info < (3, 10):
    from typing_extensions import TypeAlias
else:
    from typing import TypeAlias

from acouchbase_analytics.protocol._core.client_adapter import _AsyncClientAdapter
from acouchbase_analytics.protocol.scope import AsyncScope

if TYPE_CHECKING:
    from acouchbase_analytics.protocol.cluster import AsyncCluster


class AsyncDatabase:
    def __init__(self, cluster: AsyncCluster, database_name: str) -> None:
        self._database_name = database_name
        self._cluster = cluster

    @property
    def client_adapter(self) -> _AsyncClientAdapter:
        """
        **INTERNAL**
        """
        return self._cluster.client_adapter

    @property
    def name(self) -> str:
        """
        str: The name of this :class:`~acouchbase_analytics.protocol.database.Database` instance.
        """
        return self._database_name

    def scope(self, scope_name: str) -> AsyncScope:
        return AsyncScope(self, scope_name)


Database: TypeAlias = AsyncDatabase
