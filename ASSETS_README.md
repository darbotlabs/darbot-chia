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
│   ├── icon.png (128x128)
│   ├── activity-bar-icon.svg (16x16)
│   └── status/
│       ├── connected.svg (16x16)
│       ├── disconnected.svg (16x16)
│       └── syncing.svg (16x16)
├── npm-package/
│   ├── logo.png (512x512)
│   └── badge.svg (32x32)
├── marketing/
│   ├── github-social-preview.png (1280x640)
│   └── marketplace-banner.png (1376x80)
└── brand/
    ├── style-guide.md
    └── color-palette.png
```

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

- [ ] VSCode extension icon (128x128)
- [ ] Activity bar icon (16x16 SVG)
- [ ] Status indicators (16x16 SVG set)
- [ ] npm package logo (512x512)
- [ ] npm package badge (32x32 SVG)
- [ ] GitHub social preview (1280x640)
- [ ] Marketplace banner (1376x80)
- [ ] Brand style guide

## Asset Creation Guidelines

When creating assets, please ensure:

1. **Consistency**: All assets should follow the same design language
2. **Accessibility**: Icons should be clearly visible in both light and dark themes
3. **Quality**: Use vector formats (SVG) when possible for scalability
4. **Optimization**: Compress images appropriately for web use
5. **Licensing**: Ensure all assets are properly licensed for open source use

## Placeholder Assets

Until proper branded assets are created, the extension will use:
- VS Code's built-in icons (`$(server-process)`, `$(account)`, etc.)
- Placeholder colors and gradients
- Generic shapes and symbols

These should be replaced with proper branded assets before the v0.1 production release.