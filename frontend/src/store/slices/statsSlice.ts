import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { utilService } from '@/services/api';

interface StatsState {
    totalBooks: number;
    totalUsers: number;
    loading: boolean;
    error: string | null;
}

const initialState: StatsState = {
    totalBooks: 0,
    totalUsers: 0,
    loading: false,
    error: null,
};

export const fetchStats = createAsyncThunk(
    'stats/fetchStats',
    async () => {
        try {
            const [totalBooks, totalUsers] = await Promise.all([
                utilService.getTotalBooks(),
                utilService.getTotalUsers(),
            ]);
            return { totalBooks, totalUsers };
        } catch (error) {
            throw error;
        }
    }
);

const statsSlice = createSlice({
    name: 'stats',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(fetchStats.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchStats.fulfilled, (state, action) => {
                state.loading = false;
                state.totalBooks = action.payload.totalBooks;
                state.totalUsers = action.payload.totalUsers;
            })
            .addCase(fetchStats.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to fetch stats';
            });
    },
});

export default statsSlice.reducer; 