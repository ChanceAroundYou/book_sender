import { configureStore } from '@reduxjs/toolkit';
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';
import authReducer from './slices/authSlice';
import bookReducer from './slices/bookSlice';
// import seriesReducer from './slices/seriesSlice'; // Deprecated
import taskReducer from './slices/taskSlice';
import userReducer from './slices/userSlice';
import downloadReducer from './slices/downloadSlice';
// import adminReducer from './slices/adminSlice'; // Deprecated
import uiReducer from './slices/uiSlice';
import statsReducer from './slices/statsSlice';

export const store = configureStore({
    reducer: {
        auth: authReducer,
        book: bookReducer,
        // series: seriesReducer, // Deprecated
        task: taskReducer,
        user: userReducer,
        download: downloadReducer,
        // admin: adminReducer, // Deprecated
        ui: uiReducer,
        stats: statsReducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: {
                // Ignore these action types
                ignoredActions: ['persist/PERSIST'], // Example, keep if you use redux-persist
                // Ignore these field paths in all actions
                ignoredActionPaths: ['payload.file', 'meta.arg.payload.file'], // More generic for file uploads if needed
                // Ignore these paths in the state
                // ignoredPaths: ['admin.books.cover', 'admin.series.cover'], // Paths from deprecated admin slice removed
                // Add new paths here if other slices introduce non-serializable data e.g. File objects
            },
        }),
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Export a hook that can be reused to resolve types
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector; 