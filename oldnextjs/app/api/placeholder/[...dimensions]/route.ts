import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET(
  request: NextRequest,
  { params }: { params: { dimensions: string[] } }
) {
  try {
    // Get dimensions from URL (e.g., /api/placeholder/400/300)
    const [width, height] = params.dimensions;

    // For now, just return a simple fallback image URL
    // In a real app, you might generate a placeholder image
    const fallbackImagePath = path.join(process.cwd(), 'public', 'hero', 'travelhero.webp');

    // Check if the fallback image exists
    if (fs.existsSync(fallbackImagePath)) {
      // Read the image file
      const imageBuffer = fs.readFileSync(fallbackImagePath);

      return new NextResponse(imageBuffer, {
        headers: {
          'Content-Type': 'image/webp',
          'Cache-Control': 'public, max-age=31536000',
        },
      });
    }

    // If image doesn't exist, return a simple SVG placeholder
    const svg = `
      <svg width="${width || 400}" height="${height || 300}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#f3f4f6"/>
        <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="16" fill="#6b7280" text-anchor="middle" dy=".3em">
          ${width || 400} × ${height || 300}
        </text>
      </svg>
    `;

    return new NextResponse(svg, {
      headers: {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'public, max-age=31536000',
      },
    });
  } catch (error) {
    console.error('Error serving placeholder image:', error);

    // Return a simple error SVG
    const errorSvg = `
      <svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#fee2e2"/>
        <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="14" fill="#dc2626" text-anchor="middle" dy=".3em">
          Image Error
        </text>
      </svg>
    `;

    return new NextResponse(errorSvg, {
      headers: {
        'Content-Type': 'image/svg+xml',
      },
    });
  }
}