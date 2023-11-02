import sys, requests, json, re, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import apprise


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def check_inputs(config):
    required_fields = ['body']
    
    if not 'url' in config and not 'tag' in config:
        eprint("A URL or tag needs to be specified.")
        return False

    if 'tag' in config and not 'config' in config:
        eprint("Using a tag requires setting a configuration file defined in setup.")
        return False
    
    if 'tag' in config and 'config' in config:
        if not os.path.exists(config['config']):
            eprint("Unable to locate config file {}".format(config['config']))
            return False

    for field in required_fields:
        if not field in config:
            eprint("No "+field+" specified.")
            return False
        
    return True


if len(sys.argv) > 1 and sys.argv[1] == "--execute":
    alert = json.load(sys.stdin)
    if check_inputs(alert['configuration']):
        #load config
        config = alert['configuration']
        

        if 'config' in config and 'tag' in config:
            ac = apprise.AppriseConfig()
            ac.add(config['config'])

            ar = apprise.Apprise()
            ar.add(ac)

            if "title" in config:
                ar.notify(
                    body=config['body'],
                    title=config['title'],
                    tag=config['tag']
                )
            else:
                ar.notify(
                    body=config['body'],
                    tag=config['tag']
                )


        if 'url' in config:
            ar = apprise.Apprise()
            ar.add(config['url'])

            if "title" in config:
                ar.notify(
                    body=config['body'],
                    title=config['title']
                )
            else:
                ar.notify(
                    body=config['body']
                )

    else:
        eprint("Invalid configuration detected. Stopped.")
else:
    eprint("FATAL No execute flag given")
