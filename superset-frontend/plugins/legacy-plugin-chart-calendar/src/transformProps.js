/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

import { getNumberFormatter } from '@superset-ui/core';
import { getFormattedUTCTime } from './utils';

export default function transformProps(chartProps) {
  const {
    height,
    formData,
    queriesData,
    datasource,
    hooks: { onContextMenu },
  } = chartProps;
  const {
    cellPadding,
    cellRadius,
    cellSize,
    domainGranularity,
    linearColorScheme,
    showLegend,
    showMetricName,
    showValues,
    steps,
    subdomainGranularity,
    xAxisTimeFormat,
    yAxisFormat,
  } = formData;

  const { verboseMap } = datasource;
  const timeFormatter = ts => getFormattedUTCTime(ts, xAxisTimeFormat);
  const valueFormatter = getNumberFormatter(yAxisFormat);

  return {
    height,
    data: queriesData[0].data,
    cellPadding,
    cellRadius,
    cellSize,
    domainGranularity,
    linearColorScheme,
    onContextMenu,
    showLegend,
    showMetricName,
    showValues,
    steps,
    subdomainGranularity,
    timeFormatter,
    valueFormatter,
    verboseMap,
  };
}
