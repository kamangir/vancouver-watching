# 🌈 Vancouver Watching (`vanwatch`)

`vanwatch` 🌈 runs [YOLO 🚀](https://github.com/ultralytics/ultralytics), [OpenAI Vision](https://github.com/kamangir/openai-commands/tree/main/openai_commands/vision), and other AI algo on traffic cameras to extract timeseries of urban activity at scale.


```bash
pip install vancouver-watching
```

```bash
@select
vanwatch ingest \
	area=vancouver,count=4 . \
	detect,gif,publish
@open QGIS .
```

--table--


```mermaid
graph LR
    discover["vanwatch<br>discover<br>target=&lt;target&gt;<br>&lt;object-name&gt;"]
    object1["geojson"]:::folder
    ingest["vanwatch<br>ingest<br>target=&lt;target&gt;<br>&lt;object-name&gt;"]
    detect["vanwatch<br>detect<br>gif,publish<br>&lt;object-name&gt;"]
    ingest_detect["vanwatch<br>ingest<br>target=&lt;target&gt;<br>&lt;object-name&gt;<br>detect,gif,publish"]
    object2["geojson"]:::folder

    discover --> object1
    object1 -- "#target" --> ingest
    object1 -- "#target" --> ingest_detect
    ingest --> object2
    ingest_detect --> object2
    object2 --> detect
    detect --> object2

    classDef folder fill:#999,stroke:#333,stroke-width:2px;
```

---

--signature--
