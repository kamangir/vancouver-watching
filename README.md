# Watching Vancouver


Idea: run [YOLOv5 🚀](https://github.com/kamangir/yolov5) on [traffic images in the City of Vancouver](https://opendata.vancouver.ca/explore/dataset/web-cam-url-links/information/). 

## install

```bash
abcli git clone vancouver-watching install
vanwatch help verbose
```


## ingest

```bash
abcli select
vanwatch ingest
```

Now, you have downloaded [web_cam_url_links.geojson](https://github.com/kamangir/Vancouver-Watching/blob/main/data/web_cam_url_links.geojson).