# Book Sender API 文档

## 通用说明

### 认证
除了注册和登录接口外，所有接口都需要在请求头中携带 Bearer Token：
```
Authorization: Bearer <access_token>
```

### 响应格式
所有接口返回 JSON 格式数据。错误响应格式：
```json
{
  "detail": "错误信息"
}
```

### 通用查询参数
大多数列表接口支持以下查询参数：
- `limit`: number, 可选，默认 50，每页记录数
- `skip`: number, 可选，默认 0，跳过记录数
- `order_by`: string, 可选，排序字段
- `order_desc`: boolean, 可选，是否降序排序

## 1. 认证相关 API

### 1.1 用户注册
- **接口**: `POST /api/v1/register`
- **描述**: 注册新用户
- **请求体**:
  ```typescript
  {
    email: string;      // 必填，邮箱地址
    password: string;   // 必填，密码（至少6个字符）
    username?: string;  // 可选，用户名（不提供则自动生成）
  }
  ```
- **响应**:
  ```typescript
  {
    id: number;
    email: string;
    username: string;
    created_at: string;  // ISO 8601 格式
    updated_at: string;  // ISO 8601 格式
    subscriptions: Array<{
      series: string;
      date: string;     // YYYY-MM-DD 格式
    }>;
    books: Array<{
      id: number;
      title: string;
      status: string;
    }>;
  }
  ```

### 1.2 用户登录
- **接口**: `POST /api/v1/login`
- **描述**: 用户登录获取令牌
- **请求体**:
  ```typescript
  {
    email: string;     // 必填，邮箱地址
    password: string;  // 必填，密码
  }
  ```
- **响应**:
  ```typescript
  {
    access_token: string;
    token_type: "bearer";
  }
  ```

### 1.3 获取当前用户信息
- **接口**: `GET /api/v1/me`
- **描述**: 获取当前登录用户信息
- **认证**: 需要 Bearer Token
- **响应**: 同注册接口响应

## 2. 图书管理 API

### 查询参数说明
所有图书相关的 GET 接口都支持以下查询参数格式：
```typescript
{
  field_name: string | number | boolean;  // 直接值匹配
  // 或
  field_name: {
    operator: string;  // 操作符
    value: any;       // 查询值
  }
}
```

支持的操作符（operator）：
- `=`: 等于（默认）
- `!=`: 不等于
- `>`: 大于
- `<`: 小于
- `>=`: 大于等于
- `<=`: 小于等于
- `in`: 在数组中
- `not in`: 不在数组中
- `like`: 模糊匹配（包含）
- `not like`: 模糊不匹配（不包含）
- `between`: 区间查询（需要提供[min, max]数组）

### 2.1 获取图书列表
- **接口**: `GET /api/v1/books`
- **描述**: 获取图书列表
- **认证**: 需要 Bearer Token
- **查询参数**:
  ```typescript
  {
    // 通用查询参数
    limit?: number;      // 默认 50
    skip?: number;       // 默认 0
    order_by?: string;   // 排序字段，默认 "id"
    order_desc?: boolean;// 是否降序，默认 true

    // 图书字段查询参数（所有字段都是可选的）
    id?: number | { operator: string; value: number };
    title?: string | { operator: string; value: string };
    author?: string | { operator: string; value: string };
    series?: string | { operator: string; value: string };
    date?: string | { operator: string; value: string };  // YYYY-MM-DD 格式
    summary?: string | { operator: string; value: string };
    cover_link?: string | { operator: string; value: string };
    detail_link?: string | { operator: string; value: string };
    download_link?: string | { operator: string; value: string };
    file_size?: number | { operator: string; value: number };
    file_format?: string | { operator: string; value: string };
    file_path?: string | { operator: string; value: string };
    downloaded_at?: string | { operator: string; value: string };
    created_at?: string | { operator: string; value: string };
    updated_at?: string | { operator: string; value: string };
  }
  ```
- **响应**:
  ```typescript
  Array<{
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
  }>
  ```

### 2.2 获取系列图书
- **接口**: `GET /api/v1/books/series`
- **描述**: 获取指定系列的所有图书
- **认证**: 需要 Bearer Token
- **查询参数**:
  ```typescript
  {
    series: string;  // 必填，图书系列
    // 其他参数同获取图书列表
  }
  ```
- **响应**: 同获取图书列表

