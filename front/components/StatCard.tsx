import React from "react";
import { Card } from "@/components/ui/card";
import { ArrowUp, ArrowDown } from "lucide-react";
import { motion } from "framer-motion";

export default function StatCard({ title, value, unit, icon: Icon, trend, trendValue, color = "indigo" }) {
  const colorClasses = {
    indigo: "from-indigo-600 to-blue-500 shadow-indigo-500/20",
    green: "from-green-600 to-emerald-500 shadow-green-500/20",
    purple: "from-purple-600 to-pink-500 shadow-purple-500/20",
    orange: "from-orange-600 to-amber-500 shadow-orange-500/20",
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="relative overflow-hidden border-slate-200 bg-white/80 backdrop-blur-sm hover:shadow-xl transition-all duration-300">
        <div className="p-6">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-2">{title}</p>
              <div className="flex items-baseline gap-2">
                <h3 className="text-4xl font-bold text-slate-900">{value}</h3>
                {unit && <span className="text-lg font-medium text-slate-500">{unit}</span>}
              </div>
              {trend && (
                <div className="flex items-center gap-1 mt-3">
                  {trend === "up" ? (
                    <ArrowUp className="w-4 h-4 text-green-600" />
                  ) : (
                    <ArrowDown className="w-4 h-4 text-red-600" />
                  )}
                  <span className={`text-sm font-semibold ${trend === "up" ? "text-green-600" : "text-red-600"}`}>
                    {trendValue}
                  </span>
                  <span className="text-sm text-slate-500">vs last week</span>
                </div>
              )}
            </div>
            <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${colorClasses[color]} flex items-center justify-center shadow-lg`}>
              <Icon className="w-7 h-7 text-white" />
            </div>
          </div>
        </div>
        <div className={`absolute -bottom-1 -right-1 w-32 h-32 rounded-full bg-gradient-to-br ${colorClasses[color]} opacity-5`} />
      </Card>
    </motion.div>
  );
}