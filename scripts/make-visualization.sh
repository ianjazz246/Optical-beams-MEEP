#!/bin/sh
# Script with workaround for h5topng colormap error

CONDA_PATH="$(conda info -s | awk '/CONDA_ROOT:/ {print $2}')"
# Probably will need to change package path when version changes
COLORMAPS_DIR="$CONDA_PATH/pkgs/h5utils-1.13.1-nompi_hd2bf37e_1113/share/h5utils/colormaps/"
DATA_COLORMAP=bluered
OVERLAY_COLORMAP=green

if [ $# -lt 1 ]; then
        printf 'Too few arguments. Requires at least one arguments.\n'
        printf 'Usage: %s data-file.h5 [overlay-file.h5] [last_dimension_slice] \n' "$0"
        printf 'last_dimension_slice is passed to -t argument of h5topng\n'
        exit 2
fi

case $# in
        1) h5topng -Zc "$COLORMAPS_DIR/$DATA_COLORMAP" "$1" ;;
        2) h5topng -Zc "$COLORMAPS_DIR/$DATA_COLORMAP" -A "$2" -a "$COLORMAPS_DIR/$OVERLAY_COLORMAP" "$1" ;;
        3) h5topng -t "$3" -Zc "$COLORMAPS_DIR/$DATA_COLORMAP" -A "$2" -a "$COLORMAPS_DIR/$OVERLAY_COLORMAP" "$1" ;;
esac

# ffmpeg -framerate 15 -pattern_type glob -i '*.png' -c:v libopenh264 -pix_fmt yuv420p "out.mp4"
