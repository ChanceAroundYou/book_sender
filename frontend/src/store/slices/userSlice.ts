import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { userService } from '@/services/api';
import type {
    User,
    UserListQueryParams,
    GetUserDetailParams,
    CreateUserParams,
    UpdateUserParams,
    UserSubscriptionParams,
    ApiError,
} from '@/types';

interface UserState {
    users: User[];
    totalUsers: number;
    currentUser: User | null;
    loading: boolean;
    error: string | null;
    // Specific state for user being managed by admin, if needed
    managedUser: User | null;
    // Filters and pagination for user list
    filters: Partial<UserListQueryParams>;
    pagination: { page: number; pageSize: number };
}

const initialState: UserState = {
    users: [],
    totalUsers: 0,
    currentUser: null, // This could be populated by fetchCurrentUser from authSlice
    loading: false,
    error: null,
    managedUser: null,
    filters: { limit: 50, skip: 0 },
    pagination: { page: 1, pageSize: 50 },
};

// Async Thunks
export const fetchUsers = createAsyncThunk<
    { items: User[], total: number }, // Return type: array of users and total count
    UserListQueryParams | undefined,    // Argument type
    { rejectValue: string; state: { user: UserState } } // ThunkApiConfig
>(
    'users/fetchUsers',
    async (params, { rejectWithValue, getState }) => {
        const { user } = getState();
        const queryParams: UserListQueryParams = {
            ...user.filters,
            limit: user.pagination.pageSize,
            skip: (user.pagination.page - 1) * user.pagination.pageSize,
            ...(params || {}),
        };
        try {
            const fetchedUsers = await userService.getUsers(queryParams);
            // Assuming API directly returns Array<User> and total is based on length or a header (not shown)
            // If API sends total, use that. Otherwise, length of items.
            return { items: fetchedUsers, total: fetchedUsers.length };
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to fetch users');
        }
    }
);

export const fetchUserById = createAsyncThunk<
    User,
    GetUserDetailParams,
    { rejectValue: string }
>(
    'users/fetchUserById',
    async (params, { rejectWithValue }) => {
        try {
            const user = await userService.getUserById(params);
            return user;
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to fetch user details');
        }
    }
);

export const createUserAdmin = createAsyncThunk<
    User,
    CreateUserParams,
    { rejectValue: string }
>(
    'users/createUserAdmin', // "Admin" suffix to distinguish if a user creates their own account elsewhere
    async (params, { rejectWithValue }) => {
        try {
            const newUser = await userService.createUser(params);
            return newUser;
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to create user');
        }
    }
);

export const updateUserAdmin = createAsyncThunk<
    User,
    UpdateUserParams,
    { rejectValue: string }
>(
    'users/updateUserAdmin',
    async (params, { rejectWithValue }) => {
        try {
            const updatedUser = await userService.updateUser(params);
            return updatedUser;
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to update user');
        }
    }
);

export const deleteUserAdmin = createAsyncThunk<
    { userId: number }, // Return userId for identification in reducer
    { user_id: number },
    { rejectValue: string }
>(
    'users/deleteUserAdmin',
    async (params, { rejectWithValue }) => {
        try {
            await userService.deleteUser(params);
            return { userId: params.user_id };
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to delete user');
        }
    }
);

export const addUserSubscription = createAsyncThunk<
    User, // Returns the updated user object with new subscriptions
    UserSubscriptionParams,
    { rejectValue: string }
>(
    'users/addUserSubscription',
    async (params, { rejectWithValue }) => {
        try {
            const updatedUser = await userService.addUserSubscription(params);
            return updatedUser;
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to add subscription');
        }
    }
);

export const deleteUserSubscription = createAsyncThunk<
    User, // Returns the updated user object
    { user_id: number; series: string },
    { rejectValue: string }
>(
    'users/deleteUserSubscription',
    async (params, { rejectWithValue }) => {
        try {
            const updatedUser = await userService.deleteUserSubscription(params);
            return updatedUser;
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to delete subscription');
        }
    }
);

