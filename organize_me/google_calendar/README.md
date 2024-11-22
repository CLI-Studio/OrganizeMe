### Setting Up Google Calendar API Credentials

This project requires Google Calendar API credentials to access the calendar data. Follow these steps to set up `credentials.json` for your local environment.
### Shortcut
link to get credentials.json: [Google Calendar API](https://console.cloud.google.com/apis/credentials?authuser=1&project=organize-me-2024)

#### Prerequisites

* A Google account.
* Access to Google Cloud Console.

#### Steps to Set Up `credentials.json`

1. **Create a Project in Google Cloud Console**
    * Go to the [Google Cloud Console](https://console.cloud.google.com/).
    * Click **Select a Project** at the top of the page, then **New Project**. Name the project and click **Create**.

2. **Enable the Google Calendar API**
    * In the left-hand menu, navigate to **APIs & Services > Library**.
    * Search for **Google Calendar API** and click **Enable**.

3. **Create OAuth Credentials**
    * Go to **APIs & Services > Credentials** in the left-hand menu.
    * Click **Create Credentials** and select **OAuth client ID**.
    * If prompted, configure the **OAuth consent screen** (only necessary for the first setup). Fill out the required fields and save.
    * Choose **Desktop App** as the application type, then click **Create**.
    * Download the `credentials.json` file by clicking **Download JSON**. This file contains the necessary client ID and client secret.

4. **Move `credentials.json` to Your Project Directory**
    * Place the downloaded `credentials.json` file in the root directory of your project (or specify its path in the script if it’s stored elsewhere).

5. **Run the Project**
    * On the first run, you’ll be prompted to authorize access. After authorizing, a `token.json` file will be created automatically. This file stores access tokens for future use, so you won’t need to re-authenticate each time.



#### Troubleshooting

* If you encounter a `FileNotFoundError` for `credentials.json`, ensure the file is named correctly and located in the root directory of your project.
* For any issues with Google Calendar API permissions, double-check that the API is enabled and that the OAuth consent screen is set up.
* After first run, delete the `token.json` file if you encounter any issues with authentication. The script will prompt you to re-authenticate.