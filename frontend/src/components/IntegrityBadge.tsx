interface IntegrityBadgeProps {
  score: number;
  size?: "sm" | "md" | "lg";
}

export default function IntegrityBadge({
  score,
  size = "md",
}: IntegrityBadgeProps) {
  const getColor = () => {
    if (score >= 80) return "border-green-500 text-green-700 bg-green-50";
    if (score >= 60) return "border-yellow-500 text-yellow-700 bg-yellow-50";
    return "border-red-500 text-red-700 bg-red-50";
  };

  const getLabel = () => {
    if (score >= 80) return "High";
    if (score >= 60) return "Medium";
    return "Low";
  };

  const sizes = {
    sm: "w-12 h-12 text-sm",
    md: "w-16 h-16 text-lg",
    lg: "w-20 h-20 text-2xl",
  };

  return (
    <div className="flex flex-col items-center gap-1">
      <div
        className={`${sizes[size]} ${getColor()} rounded-full border-2 flex items-center justify-center font-bold`}
      >
        {Math.round(score)}
      </div>
      <span className="text-xs text-gray-500">{getLabel()} Integrity</span>
    </div>
  );
}
