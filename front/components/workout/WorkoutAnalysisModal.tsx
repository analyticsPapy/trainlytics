import React from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { format } from "date-fns";
import { 
  Activity, 
  Clock, 
  MapPin, 
  Heart, 
  Flame, 
  Mountain, 
  TrendingUp,
  Gauge,
  MessageSquare,
  Smile
} from "lucide-react";
import { Separator } from "@/components/ui/separator";

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

const feelingEmojis = {
  great: "😄",
  good: "🙂",
  okay: "😐",
  tired: "😮‍💨",
  poor: "😔"
};

export default function WorkoutAnalysisModal({ workout, open, onClose, allWorkouts = [] }) {
  if (!workout) return null;

  // Calculate pace if distance and duration available
  const pace = workout.distance_km && workout.duration_minutes 
    ? (workout.duration_minutes / workout.distance_km).toFixed(2)
    : null;

  // Calculate speed
  const speed = workout.distance_km && workout.duration_minutes
    ? ((workout.distance_km / workout.duration_minutes) * 60).toFixed(2)
    : null;

  // Calculate averages from similar workouts
  const similarWorkouts = allWorkouts.filter(w => 
    w.activity_type === workout.activity_type && w.id !== workout.id
  );

  const avgDistance = similarWorkouts.length > 0
    ? (similarWorkouts.reduce((sum, w) => sum + (w.distance_km || 0), 0) / similarWorkouts.length).toFixed(2)
    : null;

  const avgDuration = similarWorkouts.length > 0
    ? (similarWorkouts.reduce((sum, w) => sum + (w.duration_minutes || 0), 0) / similarWorkouts.length).toFixed(0)
    : null;

  const avgHeartRate = similarWorkouts.filter(w => w.avg_heart_rate).length > 0
    ? Math.round(similarWorkouts.reduce((sum, w) => sum + (w.avg_heart_rate || 0), 0) / similarWorkouts.filter(w => w.avg_heart_rate).length)
    : null;

  const avgCalories = similarWorkouts.length > 0
    ? Math.round(similarWorkouts.reduce((sum, w) => sum + (w.calories || 0), 0) / similarWorkouts.length)
    : null;

  // Calculate efficiency score (0-100)
  let efficiencyScore = 50; // Base score
  if (workout.feeling === "great") efficiencyScore += 20;
  else if (workout.feeling === "good") efficiencyScore += 10;
  else if (workout.feeling === "poor") efficiencyScore -= 20;
  else if (workout.feeling === "tired") efficiencyScore -= 10;

  if (workout.intensity === "easy" && workout.feeling !== "poor") efficiencyScore += 10;
  if (workout.avg_heart_rate && workout.avg_heart_rate < 150) efficiencyScore += 10;
  if (pace && avgDistance && workout.distance_km > parseFloat(avgDistance)) efficiencyScore += 10;

  efficiencyScore = Math.max(0, Math.min(100, efficiencyScore));

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-3 text-2xl">
            <span className="text-4xl">{activityIcons[workout.activity_type]}</span>
            <div>
              <div className="capitalize">{workout.activity_type} Session</div>
              <p className="text-sm font-normal text-slate-500 mt-1">
                {format(new Date(workout.date), "EEEE, MMMM d, yyyy • h:mm a")}
              </p>
            </div>
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-6 mt-4">
          {/* Key Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {workout.distance_km && (
              <Card className="border-slate-200 bg-gradient-to-br from-blue-50 to-blue-100/50">
                <CardContent className="p-4">
                  <div className="flex items-center gap-2 text-slate-600 mb-2">
                    <MapPin className="w-4 h-4" />
                    <span className="text-sm font-medium">Distance</span>
                  </div>
                  <p className="text-3xl font-bold text-slate-900">{workout.distance_km}</p>
                  <p className="text-sm text-slate-600">km</p>
                  {avgDistance && (
                    <p className="text-xs text-slate-500 mt-1">
                      Avg: {avgDistance} km
                    </p>
                  )}
                </CardContent>
              </Card>
            )}

            {workout.duration_minutes && (
              <Card className="border-slate-200 bg-gradient-to-br from-purple-50 to-purple-100/50">
                <CardContent className="p-4">
                  <div className="flex items-center gap-2 text-slate-600 mb-2">
                    <Clock className="w-4 h-4" />
                    <span className="text-sm font-medium">Duration</span>
                  </div>
                  <p className="text-3xl font-bold text-slate-900">{workout.duration_minutes}</p>
                  <p className="text-sm text-slate-600">minutes</p>
                  {avgDuration && (
                    <p className="text-xs text-slate-500 mt-1">
                      Avg: {avgDuration} min
                    </p>
                  )}
                </CardContent>
              </Card>
            )}

            {workout.calories && (
              <Card className="border-slate-200 bg-gradient-to-br from-orange-50 to-orange-100/50">
                <CardContent className="p-4">
                  <div className="flex items-center gap-2 text-slate-600 mb-2">
                    <Flame className="w-4 h-4" />
                    <span className="text-sm font-medium">Calories</span>
                  </div>
                  <p className="text-3xl font-bold text-slate-900">{workout.calories}</p>
                  <p className="text-sm text-slate-600">kcal</p>
                  {avgCalories && (
                    <p className="text-xs text-slate-500 mt-1">
                      Avg: {avgCalories} kcal
                    </p>
                  )}
                </CardContent>
              </Card>
            )}

            {workout.elevation_gain && (
              <Card className="border-slate-200 bg-gradient-to-br from-green-50 to-green-100/50">
                <CardContent className="p-4">
                  <div className="flex items-center gap-2 text-slate-600 mb-2">
                    <Mountain className="w-4 h-4" />
                    <span className="text-sm font-medium">Elevation</span>
                  </div>
                  <p className="text-3xl font-bold text-slate-900">{workout.elevation_gain}</p>
                  <p className="text-sm text-slate-600">meters</p>
                </CardContent>
              </Card>
            )}
          </div>

          <Separator />

          {/* Performance Metrics */}
          <div>
            <h3 className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-indigo-600" />
              Performance Metrics
            </h3>
            <div className="grid md:grid-cols-2 gap-4">
              {pace && (
                <Card className="border-slate-200">
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-slate-600 mb-1">Average Pace</p>
                        <p className="text-2xl font-bold text-slate-900">{pace}</p>
                        <p className="text-sm text-slate-600">min/km</p>
                      </div>
                      <Gauge className="w-10 h-10 text-indigo-600" />
                    </div>
                  </CardContent>
                </Card>
              )}

              {speed && (
                <Card className="border-slate-200">
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-slate-600 mb-1">Average Speed</p>
                        <p className="text-2xl font-bold text-slate-900">{speed}</p>
                        <p className="text-sm text-slate-600">km/h</p>
                      </div>
                      <Activity className="w-10 h-10 text-green-600" />
                    </div>
                  </CardContent>
                </Card>
              )}

              {workout.avg_heart_rate && (
                <Card className="border-slate-200">
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-slate-600 mb-1">Avg Heart Rate</p>
                        <p className="text-2xl font-bold text-slate-900">{workout.avg_heart_rate}</p>
                        <p className="text-sm text-slate-600">bpm</p>
                        {avgHeartRate && (
                          <p className="text-xs text-slate-500 mt-1">
                            Avg: {avgHeartRate} bpm
                          </p>
                        )}
                      </div>
                      <Heart className="w-10 h-10 text-red-600" />
                    </div>
                  </CardContent>
                </Card>
              )}

              {workout.max_heart_rate && (
                <Card className="border-slate-200">
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-slate-600 mb-1">Max Heart Rate</p>
                        <p className="text-2xl font-bold text-slate-900">{workout.max_heart_rate}</p>
                        <p className="text-sm text-slate-600">bpm</p>
                      </div>
                      <Heart className="w-10 h-10 text-red-700" />
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>

          <Separator />

          {/* Intensity & Feeling */}
          <div className="grid md:grid-cols-2 gap-4">
            {workout.intensity && (
              <Card className="border-slate-200">
                <CardContent className="p-4">
                  <p className="text-sm text-slate-600 mb-3 font-medium">Intensity Level</p>
                  <Badge className={`${intensityColors[workout.intensity]} border text-base px-4 py-2`}>
                    {workout.intensity.charAt(0).toUpperCase() + workout.intensity.slice(1)}
                  </Badge>
                </CardContent>
              </Card>
            )}

            {workout.feeling && (
              <Card className="border-slate-200">
                <CardContent className="p-4">
                  <p className="text-sm text-slate-600 mb-3 font-medium flex items-center gap-2">
                    <Smile className="w-4 h-4" />
                    How You Felt
                  </p>
                  <div className="flex items-center gap-2">
                    <span className="text-3xl">{feelingEmojis[workout.feeling]}</span>
                    <span className="text-lg font-semibold text-slate-900 capitalize">
                      {workout.feeling}
                    </span>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Efficiency Score */}
          <Card className="border-indigo-200 bg-gradient-to-r from-indigo-50 to-blue-50">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-slate-900 mb-1">Workout Efficiency Score</h3>
                  <p className="text-sm text-slate-600">Based on intensity, feeling, and performance</p>
                </div>
                <div className="text-right">
                  <p className="text-4xl font-bold text-indigo-600">{efficiencyScore}</p>
                  <p className="text-sm text-slate-600">/100</p>
                </div>
              </div>
              <div className="h-3 bg-slate-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-indigo-600 to-blue-500 rounded-full transition-all duration-500"
                  style={{ width: `${efficiencyScore}%` }}
                />
              </div>
              <div className="mt-3 text-sm text-slate-600">
                {efficiencyScore >= 80 && "🏆 Excellent performance! Keep up the great work."}
                {efficiencyScore >= 60 && efficiencyScore < 80 && "💪 Good effort! You're making solid progress."}
                {efficiencyScore >= 40 && efficiencyScore < 60 && "👍 Decent workout. Consider your recovery needs."}
                {efficiencyScore < 40 && "😴 Take it easy. Rest and recovery are important too."}
              </div>
            </CardContent>
          </Card>

          {/* Notes */}
          {workout.notes && (
            <Card className="border-slate-200">
              <CardContent className="p-4">
                <p className="text-sm text-slate-600 mb-2 font-medium flex items-center gap-2">
                  <MessageSquare className="w-4 h-4" />
                  Workout Notes
                </p>
                <p className="text-slate-700 leading-relaxed">{workout.notes}</p>
              </CardContent>
            </Card>
          )}

          {/* Comparison Summary */}
          {similarWorkouts.length > 0 && (
            <Card className="border-slate-200 bg-slate-50">
              <CardContent className="p-4">
                <h3 className="text-sm font-semibold text-slate-900 mb-3">
                  Comparison with Your {workout.activity_type} Workouts
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  {workout.distance_km && avgDistance && (
                    <div>
                      <p className="text-slate-600">Distance</p>
                      <p className={`font-semibold ${workout.distance_km > parseFloat(avgDistance) ? 'text-green-600' : 'text-slate-900'}`}>
                        {workout.distance_km > parseFloat(avgDistance) ? '↑' : '↓'} 
                        {Math.abs(((workout.distance_km - parseFloat(avgDistance)) / parseFloat(avgDistance)) * 100).toFixed(0)}%
                      </p>
                    </div>
                  )}
                  {workout.duration_minutes && avgDuration && (
                    <div>
                      <p className="text-slate-600">Duration</p>
                      <p className={`font-semibold ${workout.duration_minutes > parseFloat(avgDuration) ? 'text-blue-600' : 'text-slate-900'}`}>
                        {workout.duration_minutes > parseFloat(avgDuration) ? '↑' : '↓'} 
                        {Math.abs(((workout.duration_minutes - parseFloat(avgDuration)) / parseFloat(avgDuration)) * 100).toFixed(0)}%
                      </p>
                    </div>
                  )}
                  {workout.calories && avgCalories && (
                    <div>
                      <p className="text-slate-600">Calories</p>
                      <p className={`font-semibold ${workout.calories > avgCalories ? 'text-orange-600' : 'text-slate-900'}`}>
                        {workout.calories > avgCalories ? '↑' : '↓'} 
                        {Math.abs(((workout.calories - avgCalories) / avgCalories) * 100).toFixed(0)}%
                      </p>
                    </div>
                  )}
                  {workout.avg_heart_rate && avgHeartRate && (
                    <div>
                      <p className="text-slate-600">Heart Rate</p>
                      <p className={`font-semibold ${workout.avg_heart_rate < avgHeartRate ? 'text-green-600' : 'text-slate-900'}`}>
                        {workout.avg_heart_rate < avgHeartRate ? '↓' : '↑'} 
                        {Math.abs(((workout.avg_heart_rate - avgHeartRate) / avgHeartRate) * 100).toFixed(0)}%
                      </p>
                    </div>
                  )}
                </div>
                <p className="text-xs text-slate-500 mt-3">
                  Based on {similarWorkouts.length} similar {workout.activity_type} workouts
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}