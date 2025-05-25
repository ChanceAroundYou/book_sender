# Frontend API Services Documentation

## Types

```typescript
// Common Types
interface PaginationParams {
    limit?: number;      // 默认 50
    skip?: number;       // 默认 0
    order_by?: string;   // 排序字段
    order_desc?: boolean;// 是否降序排序
}

// PaginatedResponse is a frontend concept if total count is derived from headers or other means.
// Backend list endpoints in api.md return Array<T>.
// interface PaginatedResponse<T> {
//     items: T[];
//     total: number;
// }

interface QueryOperator<T> {
    operator: '=' | '!=' | '>' | '<' | '>=' | '<=' | 'in' | 'not in' | 'like' | 'not like' | 'between';
    value: T | T[];
}

// User Types
interface User {
    id: number;
    email: string;
    username: string;
    created_at: string;    // ISO 8601 格式
    updated_at: string;    // ISO 8601 格式
    subscriptions: Array<{
        series: string;
        date: string;     // YYYY-MM-DD 格式
    }>;
    books: Array<{
        id: number;
        title: string;
        status: string; // Note: `status` field for book association might need more context from backend model if it's different from general book status.
    }>;
}

// Book Types
interface Book {
    id: number;
    title: string;
    author: string | null;
    cover_link: string;
    detail_link: string;
    download_link: string;
    series: string;
    file_size: number;
    file_format: string;
    file_path: string | null;
    date: string;          // YYYY-MM-DD 格式
    summary: string | null;
    downloaded_at: string | null;  // ISO 8601 格式
    created_at: string;    // ISO 8601 格式
    updated_at: string;    // ISO 8601 格式
    users: Array<{ // Added based on api.md GET /books response
        id: number;
        username: string;
        email: string;
        status: string;
    }>;
}

interface BookQueryParams extends PaginationParams {
    id?: number | QueryOperator<number>;
    title?: string | QueryOperator<string>;
    author?: string | QueryOperator<string>;
    series?: string | QueryOperator<string>;
    date?: string | QueryOperator<string>;
    summary?: string | QueryOperator<string>;
    cover_link?: string | QueryOperator<string>;
    detail_link?: string | QueryOperator<string>;
    download_link?: string | QueryOperator<string>;
    file_size?: number | QueryOperator<number>;
    file_format?: string | QueryOperator<string>;
    file_path?: string | QueryOperator<string>;
    downloaded_at?: string | QueryOperator<string>;
    created_at?: string | QueryOperator<string>;
    updated_at?: string | QueryOperator<string>;
}

interface CreateBookPayload { // Request Body for POST /api/v1/book
    title: string;
    date: string;         // YYYY-MM-DD 格式
    series: string;       // 必填，系列 (as per api.md 2.5, and implies backend creates from these params)
    author?: string;
    summary?: string;
    cover_link?: string;
    detail_link?: string;
    download_link?: string;
    file_format?: string;
    file_size?: number;
    file_path?: string;
}

// For PUT /api/v1/book, parameters are sent in the query string.
interface UpdateBookQueryParams extends Partial<CreateBookPayload> { 
    id: number; // Required query param for identifying the book
    // All other fields from CreateBookPayload are optional for update as query params.
}


// Task Types
interface Task {
    id: string;
    name: string; 
    status: 'pending' | 'started' | 'success' | 'failure' | 'retry';
    args: any[];       
    kwargs: Record<string, any>; 
    result: any;
    error: string | null;
    started_at: string | null;   
    completed_at: string | null; 
    parent_id: string | null; 
    created_at: string;
    updated_at: string;
}

interface TaskQueryParams extends PaginationParams {
    id?: string;
    name?: string;
    status?: Task['status'];
    parent_id?: string;
}

// API Error Type
interface ApiError {
    detail: string;
}

// Generic response for services that might return a message or an error object (like Crawl, Download, Distribute)
interface ServiceResponseMessageOrError {
    message?: string;
    error?: string;
}

```

## Services

### Authentication Service
```typescript
interface LoginParams {
    email: string;
    password: string;
}

interface RegisterParams { // Request body for POST /api/v1/register
    email: string;
    password: string;
    username?: string; 
}

const authService = {
    async login(params: LoginParams): Promise<{ access_token: string; token_type: "bearer" }> {
        // POST /api/v1/login
    },

    async register(params: RegisterParams): Promise<User> {
        // POST /api/v1/register
    },

    async getCurrentUser(): Promise<User> {
        // GET /api/v1/me
    },
};
```

### Book Service
```typescript
const bookService = {
    async getBooks(params?: BookQueryParams): Promise<Array<Book>> {
        // GET /api/v1/books
    },

    // GET /api/v1/books/series - Query params: series (string, required), other BookQueryParams optional
    async getSeriesBooks(series: string, params?: Omit<BookQueryParams, 'series'>): Promise<Array<Book>> {
        // GET /api/v1/books/series?series={series}
    },

    // GET /api/v1/books/all - Query params: limit (number, optional)
    async getLatestBooks(params?: { limit?: number }): Promise<Array<Book>> {
        // GET /api/v1/books/all
    },

    // GET /api/v1/book - Query with any field from BookQueryParams to find first match
    async getBook(params: Partial<BookQueryParams>): Promise<Book> { 
        // GET /api/v1/book
    },

    async createBook(payload: CreateBookPayload): Promise<Book> {
        // POST /api/v1/book (Payload is request body)
    },

    // PUT /api/v1/book - Query params: id (required), other fields from CreateBookPayload (optional)
    async updateBook(params: UpdateBookQueryParams): Promise<Book> {
        // PUT /api/v1/book (Params are query parameters)
    },

    // DELETE /api/v1/book - Query with any field from BookQueryParams to delete first match
    async deleteBook(params: Partial<BookQueryParams>): Promise<{ message: string }> { 
        // DELETE /api/v1/book (Params are query parameters)
    },
};
```

