# discover and Ingest an Area

![image](https://user-images.githubusercontent.com/1007567/196573547-b1c71b3b-7fac-4d2c-bba0-a87b063830da.png)

to see the list of areas supported by `vanwatch` type in,

```bash
vanwatch list areas
```

to discover the available cameras in an area type in,

```bash
vanwatch discover area=vancouver
```

you have generated a `geojson` of [traffic images in the City of Vancouver](./data/vancouver.geojson). Now, you can ingest the traffic images from this area and detect people and cars in them,

```bash
vanwatch ingest area=vancouver,count=2,publish
```

![image](https://github.com/kamangir/assets/blob/main/vanwatch/2023-11-25-openai-vision/DavieWestBute-inference.jpg?raw=true)

model: https://hub.ultralytics.com/models/R6nMlK6kQjSsQ76MPqQM?tab=preview

[![image](https://github.com/kamangir/assets/blob/main/vanwatch/2023-11-25-openai-vision/QGIS.png?raw=true)](./QGIS/2023-11-12-12-03-40-85851.geojson)

![image](https://github.com/kamangir/assets/blob/main/vanwatch/2023-11-12-14-42-23-96479.gif?raw=true?raw=1)


![image](https://kamangir-public.s3.ca-central-1.amazonaws.com/2024-01-06-20-39-46-73614/2024-01-06-20-39-46-73614-2X.gif?raw=true)


dataset: [vanwatch-cache-2024-02-28-21-04-19-26236.tar.gz](https://kamangir-public.s3.ca-central-1.amazonaws.com/vanwatch-cache-2024-02-28-21-04-19-26236.tar.gz) ([details](https://medium.com/@arash-kamangir/vancouver-watching-with-ai-37-72b6a032b7fa)).