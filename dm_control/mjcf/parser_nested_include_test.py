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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or  implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""Tests for nested MJCF include parsing."""

from absl.testing import absltest
from dm_control.mjcf import parser


class ParserNestedIncludeTest(absltest.TestCase):

  def testNestedIncludeSplicesChildrenAtIncludeLocation(self):
    model = parser.from_xml_string(
        b"""
        <mujoco model="nested_include">
          <worldbody>
            <body name="parent">
              <include file="child.xml"/>
            </body>
          </worldbody>
        </mujoco>
        """,
        assets={
            'child.xml': b"""
              <mujoco>
                <geom name="included_geom" type="sphere" size="0.1"/>
              </mujoco>
            """,
        },
    )

    parent = model.find('body', 'parent')
    included_geom = model.find('geom', 'included_geom')
    self.assertIsNotNone(included_geom)
    self.assertIs(included_geom.parent, parent)

  def testNestedIncludeResolvesRelativeIncludesInAssets(self):
    model = parser.from_xml_string(
        b"""
        <mujoco model="recursive_nested_include">
          <worldbody>
            <body name="parent">
              <include file="parts/child.xml"/>
            </body>
          </worldbody>
        </mujoco>
        """,
        assets={
            'parts/child.xml': b"""
              <mujoco>
                <include file="grandchild.xml"/>
              </mujoco>
            """,
            'parts/grandchild.xml': b"""
              <mujoco>
                <geom name="grandchild_geom" type="box" size="0.1 0.1 0.1"/>
              </mujoco>
            """,
        },
    )

    parent = model.find('body', 'parent')
    grandchild_geom = model.find('geom', 'grandchild_geom')
    self.assertIsNotNone(grandchild_geom)
    self.assertIs(grandchild_geom.parent, parent)


if __name__ == '__main__':
  absltest.main()
