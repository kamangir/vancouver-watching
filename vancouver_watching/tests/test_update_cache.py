from vancouver_watching.QGIS import update_cache
from abcli.plugins import cache


def test_update_cache():
    assert update_cache(cache.read("vanwatch.cache"))
