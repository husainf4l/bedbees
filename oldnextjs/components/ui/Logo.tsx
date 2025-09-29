import React from "react";
import Image from "next/image";

interface LogoProps {
  size?: "sm" | "md" | "lg" | "xl";
  variant?: "default" | "white";
  className?: string;
}

const Logo: React.FC<LogoProps> = ({
  size = "md",
  variant = "default",
  className = "",
}) => {
  const sizes = {
    sm: { width: 80, height: 24 },
    md: { width: 100, height: 30 },
    lg: { width: 120, height: 36 },
    xl: { width: 140, height: 42 },
  };

  const containerClasses = {
    sm: "w-[80px] h-6",
    md: "w-[100px] h-[30px]",
    lg: "w-[120px] h-9",
    xl: "w-[140px] h-[42px]",
  };

  return (
    <div
      className={`${containerClasses[size]} ${className} flex items-center justify-center relative`}
    >
      <Image
        src="/logo/raheva-logo.png"
        alt="Raheva Logo"
        width={sizes[size].width}
        height={sizes[size].height}
        className={`object-contain transition-opacity duration-200 hover:opacity-90 ${
          variant === "white" ? "brightness-0 invert" : ""
        }`}
        priority
        sizes={`${sizes[size].width}px`}
      />
    </div>
  );
};

export default Logo;