### 2.3 获取所有系列最新图书
- **接口**: `GET /api/v1/books/all`
- **描述**: 获取所有图书，每个系列返回最新一本，OTHER 系列显示全部
- **认证**: 需要 Bearer Token
- **查询参数**:
  ```typescript
  {
    limit?: number;  // 默认 50，用于限制 OTHER 系列的返回数量
  }
  ```
- **响应**: 同获取图书列表

### 2.4 获取单本图书
- **接口**: `GET /api/v1/book`
- **描述**: 获取单本图书详情
- **认证**: 需要 Bearer Token
- **查询参数**: 同获取图书列表，使用任意字段进行查询，返回匹配的第一本书
- **响应**: 同图书列表中的单个图书对象
- **错误**: 404 - Book not found

### 2.5 创建图书
- **接口**: `POST /api/v1/book`
- **描述**: 创建新图书
- **认证**: 需要 Bearer Token
- **请求体**:
  ```typescript
  {
    title: string;         // 必填，书籍标题
    date: string;         // 必填，YYYY-MM-DD 格式
    series?: string;       // 可选，系列
    author?: string;      // 可选，作者
    summary?: string;     // 可选，简介
    cover_link?: string;  // 可选，封面链接
    detail_link?: string; // 可选，详情链接
    download_link?: string;// 可选，下载链接
    file_format?: string; // 可选，文件格式 (pdf/epub/mobi)
    file_size?: number;   // 可选，文件大小
    file_path?: string;   // 可选，文件路径
  }
  ```
- **响应**: 同图书列表中的单个图书对象

### 2.6 更新图书
- **接口**: `PUT /api/v1/book`
- **描述**: 更新图书信息
- **认证**: 需要 Bearer Token
- **查询参数**:
  ```typescript
  {
    id: number;  // 必填，图书ID
    // 其他字段同创建图书，都是可选的
  }
  ```
- **响应**: 同图书列表中的单个图书对象
- **错误**: 
  - 400 - Book ID is required
  - 404 - Book not found

### 2.7 删除图书
- **接口**: `DELETE /api/v1/book`
- **描述**: 删除图书
- **认证**: 需要 Bearer Token
- **查询参数**: 同获取图书列表，使用任意字段进行查询，删除匹配的第一本书
- **响应**:
  ```typescript
  {
    message: string;  // 删除成功消息
  }
  ```
- **错误**: 404 - Book not found

## 3. 爬虫 API

### 3.1 爬取图书列表
- **接口**: `POST /api/v1/crawl/books/{series}`
- **描述**: 开始爬取指定系列的图书列表
- **认证**: 需要 Bearer Token
- **路径参数**:
  - `series`: string, 可选，图书系列，默认值 "economist"
- **查询参数**:
  - `page`: number, 可选，页码，默认值 1
- **响应**:
  ```typescript
  {
    message: string;  // 成功时返回 "Book list crawl task start."
  } | {
    error: string;   // 失败时返回错误信息
  }
  ```

### 3.2 爬取单本图书
- **接口**: `POST /api/v1/crawl/book/{series}`
- **描述**: 爬取单本图书信息
- **认证**: 需要 Bearer Token
- **路径参数**:
  - `series`: string, 可选，图书系列，默认值 "economist"
- **查询参数**: 同图书管理 API 的查询参数，用于查找要爬取的图书
- **响应**:
  ```typescript
  {
    message: string;  // 成功时返回 "Book crawl task start."
  } | {
    error: string;   // 失败时返回错误信息
  }
  ```
- **错误**:
  - 404 - Book not found（当找不到指定的图书时）
  - 其他运行时错误会在 error 字段中返回具体信息

## 4. 下载 API

### 4.1 批量下载图书
- **接口**: `POST /api/v1/download/books`
- **描述**: 批量下载图书，自动过滤未下载且有下载链接的图书
- **认证**: 需要 Bearer Token
- **查询参数**: 同图书管理 API 的查询参数
  ```typescript
  {
    // 注意：以下条件会自动添加
    file_size: 0,  // 只下载未下载的图书
    download_link: {  // 必须有下载链接
      operator: "!=",
      value: ""
    }
    // 其他查询参数同图书管理 API
  }
  ```
- **响应**:
  ```typescript
  {
    message: string;  // 成功时返回 "{n} books starts to download."
  } | {
    error: string;   // 失败时返回错误信息
  }
  ```

