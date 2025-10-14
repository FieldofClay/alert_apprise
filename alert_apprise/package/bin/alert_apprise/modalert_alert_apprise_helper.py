# encoding = utf-8
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import apprise


def process_event(helper, *args, **kwargs):
    helper.log_info("Alert action alert_apprise started.")
    
    # Get parameters
    url = helper.get_param("url")
    tag = helper.get_param("tag")
    body = helper.get_param("body")
    title = helper.get_param("title")
    
    # Get global configuration file path from settings
    config_file = helper.get_global_setting("config_file")
    
    try:
        # Using tag with config file
        if tag and config_file:
            helper.log_info("Using tag '{}' with config file '{}'".format(tag, config_file))
            
            ac = apprise.AppriseConfig()
            ac.add(config_file)
            
            ar = apprise.Apprise()
            ar.add(ac)
            
            if title:
                result = ar.notify(body=body, title=title, tag=tag)
            else:
                result = ar.notify(body=body, tag=tag)
        
        # Using direct URL
        elif url:
            helper.log_info("Using direct URL: {}".format(url))
            
            ar = apprise.Apprise()
            ar.add(url)
            
            if title:
                result = ar.notify(body=body, title=title)
            else:
                result = ar.notify(body=body)
        
        else:
            helper.log_error("No valid notification method specified.")
            return 1
        
        if result:
            helper.log_info("Apprise notification sent successfully.")
            return 0
        else:
            helper.log_error("Apprise notification failed.")
            return 1
            
    except Exception as e:
        helper.log_error("Error sending Apprise notification: {}".format(str(e)))
        import traceback
        helper.log_error(traceback.format_exc())
        return 1
