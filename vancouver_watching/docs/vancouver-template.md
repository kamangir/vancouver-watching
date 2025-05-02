# 🌈 Vancouver

help::: vancouver_watching discover

```bash
@select vanwatch-discover-$(@@timestamp)
vanwatch discover target=vancouver .
@assets publish extensions=geojson,push .
```

set:::discover_object_name vanwatch-discover-2025-05-01-wqlqzq

metadata:::get:::discover_object_name

assets:::get:::discover_object_name/detections.geojson

help::: vancouver_watching ingest


```bash
@select vanwatch-ingest-$(@@timestamp)
vanwatch ingest \
  target=vancouver,count=4 . \
  detect,gif
@assets publish extensions=gif,push . \
	--asset_name vanwatch-ingest-vancouver
```

set:::ingest_object_name vanwatch-ingest-vancouver

assets:::get:::ingest_object_name/get:::ingest_object_name.gif