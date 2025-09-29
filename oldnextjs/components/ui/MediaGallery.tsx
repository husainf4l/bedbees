"use client";

import { useState } from "react";
import Image from "next/image";
import {
  XMarkIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
} from "@heroicons/react/24/outline";

interface MediaGalleryProps {
  images: string[];
  title: string;
}

export default function MediaGallery({ images, title }: MediaGalleryProps) {
  const [isLightboxOpen, setIsLightboxOpen] = useState(false);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  // Debug logging
  console.log("MediaGallery received:", {
    images,
    title,
    imageCount: images?.length || 0,
  });

  const openLightbox = (index: number) => {
    console.log("Opening lightbox at index:", index);
    setCurrentImageIndex(index);
    setIsLightboxOpen(true);
  };

  const closeLightbox = () => {
    console.log("Closing lightbox");
    setIsLightboxOpen(false);
  };

  const nextImage = () => {
    setCurrentImageIndex((prev) => (prev + 1) % images.length);
  };

  const prevImage = () => {
    setCurrentImageIndex((prev) => (prev - 1 + images.length) % images.length);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Escape") closeLightbox();
    if (e.key === "ArrowRight") nextImage();
    if (e.key === "ArrowLeft") prevImage();
  };

  // Create mosaic layout - first image is large, others are smaller
  const renderMosaicGrid = () => {
    if (!images || images.length === 0) {
      console.warn("No images provided to MediaGallery");
      return (
        <div className="relative h-96 md:h-[500px] rounded-lg overflow-hidden bg-gray-200 flex items-center justify-center">
          <div className="text-gray-500 text-center">
            <svg
              className="w-16 h-16 mx-auto mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1}
                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
            <p className="text-lg font-medium">No images available</p>
            <p className="text-sm">
              Please add photos to showcase this accommodation
            </p>
          </div>
        </div>
      );
    }

    if (images.length === 1) {
      return (
        <div className="relative h-96 md:h-[500px] rounded-lg overflow-hidden cursor-pointer group">
          <img
            src={images[0]}
            alt={`${title} 1`}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            onClick={() => openLightbox(0)}
            onLoad={() =>
              console.log("✅ MediaGallery image loaded:", images[0])
            }
            onError={(e) => {
              console.error("❌ MediaGallery image failed:", images[0]);
              const img = e.target as HTMLImageElement;
              img.src = "/hero/hero1.webp";
            }}
          />
          <div className="absolute top-4 left-4 bg-black bg-opacity-60 text-white px-3 py-1 rounded-lg text-sm font-medium">
            1 photo
          </div>
        </div>
      );
    }

    return (
      <div className="relative">
        <div className="grid grid-cols-4 grid-rows-2 gap-2 h-96 md:h-[500px]">
          {/* Main large image */}
          <div
            className="col-span-2 row-span-2 relative rounded-lg overflow-hidden cursor-pointer group"
            onClick={() => openLightbox(0)}
          >
            <img
              src={images[0]}
              alt={`${title} 1`}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              onLoad={() =>
                console.log("✅ MediaGallery main image loaded:", images[0])
              }
              onError={(e) => {
                console.error("❌ MediaGallery main image failed:", images[0]);
                const img = e.target as HTMLImageElement;
                img.src = "/hero/hero1.webp";
              }}
            />
          </div>

          {/* Smaller images */}
          {images.slice(1, 5).map((image, index) => (
            <div
              key={index + 1}
              className="relative rounded-lg overflow-hidden cursor-pointer group"
              onClick={() => openLightbox(index + 1)}
            >
              <img
                src={image}
                alt={`${title} ${index + 2}`}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                onLoad={() =>
                  console.log(
                    `✅ MediaGallery image ${index + 2} loaded:`,
                    image
                  )
                }
                onError={(e) => {
                  console.error(
                    `❌ MediaGallery image ${index + 2} failed:`,
                    image
                  );
                  const img = e.target as HTMLImageElement;
                  img.src = "/hero/hero1.webp";
                }}
              />
              {/* Show "+X more" overlay on last image if there are more images */}
              {index === 3 && images.length > 5 && (
                <div className="absolute inset-0 bg-black/60 flex items-center justify-center">
                  <span className="text-white text-xl font-semibold">
                    +{images.length - 5} more
                  </span>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Photo count overlay */}
        <div className="absolute top-4 left-4 bg-black bg-opacity-60 text-white px-3 py-1 rounded-lg text-sm font-medium">
          {images.length} photos
        </div>
      </div>
    );
  };

  return (
    <>
      {/* Mosaic Grid */}
      <div className="mb-6">
        {renderMosaicGrid()}

        {/* Image counter */}
        <div className="mt-3 text-sm text-gray-600 text-center">
          {images.length} {images.length === 1 ? "photo" : "photos"}
        </div>
      </div>

      {/* Lightbox */}
      {isLightboxOpen && (
        <div
          className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center"
          onClick={closeLightbox}
          onKeyDown={handleKeyDown}
          tabIndex={0}
        >
          {/* Close button */}
          <button
            onClick={closeLightbox}
            className="absolute top-4 right-4 z-10 p-2 rounded-full bg-black/50 text-white hover:bg-black/70 transition-colors"
          >
            <XMarkIcon className="w-6 h-6" />
          </button>

          {/* Image counter */}
          <div className="absolute top-4 left-4 z-10 px-3 py-1 rounded-full bg-black/50 text-white text-sm">
            {currentImageIndex + 1} / {images.length}
          </div>

          {/* Previous button */}
          {images.length > 1 && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                prevImage();
              }}
              className="absolute left-4 z-10 p-3 rounded-full bg-black/50 text-white hover:bg-black/70 transition-colors"
            >
              <ChevronLeftIcon className="w-6 h-6" />
            </button>
          )}

          {/* Next button */}
          {images.length > 1 && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                nextImage();
              }}
              className="absolute right-4 z-10 p-3 rounded-full bg-black/50 text-white hover:bg-black/70 transition-colors"
            >
              <ChevronRightIcon className="w-6 h-6" />
            </button>
          )}

          {/* Main image */}
          <div
            className="relative max-w-4xl max-h-[90vh] w-full h-full mx-4"
            onClick={(e) => e.stopPropagation()}
          >
            <Image
              src={images[currentImageIndex]}
              alt={`${title} ${currentImageIndex + 1}`}
              fill
              className="object-contain"
              priority
            />
          </div>

          {/* Thumbnail strip at bottom */}
          {images.length > 1 && (
            <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 max-w-4xl w-full px-4">
              <div className="flex justify-center space-x-2 overflow-x-auto pb-2">
                {images.map((image, index) => (
                  <button
                    key={index}
                    onClick={(e) => {
                      e.stopPropagation();
                      setCurrentImageIndex(index);
                    }}
                    className={`flex-shrink-0 w-16 h-12 rounded-lg overflow-hidden border-2 transition-all ${
                      currentImageIndex === index
                        ? "border-white scale-110"
                        : "border-transparent opacity-70 hover:opacity-100"
                    }`}
                  >
                    <Image
                      src={image}
                      alt={`${title} ${index + 1}`}
                      width={64}
                      height={48}
                      className="object-cover w-full h-full"
                    />
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </>
  );
}
