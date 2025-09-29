"use client";

import { useState, useRef, useCallback } from "react";
import {
  PhotoIcon,
  XMarkIcon,
  ArrowUpOnSquareIcon,
} from "@heroicons/react/24/outline";
import { uploadService } from "@/services/upload.service";

interface UploadedImage {
  id: string;
  file: File;
  preview: string;
  uploaded: boolean;
  uploading: boolean;
  error?: string;
}

interface PhotoUploadProps {
  images: string[];
  onImagesChange: (images: string[]) => void;
  maxImages?: number;
  maxSizeInMB?: number;
  acceptedFormats?: string[];
  className?: string;
  title?: string;
  subtitle?: string;
}

export default function PhotoUpload({
  images,
  onImagesChange,
  maxImages = 10,
  maxSizeInMB = 5,
  acceptedFormats = [".jpg", ".jpeg", ".png", ".webp"],
  className = "",
  title = "Upload Photos",
  subtitle = "Add photos to showcase your listing",
}: PhotoUploadProps) {
  const [uploadedImages, setUploadedImages] = useState<UploadedImage[]>([]);
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Convert file to base64 for preview
  const getFilePreview = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  };

  // Validate file
  const validateFile = (file: File): string | null => {
    // Check file size
    if (file.size > maxSizeInMB * 1024 * 1024) {
      return `File size must be less than ${maxSizeInMB}MB`;
    }

    // Check file type
    const fileExtension = "." + file.name.split(".").pop()?.toLowerCase();
    if (!acceptedFormats.includes(fileExtension)) {
      return `File type must be one of: ${acceptedFormats.join(", ")}`;
    }

    return null;
  };

  // Upload file to backend
  const uploadFile = async (file: File): Promise<string> => {
    return await uploadService.uploadFile(file);
  };

  // Handle file selection
  const handleFiles = useCallback(
    async (fileList: FileList) => {
      const files = Array.from(fileList);
      const totalImages = uploadedImages.length + images.length + files.length;

      if (totalImages > maxImages) {
        setError(`Maximum ${maxImages} images allowed`);
        return;
      }

      setError("");

      // Process each file
      for (const file of files) {
        const validation = validateFile(file);
        if (validation) {
          setError(validation);
          continue;
        }

        try {
          const preview = await getFilePreview(file);
          const imageId =
            Date.now().toString() + Math.random().toString(36).substr(2, 9);

          const newImage: UploadedImage = {
            id: imageId,
            file,
            preview,
            uploaded: false,
            uploading: true,
          };

          // Add to state immediately with uploading status
          setUploadedImages((prev) => [...prev, newImage]);

          // Start upload
          try {
            const uploadedUrl = await uploadFile(file);

            // Update state with successful upload
            setUploadedImages((prev) =>
              prev.map((img) =>
                img.id === imageId
                  ? { ...img, uploaded: true, uploading: false }
                  : img
              )
            );

            // Add to the main images array
            onImagesChange([...images, uploadedUrl]);
            console.log("Photo uploaded successfully:", uploadedUrl);
          } catch (uploadError) {
            // Update state with upload error
            setUploadedImages((prev) =>
              prev.map((img) =>
                img.id === imageId
                  ? {
                      ...img,
                      uploaded: false,
                      uploading: false,
                      error:
                        uploadError instanceof Error
                          ? uploadError.message
                          : "Upload failed",
                    }
                  : img
              )
            );
          }
        } catch (previewError) {
          setError("Failed to process file");
        }
      }
    },
    [uploadedImages, images, maxImages, onImagesChange]
  );

  // Handle drag events
  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  // Handle drop
  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      console.log("File drop triggered", e.dataTransfer.files);
      setDragActive(false);

      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        handleFiles(e.dataTransfer.files);
      }
    },
    [handleFiles]
  );

  // Handle file input change
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log("File input change triggered", e.target.files);
    e.preventDefault();
    e.stopPropagation();
    if (e.target.files && e.target.files[0]) {
      handleFiles(e.target.files);
    }
  };

  // Remove uploaded image
  const removeUploadedImage = (imageId: string) => {
    setUploadedImages((prev) => prev.filter((img) => img.id !== imageId));
  };

  // Remove existing image
  const removeExistingImage = (index: number) => {
    const newImages = images.filter((_, i) => i !== index);
    onImagesChange(newImages);
  };

  // Retry upload
  const retryUpload = async (imageId: string) => {
    const image = uploadedImages.find((img) => img.id === imageId);
    if (!image) return;

    setUploadedImages((prev) =>
      prev.map((img) =>
        img.id === imageId ? { ...img, uploading: true, error: undefined } : img
      )
    );

    try {
      const uploadedUrl = await uploadFile(image.file);

      setUploadedImages((prev) =>
        prev.map((img) =>
          img.id === imageId
            ? { ...img, uploaded: true, uploading: false }
            : img
        )
      );

      onImagesChange([...images, uploadedUrl]);
    } catch (error) {
      setUploadedImages((prev) =>
        prev.map((img) =>
          img.id === imageId
            ? {
                ...img,
                uploading: false,
                error: error instanceof Error ? error.message : "Upload failed",
              }
            : img
        )
      );
    }
  };

  const totalImages = images.length + uploadedImages.length;
  const canAddMore = totalImages < maxImages;

  return (
    <div className={`space-y-6 ${className}`}>
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
        <p className="text-gray-600 text-sm">{subtitle}</p>
        <p className="text-gray-500 text-xs mt-1">
          Maximum {maxImages} images • Up to {maxSizeInMB}MB each •{" "}
          {acceptedFormats.join(", ")}
        </p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      {/* Upload Area */}
      {canAddMore && (
        <div
          className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200 ${
            dragActive
              ? "border-green-400 bg-green-50"
              : "border-gray-300 hover:border-gray-400 hover:bg-gray-50"
          }`}
          onDragEnter={(e) => {
            e.preventDefault();
            e.stopPropagation();
            handleDrag(e);
          }}
          onDragLeave={(e) => {
            e.preventDefault();
            e.stopPropagation();
            handleDrag(e);
          }}
          onDragOver={(e) => {
            e.preventDefault();
            e.stopPropagation();
            handleDrag(e);
          }}
          onDrop={(e) => {
            e.preventDefault();
            e.stopPropagation();
            handleDrop(e);
          }}
        >
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept={acceptedFormats.join(",")}
            onChange={handleInputChange}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            form="none"
          />

          <div className="space-y-4">
            <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center">
              <PhotoIcon className="w-8 h-8 text-gray-400" />
            </div>

            <div>
              <p className="text-lg font-medium text-gray-900 mb-2">
                {dragActive ? "Drop photos here" : "Upload photos"}
              </p>
              <p className="text-gray-600 text-sm mb-4">
                Drag and drop your photos here, or{" "}
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="text-green-600 hover:text-green-700 font-medium"
                >
                  browse files
                </button>
              </p>
            </div>

            <div className="flex items-center justify-center">
              <ArrowUpOnSquareIcon className="w-5 h-5 text-gray-400 mr-2" />
              <span className="text-sm text-gray-500">
                {totalImages} of {maxImages} photos
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Image Grid */}
      {(images.length > 0 || uploadedImages.length > 0) && (
        <div>
          <h4 className="text-md font-medium text-gray-900 mb-4">
            Your Photos ({totalImages})
          </h4>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {/* Existing Images */}
            {images.map((imageUrl, index) => (
              <div key={`existing-${index}`} className="relative group">
                <div className="aspect-square rounded-lg overflow-hidden bg-gray-100">
                  <img
                    src={imageUrl}
                    alt={`Uploaded ${index + 1}`}
                    className="w-full h-full object-cover"
                  />
                </div>

                <button
                  type="button"
                  onClick={() => removeExistingImage(index)}
                  className="absolute top-2 right-2 p-1.5 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-600"
                >
                  <XMarkIcon className="w-4 h-4" />
                </button>

                {index === 0 && (
                  <div className="absolute bottom-2 left-2 px-2 py-1 bg-green-500 text-white text-xs rounded font-medium">
                    Cover Photo
                  </div>
                )}
              </div>
            ))}

            {/* Uploading/Uploaded Images */}
            {uploadedImages.map((image, index) => (
              <div key={image.id} className="relative group">
                <div className="aspect-square rounded-lg overflow-hidden bg-gray-100">
                  <img
                    src={image.preview}
                    alt={`Uploading ${index + 1}`}
                    className={`w-full h-full object-cover transition-opacity ${
                      image.uploading ? "opacity-50" : "opacity-100"
                    }`}
                  />

                  {/* Upload Status Overlay */}
                  {image.uploading && (
                    <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                      <div className="text-white text-center">
                        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mx-auto mb-2"></div>
                        <div className="text-xs">Uploading...</div>
                      </div>
                    </div>
                  )}

                  {image.error && (
                    <div className="absolute inset-0 bg-red-500 bg-opacity-80 flex items-center justify-center">
                      <div className="text-white text-center p-2">
                        <div className="text-xs mb-2">{image.error}</div>
                        <button
                          type="button"
                          onClick={() => retryUpload(image.id)}
                          className="text-xs bg-white text-red-500 px-2 py-1 rounded hover:bg-gray-100"
                        >
                          Retry
                        </button>
                      </div>
                    </div>
                  )}

                  {image.uploaded && (
                    <div className="absolute top-2 left-2 p-1 bg-green-500 text-white rounded-full">
                      <svg
                        className="w-3 h-3"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                          clipRule="evenodd"
                        />
                      </svg>
                    </div>
                  )}
                </div>

                <button
                  type="button"
                  onClick={() => removeUploadedImage(image.id)}
                  className="absolute top-2 right-2 p-1.5 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-600"
                >
                  <XMarkIcon className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>

          {/* Instructions */}
          {images.length === 0 && uploadedImages.length > 0 && (
            <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-sm text-blue-700">
                <strong>Tip:</strong> The first photo will be used as your cover
                photo. You can reorder photos by uploading them in your
                preferred order.
              </p>
            </div>
          )}
        </div>
      )}

      {/* Quick Add Button */}
      {canAddMore && (images.length > 0 || uploadedImages.length > 0) && (
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          className="w-full py-3 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-gray-400 hover:text-gray-700 transition-colors flex items-center justify-center gap-2"
        >
          <PhotoIcon className="w-5 h-5" />
          Add More Photos ({maxImages - totalImages} remaining)
        </button>
      )}
    </div>
  );
}
