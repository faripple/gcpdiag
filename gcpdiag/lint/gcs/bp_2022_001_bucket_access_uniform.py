# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Buckets are using uniform access

Google recommends using uniform access for a
Cloud Storage bucket IAM policy

https://cloud.google.com/storage/docs/access-control#choose_between_uniform_and_fine-grained_access
"""

from gcpdiag import lint, models
from gcpdiag.queries import gcs

IGNORE_WITH_LABELS = {'goog-composer-environment'}


def run_rule(context: models.Context, report: lint.LintReportRuleInterface):
  buckets = gcs.get_buckets(context)
  bucket_count = 0
  for b in buckets.values():
    bucket_count += 1
    if set(b.labels.keys()) & IGNORE_WITH_LABELS:
      report.add_skipped(b, 'Google-managed bucket')
    elif b.is_uniform_access():
      report.add_ok(b)
    else:
      report.add_failed(b,
                        'it is recommend to use uniform access on your bucket')

  if bucket_count == 0:
    report.add_skipped(None, 'no buckets found')
