#! /usr/bin/env bash

function abcli_install_vancouver_watching() {
    pip3 install geojson
    pip3 install beautifulsoup4
    pip3 install geopandas
    pip3 install tqdm
}

abcli_install_module vancouver_watching 103