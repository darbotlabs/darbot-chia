#!/bin/bash

echo "Building Darbot Chia VSCode Extension and NPM Package..."

# Build npm package first
echo "Building npm package..."
cd npm-package
if [ -f "package.json" ]; then
    npm install
    npm run build
    echo "✓ npm package built successfully"
else
    echo "✗ npm package.json not found"
fi

cd ..

# Build VSCode extension
echo "Building VSCode extension..."
cd vscode-extension
if [ -f "package.json" ]; then
    npm install
    npm run compile
    echo "✓ VSCode extension compiled successfully"
else
    echo "✗ VSCode extension package.json not found"
fi

cd ..

echo "Build complete!"
echo ""
echo "To package the VSCode extension for distribution:"
echo "  cd vscode-extension && npm install -g vsce && vsce package"
echo ""
echo "To publish the npm package:"
echo "  cd npm-package && npm publish"