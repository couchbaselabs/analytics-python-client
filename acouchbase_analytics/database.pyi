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

from acouchbase_analytics.protocol.cluster import AsyncCluster as AsyncCluster
from acouchbase_analytics.scope import AsyncScope

class AsyncDatabase:
    def __init__(self, cluster: AsyncCluster, database_name: str) -> None: ...
    @property
    def name(self) -> str: ...
    def scope(self, scope_name: str) -> AsyncScope: ...
