# 🌈 Toronto 🔥

help::: vancouver_watching discover

```bash
@select vanwatch-discover-$(@@timestamp)
vanwatch discover target=toronto .
@assets publish extensions=geojson,push .
```

set:::discover_object_name TBA

metadata:::get:::discover_object_name

assets:::get:::discover_object_name/detections.geojson

help::: vancouver_watching ingest


```bash
@select vanwatch-ingest-$(@@timestamp)
vanwatch ingest \
  target=toronto,count=4 . \
  detect,gif
@assets publish extensions=gif,push . \
	--asset_name vanwatch-ingest-toronto
```

set:::ingest_object_name vanwatch-ingest-toronto

assets:::get:::ingest_object_name/get:::ingest_object_name.gif