#!/bin/bash
echo -ne "\033]0;NCM-Api\007"
echo "NCM-Api By XiaoMao 2025"
python3 main.py
echo "请按任意键继续. . . "
read -n 1 -s