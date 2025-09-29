"use client";

import { useState } from "react";
import PhotoUpload from "@/components/ui/PhotoUpload";

export default function DebugImages() {
  const [images, setImages] = useState<string[]>([]);

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-8 text-center">
        📸 Photo Upload Component Test
      </h1>

      {/* Photo Upload Test */}
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <PhotoUpload
          images={images}
          onImagesChange={setImages}
          maxImages={8}
          maxSizeInMB={5}
          title="Test Photo Upload"
          subtitle="Upload photos to test the component functionality"
        />

        {/* Debug Info */}
        {images.length > 0 && (
          <div className="mt-8 p-4 bg-gray-100 rounded-lg">
            <h3 className="font-semibold text-gray-900 mb-2">Debug Info:</h3>
            <p className="text-sm text-gray-600">
              <strong>Images count:</strong> {images.length}
            </p>
            <div className="mt-2">
              <strong>Uploaded images:</strong>
              <ul className="mt-1 space-y-1">
                {images.map((url, index) => (
                  <li key={index} className="text-xs text-blue-600 break-all">
                    {index + 1}. {url}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>

      {/* Test 1: Direct image loading */}
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-xl font-bold mb-4">Test 1: Direct Image Loading</h2>
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center">
            <p className="mb-2 text-sm text-gray-600">apartment.webp</p>
            <img
              src="/hero/apartment.webp"
              alt="Apartment"
              className="w-full h-32 object-cover rounded border-2 border-blue-500"
              onLoad={() =>
                console.log("✅ apartment.webp loaded successfully!")
              }
              onError={() => console.error("❌ apartment.webp failed to load")}
            />
          </div>
          <div className="text-center">
            <p className="mb-2 text-sm text-gray-600">hotel.webp</p>
            <img
              src="/hero/hotel.webp"
              alt="Hotel"
              className="w-full h-32 object-cover rounded border-2 border-green-500"
              onLoad={() => console.log("✅ hotel.webp loaded successfully!")}
              onError={() => console.error("❌ hotel.webp failed to load")}
            />
          </div>
        </div>
      </div>

      {/* Test 2: Simple accommodation card */}
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-xl font-bold mb-4">
          Test 2: Simple Accommodation Card
        </h2>
        <div className="max-w-md">
          <div className="aspect-video bg-gray-200 rounded-lg overflow-hidden mb-4">
            <img
              src="/hero/apartment.webp"
              alt="Test Accommodation"
              className="w-full h-full object-cover"
              onLoad={() => console.log("✅ Card image loaded")}
              onError={(e) => {
                console.error("❌ Card image failed");
                const img = e.target as HTMLImageElement;
                img.src =
                  "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect width='400' height='300' fill='%23ff0000'/%3E%3Ctext x='200' y='150' font-family='Arial' font-size='20' fill='white' text-anchor='middle'%3EFAILED TO LOAD%3C/text%3E%3C/svg%3E";
              }}
            />
          </div>
          <h3 className="text-lg font-bold">Test Accommodation</h3>
          <p className="text-gray-600">This should show an image above</p>
        </div>
      </div>

      {/* Test 3: Console check */}
      <div className="bg-yellow-50 p-6 rounded-lg border border-yellow-200">
        <h2 className="text-xl font-bold mb-4">Test 3: Console Instructions</h2>
        <div className="space-y-2 text-sm">
          <p>
            <strong>1.</strong> Press F12 to open DevTools
          </p>
          <p>
            <strong>2.</strong> Go to Network tab
          </p>
          <p>
            <strong>3.</strong> Reload this page
          </p>
          <p>
            <strong>4.</strong> Filter by &quot;Images&quot; to see if
            hero/*.webp files are loading
          </p>
          <p>
            <strong>5.</strong> Check Console tab for any error messages
          </p>
        </div>
      </div>
    </div>
  );
}
