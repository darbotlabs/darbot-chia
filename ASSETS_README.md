# Asset Requirements for @darbotlabs/darbot-chia

This document outlines the asset requirements for the Darbot Chia VSCode extension and npm package.

## VSCode Extension Assets

### Extension Icon
- **Location**: `vscode-extension/assets/icon.png`
- **Size**: 128x128 pixels
- **Format**: PNG with transparent background
- **Purpose**: Main extension icon displayed in VSCode marketplace and extension manager

### Activity Bar Icon
- **Location**: `vscode-extension/assets/activity-bar-icon.svg`
- **Size**: 16x16 pixels (scalable SVG preferred)
- **Format**: SVG or PNG
- **Purpose**: Icon displayed in VSCode activity bar

### Status Bar Icons
- **Location**: `vscode-extension/assets/status/`
- **Files needed**:
  - `connected.svg` - 16x16px - Green indicator for connected state
  - `disconnected.svg` - 16x16px - Red indicator for disconnected state
  - `syncing.svg` - 16x16px - Orange/yellow indicator for syncing state
- **Format**: SVG preferred for scalability

## npm Package Assets

### Package Logo
- **Location**: `npm-package/assets/logo.png`
- **Size**: 512x512 pixels
- **Format**: PNG with transparent background
- **Purpose**: Main logo for npm package documentation and README

### Package Badge/Icon
- **Location**: `npm-package/assets/badge.svg`
- **Size**: 32x32 pixels
- **Format**: SVG
- **Purpose**: Small icon for inline use in documentation

## Marketing Assets

### GitHub Social Preview
- **Location**: `assets/github-social-preview.png`
- **Size**: 1280x640 pixels
- **Format**: PNG
- **Purpose**: Social media preview image for GitHub repository

### Marketplace Banner
- **Location**: `assets/marketplace-banner.png`
- **Size**: 1376x80 pixels
- **Format**: PNG
- **Purpose**: Banner image for VSCode marketplace listing

## Brand Guidelines

### Color Palette
The Darbot Chia brand should use colors that complement the Chia ecosystem:

- **Primary Green**: #3AAC59 (Chia's signature green)
- **Secondary Blue**: #1976D2 (Professional blue for contrast)
- **Dark Gray**: #2D3748 (For dark theme compatibility)
- **Light Gray**: #F7FAFC (For light theme compatibility)
- **Warning Orange**: #FF8C00 (For alerts and warnings)
- **Error Red**: #E53E3E (For error states)

### Typography
- **Primary Font**: Use system fonts (San Francisco, Segoe UI, Roboto)
- **Monospace**: Use VS Code's editor font for code snippets

### Logo Design Principles
1. **Simple and Clean**: Should work well at small sizes (16px)
2. **Recognizable**: Should be easily identifiable as Chia-related
3. **Scalable**: Must work in both light and dark themes
4. **Professional**: Suitable for enterprise development environments

## File Organization

```
assets/
├── vscode-extension/
│   ├── icon.png (128x128) - from leaf_128.png
│   ├── activity-bar-icon.png (16x16) - from leaf_16.png
│   └── status/
│       ├── connected.png (32x32) - from leaf_32_connected.png
│       ├── disconnected.png (32x32) - from leaf_32_disconnected.png
│       └── syncing.png (32x32) - from leaf_32_syncing.png
├── npm-package/
│   ├── logo.png (512x512) - from leaf_512.png
│   └── badge.png (32x32) - from leaf_32.png
├── marketing/
│   ├── github-social-preview.png (1280x640) - from social_preview_1280x640.png
│   └── marketplace-banner.png (1400x560) - from marketplace_banner_1400x560.png
└── brand/
    ├── style-guide.md
    └── color-palette.png
```

## Asset Installation

All required assets have been provided in GitHub comment #2926275214. To install them:

1. Download each asset from the comment
2. Place them in the corresponding locations shown above
3. Ensure proper file naming matches the destinations listed
4. The VSCode extension and NPM package are already configured to reference these asset paths

## Implementation Notes

### VSCode Extension
Update the `package.json` to reference the icon:
```json
{
  "icon": "assets/icon.png",
  "contributes": {
    "viewsContainers": {
      "activitybar": [
        {
          "id": "darbotChia",
          "title": "Darbot Chia",
          "icon": "assets/activity-bar-icon.svg"
        }
      ]
    }
  }
}
```

### npm Package
Add logo to the README:
```markdown
<div align="center">
  <img src="assets/logo.png" alt="Darbot Chia Logo" width="200">
  <h1>@darbotlabs/darbot-chia</h1>
</div>
```

## Current Status

- [x] VSCode extension icon (128x128) - `leaf_128.png` provided in comment #2926275214
- [x] Activity bar icon (16x16) - `leaf_16.png` provided in comment #2926275214
- [x] Status indicators (32x32 set) - `leaf_32_connected.png`, `leaf_32_disconnected.png`, `leaf_32_syncing.png` provided in comment #2926275214
- [x] npm package logo (512x512) - `leaf_512.png` provided in comment #2926275214
- [x] npm package badge (32x32) - `leaf_32.png` provided in comment #2926275214
- [x] GitHub social preview (1280x640) - `social_preview_1280x640.png` provided in comment #2926275214
- [x] Marketplace banner (1400x560) - `marketplace_banner_1400x560.png` provided in comment #2926275214
- [ ] Brand style guide

## Asset Creation Guidelines

When creating assets, please ensure:

1. **Consistency**: All assets should follow the same design language
2. **Accessibility**: Icons should be clearly visible in both light and dark themes
3. **Quality**: Use vector formats (SVG) when possible for scalability
4. **Optimization**: Compress images appropriately for web use
5. **Licensing**: Ensure all assets are properly licensed for open source use

## Provided Assets

All branded assets have been provided in GitHub comment #2926275214 and are ready for integration:

- Professional leaf-based logo design in multiple sizes (16px, 32px, 128px, 512px)
- Status indicators for connected, disconnected, and syncing states
- Marketing assets including GitHub social preview and VSCode marketplace banner
- Consistent design language across all asset sizes

The extension and NPM package have been updated to reference these assets. Once downloaded and placed in the appropriate directories, they will replace the placeholder icons.

## Legacy Placeholder Information

Previously, until proper branded assets were created, the extension used:
- VS Code's built-in icons (`$(server-process)`, `$(account)`, etc.)
- Placeholder colors and gradients  
- Generic shapes and symbols

These placeholders have now been replaced with proper asset references in the configuration files.