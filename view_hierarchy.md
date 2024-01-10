# View Hierarchy Capture Using Droidbot API

## Workflow

- Clone this project with submodules:

```
git clone --recursive https://github.com/piaoliangkb/StateCapture.git
```

- Ensure that the `droidbotApp.apk` is placed in the `resources` directory.

- Install all Python dependencies

```
pip3 install -e droidbot/
pip3 install flask
```

- Start web server (it takes about 40 seconds to setup the initialization process)

```
python3 start.py
```

- Query XML from `http://127.0.0.1:5000/get_view`
