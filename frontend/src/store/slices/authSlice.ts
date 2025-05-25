import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { authService } from '@/services/api';
import type { User, LoginParams, RegisterParams, ApiError } from '@/types';

interface AuthState {
    user: User | null;
    token: string | null;
    loading: boolean;
    error: string | null;
}

const initialState: AuthState = {
    user: null,
    token: localStorage.getItem('token'), // Initialize token from localStorage
    loading: false,
    error: null,
};

// Async Thunks
export const loginUser = createAsyncThunk(
    'auth/login',
    async (params: LoginParams, { rejectWithValue }) => {
        try {
            const data = await authService.login(params);
            localStorage.setItem('token', data.access_token);
            const user = await authService.getCurrentUser();
            return { token: data.access_token, user };
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Login failed');
        }
    }
);

export const registerUser = createAsyncThunk(
    'auth/register',
    async (params: RegisterParams, { rejectWithValue }) => {
        try {
            // Assuming register does not auto-login, so no token is returned/stored here.
            // If it does auto-login and returns a token, this needs adjustment like loginUser.
            const user = await authService.register(params);
            return user; // Or { user, token } if backend returns token
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Registration failed');
        }
    }
);

export const fetchCurrentUser = createAsyncThunk(
    'auth/fetchCurrentUser',
    async (_, { rejectWithValue, getState }) => {
        const { auth } = getState() as { auth: AuthState };
        if (!auth.token) {
            return rejectWithValue('No token found');
        }
        try {
            const user = await authService.getCurrentUser();
            return user;
        } catch (error) {
            localStorage.removeItem('token'); // Token might be invalid
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to fetch user');
        }
    }
);

export const logoutUser = createAsyncThunk(
    'auth/logout',
    async () => {
        localStorage.removeItem('token');
        // Potentially call a backend logout endpoint if it exists
        // await authService.logout(); 
    }
);

export const forgotPasswordThunk = createAsyncThunk<
    { message: string }, // Success return type
    string, // Argument type (email)
    { rejectValue: string } // ThunkApiConfig
>(
    'auth/forgotPassword',
    async (email, { rejectWithValue }) => {
        try {
            const response = await authService.forgotPassword(email);
            return response; // Contains { message: string }
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to send password reset email.');
        }
    }
);

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setUser: (state, action: PayloadAction<User | null>) => {
            state.user = action.payload;
        },
        setToken: (state, action: PayloadAction<string | null>) => {
            state.token = action.payload;
            if (action.payload) {
                localStorage.setItem('token', action.payload);
            } else {
                localStorage.removeItem('token');
            }
        },
        clearAuthError: (state) => {
            state.error = null;
        }
    },
    extraReducers: (builder) => {
        builder
            // Login
            .addCase(loginUser.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(loginUser.fulfilled, (state, action) => {
                state.loading = false;
                state.user = action.payload.user;
                state.token = action.payload.token;
            })
            .addCase(loginUser.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
                state.user = null;
                state.token = null;
            })
            // Register
            .addCase(registerUser.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(registerUser.fulfilled, (state, action: PayloadAction<User>) => {
                state.loading = false;
                // User is registered but not logged in by default in this setup
                // To auto-login, dispatch loginUser or modify registerUser thunk
                state.user = action.payload; // Store registered user details if needed, or null
            })
            .addCase(registerUser.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            })
            // Fetch Current User
            .addCase(fetchCurrentUser.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchCurrentUser.fulfilled, (state, action: PayloadAction<User>) => {
                state.loading = false;
                state.user = action.payload;
            })
            .addCase(fetchCurrentUser.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
                state.user = null;
                state.token = null; // Also clear token as it might be invalid
            })
            // Logout
            .addCase(logoutUser.fulfilled, (state) => {
                state.user = null;
                state.token = null;
                state.loading = false;
                state.error = null;
            })
            // Forgot Password
            .addCase(forgotPasswordThunk.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(forgotPasswordThunk.fulfilled, (state) => {
                state.loading = false;
                // The message can be used in the component for notification
                // No direct state change here other than loading/error
            })
            .addCase(forgotPasswordThunk.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            });
    },
});

export const { setUser, setToken, clearAuthError } = authSlice.actions;
export default authSlice.reducer; 