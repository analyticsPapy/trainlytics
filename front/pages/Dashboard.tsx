import React from "react";
import { base44 } from "@/api/base44Client";
import { useQuery } from "@tanstack/react-query";
import { Activity, Clock, TrendingUp, Target, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { createPageUrl } from "@/utils";
import StatCard from "../../components/dashboard/StatCard";
import RecentWorkouts from "../../components/dashboard/RecentWorkouts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { format, subWeeks, startOfWeek, endOfWeek } from "date-fns";

export default function Dashboard() {
  const { data: workouts = [], isLoading } = useQuery({
    queryKey: ['workouts'],
    queryFn: () => base44.entities.Workout.list('-date'),
    initialData: [],
  });

  const { data: goals = [] } = useQuery({
    queryKey: ['goals'],
    queryFn: () => base44.entities.Goal.list('-created_date'),
    initialData: [],
  });

  // Calculate stats
  const thisWeekStart = startOfWeek(new Date(), { weekStartsOn: 1 });
  const thisWeekEnd = endOfWeek(new Date(), { weekStartsOn: 1 });
  const lastWeekStart = startOfWeek(subWeeks(new Date(), 1), { weekStartsOn: 1 });
  const lastWeekEnd = endOfWeek(subWeeks(new Date(), 1), { weekStartsOn: 1 });

  const thisWeekWorkouts = workouts.filter(w => {
    const date = new Date(w.date);
    return date >= thisWeekStart && date <= thisWeekEnd;
  });

  const lastWeekWorkouts = workouts.filter(w => {
    const date = new Date(w.date);
    return date >= lastWeekStart && date <= lastWeekEnd;
  });

  const totalDistance = thisWeekWorkouts.reduce((sum, w) => sum + (w.distance_km || 0), 0);
  const lastWeekDistance = lastWeekWorkouts.reduce((sum, w) => sum + (w.distance_km || 0), 0);
  const distanceTrend = lastWeekDistance > 0 ? (((totalDistance - lastWeekDistance) / lastWeekDistance) * 100).toFixed(1) : 0;

  const totalDuration = thisWeekWorkouts.reduce((sum, w) => sum + (w.duration_minutes || 0), 0);
  const lastWeekDuration = lastWeekWorkouts.reduce((sum, w) => sum + (w.duration_minutes || 0), 0);
  const durationTrend = lastWeekDuration > 0 ? (((totalDuration - lastWeekDuration) / lastWeekDuration) * 100).toFixed(1) : 0;

  const avgHeartRate = thisWeekWorkouts.length > 0 
    ? Math.round(thisWeekWorkouts.reduce((sum, w) => sum + (w.avg_heart_rate || 0), 0) / thisWeekWorkouts.length)
    : 0;

  const activeGoals = goals.filter(g => g.status === "active");

  return (
    <div className="p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-4xl font-bold text-slate-900 mb-2">Welcome Back, Athlete</h1>
            <p className="text-slate-600 text-lg">Here's your performance overview for this week</p>
          </div>
          <Link to={createPageUrl("Workouts")}>
            <Button className="bg-gradient-to-r from-indigo-600 to-blue-500 hover:from-indigo-700 hover:to-blue-600 shadow-lg shadow-indigo-500/30">
              <Plus className="w-5 h-5 mr-2" />
              Log Workout
            </Button>
          </Link>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Workouts"
            value={thisWeekWorkouts.length}
            unit="this week"
            icon={Activity}
            trend={thisWeekWorkouts.length > lastWeekWorkouts.length ? "up" : "down"}
            trendValue={`${Math.abs(thisWeekWorkouts.length - lastWeekWorkouts.length)}`}
            color="indigo"
          />
          <StatCard
            title="Distance"
            value={totalDistance.toFixed(1)}
            unit="km"
            icon={TrendingUp}
            trend={totalDistance > lastWeekDistance ? "up" : "down"}
            trendValue={`${Math.abs(distanceTrend)}%`}
            color="green"
          />
          <StatCard
            title="Duration"
            value={Math.round(totalDuration)}
            unit="min"
            icon={Clock}
            trend={totalDuration > lastWeekDuration ? "up" : "down"}
            trendValue={`${Math.abs(durationTrend)}%`}
            color="purple"
          />
          <StatCard
            title="Avg Heart Rate"
            value={avgHeartRate || "—"}
            unit={avgHeartRate ? "bpm" : ""}
            icon={Activity}
            color="orange"
          />
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Recent Workouts */}
          <div className="lg:col-span-2">
            <RecentWorkouts workouts={workouts} isLoading={isLoading} />
          </div>

          {/* Active Goals */}
          <div>
            <Card className="border-slate-200 bg-white/80 backdrop-blur-sm">
              <CardHeader className="border-b border-slate-100">
                <CardTitle className="flex items-center gap-2 text-xl">
                  <Target className="w-5 h-5 text-indigo-600" />
                  Active Goals
                </CardTitle>
              </CardHeader>
              <CardContent className="p-6">
                {activeGoals.length > 0 ? (
                  <div className="space-y-4">
                    {activeGoals.map((goal) => (
                      <div key={goal.id} className="p-4 rounded-xl border border-slate-200 bg-white">
                        <div className="flex items-start justify-between mb-3">
                          <h4 className="font-semibold text-slate-900">{goal.title}</h4>
                          <Badge className="bg-indigo-100 text-indigo-700 border-indigo-200">
                            {goal.goal_type}
                          </Badge>
                        </div>
                        <div className="mb-2">
                          <div className="flex justify-between text-sm mb-1">
                            <span className="text-slate-600">Progress</span>
                            <span className="font-semibold text-slate-900">{goal.progress || 0}%</span>
                          </div>
                          <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                            <div 
                              className="h-full bg-gradient-to-r from-indigo-600 to-blue-500 rounded-full transition-all duration-500"
                              style={{ width: `${goal.progress || 0}%` }}
                            />
                          </div>
                        </div>
                        <p className="text-sm text-slate-500">
                          Deadline: {format(new Date(goal.deadline), "MMM d, yyyy")}
                        </p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <Target className="w-12 h-12 text-slate-300 mx-auto mb-3" />
                    <p className="text-slate-500 mb-4">No active goals yet</p>
                    <Link to={createPageUrl("Goals")}>
                      <Button variant="outline" size="sm">
                        <Plus className="w-4 h-4 mr-2" />
                        Create Goal
                      </Button>
                    </Link>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}