#!/bin/bash
echo "Start"
(trap 'kill 0' SIGINT; ./cyber_mind & ./cyber_nano )
echo "end"
