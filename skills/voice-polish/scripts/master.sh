#!/usr/bin/env bash
# Bring a processed voice file to a loudness target with a true-peak-safe ceiling.
#
#   master.sh <in.wav> <out.wav> [target_lufs=-14] [ceiling_dbtp=-1]
#
# Linear gain to the target, then a limiter run at 4x the sample rate (so it catches
# inter-sample peaks), then a re-measure. Writes 24-bit WAV at the input sample rate.
set -euo pipefail

in="$1"; out="$2"; target="${3:--14}"; ceiling="${4:--1}"

measure() {   # prints "I TP" for a file
    ffmpeg -hide_banner -nostats -i "$1" -af ebur128=peak=true -f null - 2>&1 \
        | awk '/^ +I:/ {i=$2} /^ +Peak:/ {p=$2} END {print i, p}'
}

read -r I _ < <(measure "$in")
sr=$(ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate -of csv=p=0 "$in")
gain=$(awk -v t="$target" -v i="$I" 'BEGIN {printf "%.2f", t - i}')
# 0.3 dB of headroom under the ceiling for the resample back to the source rate.
limit=$(awk -v c="$ceiling" 'BEGIN {printf "%.5f", 10 ^ ((c - 0.3) / 20)}')

ffmpeg -v error -y -i "$in" \
    -af "volume=${gain}dB,aresample=$((sr * 4)),alimiter=limit=${limit}:attack=5:release=80:level=disabled,aresample=${sr}" \
    -c:a pcm_s24le "$out"

read -r I2 TP2 < <(measure "$out")
echo "master: ${I} LUFS -> ${I2} LUFS (gain ${gain} dB), true peak ${TP2} dBTP (ceiling ${ceiling}) -> ${out}"
if awk -v p="$TP2" -v c="$ceiling" 'BEGIN {exit !(p > c)}'; then
    echo "master: WARNING true peak ${TP2} dBTP is above the ${ceiling} dBTP ceiling" >&2
fi
