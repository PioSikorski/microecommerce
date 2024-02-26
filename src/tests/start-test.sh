#!/bin/bash

sleep 15

pytest -v -p no:warnings -k "not test_integration"