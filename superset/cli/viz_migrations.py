# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import annotations

from enum import Enum

import click
from flask.cli import with_appcontext

from superset import db


class VizType(str, Enum):
    AREA = "area"
    BAR = "bar"
    BUBBLE = "bubble"
    DIST_BAR = "dist_bar"
    DUAL_LINE = "dual_line"
    HEATMAP = "heatmap"
    HISTOGRAM = "histogram"
    LINE = "line"
    PIVOT_TABLE = "pivot_table"
    SANKEY = "sankey"
    SUNBURST = "sunburst"
    TREEMAP = "treemap"


@click.group()
def migrate_viz() -> None:
    """
    Migrate a viz from one type to another.
    """


@migrate_viz.command()
@with_appcontext
@click.option(
    "--viz_type",
    "-t",
    help=f"The viz type to upgrade: {', '.join(list(VizType))}",
    required=True,
)
@click.option(
    "--chart_id",
    help="The chart ID to upgrade",
    type=int,
)
def upgrade(viz_type: str, chart_id: int | None = None) -> None:
    """Upgrade a viz to the latest version."""
    migrate(VizType(viz_type), chart_id)


@migrate_viz.command()
@with_appcontext
@click.option(
    "--viz_type",
    "-t",
    help=f"The viz type to downgrade: {', '.join(list(VizType))}",
    required=True,
)
@click.option(
    "--chart_id",
    help="The chart ID to downgrade",
    type=int,
)
def downgrade(viz_type: str, chart_id: int | None = None) -> None:
    """Downgrade a viz to the previous version."""
    migrate(VizType(viz_type), chart_id, is_downgrade=True)


def migrate(
    viz_type: VizType, chart_id: int | None = None, is_downgrade: bool = False
) -> None:
    """Migrate a viz from one type to another."""
    # pylint: disable=import-outside-toplevel
    from superset.migrations.shared.migrate_viz.processors import (
        MigrateAreaChart,
        MigrateBarChart,
        MigrateBubbleChart,
        MigrateDistBarChart,
        MigrateDualLine,
        MigrateHeatmapChart,
        MigrateHistogramChart,
        MigrateLineChart,
        MigratePivotTable,
        MigrateSankey,
        MigrateSunburst,
        MigrateTreeMap,
    )

    migrations = {
        VizType.AREA: MigrateAreaChart,
        VizType.BAR: MigrateBarChart,
        VizType.BUBBLE: MigrateBubbleChart,
        VizType.DIST_BAR: MigrateDistBarChart,
        VizType.DUAL_LINE: MigrateDualLine,
        VizType.HEATMAP: MigrateHeatmapChart,
        VizType.HISTOGRAM: MigrateHistogramChart,
        VizType.LINE: MigrateLineChart,
        VizType.PIVOT_TABLE: MigratePivotTable,
        VizType.SANKEY: MigrateSankey,
        VizType.SUNBURST: MigrateSunburst,
        VizType.TREEMAP: MigrateTreeMap,
    }
    if is_downgrade:
        migrations[viz_type].downgrade(db.session, chart_id)
    else:
        migrations[viz_type].upgrade(db.session, chart_id)
