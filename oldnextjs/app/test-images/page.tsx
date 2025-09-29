"use client";

export default function TestImages() {
  const testImages = [
    "/hero/apartment.webp",
    "/hero/hotel.webp",
    "/hero/villa.webp",
    "/hero/resort.webp",
    "/hero/chalets.webp",
    "/hero/motels.webp",
  ];

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Image Test Page</h1>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {testImages.map((imagePath, index) => (
          <div
            key={index}
            className="border border-gray-300 rounded-lg overflow-hidden"
          >
            <img
              src={imagePath}
              alt={`Test image ${index + 1}`}
              className="w-full h-48 object-cover"
              onLoad={() => console.log(`✅ Image loaded: ${imagePath}`)}
              onError={(e) => {
                console.error(`❌ Image failed to load: ${imagePath}`);
                const target = e.target as HTMLImageElement;
                target.style.backgroundColor = "#f3f4f6";
                target.alt = "Failed to load";
              }}
            />
            <div className="p-2 text-sm text-gray-600">{imagePath}</div>
          </div>
        ))}
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-bold mb-4">Single Large Test Image</h2>
        <div className="max-w-md">
          <img
            src="/hero/apartment.webp"
            alt="Single test image"
            className="w-full h-64 object-cover rounded-lg border"
            onLoad={() => console.log("✅ Single image loaded successfully")}
            onError={(e) => {
              console.error("❌ Single image failed to load");
              const target = e.target as HTMLImageElement;
              target.style.backgroundColor = "#ef4444";
              target.alt = "FAILED TO LOAD";
            }}
          />
        </div>
      </div>
    </div>
  );
}
