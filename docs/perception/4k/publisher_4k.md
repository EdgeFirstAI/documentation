# Maivin Publisher with 4K

## Overview

The Maivin Publisher supports automatic 4K tile stitching for MCAP files containing 4 individual camera tiles. When 4 tile topics are detected in an MCAP file, the system automatically stitches them into a single 4K (3840x2160) image and uses these stitched images in the ZIP export instead of individual tile images.

## How It Works

### 1. Tile Detection

The system automatically detects when all 4 required tile topics are present in the MCAP file:

- `/camera/h264/tl` (Top Left)
- `/camera/h264/tr` (Top Right)
- `/camera/h264/bl` (Bottom Left)
- `/camera/h264/br` (Bottom Right)

Each topic must contain H.264 encoded video data.  The publisher detects recordings carrying a hostname prefix or the legacy `rt/` prefix on the tile topics automatically.

### 2. Tile Processing Pipeline

```text
MCAP File → H.264 Decode → Tile Stitching → 4K JPEG → ZIP Export
```

#### Step 1: H.264 Decoding

- Each tile is decoded from H.264 to RGB using stream accumulation
- Handles partial frames and keyframe detection
- Maintains separate decoders for each tile position
- Uses fallback frames when decode fails

#### Step 2: Tile Stitching

- Combines 4 individual 1920x1080 tiles into one 3840x2160 image
- Arranges tiles in 2x2 grid:

<div class="grid cards" markdown style="text-align:center;">
- Top Left
- Top Right
- Bottom Left
- Bottom Right
</div>
- Creates high-quality JPEG output (85% quality)

#### Step 3: ZIP Integration

- Stitched 4K images replace individual tile images in ZIP export
- Uses sequential matching (stitched frame 0 → sample 0, etc.)
- Falls back to original images when no stitched frames are available

## Recording the 4K Topics

The [Recording Service](../data_collection/recording.md) records every published topic by default, including the four tile topics once [tiling is enabled](camera_4k.md).  If the recorder was configured with an explicit topic list, the tile topics must be [added manually](../../platforms/configuration/mcap_recording.md#adding-topics-manually-to-the-recording-service) before recording the 4K streams.

!!! warning

    Stitching 4K tiled recordings of about 60 seconds or longer can exhaust the device memory, refer to the [Known Issues](../../platforms/software/issues.md#publisher-4k-tile-stitching-runs-out-of-memory-edgeai-1470).  Record short clips when using the tile topics and stop the `camera` and `model` services before running the publisher on the device.

## Usage

The Publisher binary is included on the platform and you must [SSH](../../platforms/networking/ssh.md) onto platform to run the command.

### Command Line

```bash
publisher zip --out test your_file.mcap
```

The system automatically detects tile topics and switches to stitching mode - no additional flags required.

### Output

When tile stitching is active, you'll see logs like:

```text
[INFO] Successfully created 198 stitched 4K frames
[INFO] Using stitched frame 0 for sample 0 (timestamp: 4037102265000)
[INFO] Using stitched frame 1 for sample 1 (timestamp: 4037140961000)
```

## Technical Details

### Tile Positioning

```rust
TilePosition::TopLeft     → (0, 0)
TilePosition::TopRight    → (1920, 0)
TilePosition::BottomLeft  → (0, 1080)
TilePosition::BottomRight → (1920, 1080)
```

### Image Processing

- **Input**: 4x H.264 encoded tiles (1920x1080 each)
- **Processing**: H.264 decode → RGB → Stitching → JPEG encode
- **Output**: Single 4K JPEG (3840x2160)

### Memory Management

- Stream accumulation for H.264 decoding
- Automatic cleanup of old incomplete frames
- Efficient memory usage with frame buffering

## Performance

### Processing Speed

- Typical processing: ~200-400 frames per second
- Memory usage: Optimized with stream accumulation
- Disk I/O: Minimal - processes in memory

### Quality Settings

- JPEG quality: 85% (configurable)
- Color space: RGB
- Compression: Optimized for quality/size balance

## Error Handling

### Decode Failures

- Uses fallback frames from previous successful decode
- Continues processing other tiles
- Logs warnings for failed tiles

### Missing Tiles

- Processes available tiles (partial stitching)
- Logs information about missing tile positions
- Graceful degradation

### Timestamp Mismatches

- Uses sequential matching instead of timestamp-based matching
- Handles different time bases between samples and video frames
- Robust fallback to original images

## Configuration

### Tile Topics

The system looks for these specific topic names:

```rust
let tile_topics = [
    "/camera/h264/tl",
    "/camera/h264/tr", 
    "/camera/h264/bl",
    "/camera/h264/br",
];
```

### Frame Processing

- **Cleanup threshold**: 1000ms (incomplete frames older than 1 second are discarded)
- **Force process threshold**: 100ms (frames with 3+ tiles are processed after 100ms)
- **Accumulation limit**: 200KB per tile (prevents memory issues)

## File Structure

### Source Files

- `src/tile_stitcher.rs` - Main stitching logic
- `src/zip.rs` - ZIP export integration
- `src/main.rs` - CLI integration

### Key Functions

- `has_tile_topics()` - Detects if all 4 tile topics are present
- `process_mcap_tiles_for_zip()` - Processes tiles and creates stitched frames
- `write_all_with_stitched_images()` - ZIP export with stitched images

## Troubleshooting

### Common Issues

1. **Empty ZIP file**: Usually indicates timestamp mismatch - fixed with sequential matching
2. **Missing tiles**: Check that all 4 tile topics are present and contain H.264 data
3. **Decode errors**: May indicate corrupted H.264 data or missing keyframes

### Debug Logging

Enable debug logging to see detailed processing information:

```bash
RUST_LOG=debug sudo ./edgefirst-publisher zip --out test your_file.mcap
```

### Performance Issues

- Large MCAP files may take time to process
- Memory usage scales with number of concurrent frames
- Consider processing in smaller chunks for very large files

## Future Enhancements

- Configurable tile topic names
- Support for different tile arrangements
- Real-time stitching mode
- Quality settings via command line
- Support for other output formats (PNG, etc.)

## Dependencies

- `openh264` - H.264 decoding
- `image` - JPEG encoding
- `turbojpeg` - Image compression
- `zip` - ZIP file creation
- `mcap` - MCAP file parsing

## License

This feature is part of the Maivin Publisher project and follows the same license terms.
