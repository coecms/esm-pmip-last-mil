#!/g/data/hh5/public/apps/miniconda3/envs/analysis3-20.07/bin/python
# Copyright 2020 Scott Wales
# author: Scott Wales <scott.wales@unimelb.edu.au>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mule
import xarray
import os
import shutil
from glob import glob
import numpy

landuse = xarray.open_dataset('work/atmosphere/INPUT/luh2_v2h_states_cable_N96.nc').cable_fraction

def normalise(da):
    da = (numpy.clip(da, 0, 1)).round(decimals=3)
    da[0,:,:] += numpy.where(da[3:,:,:].sum('cable_type') == 0, 0.001, 0)
    return da / da.sum('cable_type')

class ReplaceOp(mule.DataOperator):
    def __init__(self, da):
        self.da = normalise(da)

    def new_field(self, source):
        return source

    def transform(self, source, result):
        return self.da.isel(cable_type = source.lbuser5 - 1).data

# The last restart of the run
#restart = sorted(glob('work/atmosphere/aiihca.da*'))[-1]
restart = 'work/atmosphere/restart_dump.astart'

stash_landfrac = 216
stash_landfrac_lastyear = 835

mf = mule.DumpFile.from_file(restart)

year = mf.fixed_length_header.t2_year
year = 850

print(f'Updating land use for year {year} in {restart}')

out = mf.copy()
out.validate = lambda *args, **kwargs: True

set_current_landuse = ReplaceOp(landuse.sel(time=year))
set_previous_landuse = ReplaceOp(landuse.sel(time=year-1, method='nearest'))

for f in mf.fields:
    if f.lbuser4 == stash_landfrac:
        f = set_current_landuse(f)

    if f.lbuser4 == stash_landfrac_lastyear:
        f = set_previous_landuse(f)

    out.fields.append(f)

tmpfile = os.path.join(os.environ['TMPDIR'], 'updated_landuse.astart')
out.to_file(tmpfile)

shutil.copy(tmpfile, restart)
