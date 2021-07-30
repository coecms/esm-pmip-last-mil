#!/bin/bash
#  Copyright 2020 Scott Wales
#
#  \author  Scott Wales <scott.wales@unimelb.edu.au>
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


source /etc/profile.d/modules.sh
module use /g/data/hh5/public/modules
module load conda/analysis3
module load nco

set -eu

# Sets the start date in the most recent restart directory

export UMDIR=~access/umdir

start_year=$1

payu_restart=$(ls -d ./archive/restart* | sort -t t -k 3 -n | tail -n 1)

echo "Setting restart year in ${payu_restart} to ${start_year}"

if [ ! -d $payu_restart/ocean ]; then
    echo "No restart directory"
    exit 1
fi

# Update ocean start time
cat > $payu_restart/ocean/ocean_solo.res << EOF
    3
    1 1 1 0 0 0
    $start_year 1 1 0 0 0
EOF

# Update atmos start time
python scripts/update_um_year.py $start_year $payu_restart/atmosphere/restart_dump.astart 2> /dev/null

cat > $payu_restart/atmosphere/um.res.yaml << EOF
end_date: $(printf %04d $start_year)-01-01 00:00:00
EOF

# Update ice start time
cat > $payu_restart/ice/cice_in.nml << EOF
&setup_nml
istep0=0,
npt=0,
dt=3600,
/
EOF

cat > $payu_restart/ice/input_ice.nml << EOF
&coupling
runtime0=0
runtime=0
/
EOF

ncatted -a units,time,o,c,"seconds since ${start_year}-01-01 00:00:00" $payu_restart/ice/mice.nc

secs_realyr=$(python -c "from datetime import date; d=(date(${start_year},1,1)-date(1,1,1)); print(d.days*24*60*60)")
mv $payu_restart/ice/iced.* $payu_restart/ice/iced.orig
scripts/cicedumpdatemodify.py -i $payu_restart/ice/iced.orig -o $payu_restart/ice/iced.${start_year} --istep0=0 --time=0--time_forc=0.
rm $payu_restart/ice/iced.orig
cat > $payu_restart/ice/ice.restart_file << EOF
iced.${start_year}
EOF
