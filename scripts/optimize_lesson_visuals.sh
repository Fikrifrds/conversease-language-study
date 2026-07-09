#!/bin/bash
# Convert all lesson visual PNGs to WebP and resize to 1200px width.
# Run from repo root: bash scripts/optimize_lesson_visuals.sh

set -euo pipefail

IMAGE_DIR="apps/web/public/images/lesson-visual-library"
TARGET_WIDTH=1200

if ! command -v cwebp &> /dev/null; then
    echo "Error: cwebp not found. Install with: brew install webp"
    exit 1
fi

echo "Converting PNG → WebP (${TARGET_WIDTH}px width)..."
echo ""

count=0
saved=0

find "$IMAGE_DIR" -name "*.png" -type f | while read -r png_file; do
    webp_file="${png_file%.png}.webp"

    # Get original size
    orig_size=$(stat -f%z "$png_file" 2>/dev/null || stat -c%s "$png_file" 2>/dev/null)

    # Get original dimensions
    orig_width=$(sips -g pixelWidth "$png_file" 2>/dev/null | tail -1 | awk '{print $2}')
    orig_height=$(sips -g pixelHeight "$png_file" 2>/dev/null | tail -1 | awk '{print $2}')

    # Calculate target height maintaining aspect ratio
    target_height=$((orig_height * TARGET_WIDTH / orig_width))

    # Resize and convert to WebP
    cwebp -q 80 -resize "$TARGET_WIDTH" "$target_height" "$png_file" -o "$webp_file" 2>/dev/null

    # Get new size
    new_size=$(stat -f%z "$webp_file" 2>/dev/null || stat -c%s "$webp_file" 2>/dev/null)

    # Calculate savings
    savings=$(( (orig_size - new_size) * 100 / orig_size ))

    echo "  $(basename "$png_file"): $(numfmt --to=iec $orig_size 2>/dev/null || echo "${orig_size}B") → $(numfmt --to=iec $new_size 2>/dev/null || echo "${new_size}B") (-${savings}%)"

    count=$((count + 1))
    saved=$((saved + orig_size - new_size))
done

echo ""
echo "Done! Converted $count files."
echo "Total saved: $(numfmt --to=iec $saved 2>/dev/null || echo "${saved}B")"
echo ""
echo "Next steps:"
echo "1. Update image references in apps/web/lib/data.ts: .png → .webp"
echo "2. Update width/height in data.ts to $TARGET_WIDTH x (proportional)"
echo "3. Delete original PNGs: find $IMAGE_DIR -name '*.png' -delete"
echo "4. Commit the WebP files"
