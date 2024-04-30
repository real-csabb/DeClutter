# DeClutter

Open Terminal and run:
```lsof -i tcp:3000```

If anything, run:
```kill [your PID here]```

Then run:
```pip install -r requirements.txt```

Just in case, run:
```npm install electron```

Start DeClutter:
```npm run start```

Just in case, run the following command in application window:
```command+r```
---
## Features
- Click on "Manage Your Library", select files, and click add. Wait.
- Click the search bar, hover over the dropdown button, and start typing. Hit enter. This feature does not like uppercase.
- In order to reset homepage, hit enter.
- Click on categories to see different clusters.
- Clicking "View More" may break the app. In this case, kill the app, rerun lsof, and restart the app.