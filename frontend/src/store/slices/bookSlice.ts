import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { bookService, distributeService } from '@/services/api';
import type {
    Book,
    BookQueryParams,
    CreateBookPayload,
    UpdateBookQueryParams,
    ApiError,
    DistributeBookParams,
    ServiceResponseMessageOrError,
    DistributeSeriesParams,
} from '@/types';

interface BookState {
    items: Book[];
    total: number; // For pagination, if available from API or calculated
    loading: boolean;
    error: string | null;
    currentBook: Book | null; // For single book view
    // Filters and pagination can be part of this slice or a separate UI slice
    filters: Partial<BookQueryParams>;
    pagination: { page: number; pageSize: number };
}

const initialState: BookState = {
    items: [],
    total: 0,
    loading: false,
    error: null,
    currentBook: null,
    filters: { limit: 50, skip: 0, order_by: 'date', order_desc: true },
    pagination: { page: 1, pageSize: 50 }, // Example, adjust as needed
};

// Async Thunks
export const fetchBooks = createAsyncThunk<
    { items: Book[], total: number }, // Return type
    BookQueryParams | undefined, // Argument type
    { rejectValue: string; state: { book: BookState } } // ThunkApiConfig
>(
    'books/fetchBooks',
    async (params, { rejectWithValue, getState }) => {
        const { book } = getState();
        // Use provided params, or fallback to params from state including pagination
        const queryParams: BookQueryParams = {
            ...book.filters,
            limit: book.pagination.pageSize,
            skip: (book.pagination.page - 1) * book.pagination.pageSize,
            ...(params || {}), // Override with explicitly passed params
        };
        try {
            const books = await bookService.getBooks(queryParams);
            return { items: books, total: books.length }; // Adjust if API sends total
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to fetch books');
        }
    }
);

export const fetchSeriesBooks = createAsyncThunk<
    { items: Book[], total: number },
    { series: string; params?: Omit<BookQueryParams, 'series'> },
    { rejectValue: string }
>(
    'books/fetchSeriesBooks',
    async (args, { rejectWithValue }) => {
        try {
            const books = await bookService.getSeriesBooks(args.series, args.params);
            return { items: books, total: books.length };
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to fetch series books');
        }
    }
);

export const fetchLatestBooks = createAsyncThunk<
    { items: Book[], total: number },
    Partial<BookQueryParams> | undefined,
    { rejectValue: string; state: { book: BookState } }
>(
    'books/fetchLatestBooks',
    async (params, { rejectWithValue, getState }) => {
        // Use provided params, or fallback to params from state including pagination
        const { book } = getState();
        const queryParams: BookQueryParams = {
            ...book.filters,
            limit: book.pagination.pageSize,
            skip: (book.pagination.page - 1) * book.pagination.pageSize,
            ...(params || {}), // Override with explicitly passed params
        };
        try {
            const books = await bookService.getLatestBooks(queryParams);
            return { items: books, total: books.length };
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to fetch latest books');
        }
    }
);

export const fetchBookById = createAsyncThunk<
    Book,
    Partial<BookQueryParams>,
    { rejectValue: string }
>(
    'books/fetchBookById',
    async (params, { rejectWithValue }) => {
        try {
            const book = await bookService.getBook(params);
            return book;
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to fetch book');
        }
    }
);

export const createNewBook = createAsyncThunk<
    Book,
    CreateBookPayload,
    { rejectValue: string }
>(
    'books/createBook',
    async (payload, { rejectWithValue }) => {
        try {
            const newBook = await bookService.createBook(payload);
            return newBook;
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to create book');
        }
    }
);

export const updateExistingBook = createAsyncThunk<
    Book,
    UpdateBookQueryParams,
    { rejectValue: string }
>(
    'books/updateBook',
    async (params, { rejectWithValue }) => {
        try {
            const updatedBook = await bookService.updateBook(params);
            return updatedBook;
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to update book');
        }
    }
);

export const removeBook = createAsyncThunk<
    Partial<BookQueryParams>, // Return the params for identification
    Partial<BookQueryParams>,
    { rejectValue: string }
>(
    'books/deleteBook',
    async (params, { rejectWithValue }) => {
        try {
            await bookService.deleteBook(params);
            return params;
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to delete book');
        }
    }
);

export const distributeBookAction = createAsyncThunk<
    ServiceResponseMessageOrError, // Return type from distributeService
    DistributeBookParams,          // Argument type
    { rejectValue: string }        // ThunkApiConfig
>(
    'books/distributeBook',
    async (params, { rejectWithValue }) => {
        try {
            const response = await distributeService.distributeBook(params);
            if (response.error) {
                return rejectWithValue(response.error);
            }
            return response;
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to distribute book');
        }
    }
);

export const distributeSeriesAction = createAsyncThunk<
    ServiceResponseMessageOrError, // Return type
    DistributeSeriesParams,        // Argument type
    { rejectValue: string }        // ThunkApiConfig
