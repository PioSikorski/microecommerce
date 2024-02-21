#!/bin/bash

sleep 10

pytest -v -p no:warnings -k "not test_integration"