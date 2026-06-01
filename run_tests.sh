#!/bin/bash

echo "Running ZI Agent System Tests..."
echo "================================"

cd agent-system
python tests/test_basic.py

echo ""
echo "Tests completed. Check output above for results."