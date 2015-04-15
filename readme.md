# Arsenic - Fume

Fume is the back end component of Arsenic that interfaces with any number of
zabbix instances or other collectors to aggregate data and make it available via
restful api.

Fume relies on redis pubsub for ipc between Moxxy and Sydney (the api
components of Arsenic).

