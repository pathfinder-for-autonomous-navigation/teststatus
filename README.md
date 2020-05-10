# teststatus
Tracks status of PAN testing. Never again will we wonder where did HITLs break.

To run, activate a virtual environment, install the requirements, then run

    python main.py

There will be a portal available at http://localhost:8080 . Try out the following endpoints:

- `/dummy` will instantiate the portal with dummy data
- `/reset` resets the database
- `/new-commit` uses the [Github Webhook format for pushes](https://developer.github.com/v3/activity/events/types/#pushevent). Expected format: application/json.
