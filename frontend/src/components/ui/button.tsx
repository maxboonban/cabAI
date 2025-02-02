import * as React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "outline" | "primary"; // Button variant
  size?: "sm" | "md" | "lg"; // Button size
  fullWidth?: boolean; // Option to make the button full-width
  className?: string; // Allow additional custom classes
}

const Button: React.FC<ButtonProps> = ({
  variant = "default",
  size = "md",
  children,
  fullWidth = false,
  className,
  ...props
}) => {
  // Define the base button classes
  let baseClasses = "flex items-center justify-center whitespace-nowrap pointer";

  // Customize button based on the variant
  let variantClasses = "bg-transparent text-white"; // add hover later

  // Customize button based on the size
  let sizeClasses = "";
  switch (size) {
    case "sm":
      sizeClasses = "px-3 py-2 text-sm";
      break;
    case "md":
      sizeClasses = "px-4 py-2 text-base";
      break;
    case "lg":
      sizeClasses = "px-6 py-3 text-lg";
      break;
  }

  // Prevent vertical growth by setting fixed padding and height
  const preventVerticalGrowthClasses = "h-auto max-h-[40px]";

  // Combine everything
  const buttonClasses = `${baseClasses} ${variantClasses} ${sizeClasses} ${preventVerticalGrowthClasses} ${fullWidth ? "w-full" : "w-auto"} ${className || ""}`;

  return (
    <button className={buttonClasses} {...props}>
      {children}
    </button>
  );
};

export default Button;
