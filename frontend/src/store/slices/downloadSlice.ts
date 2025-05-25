import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { downloadService } from '@/services/api';
import type { ApiError, ServiceResponseMessageOrError } from '@/types';

interface DownloadBookParams {
    id: number;
    // Potentially other params like format preference if API supports
}

interface DownloadState {
    loading: {
        [bookId: string]: boolean; // Track loading per book ID
    };
    error: string | null;
    // Store messages or status per download if needed
    // downloadStatus: { [bookId: string]: ServiceResponseMessageOrError } 
}

const initialState: DownloadState = {
    loading: {},
    error: null,
    // downloadStatus: {}
};

export const triggerBookDownload = createAsyncThunk<
    ServiceResponseMessageOrError, // Return type
    DownloadBookParams,            // Argument type { id: number }
    { rejectValue: string }       // ThunkApiConfig
>(
    'download/triggerBookDownload',
    async (params, { rejectWithValue }) => {
        try {
            // Assuming downloadService.downloadBook takes {id} and initiates download,
            // returning a message or error.
            const response = await downloadService.downloadBook({ id: params.id });
            if (response.error) {
                return rejectWithValue(response.error);
            }
            return response; // { message: string } or { error: string }
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to start download.');
        }
    }
);

const downloadSlice = createSlice({
    name: 'download',
    initialState,
    reducers: {
        clearDownloadError: (state) => {
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(triggerBookDownload.pending, (state, action) => {
                const bookId = action.meta.arg.id;
                state.loading[bookId] = true;
                state.error = null;
            })
            .addCase(triggerBookDownload.fulfilled, (state, action: PayloadAction<ServiceResponseMessageOrError, string, { arg: DownloadBookParams }>) => {
                const bookId = action.meta.arg.id;
                state.loading[bookId] = false;
                // Message handling will likely be in the component via notifications
                // Can store action.payload in state.downloadStatus[bookId] if needed for UI feedback
            })
            .addCase(triggerBookDownload.rejected, (state, action: PayloadAction<string | undefined, string, { arg: DownloadBookParams }>) => {
                const bookId = action.meta.arg.id;
                state.loading[bookId] = false;
                state.error = action.payload || 'Download failed.';
            });
    },
});

export const { clearDownloadError } = downloadSlice.actions;
export default downloadSlice.reducer; 