# Vancouver Watching (`vanwatch`) 🌈

`vanwatch` 🌈 discovers and ingests images from traffic cameras in an area and then runs [YOLO 🚀](https://github.com/ultralytics/ultralytics), [OpenAI Vision](https://github.com/kamangir/openai_commands#vision), and other vision algo to extract information about urban activity at scale. Also see [`@vanwatch`](https://github.com/kamangir/notebooks-and-scripts/tree/main/scripts#vanwatch).

```bash
 > vanwatch help
vanwatch conda create [validate,~recreate]
 . create conda environment.
vanwatch conda validate
 . validate conda environment.
vanwatch discover \
	[area=<area>,~upload] \
	[-|<object-name>] \
	[<args>]
 . discover area -> <object-name>.
vanwatch ingest \
	area=<area>,count=<count>,dryrun,gif,model=<model-id>,~process,publish,~upload \
	-|<object-name> \
	[<args>]
 . ingest <area> -> <object-name>.
vanwatch list [area=<area>,discovery|ingest,published] \
	[--count <count>] \
	[--delim space] \
	[--log 0] \
	[--offset <offset>]
 . list objects from area.
2 area(s): iran,vancouver
vanwatch list areas
 . list areas.
vanwatch vision "prompt" \
	[area=<area>,offset=<1>,auto|low|high,dryrun,~upload] \
	Davie,Bute \
	[--verbose 1]
 . openai_commands vision: prompt @ <area>/intersection.
vanwatch process \
	count=<count>,~download,gif,model=<model-id>,publish,~upload \
	.|<object-name> \
	[--detect_objects 0] \
	[--do_dryrun 1] \
	[--overwrite 1] \
	[--verbose 1]
 . process <object-name>.
vanwatch pylint
 . pylint vancouver_watching.
vanwatch update|update_cache \
	area=<vancouver>,overwrite,process,~publish,refresh,~upload \
	[--verbose 1]
 . update QGIS cache.
vancouver_watching test \
	[dryrun,~ingest,~list,~process,upload]
 . test vancouver_watching.
```

---

last build [🔗](https://kamangir-public.s3.ca-central-1.amazonaws.com/test_vancouver_watching_ingest/animation.gif):

![image](https://kamangir-public.s3.ca-central-1.amazonaws.com/test_vancouver_watching_ingest/animation.gif?raw=true)

---

## Discover and Ingest an Area

![image](https://user-images.githubusercontent.com/1007567/196573547-b1c71b3b-7fac-4d2c-bba0-a87b063830da.png)

To see the list of areas supported by `vanwatch` type in,

```bash
vanwatch list areas
```

To discover the available cameras in an area type in,

```bash
vanwatch discover area=vancouver
```

You have generated a `geojson` of [traffic images in the City of Vancouver](./data/vancouver.geojson). Now, you can ingest the traffic images from this area and detect people and cars in them,

```bash
vanwatch ingest area=vancouver,count=2,publish
```

![image](https://github.com/kamangir/assets/blob/main/vanwatch/2023-11-25-openai-vision/DavieWestBute-inference.jpg?raw=true)

model: https://hub.ultralytics.com/models/R6nMlK6kQjSsQ76MPqQM?tab=preview

[![image](https://github.com/kamangir/assets/blob/main/vanwatch/2023-11-25-openai-vision/QGIS.png?raw=true)](./QGIS/2023-11-12-12-03-40-85851.geojson)

![image](https://github.com/kamangir/assets/blob/main/vanwatch/2023-11-12-14-42-23-96479.gif?raw=true?raw=1)

![image](https://github.com/kamangir/assets/blob/main/vanwatch/2024-01-06-20-39-46-73614-QGIS.gif?raw=true?raw=1)

dataset: [vanwatch-cache-2024-02-28-21-04-19-26236.tar.gz](https://kamangir-public.s3.ca-central-1.amazonaws.com/vanwatch-cache-2024-02-28-21-04-19-26236.tar.gz) ([details](https://medium.com/@arash-kamangir/vancouver-watching-with-ai-37-72b6a032b7fa)).

---

To use on [AWS SageMaker](https://aws.amazon.com/sagemaker/) replace `<plugin-name>` with `vanwatch` and follow [these instructions](https://github.com/kamangir/blue-plugin/blob/main/SageMaker.md).
