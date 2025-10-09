#!/bin/bash

# Quick Image Optimization for BedBees
# Creates backup and runs optimization

echo "🖼️  BedBees Image Optimization"
echo "================================"
echo ""

# Check if images directory exists
if [ ! -d "static/core/images" ]; then
    echo "❌ Error: static/core/images directory not found!"
    exit 1
fi

# Show current size
echo "📊 Current folder size:"
du -sh static/core/images/
echo ""

# Ask for confirmation
read -p "Create backup before optimizing? (recommended) [Y/n]: " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    echo "💾 Creating backup..."
    
    # Create backup with timestamp
    timestamp=$(date +%Y%m%d_%H%M%S)
    backup_dir="static/core/images_backup_${timestamp}"
    
    cp -r static/core/images "$backup_dir"
    
    if [ $? -eq 0 ]; then
        echo "✅ Backup created: $backup_dir"
        backup_size=$(du -sh "$backup_dir" | cut -f1)
        echo "📦 Backup size: $backup_size"
    else
        echo "❌ Backup failed! Aborting."
        exit 1
    fi
else
    echo "⚠️  Skipping backup (not recommended)"
fi

echo ""
echo "🚀 Starting optimization..."
echo ""

# Run Python optimization script
python3 optimize_images.py

echo ""
echo "✅ Done!"
echo ""
echo "📊 New folder size:"
du -sh static/core/images/
echo ""
echo "💡 To restore backup: cp -r $backup_dir static/core/images"
