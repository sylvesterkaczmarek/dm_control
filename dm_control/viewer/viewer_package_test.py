# Copyright 2026 The dm_control Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Tests for the dm_control.viewer package import behavior."""

import subprocess
import sys

from absl.testing import absltest


class ViewerPackageTest(absltest.TestCase):

  def _run_isolated(self, source):
    result = subprocess.run(
        [sys.executable, '-c', source],
        check=False,
        capture_output=True,
        text=True,
    )
    self.assertEqual(result.returncode, 0, msg=result.stderr)

  def test_import_does_not_load_application(self):
    self._run_isolated("""
import sys
import dm_control.viewer
assert 'dm_control.viewer.application' not in sys.modules
assert 'dm_control._render' not in sys.modules
""")

  def test_application_attribute_loads_lazily(self):
    self._run_isolated("""
import sys
import types

application = types.ModuleType('dm_control.viewer.application')
sys.modules['dm_control.viewer.application'] = application

import dm_control.viewer as viewer
assert 'application' not in viewer.__dict__
assert viewer.application is application
assert viewer.application is application
""")


if __name__ == '__main__':
  absltest.main()
