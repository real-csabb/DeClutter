# DeClutter

Open Terminal and run:
```lsof -i tcp:3000```

If anything, run:
```kill [your PID here]```

Navigate to the DeClutter directory on your system. 
```cd DeClutter/```

Run:
```python -m venv venv```

Activate your virtual environment:
```source ./venv/bin/activate```

Then run:
```pip install -r requirements.txt```

Install Electron:
```npm install electron```

Start DeClutter:
```npm run start```

Pay attention to the JavaScript Console. If the connection being refused is not letting up, restart the app. This error is due to Flask refusing to run on your system.

Just in case, run the following command in application window:
```command+r```

## Features
- Click on "Manage Your Library", select files, and click add. Wait.
- Click the search bar, hover over the dropdown button, and start typing. Hit enter. This feature does not like uppercase.
- In order to reset homepage, hit enter.
- Click on categories to see different clusters.
- Clicking "View More" may break the app. In this case, kill the app, rerun lsof, and restart the app.
- You can click the on-hover text to open the file. In order to get back to the homepage, red circle or x out of this.