>(
    'books/distributeSeries',
    async (params, { rejectWithValue }) => {
        try {
            const response = await distributeService.distributeSeries(params);
            if (response.error) {
                return rejectWithValue(response.error);
            }
            return response;
        } catch (error) {
            const apiError = error as ApiError;
            return rejectWithValue(apiError.detail || 'Failed to distribute series');
        }
    }
);

const bookSlice = createSlice({
    name: 'books',
    initialState,
    reducers: {
        setBookFilters: (state, action: PayloadAction<Partial<BookQueryParams>>) => {
            state.filters = { ...initialState.filters, ...action.payload }; // Reset to initial + new, to clear old ones
            state.pagination = { ...initialState.pagination, pageSize: state.filters.limit || initialState.pagination.pageSize };
            state.filters.skip = (state.pagination.page - 1) * (state.filters.limit || initialState.pagination.pageSize);
        },
        setBookPagination: (state, action: PayloadAction<{ page?: number; pageSize?: number }>) => {
            const newPage = action.payload.page || state.pagination.page;
            const newPageSize = action.payload.pageSize || state.pagination.pageSize;
            state.pagination = { page: newPage, pageSize: newPageSize };
            state.filters.limit = newPageSize;
            state.filters.skip = (newPage - 1) * newPageSize;
        },
        clearBookError: (state) => {
            state.error = null;
        },
        setCurrentBookAction: (state, action: PayloadAction<Book | null>) => {
            state.currentBook = action.payload;
        }
    },
    extraReducers: (builder) => {
        builder
            // fetchBooks
            .addCase(fetchBooks.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchBooks.fulfilled, (state, action: PayloadAction<{ items: Book[], total: number }>) => {
                state.loading = false;
                state.items = action.payload.items;
                state.total = action.payload.total;
            })
            .addCase(fetchBooks.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Failed to fetch books';
            })
            // fetchSeriesBooks
            .addCase(fetchSeriesBooks.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchSeriesBooks.fulfilled, (state, action: PayloadAction<{ items: Book[], total: number }>) => {
                state.loading = false;
                state.items = action.payload.items; // Assuming these replace current items, adjust if appending
                state.total = action.payload.total;
            })
            .addCase(fetchSeriesBooks.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Failed to fetch series books';
            })
            // fetchLatestBooks
            .addCase(fetchLatestBooks.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchLatestBooks.fulfilled, (state, action: PayloadAction<{ items: Book[], total: number }>) => {
                state.loading = false;
                state.items = action.payload.items; // Assuming these replace current items
                state.total = action.payload.total;
            })
            .addCase(fetchLatestBooks.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Failed to fetch latest books';
            })
            // fetchBookById
            .addCase(fetchBookById.pending, (state) => {
                state.loading = true;
                state.error = null;
                state.currentBook = null;
            })
            .addCase(fetchBookById.fulfilled, (state, action: PayloadAction<Book>) => {
                state.loading = false;
                state.currentBook = action.payload;
            })
            .addCase(fetchBookById.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Failed to fetch book';
            })
            // createNewBook
            .addCase(createNewBook.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(createNewBook.fulfilled, (state, action: PayloadAction<Book>) => {
                state.loading = false;
                state.items.unshift(action.payload);
                state.total += 1;
            })
            .addCase(createNewBook.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Failed to create book';
            })
            // updateExistingBook
            .addCase(updateExistingBook.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(updateExistingBook.fulfilled, (state, action: PayloadAction<Book>) => {
                state.loading = false;
                const index = state.items.findIndex(book => book.id === action.payload.id);
                if (index !== -1) {
                    state.items[index] = action.payload;
                }
                if (state.currentBook && state.currentBook.id === action.payload.id) {
                    state.currentBook = action.payload;
                }
            })
            .addCase(updateExistingBook.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Failed to update book';
            })
            // removeBook
            .addCase(removeBook.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(removeBook.fulfilled, (state, action: PayloadAction<Partial<BookQueryParams>>) => {
                state.loading = false;
                if (action.payload.id) {
                    state.items = state.items.filter(book => book.id !== action.payload.id);
                    state.total -= 1;
                }
            })
            .addCase(removeBook.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Failed to delete book';
            })
            // distributeBookAction
            .addCase(distributeBookAction.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(distributeBookAction.fulfilled, (state, action: PayloadAction<ServiceResponseMessageOrError>) => {
                state.loading = false;
            })
            .addCase(distributeBookAction.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Failed to distribute book';
            })
            // distributeSeriesAction
            .addCase(distributeSeriesAction.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(distributeSeriesAction.fulfilled, (state, action: PayloadAction<ServiceResponseMessageOrError>) => {
                state.loading = false;
            })
            .addCase(distributeSeriesAction.rejected, (state, action: PayloadAction<string | undefined>) => {
                state.loading = false;
                state.error = action.payload || 'Failed to distribute series';
            });
    },
});

export const { setBookFilters, setBookPagination, clearBookError, setCurrentBookAction } = bookSlice.actions;
export default bookSlice.reducer; 