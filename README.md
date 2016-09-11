# cnav-sense
Sense HAT messaging system for [cnav-sense](https://circleci.com/gh/konradko/cnav-sense).

## Required hardware

* Raspberry Pi 1 or Zero
* Sense HAT

## Local installation

    $ git clone https://github.com/konradko/cnav-sense
    $ cd cnav-sense
    $ mkvirtualenv cnav-sense -a .
    $ make
    $ make test


## Deployment setup

1. Create a new Raspberry Pi 1 / Zero application (e.g. `cnavsense`) on [resin.io](https://dashboard.resin.io/)
    1. Resin OS => 1.11.0 is required for Sense HAT, newer (but less stable) OS versions are available on [resinstaging.io](https://dashboard.resinstaging.io)
    2. You can create an app on both and copy ``config.json`` file from resinstaging.io SD card to resin.io one - that way it will show up on resin.io
2. Add resin remote to the `cnav-sense` repository, e.g.:

    ```
    $ git remote add resin username@git.resin.io:username/cnavsense.git
    ```

3. Decrease GPU memory

| Fleet Configuration variable | Value |
| ------------- | ------------- |
| RESIN_HOST_CONFIG_gpu_mem | 16 |

4. Use resin.io application device OS and flash it on an SD card ([etcher.io](https://www.etcher.io/) recommended)
5. Put the SD card in the Raspberry Pi and wait for it to update (check status on [resin.io](https://dashboard.resin.io/) dashboard)


## Monitoring

### [Sentry](http://www.getsentry.com/)
Application exception tracking and alerting

| Environment variable | Example value | Description
| ------------- | ------------- | ------------- |
| SENTRY_DSN | https://user:pass@app.getsentry.com/appnum | [Sentry](getsentry.com) DSN address |


### [Papertrail](http://www.papertrailapp.com/)
System and application logs

| Environment variable | Example value | Description
| ------------- | ------------- | ------------- |
| PAPERTRAIL_HOST | logs.papertrailapp.com | [Papertrail](papertrailapp.com) host |
| PAPERTRAIL_PORT | 12345 | Papertrail host port |
| SENSE_LOG_PATH | /data/log/cnavsense | Sense app log path |


### [Prometheus](http://www.prometheus.io/)
System metrics and alerting

| Environment variable | Example value | Description
| ------------- | ------------- | ------------- |
| SMTP_HOST | smtp.mailgun.org:1234 | SMTP host and port |
| SMTP_ACCOUNT | postmaster@mailgun.com | Email address to send from |
| SMTP_PASSWORD | password123 | Password for the email address |
| THRESHOLD_CPU | 70 | max % of CPU in use |
| THRESHOLD_FS | 40 | min % of filesystem available |
| THRESHOLD_MEM | 300  | min MB of mem available |
| LOCAL_STORAGE_RETENTION | 360h0m0s | Period of data retention |

The metrics dashboard will be available at http://your-device-ip/consoles/node.html (you can make it available on the internet by enabling Public URL in resin.io dashboard).


## Deployment 

    $ make deploy

## SSH into the container using local network 

1. In resin.io dashboard set `CLIENT_PUBKEYS` environment variable to '\n' separated list of public keys, on OSX you can copy your public key with:
    ```
    $ cat ~/.ssh/id_rsa.pub | pbcopy
    ```
    | Environment variable | Example value | Description
    | ------------- | ------------- | ------------- |
    | CLIENT_PUBKEYS | ssh-rsa pubkeyone\nssh-rsa pubkeytwo | '\n' separated list of public keys that are allowed access |

2. SSH into a container using local address (you can get it from resin.io dashboard or using [resin-cli](https://github.com/resin-io/resin-cli)), e.g.:
    ```
    $ ssh root@192.168.1.15
    ```
