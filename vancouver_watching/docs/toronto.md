# 🌈 Toronto 🔥

```bash
vanwatch \
	discover \
	[target=<target>,count=<-1>,dryrun,~tag,~upload] \
	[-|<object-name>] \
	[<args>]
 . discover <target> -> <object-name>.
   target: toronto | vancouver
```

```bash
@select vanwatch-discover-$(@@timestamp)
vanwatch discover target=toronto .
@assets publish extensions=geojson,push .
```


```yaml
{}

```

[detections.geojson](https://github.com/kamangir/assets/blob/main/TBA/detections.geojson)

```bash
vanwatch \
	ingest \
	[target=<target>,count=<-1>,~download,dryrun,~upload] \
	[-|<object-name>] \
	[detect,count=<-1>,~download,dryrun,gif,model=<model-id>,~upload] \
	[--overwrite 1] \
	[--verbose 1]
 . ingest <target> -> <object-name>.
   target: toronto | vancouver
```


```bash
@select vanwatch-ingest-$(@@timestamp)
vanwatch ingest \
  target=toronto,count=4 . \
  detect,gif
@assets publish extensions=gif,push . \
	--asset_name vanwatch-ingest-toronto
```


![image](https://github.com/kamangir/assets/blob/main/vanwatch-ingest-toronto/vanwatch-ingest-toronto.gif?raw=true)
