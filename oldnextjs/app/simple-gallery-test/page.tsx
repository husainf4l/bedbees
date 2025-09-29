"use client";

export default function SimpleGalleryTest() {
  const testAccommodation = {
    id: "test",
    title: "Test Accommodation",
    images: [
      "/hero/apartment.webp",
      "/hero/hotel.webp",
      "/hero/villa.webp",
      "/hero/resort.webp",
      "/hero/chalets.webp",
      "/hero/motels.webp",
    ],
  };

  console.log("Test accommodation:", testAccommodation);

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Simple Gallery Test</h1>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden max-w-md">
        <div className="relative overflow-hidden rounded-t-lg">
          {testAccommodation.images.length === 1 ? (
            <div className="aspect-video bg-gray-200 relative cursor-pointer">
              <img
                src={testAccommodation.images[0]}
                alt={testAccommodation.title}
                className="w-full h-full object-cover"
                onLoad={() => console.log("✅ Single image loaded")}
                onError={() => console.error("❌ Single image failed")}
              />
            </div>
          ) : testAccommodation.images.length >= 4 ? (
            <div className="grid grid-cols-2 gap-1 aspect-video">
              <div className="bg-gray-200 relative cursor-pointer">
                <img
                  src={testAccommodation.images[0]}
                  alt={`${testAccommodation.title} 1`}
                  className="w-full h-full object-cover"
                  onLoad={() => console.log("✅ Image 1 loaded")}
                  onError={() => console.error("❌ Image 1 failed")}
                />
              </div>
              <div className="grid grid-rows-2 gap-1">
                <div className="bg-gray-200 relative cursor-pointer">
                  <img
                    src={testAccommodation.images[1]}
                    alt={`${testAccommodation.title} 2`}
                    className="w-full h-full object-cover"
                    onLoad={() => console.log("✅ Image 2 loaded")}
                    onError={() => console.error("❌ Image 2 failed")}
                  />
                </div>
                <div className="grid grid-cols-2 gap-1">
                  <div className="bg-gray-200 relative cursor-pointer">
                    <img
                      src={testAccommodation.images[2]}
                      alt={`${testAccommodation.title} 3`}
                      className="w-full h-full object-cover"
                      onLoad={() => console.log("✅ Image 3 loaded")}
                      onError={() => console.error("❌ Image 3 failed")}
                    />
                  </div>
                  <div className="bg-gray-200 relative cursor-pointer">
                    <img
                      src={testAccommodation.images[3]}
                      alt={`${testAccommodation.title} 4`}
                      className="w-full h-full object-cover"
                      onLoad={() => console.log("✅ Image 4 loaded")}
                      onError={() => console.error("❌ Image 4 failed")}
                    />
                    {testAccommodation.images.length > 4 && (
                      <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center text-white font-bold text-lg">
                        +{testAccommodation.images.length - 4} more
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ) : null}
        </div>

        <div className="p-4">
          <h3 className="font-bold text-lg">{testAccommodation.title}</h3>
          <p className="text-gray-600">
            Images: {testAccommodation.images.length}
          </p>
        </div>
      </div>
    </div>
  );
}
