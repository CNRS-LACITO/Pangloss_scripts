#!/bin/sh

java -classpath log4j-api-2.20.0.jar:log4j-core-2.20.0.jar:log4j-1.2-api-2.20.0.jar:harvester2.jar:xalan.jar ORG.oclc.oai.harvester2.app.RawWrite https://cocoon.huma-num.fr/crdo_servlet/oai-pmh -metadataPrefix olac -setSpec set-af3bd0fd-2b33-3b0b-a6f1-49a7fc551eb1 -out metadata_pangloss.xml