### 4.2 下载单本图书
- **接口**: `POST /api/v1/download/book`
- **描述**: 下载单本图书
- **认证**: 需要 Bearer Token
- **查询参数**: 同图书管理 API 的查询参数，用于查找要下载的图书
- **响应**:
  ```typescript
  {
    message: string;  // 成功时返回 "Book {title} download task start."
  } | {
    error: string;   // 失败时返回错误信息
  }
  ```
- **错误**:
  - 404 - Book not found（当找不到指定的图书时）
  - 其他运行时错误会在 error 字段中返回具体信息

## 5. 分发 API

### 5.1 批量分发图书
- **接口**: `POST /api/v1/distribute/books`
- **描述**: 批量发送书籍到指定邮箱，自动过滤未下载且有下载链接的图书
- **认证**: 需要 Bearer Token
- **查询参数**:
  ```typescript
  {
    email: string;  // 必填，收件人邮箱

    // 注意：以下条件会自动添加
    file_size: 0,  // 只发送未下载的图书
    download_link: {  // 必须有下载链接
      operator: "!=",
      value: ""
    }
    // 其他查询参数同图书管理 API
  }
  ```
- **响应**:
  ```typescript
  {
    message: string;  // 成功时返回 "发送{n}本书籍到 {email}"
  } | {
    error: string;   // 失败时返回错误信息，如"未指定收件人邮箱"
  }
  ```

### 5.2 分发单本图书
- **接口**: `POST /api/v1/distribute/book`
- **描述**: 发送单本书籍到指定邮箱
- **认证**: 需要 Bearer Token
- **查询参数**:
  ```typescript
  {
    email: string;  // 必填，收件人邮箱
    // 其他查询参数同图书管理 API，用于查找要发送的图书
  }
  ```
- **响应**:
  ```typescript
  {
    message: string;  // 成功时返回 "发送书籍 {title} 到 {email}"
  } | {
    error: string;   // 失败时返回错误信息，如"未指定收件人邮箱"
  }
  ```
- **错误**:
  - 404 - Book not found（当找不到指定的图书时）
  - "未指定收件人邮箱" - 当没有提供 email 参数时
  - 其他运行时错误会在 error 字段中返回具体信息

## 6. 任务管理 API

### 6.1 获取任务列表
- **接口**: `GET /api/v1/tasks`
- **描述**: 获取任务列表
- **认证**: 需要 Bearer Token
- **查询参数**:
  ```typescript
  {
    // 通用查询参数
    limit?: number;      // 默认 50
    skip?: number;       // 默认 0
    order_by?: string;   // 默认 "created_at"
    
    // 任务字段查询参数（所有字段都是可选的）
    id?: string;
    name?: string;
    status?: "pending" | "started" | "success" | "failure" | "retry";
    parent_id?: string;
    started_at?: string;
    completed_at?: string;
  }
  ```
- **响应**:
  ```typescript
  Array<{
    id: string;
    name: string;
    status: "pending" | "started" | "success" | "failure" | "retry";
    args: any[];        // 任务参数
    kwargs: Record<string, any>;  // 任务关键字参数
    result: any;        // 任务结果
    error: string | null;  // 错误信息
    started_at: string | null;  // ISO 8601 格式
    completed_at: string | null;  // ISO 8601 格式
    parent_id: string | null;  // 父任务ID
    created_at: string;  // ISO 8601 格式
    updated_at: string;  // ISO 8601 格式
  }>
  ```

### 6.2 获取任务详情
- **接口**: `GET /api/v1/tasks/{task_id}`
- **描述**: 获取单个任务详情
- **认证**: 需要 Bearer Token
- **路径参数**:
  - `task_id`: string, 必填，任务ID
- **响应**: 同任务列表中的单个任务对象
- **错误**:
  - 404 - Task not found

### 6.3 删除任务
- **接口**: `DELETE /api/v1/tasks/{task_id}`
- **描述**: 删除任务
- **认证**: 需要 Bearer Token
- **路径参数**:
  - `task_id`: string, 必填，任务ID
- **响应**:
  ```typescript
  {
    message: string;  // "Task deleted successfully"
  }
  ```
- **错误**:
  - 404 - Task not found

### 6.4 获取任务状态统计
- **接口**: `GET /api/v1/tasks/status/summary`
- **描述**: 获取任务状态统计
- **认证**: 需要 Bearer Token
- **响应**:
  ```typescript
  {
    pending?: number;
    started?: number;
    success?: number;
    failure?: number;
    retry?: number;
  }
  ```

