# 🌈 vancouver-watching

```bash
vanwatch \
	discover \
	[target=<target>,count=<-1>,dryrun,~tag,~upload] \
	[-|<object-name>] \
	[<args>]
 . discover <target> -> <object-name>.
   target: vancouver | template
```

```bash
@select vanwatch-discover-$(@@timestamp)
vanwatch discover target=vancouver .
@assets publish extensions=geojson,push .
```


```yaml
discovery:
  cameras: 196
  locations: 196

```

[detections.geojson](https://github.com/kamangir/assets/blob/main/vanwatch-discover-2025-04-23-qdgb5k/detections.geojson)

```bash
vanwatch \
	ingest \
	[target=<target>,count=<-1>,~download,dryrun,~upload] \
	[-|<object-name>] \
	[detect,count=<-1>,~download,dryrun,gif,model=<model-id>,~upload] \
	[--overwrite 1] \
	[--verbose 1]
 . ingest <target> -> <object-name>.
   target: vancouver | template
```


```bash
@select vanwatch-ingest-$(@@timestamp)
vanwatch ingest \
  target=vancouver,count=4 . \
  detect,gif
@assets publish extensions=gif,push . \
	--asset_name vanwatch-ingest-example
```


![image](https://github.com/kamangir/assets/blob/main/vanwatch-ingest-example/vanwatch-ingest-example.gif?raw=true)
