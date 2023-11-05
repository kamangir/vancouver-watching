# Vancouver Watching (`vanwatch`) 🌈

`vanwatch` 🌈 discovers and ingests images from traffic cameras in an area and then runs [YOLO 🚀](https://github.com/ultralytics/ultralytics) and other vision algo to extract information about urban activity at scale. 


```bash
 > vanwatch help
🌈 vancouver_watching-3.53.1
🌈 bird watching in downtown Vancouver with AI.

vancouver_watching conda create_env [validate]
 . create conda environmnt.
vancouver_watching conda validate
 . validate conda environmnt.
vancouver_watching discover \
	<area> \
	[~upload] \
	[--validate 1]
 . discover <area>.
vancouver_watching ingest \
	<area> \
	[dryrun,~upload] \
	[<object-name>] \
	[--count <-1>]
 . ingest <area> -> <object-name>.
vancouver_watching list <area> \
	[discovery|ingest]
 . list <area>.
vancouver_watching list areas
 . list areas.
```

## Discover and Ingest an Area

![image](https://user-images.githubusercontent.com/1007567/196573547-b1c71b3b-7fac-4d2c-bba0-a87b063830da.png)


To see the list of areas supported by `vanwatch` type in,

```bash
vanwatch list areas
```

-> [list of areas](./data/)

To discover the available cameras in an area type in,

```bash
vanwatch discover area=vancouver
```

You have generated a `geojson` of [traffic images in the City of Vancouver](./data/vancouver.geojson). Now, you can ingest the traffic images from this area and detect people and cars in them,

```bash
vanwatch ingest area=vancouver,count=2,detect
```

![image](./assets/georgiaE-inference.jpg)

model: https://hub.ultralytics.com/models/R6nMlK6kQjSsQ76MPqQM?tab=preview


## set-up

```bash
abcli git clone Vancouver-Watching install
```

To use the [Ultralytics API](https://hub.ultralytics.com/models), browse [this page](https://hub.ultralytics.com/settings?tab=api+keys) and copy your API key, then run,

```bash
@cookie write ultralytics.api.key <api-key>
```

To use on [AWS SageMaker](https://aws.amazon.com/sagemaker/), generate the seed 🌱,

```bash
@seed sagemaker
```

Then change the environment to a `PyTorch 2` image, `Python3` kernel, `ml.g4dn.xlarge` instance, and "open image terminal". Then, type in `bash` and paste the seed 🌱. Then, run,

```bash
vanwatch conda create_env validate
```

![image](./assets/sagemaker.png)