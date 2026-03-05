interface RiskGaugeProps {
  score: number;
  label?: string;
}

export default function RiskGauge({ score, label = "Risk" }: RiskGaugeProps) {
  const pct = Math.round(score * 100);
  const getColor = () => {
    if (pct <= 30) return "bg-green-500";
    if (pct <= 60) return "bg-yellow-500";
    return "bg-red-500";
  };

  return (
    <div className="flex flex-col gap-1">
      <div className="flex justify-between text-sm">
        <span className="text-gray-600">{label}</span>
        <span className="font-medium">{pct}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className={`h-2 rounded-full ${getColor()} transition-all`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
