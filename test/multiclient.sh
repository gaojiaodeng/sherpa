#!/usr/bin/env bash
process_num=1
server_type=cpu
multi_server=0
port=9002
num_seconds_per_message=0.1
sleep_sec=0
server_ip=127.0.0.1
audio=/data/nathan/audios/mms-eng.wav

. parse_options.sh || exit 1

export PATH=/data/nathan/sherpa/build/bin:$PATH
export PYTHONPATH=/data/nathan/sherpa/build/lib:/data/nathan/sherpa/sherpa/python:$PYTHONPATH
echo "parameters:"
echo "process_num $process_num"
echo "server_type $server_type"
echo "port $port"
echo "num_seconds_per_message $num_seconds_per_message"
echo "sleep_sec $sleep_sec"
echo "server_ip $server_ip"
logpath=$PWD/log/${server_type}_${process_num}p
if [ $multi_server -ne 0 ]; then
  logpath=$PWD/log/${server_type}_multi_${process_num}p
fi
echo "logpath $logpath"
mkdir -p $logpath

p=$port
for ((i=1; i<=process_num; i++));
do
  if [ $sleep_sec -ne 0 ]; then
    sleep $sleep_sec
  fi
  sherpa-online-websocket-client \
    --server-ip=$server_ip \
    --server-port=$p \
    --num-seconds-per-message=$num_seconds_per_message \
    $audio > ${logpath}/client_${i}.log &
  if [ $multi_server -ne 0 ]; then
   ((p++))
  fi
done
wait
