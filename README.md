# teststatus
Tracks status of PAN testing. Never again will we wonder where did HITLs break.

To run, activate a virtual environment, install the requirements, then run

    gunicorn -w 3 -b 0.0.0.0:2000 main:app

There will then be a portal available at http://localhost:2000.

Live demo: http://163.172.142.70:2000

![](readme-images/pre-change.png)
![](readme-images/change-dialog.png)
![](readme-images/post-change.png)

Try out the following endpoints:

- `/dummy` will instantiate the portal with dummy data
- `/reset` resets the database
- `/new-commit` uses the [Github Webhook format for pushes](https://developer.github.com/v3/activity/events/types/#pushevent). Expected format: application/json. Sample data looks like this:

```
{
	"commits" : [
		{
			"sha": "deadbeef"
		}	
	]
}
```
