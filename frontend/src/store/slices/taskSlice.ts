import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { taskService } from '@/services/api';
import type { Task, TaskQueryParams, ApiError } from '@/types';

interface TaskState {
    tasks: Task[];
    totalTasks: number;
    currentTask: Task | null;
    statusSummary: Record<Task['status'], number | undefined> | null;
    loading: boolean;
    error: string | null;
    filters: Partial<TaskQueryParams>;
    pagination: { page: number; pageSize: number };
}

const initialState: TaskState = {
    tasks: [],
    totalTasks: 0,
    currentTask: null,
    statusSummary: null,
    loading: false,
    error: null,
    filters: { limit: 50, skip: 0 },
    pagination: { page: 1, pageSize: 50 },
};

// Async Thunks
export const fetchTasks = createAsyncThunk<
    { items: Task[], total: number },
    TaskQueryParams | undefined,
    { rejectValue: string; state: { task: TaskState } }
>(
    'tasks/fetchTasks',
    async (params, { rejectWithValue, getState }) => {
        const { task } = getState();
        const queryParams: TaskQueryParams = {
            ...task.filters,
            limit: task.pagination.pageSize,
            skip: (task.pagination.page - 1) * task.pagination.pageSize,
            ...(params || {}),
        };
        try {
            const fetchedTasks = await taskService.getTasks(queryParams);
            return { items: fetchedTasks, total: fetchedTasks.length }; // Adjust if API provides total
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to fetch tasks');
        }
    }
);

export const fetchTaskById = createAsyncThunk<
    Task,
    string, // taskId
    { rejectValue: string }
>(
    'tasks/fetchTaskById',
    async (taskId, { rejectWithValue }) => {
        try {
            const task = await taskService.getTask(taskId);
            return task;
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to fetch task details');
        }
    }
);

export const deleteTaskAdmin = createAsyncThunk<
    { taskId: string }, // Return taskId for identification
    string, // taskId
    { rejectValue: string }
>(
    'tasks/deleteTaskAdmin',
    async (taskId, { rejectWithValue }) => {
        try {
            await taskService.deleteTask(taskId);
            return { taskId };
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to delete task');
        }
    }
);

export const fetchTaskStatusSummary = createAsyncThunk<
    Record<Task['status'], number | undefined>,
    void, // No arguments
    { rejectValue: string }
>(
    'tasks/fetchTaskStatusSummary',
    async (_, { rejectWithValue }) => {
        try {
            const summary = await taskService.getTaskStatusSummary();
            return summary;
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to fetch task status summary');
        }
    }
);

const taskSlice = createSlice({
    name: 'tasks',
    initialState,
    reducers: {
        setTaskFilters: (state, action: PayloadAction<Partial<TaskQueryParams>>) => {
            state.filters = { ...initialState.filters, ...action.payload };
            state.pagination = { ...initialState.pagination, pageSize: state.filters.limit || initialState.pagination.pageSize };
            state.filters.skip = (state.pagination.page - 1) * (state.filters.limit || initialState.pagination.pageSize);
        },
        setTaskPagination: (state, action: PayloadAction<{ page?: number; pageSize?: number }>) => {
            const newPage = action.payload.page || state.pagination.page;
            const newPageSize = action.payload.pageSize || state.pagination.pageSize;
            state.pagination = { page: newPage, pageSize: newPageSize };
            state.filters.limit = newPageSize;
            state.filters.skip = (newPage - 1) * newPageSize;
        },
        clearTaskError: (state) => {
            state.error = null;
        },
        setCurrentTaskAction: (state, action: PayloadAction<Task | null>) => {
            state.currentTask = action.payload;
        }
    },
    extraReducers: (builder) => {
        builder
            // Fetch Tasks
            .addCase(fetchTasks.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchTasks.fulfilled, (state, action: PayloadAction<{ items: Task[], total: number }>) => {
                state.loading = false;
                state.tasks = action.payload.items;
                state.totalTasks = action.payload.total;
            })
            .addCase(fetchTasks.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Unknown error';
            })
            // Fetch Task By Id
            .addCase(fetchTaskById.pending, (state) => {
                state.loading = true;
                state.error = null;
                state.currentTask = null;
            })
            .addCase(fetchTaskById.fulfilled, (state, action: PayloadAction<Task>) => {
                state.loading = false;
                state.currentTask = action.payload;
            })
            .addCase(fetchTaskById.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Unknown error';
            })
            // Delete Task
            .addCase(deleteTaskAdmin.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(deleteTaskAdmin.fulfilled, (state, action: PayloadAction<{ taskId: string }>) => {
                state.loading = false;
                state.tasks = state.tasks.filter(t => t.id !== action.payload.taskId);
                state.totalTasks -= 1;
                if (state.currentTask && state.currentTask.id === action.payload.taskId) {
                    state.currentTask = null;
                }
            })
            .addCase(deleteTaskAdmin.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Unknown error';
            })
            // Fetch Task Status Summary
            .addCase(fetchTaskStatusSummary.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchTaskStatusSummary.fulfilled, (state, action: PayloadAction<Record<Task['status'], number | undefined>>) => {
                state.loading = false;
                state.statusSummary = action.payload;
            })
            .addCase(fetchTaskStatusSummary.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Unknown error';
            });
    },
});

export const {
    setTaskFilters,
    setTaskPagination,
    clearTaskError,
    setCurrentTaskAction
} = taskSlice.actions;

export default taskSlice.reducer; 