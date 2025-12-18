# WebUI with 4K

## Overview

The WebUI service has a smart video streaming solution that automatically detects and streams 4K video using a tiling approach, with automatic fallback to single H.264 stream when tiles are not available. The system is designed to provide optimal video quality based on your hardware capabilities and network conditions.

Of specific note:  the following is a "behind the scenes" view of how the WebUI manages the 4K outputs from the camera service automatically.  There are no actions the user needs to take to configure the WebUI service to accept 4K video output from the camera service.

## 4K Tiling System

### How It Works

The system attempts to stream 4K video by splitting it into 4 separate 1080p tiles:

- **Top Left (TL)**: `/rt/camera/h264/tl` - 1920x1080
- **Top Right (TR)**: `/rt/camera/h264/tr` - 1920x1080  
- **Bottom Left (BL)**: `/rt/camera/h264/bl` - 1920x1080
- **Bottom Right (BR)**: `/rt/camera/h264/br` - 1920x1080

These tiles are then merged into a single 4K canvas (3840x2160) for display.

### Tile Detection Process

1. **Connection Test**: The system opens WebSocket connections to all 4 tile endpoints
2. **Data Verification**: Waits for actual video data (not just connections) from at least 2 tiles
3. **Timeout Handling**: Uses a 5-second detection timeout
4. **Smart Resolution**: Only proceeds with tiles if sufficient data is streaming

### Synchronization System

The system implements aggressive frame synchronization:

- **Frame Rate**: 15 FPS maximum for stability
- **Sync Requirement**: ALL 4 tiles must have fresh frames before updating
- **Wait Time**: Maximum 500ms wait for all tiles to be ready
- **Fallback**: Emergency update if timeout is reached

## H.264 Fallback System

### When Fallback Occurs

The system automatically falls back to single H.264 stream in these scenarios:

1. **Insufficient Tiles**: Less than 2 tiles are streaming actual data
2. **Connection Failures**: Tile endpoints are not responding
3. **Initialization Errors**: Tile mode fails to initialize properly
4. **Detection Timeout**: No tiles respond within 5 seconds

### Fallback Behavior

- **Single Stream**: Uses `/rt/camera/h264` endpoint
- **Resolution**: 1920x1080 (standard HD)
- **Performance**: Lower resource usage, more stable
- **Quality**: Good quality but not 4K

## Configuration

### Detection Settings

```javascript
// Detection timeout (milliseconds)
this.detectionTimeout = 5000;

// Minimum tiles required for 4K mode
this.requiredTiles = 4;

// Frame synchronization settings
this.syncEnabled = true;
this.updateThrottle = 67; // 15fps max
this.maxWaitForSync = 500; // Max wait for all tiles
```

### Tile URLs

```javascript
this.tileUrls = [
    '/rt/camera/h264/tl',  // Top Left
    '/rt/camera/h264/tr',  // Top Right
    '/rt/camera/h264/bl',  // Bottom Left
    '/rt/camera/h264/br'   // Bottom Right
];
this.fallbackUrl = '/rt/camera/h264';
```

## Usage

### Basic Implementation

```javascript
import SmartVideoManager from './SmartVideoManager.js';
import h264Stream from './stream.js';

const videoManager = new SmartVideoManager();

videoManager.init((timing) => {
    // Frame update callback
    console.log(`Mode: ${timing.mode}`);
    console.log(`FPS: ${timing.fps}`);
}, h264Stream).then((texture) => {
    // Use texture in your 3D scene
    material.map = texture;
});
```

### Mode Detection

```javascript
// Check current mode
const mode = videoManager.getMode();
if (mode === 'tiles') {
    console.log('Using 4K tiling');
} else {
    console.log('Using H.264 fallback');
}
```

## Troubleshooting

### Common Issues

**Tiles Not Detected:**

- Check if tile endpoints are running
- Verify network connectivity
- Check browser console for WebSocket errors

**Poor Performance:**

- Monitor CPU/GPU usage
- Reduce browser tab count
- Close other video applications
- Consider H.264 fallback

**Synchronization Issues:**

- Check network latency
- Verify all tiles are streaming
- Monitor frame timing in console

### Debug Information

The system provides detailed console logging:

- Connection status for each tile
- Data reception confirmation
- Synchronization timing
- Fallback reasons

## Technical Details

### Canvas Operations

- **4K Canvas**: 3840x2160 merged canvas
- **Tile Size**: 1920x1080 per tile
- **Positioning**: Precise pixel positioning for seamless merging
- **Update Strategy**: Only updates when all tiles are ready

### Error Handling

- **Graceful Degradation**: Always falls back to working mode
- **Resource Cleanup**: Proper disposal on errors
- **Timeout Handling**: Prevents hanging on failed connections

---

*This system is designed to provide the best possible video experience based on your hardware capabilities while maintaining stability and reliability.*
