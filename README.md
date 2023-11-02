## Apprise Alert Action
Adds an alert action to Splunk that allows sending a notification using any of the notification services supported by Apprise.

For a full list of notification services, see https://github.com/caronc/apprise/wiki

There are two ways of using this addon:
- Providing a URL in each alert action
- Using a configuration file and tags

### Providing a URL in each alert action
This requires no configuration to use. Just put a valid URL in the alert action and the service will be sent the alert.

### Using a configuration file and tags
See https://github.com/caronc/apprise/wiki/config for creating an Apprise configuration file.

To provide the configuration file to the add-on, in the Splunk UI go to *Settings>Alert Actions>Setup Apprise Alert Action*

Alternatively, this can be done by updating and placing the below config in local/alert_actions.conf

    [apprise_alert]
    param.config = <<config_file>>

Note: The default path the addon looks in for configuration files the apprise_alert/bin/ folder. Either provide a full path or relative path from this directory.