const userSlice = createSlice({
    name: 'users',
    initialState,
    reducers: {
        setUserFilters: (state, action: PayloadAction<Partial<UserListQueryParams>>) => {
            state.filters = { ...initialState.filters, ...action.payload };
            state.pagination = { ...initialState.pagination, pageSize: state.filters.limit || initialState.pagination.pageSize };
            state.filters.skip = (state.pagination.page - 1) * (state.filters.limit || initialState.pagination.pageSize);
        },
        setUserPagination: (state, action: PayloadAction<{ page?: number; pageSize?: number }>) => {
            const newPage = action.payload.page || state.pagination.page;
            const newPageSize = action.payload.pageSize || state.pagination.pageSize;
            state.pagination = { page: newPage, pageSize: newPageSize };
            state.filters.limit = newPageSize;
            state.filters.skip = (newPage - 1) * newPageSize;
        },
        clearUserError: (state) => {
            state.error = null;
        },
        setManagedUser: (state, action: PayloadAction<User | null>) => {
            state.managedUser = action.payload;
        },
        // Potentially a reducer to update currentUser if it's managed by this slice
        // and not solely by authSlice. For example, after a subscription update.
        updateCurrentUserInList: (state, action: PayloadAction<User>) => {
            if (state.currentUser && state.currentUser.id === action.payload.id) {
                state.currentUser = action.payload;
            }
            // Also update in the users list if present
            const index = state.users.findIndex(u => u.id === action.payload.id);
            if (index !== -1) {
                state.users[index] = action.payload;
            }
        }
    },
    extraReducers: (builder) => {
        builder
            // Fetch Users
            .addCase(fetchUsers.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchUsers.fulfilled, (state, action: PayloadAction<{ items: User[], total: number }>) => {
                state.loading = false;
                state.users = action.payload.items;
                state.totalUsers = action.payload.total;
            })
            .addCase(fetchUsers.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Unknown error';
            })
            // Fetch User By Id (typically for managedUser)
            .addCase(fetchUserById.pending, (state) => {
                state.loading = true;
                state.error = null;
                state.managedUser = null;
            })
            .addCase(fetchUserById.fulfilled, (state, action: PayloadAction<User>) => {
                state.loading = false;
                state.managedUser = action.payload;
            })
            .addCase(fetchUserById.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Unknown error';
            })
            // Create User
            .addCase(createUserAdmin.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(createUserAdmin.fulfilled, (state, action: PayloadAction<User>) => {
                state.loading = false;
                state.users.unshift(action.payload); // Add to list
                state.totalUsers += 1;
            })
            .addCase(createUserAdmin.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Unknown error';
            })
            // Update User
            .addCase(updateUserAdmin.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(updateUserAdmin.fulfilled, (state, action: PayloadAction<User>) => {
                state.loading = false;
                const index = state.users.findIndex(u => u.id === action.payload.id);
                if (index !== -1) {
                    state.users[index] = action.payload;
                }
                if (state.managedUser && state.managedUser.id === action.payload.id) {
                    state.managedUser = action.payload;
                }
                // If the updated user is the current logged-in user, authSlice should handle it, 
                // or dispatch an action here to authSlice, or use a shared selector.
            })
            .addCase(updateUserAdmin.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Unknown error';
            })
            // Delete User
            .addCase(deleteUserAdmin.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(deleteUserAdmin.fulfilled, (state, action: PayloadAction<{ userId: number }>) => {
                state.loading = false;
                state.users = state.users.filter(u => u.id !== action.payload.userId);
                state.totalUsers -= 1;
            })
            .addCase(deleteUserAdmin.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Unknown error';
            })
            // Add/Delete Subscription (these update a user, potentially the currentUser)
            .addMatcher(
                (action): action is PayloadAction<User> =>
                    [addUserSubscription.fulfilled.type, deleteUserSubscription.fulfilled.type].includes(action.type),
                (state, action) => {
                    state.loading = false;
                    // Update in the list
                    const index = state.users.findIndex(u => u.id === action.payload.id);
                    if (index !== -1) {
                        state.users[index] = action.payload;
                    }
                    // Update managedUser if it's the one modified
                    if (state.managedUser && state.managedUser.id === action.payload.id) {
                        state.managedUser = action.payload;
                    }
                    // Note: currentUser updates should ideally be handled by authSlice
                    // or via a dedicated action dispatched to authSlice if this user is the logged-in user
                }
            )
            .addMatcher(
                (action): action is PayloadAction<string | undefined> =>
                    [addUserSubscription.rejected.type, deleteUserSubscription.rejected.type].includes(action.type),
                (state, action) => {
                    state.loading = false;
                    state.error = action.payload || 'Subscription update failed';
                }
            )
            .addMatcher(
                (action): action is PayloadAction =>
                    [addUserSubscription.pending.type, deleteUserSubscription.pending.type].includes(action.type),
                (state) => {
                    state.loading = true;
                    state.error = null;
                }
            );
    },
});

export const {
    setUserFilters,
    setUserPagination,
    clearUserError,
    setManagedUser,
    updateCurrentUserInList
} = userSlice.actions;

export default userSlice.reducer; 