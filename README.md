# 🌈 Vancouver Watching (`vanwatch`)

`vanwatch` 🌈 runs [YOLO 🚀](https://github.com/ultralytics/ultralytics), [OpenAI Vision](https://platform.openai.com/docs/guides/vision), and other AI algo on traffic cameras to extract time-series of urban activity at scale.


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

|   |   |   |
| --- | --- | --- |
| [last build](https://kamangir-public.s3.ca-central-1.amazonaws.com/test_vancouver_watching_ingest/animation.gif?raw=true&random=9k4sQhqU46g3o3Nr) [![image](https://kamangir-public.s3.ca-central-1.amazonaws.com/test_vancouver_watching_ingest/animation.gif?raw=true&random=UCUgzKhAkkb7i7CO)](https://kamangir-public.s3.ca-central-1.amazonaws.com/test_vancouver_watching_ingest/animation.gif?raw=true&random=9k4sQhqU46g3o3Nr) | [ingest -> detect](https://github.com/kamangir/assets/raw/main/vanwatch/2023-11-25-openai-vision/QGIS.png?raw=true) [![image](https://github.com/kamangir/assets/raw/main/vanwatch/2023-11-25-openai-vision/QGIS.png?raw=true)](https://github.com/kamangir/assets/raw/main/vanwatch/2023-11-25-openai-vision/QGIS.png?raw=true) | [time-series](https://kamangir-public.s3.ca-central-1.amazonaws.com/vanwatch-cache-2024-02-28-21-04-19-26236.tar.gz) [![image](https://kamangir-public.s3.ca-central-1.amazonaws.com/2024-01-06-20-39-46-73614/2024-01-06-20-39-46-73614-2X.gif?raw=true&random=z1HpPAatz5fiRoX4)](https://kamangir-public.s3.ca-central-1.amazonaws.com/vanwatch-cache-2024-02-28-21-04-19-26236.tar.gz) |

---


[![pylint](https://github.com/kamangir/vancouver-watching/actions/workflows/pylint.yml/badge.svg)](https://github.com/kamangir/vancouver-watching/actions/workflows/pylint.yml) [![pytest](https://github.com/kamangir/vancouver-watching/actions/workflows/pytest.yml/badge.svg)](https://github.com/kamangir/vancouver-watching/actions/workflows/pytest.yml) [![bashtest](https://github.com/kamangir/vancouver-watching/actions/workflows/bashtest.yml/badge.svg)](https://github.com/kamangir/vancouver-watching/actions/workflows/bashtest.yml) [![PyPI version](https://img.shields.io/pypi/v/vancouver-watching.svg)](https://pypi.org/project/vancouver-watching/) [![PyPI - Downloads](https://img.shields.io/pypi/dd/vancouver-watching)](https://pypistats.org/packages/vancouver-watching)

built by 🌀 [`blue_options-4.175.1`](https://github.com/kamangir/awesome-bash-cli), based on 🌈 [`vancouver_watching-3.465.1`](https://github.com/kamangir/vancouver-watching).

