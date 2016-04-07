#!/bin/bash
cp secret.cfg_tmpl secret.cfg
ln -fs local_jenkins.cfg local.cfg
./bin/pip install -r requirements.txt
./bin/develop up -f || true
./bin/buildout -t 3 || ./bin/buildout -v
