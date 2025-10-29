import React, { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { Activity, Clock, MapPin, Heart, Flame, BarChart3 } from "lucide-react";
import { format } from "date-fns";
import WorkoutAnalysisModal from "../workouts/WorkoutAnalysisModal";

const activityIcons = {
  running: "🏃",
  cycling: "🚴",
  swimming: "🏊",
  walking: "🚶",
  hiking: "🥾",
  triathlon: "🏊🚴🏃",
  other: "💪"
};

const intensityColors = {
  easy: "bg-green-100 text-green-700 border-green-200",
  moderate: "bg-blue-100 text-blue-700 border-blue-200",
  hard: "bg-orange-100 text-orange-700 border-orange-200",
  maximum: "bg-red-100 text-red-700 border-red-200"
};

export default function RecentWorkouts({ workouts, isLoading }) {
  const [selectedWorkout, setSelectedWorkout] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleWorkoutClick = (workout) => {
    setSelectedWorkout(workout);
    setIsModalOpen(true);
  };

  if (isLoading) {
    return (
      <Card className="border-slate-200 bg-white/80 backdrop-blur-sm">
        <CardHeader>
          <CardTitle>Recent Workouts</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-24 bg-slate-100 rounded-xl animate-pulse" />
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <>
      <Card className="border-slate-200 bg-white/80 backdrop-blur-sm">
        <CardHeader className="border-b border-slate-100">
          <CardTitle className="flex items-center gap-2 text-xl">
            <Activity className="w-5 h-5 text-indigo-600" />
            Recent Workouts
          </CardTitle>
        </CardHeader>
        <CardContent className="p-6">
          <div className="space-y-3">
            {workouts.slice(0, 5).map((workout, index) => (
              <motion.div
                key={workout.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="p-4 rounded-xl border border-slate-200 hover:border-indigo-300 hover:shadow-lg transition-all duration-300 bg-white cursor-pointer group"
                onClick={() => handleWorkoutClick(workout)}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <span className="text-3xl">{activityIcons[workout.activity_type]}</span>
                    <div>
                      <h4 className="font-semibold text-slate-900 capitalize flex items-center gap-2">
                        {workout.activity_type}
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-6 px-2 opacity-0 group-hover:opacity-100 transition-opacity"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleWorkoutClick(workout);
                          }}
                        >
                          <BarChart3 className="w-4 h-4 text-indigo-600" />
                        </Button>
                      </h4>
                      <p className="text-sm text-slate-500">{format(new Date(workout.date), "MMM d, yyyy • h:mm a")}</p>
                    </div>
                  </div>
                  {workout.intensity && (
                    <Badge className={`${intensityColors[workout.intensity]} border font-medium`}>
                      {workout.intensity}
                    </Badge>
                  )}
                </div>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                  {workout.distance_km && (
                    <div className="flex items-center gap-2">
                      <MapPin className="w-4 h-4 text-slate-400" />
                      <span className="text-slate-600">{workout.distance_km} km</span>
                    </div>
                  )}
                  {workout.duration_minutes && (
                    <div className="flex items-center gap-2">
                      <Clock className="w-4 h-4 text-slate-400" />
                      <span className="text-slate-600">{workout.duration_minutes} min</span>
                    </div>
                  )}
                  {workout.avg_heart_rate && (
                    <div className="flex items-center gap-2">
                      <Heart className="w-4 h-4 text-red-500" />
                      <span className="text-slate-600">{workout.avg_heart_rate} bpm</span>
                    </div>
                  )}
                  {workout.calories && (
                    <div className="flex items-center gap-2">
                      <Flame className="w-4 h-4 text-orange-500" />
                      <span className="text-slate-600">{workout.calories} cal</span>
                    </div>
                  )}
                </div>

                {workout.distance_km && workout.duration_minutes && (
                  <div className="mt-3 pt-3 border-t border-slate-100">
                    <p className="text-sm text-slate-500">
                      Pace: <span className="font-semibold text-slate-700">{(workout.duration_minutes / workout.distance_km).toFixed(2)} min/km</span>
                    </p>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </CardContent>
      </Card>

      <WorkoutAnalysisModal
        workout={selectedWorkout}
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        allWorkouts={workouts}
      />
    </>
  );
}