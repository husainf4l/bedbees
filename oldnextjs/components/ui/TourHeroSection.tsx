"use client";

import Image from "next/image";

interface TourHeroSectionProps {
  image: string;
  title?: string;
  subtitle?: string;
}

export default function TourHeroSection({
  image,
  title = "Discover Amazing Tours & Experiences in Cyprus",
  subtitle = "Join unique experiences with local guides and fellow travelers",
}: TourHeroSectionProps) {
  return (
    <section className="relative h-[60vh] flex items-center justify-center overflow-hidden">
      <Image
        src={image}
        alt="Tour Experience"
        fill
        className="object-cover"
      />
      <div className="absolute inset-0 bg-black/40"></div>
      <div className="relative z-10 text-center text-white max-w-6xl mx-auto px-6">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">{title}</h1>
        <p className="text-xl mb-8 opacity-90">{subtitle}</p>
      </div>
    </section>
  );
}