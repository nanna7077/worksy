## Worksy frontend

### Running the frontend

1. Install the dependencies with `npm install` inside a virtual environment.
2. Create the `.env` file in the frontend directory with the following content:
   ```
   REACT_APP_API_URL (https://api.worksy.com or your backend url)
   REACT_APP_MAP_API_KEY (from your Google Cloud API Keys, allow access for the following APIs:
            Maps JavaScript API,
            Places API,
            Places API (New),
            Address Validation API,
            Directions API,
            Geolocation API,
            Geocoding API,
            Maps Static API,
            Maps Embed API ,)
3. Start the application with `npm start` for development or `npm run build` for production.
   [Warning: Make sure to build the application with an externally exposed backend API URL in .env]