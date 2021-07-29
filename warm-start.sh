#!/bin/bash

# Initialise an ACCESS-ESM Payu run from a CSIRO experiment
set -eu

module purge
module use /g/data/hh5/public/modules
module load conda/analysis3

start_year=850

project=p66
user=cm2704
expname=PI-01
source_year=541

csiro_source=/g/data/$project/$user/archive/$expname/restart

payu sweep > /dev/null
payu setup --archive
payu_archive=./archive

payu_restart=${payu_archive}/restart000

if [ $(ls -d ${payu_archive}/restart* | wc -l) -gt 0 ]; then
    echo "ERROR: Restart directory already exists"
    echo "Consider 'payu sweep --hard' to delete all restarts"
    exit 1
fi

mkdir $payu_restart
mkdir $payu_restart/{atmosphere,ocean,ice,coupler}

yearstart="$(printf '%04d' $source_year)0101"
pyearend="$(printf '%04d' $(( source_year - 1 )) )1231"

cp -v $csiro_source/atm/${expname}.astart-${yearstart} $payu_restart/atmosphere/restart_dump.astart

for f in $csiro_source/cpl/*-${pyearend}; do
    cp -v $f $payu_restart/coupler/$(basename ${f%-*})
done

for f in $csiro_source/ocn/*-${pyearend}; do
    cp -v $f $payu_restart/ocean/$(basename ${f%-*})
done

for f in $csiro_source/ice/*-${pyearend}; do
    cp -v $f $payu_restart/ice/$(basename ${f%-*})
done
cp -v $csiro_source/ice/iced.${yearstart} $payu_restart/ice/

scripts/set_restart_year.sh $start_year

payu sweep
