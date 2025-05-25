import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Notification {
    id: string;
    type: 'success' | 'error' | 'info' | 'warning';
    message: string;
    duration?: number;
    description?: string;
}

interface Modal {
    id: string;
    type: string;
    title: string;
    visible: boolean;
    data?: any;
}

interface UiState {
    theme: 'light' | 'dark';
    language: string;
    sidebarCollapsed: boolean;
    notifications: Notification[];
    modals: Modal[];
    loading: {
        [key: string]: boolean;
    };
    breadcrumbs: {
        path: string;
        label: string;
    }[];
}

const getInitialLanguage = (): string => {
    if (typeof window !== 'undefined') {
        return localStorage.getItem('language') || 'en';
    }
    return 'en';
};

const getInitialTheme = (): 'light' | 'dark' => {
    if (typeof window !== 'undefined') {
        return (localStorage.getItem('theme') as 'light' | 'dark') || 'light';
    }
    return 'light';
};

const initialState: UiState = {
    theme: getInitialTheme(),
    language: getInitialLanguage(),
    sidebarCollapsed: false,
    notifications: [],
    modals: [],
    loading: {},
    breadcrumbs: [],
};

const uiSlice = createSlice({
    name: 'ui',
    initialState,
    reducers: {
        setTheme: (state, action: PayloadAction<'light' | 'dark'>) => {
            state.theme = action.payload;
            if (typeof window !== 'undefined') {
                localStorage.setItem('theme', action.payload);
            }
        },
        setLanguage: (state, action: PayloadAction<string>) => {
            state.language = action.payload;
            if (typeof window !== 'undefined') {
                localStorage.setItem('language', action.payload);
            }
        },
        toggleSidebar: (state) => {
            state.sidebarCollapsed = !state.sidebarCollapsed;
        },
        setSidebarCollapsed: (state, action: PayloadAction<boolean>) => {
            state.sidebarCollapsed = action.payload;
        },
        addNotification: (state, action: PayloadAction<Omit<Notification, 'id'>>) => {
            state.notifications.push({
                ...action.payload,
                id: Date.now().toString(),
            });
        },
        removeNotification: (state, action: PayloadAction<string>) => {
            state.notifications = state.notifications.filter((n) => n.id !== action.payload);
        },
        clearNotifications: (state) => {
            state.notifications = [];
        },
        showModal: (state, action: PayloadAction<Omit<Modal, 'visible'>>) => {
            const existingModalIndex = state.modals.findIndex(m => m.id === action.payload.id);
            if (existingModalIndex !== -1) {
                state.modals[existingModalIndex] = { ...action.payload, visible: true };
            } else {
                state.modals.push({ ...action.payload, visible: true });
            }
        },
        hideModal: (state, action: PayloadAction<string>) => {
            const modalIndex = state.modals.findIndex(m => m.id === action.payload);
            if (modalIndex !== -1) {
                state.modals[modalIndex].visible = false;
            }
        },
        removeModal: (state, action: PayloadAction<string>) => {
            state.modals = state.modals.filter(m => m.id !== action.payload);
        },
        setLoading: (state, action: PayloadAction<{ key: string; value: boolean }>) => {
            state.loading[action.payload.key] = action.payload.value;
        },
        setBreadcrumbs: (state, action: PayloadAction<UiState['breadcrumbs']>) => {
            state.breadcrumbs = action.payload;
        },
    },
});

export const {
    setTheme,
    setLanguage,
    toggleSidebar,
    setSidebarCollapsed,
    addNotification,
    removeNotification,
    clearNotifications,
    showModal,
    hideModal,
    removeModal,
    setLoading,
    setBreadcrumbs,
} = uiSlice.actions;

export default uiSlice.reducer; 