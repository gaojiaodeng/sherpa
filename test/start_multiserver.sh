#!/usr/bin/env bash
process_num=1
use_gpu=false
port=9002
num_work_threads=1

. parse_options.sh || exit 1

export PATH=/data/nathan/sherpa/build/bin:$PATH
export PYTHONPATH=/data/nathan/sherpa/build/lib:/data/nathan/sherpa/sherpa/python:$PYTHONPATH
echo "parameters:"
echo "process_num $process_num"
echo "use_gpu $use_gpu"
echo "port $port"
echo "num_work_threads $num_work_threads"

for ((p=port; p<port+process_num; p++));
do
  sherpa-online-websocket-server \
    --use-gpu=$use_gpu \
    --port=$p \
    --num-work-threads=$num_work_threads \
    --num-io-threads=1 \
    --nn-model=/data/sherpa/k2fsa-zipformer-chinese-english-mixed/exp/cpu_jit.pt \
    --tokens=/data/sherpa/k2fsa-zipformer-chinese-english-mixed/data/lang_char_bpe/tokens.txt \
    --decoding-method=greedy_search \
    --log-file=./server_${p}.txt \
    --doc-root=/data/sherpa/sherpa/sherpa/bin/web &
done
