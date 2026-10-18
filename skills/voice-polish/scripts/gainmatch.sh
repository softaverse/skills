#!/usr/bin/env bash
# Gain-match candidate files for a fair listening comparison.
#
#   gainmatch.sh <out_dir> <target_lufs> <file1.wav> <file2.wav> [...]
#
# Pure linear gain (no compression or limiting, so tone and dynamics are untouched).
# Writes <out_dir>/<n>_<name>.wav for each file plus <out_dir>/AB_all.wav: every
# candidate back to back, in argument order, with 1 s of silence between them.
set -euo pipefail

out_dir="$1"; target="$2"; shift 2
mkdir -p "$out_dir"

inputs=(); filters=""; n=0
for f in "$@"; do
    n=$((n + 1))
    # Measure as stereo: a mono file upmixed afterwards would play ~3 LU louder.
    I=$(ffmpeg -hide_banner -nostats -i "$f" -af aformat=channel_layouts=stereo,ebur128 -f null - 2>&1 \
        | awk '/^ +I:/ {print $2}')
    gain=$(awk -v t="$target" -v i="$I" 'BEGIN {printf "%.2f", t - i}')
    o="$out_dir/${n}_$(basename "${f%.*}").wav"
    # Matched copies are stereo 48 kHz so they can be concatenated.
    ffmpeg -v error -y -i "$f" -af "volume=${gain}dB" -ac 2 -ar 48000 -c:a pcm_s24le "$o"
    peak=$(ffmpeg -hide_banner -nostats -i "$o" -af ebur128=peak=true -f null - 2>&1 | awk '/^ +Peak:/ {print $2}')
    echo "${n}. $(basename "$f"): ${I} LUFS, gain ${gain} dB, true peak ${peak} dBTP -> $o"
    inputs+=(-i "$o")
    [ "$n" -gt 1 ] && filters+="anullsrc=r=48000:cl=stereo,atrim=0:1[s$n];"
done

concat=""
for i in $(seq 1 "$n"); do
    [ "$i" -gt 1 ] && concat+="[s$i]"
    concat+="[$((i - 1)):a]"
done
segments=$((n * 2 - 1))
ffmpeg -v error -y "${inputs[@]}" -filter_complex "${filters}${concat}concat=n=${segments}:v=0:a=1" \
    -c:a pcm_s24le "$out_dir/AB_all.wav"
echo "back-to-back: $out_dir/AB_all.wav"
