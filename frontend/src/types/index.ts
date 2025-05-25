// Common Types
export interface PaginationParams {
    limit?: number;      // 默认 50
    skip?: number;       // 默认 0
    order_by?: string;   // 排序字段
    order_desc?: boolean;// 是否降序排序
}

export interface QueryOperator<T> {
    operator: '=' | '!=' | '>' | '<' | '>=' | '<=' | 'in' | 'not in' | 'like' | 'not like' | 'between';
    value: T | T[];
}

export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    page: number;
    pageSize: number;
}

// Auth Types
export interface User {
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
        status: string;
        cover_link: string;
    }>;
}

export interface UserListQueryParams extends PaginationParams {
    id?: number | QueryOperator<number>;
    username?: string | QueryOperator<string>;
    email?: string | QueryOperator<string>;
    created_at?: string | QueryOperator<string>;
    updated_at?: string | QueryOperator<string>;
}

export interface GetUserDetailParams {
    user_id: number;
}

export interface CreateUserParams { // Query parameters for POST /api/v1/users
    username: string;
    email: string;
    password: string;
}

export interface UpdateUserParams { // Query parameters for PUT /api/v1/users
    user_id: number;
    username?: string;
    email?: string;
    password?: string;
}

export interface UserSubscriptionParams { // Query parameters
    user_id: number;
    series: string;
    date?: string;
}

// Book Types
export interface Book {
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
    users: Array<{
        id: number;
        username: string;
        email: string;
        status: string;
    }>;
}

export interface BookQueryParams extends PaginationParams {
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
    file_format?: string;
    file_path?: string | QueryOperator<string>;
    downloaded_at?: string | QueryOperator<string>;
    created_at?: string | QueryOperator<string>;
    updated_at?: string | QueryOperator<string>;
}

export interface CreateBookPayload { // Request Body for POST /api/v1/book
    title: string;
    date: string;
    series: string;
    author?: string;
    summary?: string;
    cover_link?: string;
    detail_link?: string;
    download_link?: string;
    file_format?: string;
    file_size?: number;
    file_path?: string;
}

export interface UpdateBookQueryParams extends Partial<CreateBookPayload> { // Query parameters for PUT /api/v1/book
    id: number;
}

// Series Types
export interface Series {
    id: string;
    title: string;
    description: string;
    cover: string;
    frequency: string;
    createdAt: string;
    updatedAt: string;
}

export interface SeriesQueryParams extends PaginationParams {
    search?: string;
}

// Task Types
export interface Task {
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

export interface TaskQueryParams extends PaginationParams {
    id?: string;
    name?: string;
    status?: Task['status'];
    parent_id?: string;
}

// Subscription Types
export interface Subscription {
    id: string;
    userId: string;
    seriesId: string;
    email: string;
    active: boolean;
    createdAt: string;
    updatedAt: string;
}

// API Error Type
export interface ApiError {
    detail: string;
}

export interface ServiceResponseMessageOrError {
    message?: string;
    error?: string;
}

// Crawl Service Parameter Types
export interface CrawlBooksParams {
    series?: string;
    page?: number;
}

export interface CrawlBookParams {
    series?: string;
    [key: string]: any; // Allows for other BookQueryParams
}

// Distribute Service Parameter Types
export interface DistributeBooksParams extends Partial<BookQueryParams> {
    email: string;
}

export interface DistributeBookParams extends Partial<BookQueryParams> {
    email: string;
}

// New type for distributing a series
export interface DistributeSeriesParams {
    series: string;
    email: string;
    // Add other relevant parameters if your backend expects them
}

// Auth Service Types (Request Payloads)
export interface LoginParams {
    email: string;
    password: string;
}

export interface RegisterParams {
    email: string;
    password: string;
    username?: string;
} 