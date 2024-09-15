from blue_objects import cache

from vancouver_watching.QGIS import update_cache


def test_update_cache():
    assert update_cache(cache.read("vanwatch.cache"))
