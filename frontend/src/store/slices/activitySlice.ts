import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface Activity {
  id: string
  name: string
  activity_type: string
  start_date: string
  duration_seconds: number
  distance_meters: number
}

interface ActivityState {
  activities: Activity[]
  loading: boolean
  error: string | null
}

const initialState: ActivityState = {
  activities: [],
  loading: false,
  error: null,
}

const activitySlice = createSlice({
  name: 'activity',
  initialState,
  reducers: {
    setActivities: (state, action: PayloadAction<Activity[]>) => {
      state.activities = action.payload
      state.loading = false
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload
    },
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload
      state.loading = false
    },
  },
})

export const { setActivities, setLoading, setError } = activitySlice.actions
export default activitySlice.reducer
