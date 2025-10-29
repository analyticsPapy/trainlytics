import React, { useState } from "react";
import { base44 } from "@/api/base44Client";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Plus, X, Save, Activity } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import RecentWorkouts from "../../components/dashboard/RecentWorkouts";

export default function Workouts() {
  const [showForm, setShowForm] = useState(false);
  const queryClient = useQueryClient();

  const [formData, setFormData] = useState({
    activity_type: "running",
    date: new Date().toISOString().slice(0, 16),
    duration_minutes: "",
    distance_km: "",
    avg_heart_rate: "",
    max_heart_rate: "",
    intensity: "moderate",
    calories: "",
    elevation_gain: "",
    notes: "",
    feeling: "good"
  });

  const { data: workouts = [], isLoading } = useQuery({
    queryKey: ['workouts'],
    queryFn: () => base44.entities.Workout.list('-date'),
    initialData: [],
  });

  const createWorkoutMutation = useMutation({
    mutationFn: (data) => base44.entities.Workout.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workouts'] });
      setShowForm(false);
      setFormData({
        activity_type: "running",
        date: new Date().toISOString().slice(0, 16),
        duration_minutes: "",
        distance_km: "",
        avg_heart_rate: "",
        max_heart_rate: "",
        intensity: "moderate",
        calories: "",
        elevation_gain: "",
        notes: "",
        feeling: "good"
      });
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    const cleanData = Object.fromEntries(
      Object.entries(formData).filter(([_, v]) => v !== "")
    );
    // Convert numeric fields
    if (cleanData.duration_minutes) cleanData.duration_minutes = parseFloat(cleanData.duration_minutes);
    if (cleanData.distance_km) cleanData.distance_km = parseFloat(cleanData.distance_km);
    if (cleanData.avg_heart_rate) cleanData.avg_heart_rate = parseFloat(cleanData.avg_heart_rate);
    if (cleanData.max_heart_rate) cleanData.max_heart_rate = parseFloat(cleanData.max_heart_rate);
    if (cleanData.calories) cleanData.calories = parseFloat(cleanData.calories);
    if (cleanData.elevation_gain) cleanData.elevation_gain = parseFloat(cleanData.elevation_gain);
    
    createWorkoutMutation.mutate(cleanData);
  };

  return (
    <div className="p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-4xl font-bold text-slate-900 mb-2">Workouts</h1>
            <p className="text-slate-600 text-lg">Log and track your training sessions</p>
          </div>
          <Button 
            onClick={() => setShowForm(!showForm)}
            className="bg-gradient-to-r from-indigo-600 to-blue-500 hover:from-indigo-700 hover:to-blue-600 shadow-lg shadow-indigo-500/30"
          >
            {showForm ? <X className="w-5 h-5 mr-2" /> : <Plus className="w-5 h-5 mr-2" />}
            {showForm ? "Cancel" : "Log Workout"}
          </Button>
        </div>

        <AnimatePresence>
          {showForm && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="mb-8"
            >
              <Card className="border-slate-200 bg-white/90 backdrop-blur-sm shadow-xl">
                <CardHeader className="border-b border-slate-100">
                  <CardTitle className="flex items-center gap-2 text-xl">
                    <Activity className="w-5 h-5 text-indigo-600" />
                    New Workout
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-6">
                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="grid md:grid-cols-2 gap-6">
                      <div className="space-y-2">
                        <Label htmlFor="activity_type">Activity Type *</Label>
                        <Select
                          value={formData.activity_type}
                          onValueChange={(value) => setFormData({ ...formData, activity_type: value })}
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="running">🏃 Running</SelectItem>
                            <SelectItem value="cycling">🚴 Cycling</SelectItem>
                            <SelectItem value="swimming">🏊 Swimming</SelectItem>
                            <SelectItem value="triathlon">🏊🚴🏃 Triathlon</SelectItem>
                            <SelectItem value="walking">🚶 Walking</SelectItem>
                            <SelectItem value="hiking">🥾 Hiking</SelectItem>
                            <SelectItem value="other">💪 Other</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="date">Date & Time *</Label>
                        <Input
                          id="date"
                          type="datetime-local"
                          value={formData.date}
                          onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                          required
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="duration">Duration (minutes) *</Label>
                        <Input
                          id="duration"
                          type="number"
                          step="0.1"
                          value={formData.duration_minutes}
                          onChange={(e) => setFormData({ ...formData, duration_minutes: e.target.value })}
                          placeholder="45"
                          required
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="distance">Distance (km)</Label>
                        <Input
                          id="distance"
                          type="number"
                          step="0.01"
                          value={formData.distance_km}
                          onChange={(e) => setFormData({ ...formData, distance_km: e.target.value })}
                          placeholder="10.5"
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="intensity">Intensity</Label>
                        <Select
                          value={formData.intensity}
                          onValueChange={(value) => setFormData({ ...formData, intensity: value })}
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="easy">Easy</SelectItem>
                            <SelectItem value="moderate">Moderate</SelectItem>
                            <SelectItem value="hard">Hard</SelectItem>
                            <SelectItem value="maximum">Maximum</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="feeling">How did you feel?</Label>
                        <Select
                          value={formData.feeling}
                          onValueChange={(value) => setFormData({ ...formData, feeling: value })}
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="great">😄 Great</SelectItem>
                            <SelectItem value="good">🙂 Good</SelectItem>
                            <SelectItem value="okay">😐 Okay</SelectItem>
                            <SelectItem value="tired">😮‍💨 Tired</SelectItem>
                            <SelectItem value="poor">😔 Poor</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="avg_hr">Avg Heart Rate (bpm)</Label>
                        <Input
                          id="avg_hr"
                          type="number"
                          value={formData.avg_heart_rate}
                          onChange={(e) => setFormData({ ...formData, avg_heart_rate: e.target.value })}
                          placeholder="145"
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="max_hr">Max Heart Rate (bpm)</Label>
                        <Input
                          id="max_hr"
                          type="number"
                          value={formData.max_heart_rate}
                          onChange={(e) => setFormData({ ...formData, max_heart_rate: e.target.value })}
                          placeholder="175"
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="calories">Calories Burned</Label>
                        <Input
                          id="calories"
                          type="number"
                          value={formData.calories}
                          onChange={(e) => setFormData({ ...formData, calories: e.target.value })}
                          placeholder="450"
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="elevation">Elevation Gain (m)</Label>
                        <Input
                          id="elevation"
                          type="number"
                          value={formData.elevation_gain}
                          onChange={(e) => setFormData({ ...formData, elevation_gain: e.target.value })}
                          placeholder="120"
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="notes">Notes</Label>
                      <Textarea
                        id="notes"
                        value={formData.notes}
                        onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                        placeholder="How was your workout? Any observations?"
                        rows={3}
                      />
                    </div>

                    <Button 
                      type="submit" 
                      className="w-full bg-gradient-to-r from-green-600 to-emerald-500 hover:from-green-700 hover:to-emerald-600 shadow-lg"
                      disabled={createWorkoutMutation.isPending}
                    >
                      <Save className="w-5 h-5 mr-2" />
                      {createWorkoutMutation.isPending ? "Saving..." : "Save Workout"}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        <RecentWorkouts workouts={workouts} isLoading={isLoading} />
      </div>
    </div>
  );
}