### User Service
```typescript
interface UserListQueryParams extends PaginationParams {
    id?: number | QueryOperator<number>;
    username?: string | QueryOperator<string>;
    email?: string | QueryOperator<string>;
    created_at?: string | QueryOperator<string>; // As per api.md user query params
    updated_at?: string | QueryOperator<string>; // As per api.md user query params
}

interface GetUserDetailParams {
    user_id: number; // Required query param
}

interface CreateUserParams { // Query parameters for POST /api/v1/users as per api.md 7.3 & backend code
    username: string;
    email: string;
    password: string;
}

interface UpdateUserParams { // Query parameters for PUT /api/v1/users
    user_id: number;    
    username?: string;  
    email?: string;    
    password?: string; 
}

interface UserSubscriptionParams { // Query parameters
    user_id: number; 
    series: string;  
    date?: string;   
}


const userService = {
    async getUsers(params?: UserListQueryParams): Promise<Array<User>> {
        // GET /api/v1/users
    },

    async getUserById(params: GetUserDetailParams): Promise<User> {
        // GET /api/v1/users?user_id={params.user_id}
    },

    async createUser(params: CreateUserParams): Promise<User> {
        // POST /api/v1/users (Params are query parameters)
    },

    async updateUser(params: UpdateUserParams): Promise<User> {
        // PUT /api/v1/users (Params are query parameters)
    },

    async deleteUser(params: { user_id: number }): Promise<{ message: string }> {
        // DELETE /api/v1/users?user_id={params.user_id}
    },

    async addUserSubscription(params: UserSubscriptionParams): Promise<User> {
        // PUT /api/v1/users/subscriptions (Params are query parameters)
    },

    async deleteUserSubscription(params: { user_id: number; series: string }): Promise<User> {
        // DELETE /api/v1/users/subscriptions (Params are query parameters)
    },
};
```

### Task Service
```typescript
const taskService = {
    async getTasks(params?: TaskQueryParams): Promise<Array<Task>> {
        // GET /api/v1/tasks
    },

    async getTask(taskId: string): Promise<Task> {
        // GET /api/v1/tasks/{taskId}
    },

    async deleteTask(taskId: string): Promise<{ message: string }> {
        // DELETE /api/v1/tasks/{taskId}
    },

    // GET /api/v1/tasks/status/summary - No query params as per api.md
    async getTaskStatusSummary(): Promise<Record<Task['status'], number | undefined>> {
        // GET /api/v1/tasks/status/summary
        // Response can have undefined for statuses not present, hence `number | undefined`
    },
};
```

### Crawl Service
```typescript
// Path param `series` is optional, defaults to "economist". Query param `page` is optional, defaults to 1.
interface CrawlBooksParams {
    series?: string; // Path parameter, optional
    page?: number;   // Query parameter, optional
}

// Path param `series` is optional. Other params are BookQueryParams.
interface CrawlBookParams {
    series?: string; // Path parameter, optional
    // Other query params from BookQueryParams
    [key: string]: any; // To allow for other book query params
}

const crawlService = {
    async crawlBooks(params?: CrawlBooksParams): Promise<ServiceResponseMessageOrError> {
        // POST /api/v1/crawl/books/{series}?page={page} (series in path, page in query)
    },

    async crawlBook(params?: CrawlBookParams): Promise<ServiceResponseMessageOrError> {
        // POST /api/v1/crawl/book/{series} (series in path, others in query)
    },
};
```

### Download Service
```typescript
const downloadService = {
    // POST /api/v1/download/books - Query params: BookQueryParams (all optional)
    async downloadBooks(params?: Partial<BookQueryParams>): Promise<ServiceResponseMessageOrError> {
        // POST /api/v1/download/books (Params are query parameters)
    },

    // POST /api/v1/download/book - Query params: BookQueryParams (all optional)
    async downloadBook(params: Partial<BookQueryParams>): Promise<ServiceResponseMessageOrError> {
        // POST /api/v1/download/book (Params are query parameters)
    },
};
```

### Distribute Service
```typescript
// POST /api/v1/distribute/books - Query params: email (required), BookQueryParams (all optional)
interface DistributeBooksParams extends Partial<BookQueryParams> {
    email: string; // Query parameter
}

// POST /api/v1/distribute/book - Query params: email (required), BookQueryParams (all optional)
interface DistributeBookParams extends Partial<BookQueryParams> {
    email: string; // Query parameter
}

const distributeService = {
    async distributeBooks(params: DistributeBooksParams): Promise<ServiceResponseMessageOrError> {
        // POST /api/v1/distribute/books (Params are query parameters)
    },

    async distributeBook(params: DistributeBookParams): Promise<ServiceResponseMessageOrError> {
        // POST /api/v1/distribute/book (Params are query parameters)
    },
};
```

## Error Handling

所有接口在请求失败时会抛出 `ApiError`。错误响应格式：
```typescript
{
    detail: string;  // 错误信息
}
```

示例用法：
```typescript
try {
    const books = await bookService.getBooks({ limit: 50, skip: 0 });
    // 处理成功响应
} catch (error) {
    if (typeof error === 'object' && error !== null && 'detail' in error) { 
        const apiError = error as ApiError;
        console.error(apiError.detail);
    } else {
        console.error('发生未知错误');
    }
}
```

## Authentication

除了注册和登录接口外，所有接口都需要在请求头中携带 Bearer Token：
```typescript
const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
};
```

For file uploads (e.g., book covers), use `multipart/form-data` content type. 