## 7. 用户管理 API

### 查询参数说明
所有用户相关的 GET 接口都支持以下查询参数格式：
```typescript
{
  field_name: string | number | boolean;  // 直接值匹配
  // 或
  field_name: {
    operator: string;  // 操作符
    value: any;       // 查询值
  }
}
```

支持的操作符（operator）同图书管理 API。

### 7.1 获取用户列表
- **接口**: `GET /api/v1/users`
- **描述**: 获取用户列表
- **认证**: 需要 Bearer Token
- **查询参数**:
  ```typescript
  {
    // 通用查询参数
    limit?: number;      // 默认 50
    skip?: number;       // 默认 0
    order_by?: string;   // 排序字段，默认 "id"
    order_desc?: boolean;// 是否降序，默认 true

    // 用户字段查询参数（所有字段都是可选的）
    id?: number | { operator: string; value: number };
    username?: string | { operator: string; value: string };
    email?: string | { operator: string; value: string };
    created_at?: string | { operator: string; value: string };
    updated_at?: string | { operator: string; value: string };
  }
  ```
- **响应**: 用户信息数组

### 7.2 获取用户详情
- **接口**: `GET /api/v1/users`
- **描述**: 获取用户详情
- **认证**: 需要 Bearer Token
- **查询参数**:
  ```typescript
  {
    user_id: number;  // 必填，用户ID
  }
  ```
- **响应**: 用户信息
- **错误**:
  - 400 - "User ID is required"
  - 404 - "User not found"

### 7.3 创建用户
- **接口**: `POST /api/v1/users`
- **描述**: 创建新用户
- **认证**: 需要 Bearer Token
- **查询参数**:
  ```typescript
  {
    username: string;  // 必填，用户名
    email: string;    // 必填，邮箱
    password: string; // 必填，密码
  }
  ```
- **响应**: 用户信息

### 7.4 更新用户
- **接口**: `PUT /api/v1/users`
- **描述**: 更新用户信息
- **认证**: 需要 Bearer Token
- **查询参数**:
  ```typescript
  {
    user_id: number;     // 必填，用户ID
    username?: string;   // 可选，新用户名
    email?: string;     // 可选，新邮箱
    password?: string;  // 可选，新密码
  }
  ```
- **响应**: 用户信息
- **错误**:
  - 400 - "User ID is required"
  - 404 - "User not found"

### 7.5 删除用户
- **接口**: `DELETE /api/v1/users`
- **描述**: 删除用户
- **认证**: 需要 Bearer Token
- **查询参数**:
  ```typescript
  {
    user_id: number;  // 必填，用户ID
  }
  ```
- **响应**:
  ```typescript
  {
    message: string;  // "User deleted successfully"
  }
  ```
- **错误**:
  - 400 - "User ID is required"
  - 404 - "User not found"

### 7.6 添加用户订阅
- **接口**: `PUT /api/v1/users/subscriptions`
- **描述**: 添加用户订阅
- **认证**: 需要 Bearer Token
- **查询参数**:
  ```typescript
  {
    user_id: number;  // 必填，用户ID
    series: string;   // 必填，订阅系列
    date?: string;    // 可选，订阅日期，YYYY-MM-DD 格式
  }
  ```
- **响应**: 用户信息
- **错误**:
  - 400 - "User ID is required"
  - 400 - "Series is required"
  - 404 - "User not found"

### 7.7 删除用户订阅
- **接口**: `DELETE /api/v1/users/subscriptions`
- **描述**: 删除用户订阅
- **认证**: 需要 Bearer Token
- **查询参数**:
  ```typescript
  {
    user_id: number;  // 必填，用户ID
    series: string;   // 必填，订阅系列
  }
  ```
- **响应**: 用户信息
- **错误**:
  - 400 - "User ID is required"
  - 400 - "Series is required"
  - 404 - "User not found"

### 用户信息结构
所有返回用户信息的接口都使用以下结构：
```typescript
{
  id: number;
  email: string;
  username: string;
  created_at: string;    // ISO 8601 格式
  updated_at: string;    // ISO 8601 格式
  subscriptions: Array<{
    series: string;
    date: string;       // YYYY-MM-DD 格式
  }>;
  books: Array<{
    id: number;
    title: string;
    status: string;
  }>;
}
``` 