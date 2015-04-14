# Arsenic - Fume

Fume is the back end component of Arsenic that interfaces with any number of
zabbix instances or other collectors to aggregate data and make it available via
restful api.

Fume relies on redis pubsub for ipc between Moxxy and Sydney (the api
components of Arsenic).

## Deployment Strategy

Behind nginx reverse proxy.


# DEPRECATED
## API

All api calls are prefixed with `/api/vX.X` where `X.X` is the current api
version. At the time of writing, the api version is `v0.1`. So the api prefix is
currently: `/api/v0.1`.

The prefixing is done for two reasons:

0. To provide nginx something to filters on for reverse proxying.
0. To provide future support for updated APIs without breaking compatibility
   with components built against a specific api version.

