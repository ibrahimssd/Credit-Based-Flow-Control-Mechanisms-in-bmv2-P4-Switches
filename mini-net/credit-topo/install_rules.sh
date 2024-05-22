#!/bin/bash

echo "install forwarding rules "
sh ./forwarding_rules.sh

echo "install cloning rules"
sh ./mirroring_rules.sh


echo "install queue rules"
sh ./queue_rules.sh