# Tweet Live
Welcome to the Tweet Live project!

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Forking the Project](#forking-the-project)
  - [Prerequisites](#prerequisites)
- [GitHub Actions Integration](#github-actions-integration)
- [License](#license)
- [Technologies Used](#technologies-used)

## Introduction

Tweet Live is a Python-based application designed to help users stay updated on live Twitch streams and share notifications on Twitter and Discord. This project allows Twitch streamers to easily inform their followers when they start streaming and keep them engaged.

## Features

- Check the live status of a Twitch streamer.
- Automatically tweet a stream notification when a streamer goes live.
- Send a Discord message with embedded stream information.
- Monitor the validity of Twitch access tokens and receive mail when they are about to expire.

## Getting Started

### Forking the Project

1. Start by forking this repository to your GitHub account. Click the "Fork" button at the top right of this page to create your own copy of the project.

### Prerequisites

Before you begin, ensure you have met the following requirements:
- **Discord Webhook URL:** You need to create a Discord Webhook to receive notifications and send the message. You can create one from your Discord server by following the Discord documentation on setting up webhooks.
- **GitHub Repository with GitHub Actions Enabled:** You should have a GitHub repository where you intend to use this project. Ensure that GitHub Actions is enabled for your repository. You can check and enable it in the "Actions" tab of the repository.
- **Twitch Developer account** with client credentials (client ID and client secret).
- **Twitter Developer account*** with API keys and access tokens.

## Usage

This project is configured to be used with GitHub Actions for automated monitoring. Here's how to set it up:

1. **Fork this Repository:** Start by forking this repository to your GitHub account.

2. **Configure Secrets:** In your forked repository, go to "Settings" > "Secrets" and add the following secrets:

   - `TWITCH_CLIENT_ID`: Your Twitch Client ID.
   - `TWITCH_ACCESS_TOKEN`: Your Twitch Access Token.
   - `TWITCH_CLIENT_SECRET`: Your Twitch Client Secret.
   - `TWITCH_USERNAME`: Your Twitch Username.
   - `TWITTER_CONSUMER_KEY`: Your Twitter Consumer Key.
   - `TWITTER_CONSUMER_SECRET`: Your Twitter Consumer Secret.
   - `TWITTER_ACCESS_TOKEN`: Your Twitter Access Token.
   - `TWITTER_ACCESS_TOKEN_SECRET`: Your Twitter Access Token Secret.
   - `TWITTER_BEARER_TOKEN`: Your Twitter Bearer Token.
   - `DISCORD_WEBHOOK`: Your Discord Webhook URL.
   - `SMTP_USERNAME`: Your SMTP Email Username.
   - `SMTP_PASSWORD`: Your SMTP Email Password.
   - `SENDER_EMAIL`: Your Sender Email Address.
   - `RECIPIENT_EMAIL`: Your Recipient Email Address.
   - `REPO_NAME`: Your Forked GitHub Repository Name.

3. **GitHub Actions Workflow:** This repository includes a GitHub Actions workflow (`.github/workflows/main.yml`) that is scheduled to run at specific times. You can customize the schedule by modifying the cron expression in the workflow file.

4. **Run the Workflow:** The GitHub Actions workflow will automatically run at the scheduled times, check for updates on your Twitch schedule, and send a tweet, discord message, and email notification if a change is detected.

*Please note that this project is designed to be used with GitHub Actions, and local usage is not recommended. Forking the repository and setting up the required secrets is the recommended approach.*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Technologies Used

- Python
- Twitch API
- Twitter API
- Discord API
- SMTP (for email notifications)
- dotenv (for managing environment variables)
