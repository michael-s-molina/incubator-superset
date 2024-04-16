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
import { t } from '../translation';

// TODO Check if there's any column alignment different than ['left', 'right', 'right']
export function tooltipHtml(
  data: string[][],
  columnAlignments: ('left' | 'right' | 'middle')[],
  title?: string,
  focusedRow?: number,
) {
  const colspan = data.length > 0 ? data[0].length : 1;
  const titleRow = title
    ? `<tr><td colspan="${colspan}" style="font-weight: 700;">${title}</td></tr>`
    : '';
  return `
    <table>
        ${titleRow}
        ${data.length === 0 ? `<tr><td>${t('No data')}</td></tr>` : ''}
        ${data
          .map((row, i) => {
            const rowStyle =
              i === focusedRow ? 'font-weight: 700;' : 'opacity: 0.7;';
            let padding = 0;
            const cells = row.map((cell, j) => {
              const cellStyle = `
                text-align: ${columnAlignments[j]};
                padding-left: ${padding}px;`;
              padding = 16;
              return `<td style="${cellStyle}">${cell}</td>`;
            });
            return `<tr style="${rowStyle}">${cells.join('')}</tr>`;
          })
          .join('')}
    </table>`;
}
