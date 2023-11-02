#Options for Apprise Alert Action

action.apprise_alert = [0|1]
* Enable Apprise Alert Action

action.apprise_alert.param.url = <string>
* The Notification service URL. Please see here for more info: https://github.com/caronc/apprise/wiki
* (optional, if tags is set)

action.apprise_alert.param.tag = <string>
* Tag to use to send notificaions. Requires a configuration file.
* (optional, if URL is set)

action.apprise_alert.param.body = <string>
* Body of the alert

action.apprise_alert.param.title = <string>
* Title of the alert
* (optional)