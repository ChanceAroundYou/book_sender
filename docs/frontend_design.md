# Book Sender 前端设计文档

## 1. 技术栈选择

### 1.1 核心框架
- React 18：用于构建用户界面的JavaScript库
- TypeScript 5：提供类型系统的JavaScript超集
- Vite 4：现代前端构建工具
- React Router 6：客户端路由管理
- Redux Toolkit：状态管理工具

### 1.2 UI框架
- Ant Design 5：企业级UI组件库
- TailwindCSS 3：实用优先的CSS框架
- React Query：数据获取和缓存库
- React Hook Form：表单处理库

### 1.3 开发工具
- ESLint：代码质量检查
- Prettier：代码格式化
- Jest：单元测试框架
- React Testing Library：组件测试工具

## 2. 项目结构

项目采用模块化的目录结构，主要包含以下部分：

```
src/
├── api/          # API请求封装
├── assets/       # 静态资源文件
├── components/   # 可复用组件
├── hooks/        # 自定义React Hooks
├── layouts/      # 页面布局组件
├── pages/        # 页面组件
├── store/        # 状态管理
├── types/        # TypeScript类型定义
└── utils/        # 工具函数
```

## 3. 页面设计

### 3.1 布局设计
采用响应式布局设计，主要特点：
- 顶部导航栏：包含logo、主要导航和用户信息
- 侧边菜单：可折叠的导航菜单（管理员界面使用）
- 主内容区：自适应宽度的内容展示
- 页脚：版权信息

### 3.2 主要页面设计

#### 3.2.1 用户登录/注册页面
- 登录表单
  - 邮箱登录
  - 密码输入
  - 记住登录状态
  - 忘记密码功能
- 注册表单
  - 用户名设置
  - 邮箱设置
  - 密码设置

#### 3.2.2 首页设计
- 内容分区
  - 最新上架书籍
  - 系列书籍展示
- 搜索功能
  - 全局搜索框
  - 高级搜索选项
- 快速导航
  - 系列导航菜单

#### 3.2.3 书籍列表页面
- 搜索和筛选
  - 高级搜索表单
  - 多维度筛选器
    - 系列筛选
    - 格式筛选
    - 日期筛选
- 列表展示
  - 网格/列表视图切换
  - 排序选项
    - 最新上架
    - 发布日期
  - 分页控制
- 快速操作
  - 发送到邮箱
  - 批量发送

#### 3.2.4 书籍详情页面
- 基本信息展示
  - 封面图片
  - 书籍标题
  - 作者信息
  - 出版信息
  - 文件信息
- 分发区域
  - 发送到邮箱表单
  - 发送状态显示
- 书籍详情
  - 内容简介
  - 目录预览
  - 版权信息

#### 3.2.5 系列管理页面
- 系列信息
  - 系列封面展示
  - 系列简介
  - 出版周期
  - 订阅信息
- 期刊列表
  - 按年份分组显示
  - 封面预览
  - 期刊信息
  - 批量发送

#### 3.2.6 用户个人中心
- 个人信息管理
  - 基本信息编辑
  - 密码修改
  - 邮箱设置
- 订阅管理
  - 订阅的系列
  - 订阅设置
- 分发记录
  - 发送历史
  - 任务状态

#### 3.2.7 管理员界面
- 仪表板
  - 系统概览
  - 数据统计
  - 任务监控
- 内容管理
  - 书籍管理
    - 书籍列表
    - 添加/编辑书籍
    - 批量操作
  - 系列管理
    - 系列设置
    - 期刊管理
- 用户管理
  - 用户列表
  - 订阅管理
- 任务管理
  - 分发任务列表
  - 爬虫任务列表
  - 下载任务列表
- 系统设置
  - 基础设置
  - 邮件配置

### 3.3 路由设计
```typescript
const routes = {
  auth: {
    login: '/auth/login',
    register: '/auth/register',
    forgotPassword: '/auth/forgot-password',
  },
  home: '/',
  books: {
    list: '/books',
    detail: '/books/:id',
    series: '/books/series/:id',
  },
  user: {
    profile: '/user/profile',
    subscriptions: '/user/subscriptions',
    tasks: '/user/tasks',
    settings: '/user/settings',
  },
  admin: {
    dashboard: '/admin/dashboard',
    books: '/admin/books',
    users: '/admin/users',
    tasks: '/admin/tasks',
    settings: '/admin/settings',
  },
};
```

## 4. 组件设计

### 4.1 基础组件
- Button
  - 主按钮
  - 次要按钮
  - 文本按钮
  - 图标按钮
- Input
  - 文本输入框
  - 搜索输入框
  - 邮箱输入框
- Card
  - 基础卡片容器
  - 书籍卡片
  - 系列卡片
- Select
  - 下拉选择
  - 多选框
- Form
  - 表单容器
  - 表单项
  - 验证提示
- Modal
  - 模态框容器
  - 确认对话框
- Message
  - 操作提示
  - 错误提示
  - 加载提示

### 4.2 业务组件

#### 4.2.1 书籍相关组件
- BookCard
  - 封面图片
  - 标题信息
  - 作者信息
  - 发送按钮
- BookList
  - 网格布局
  - 列表布局
  - 加载状态
  - 空状态
- BookFilter
  - 系列选择
  - 格式筛选
  - 日期筛选
- BookSearch
  - 搜索输入
  - 高级搜索
- BookDetail
  - 信息展示
  - 发送表单
- EmailForm
  - 邮箱输入
  - 发送选项
  - 状态显示

#### 4.2.2 用户相关组件
- UserInfo
  - 基本信息展示
  - 编辑表单
- UserSubscriptions
  - 订阅列表
  - 订阅设置
- TaskList
  - 任务列表
  - 状态显示

#### 4.2.3 管理员组件
- AdminTable
  - 数据表格
  - 批量操作
  - 筛选排序
- AdminForm
  - 表单布局
  - 验证规则
  - 提交处理
- TaskMonitor
  - 任务列表
  - 状态统计

### 4.3 布局组件
- MainLayout
  - 导航栏
  - 内容区
  - 页脚
- AdminLayout
  - 侧边菜单
  - 顶部导航
  - 内容区
- AuthLayout
  - 登录表单
  - 注册表单

### 4.4 功能组件
- SearchBar
  - 搜索框
  - 高级搜索
- TaskStatus
  - 状态显示
  - 进度显示
- SeriesTree
  - 系列列表
  - 展开/折叠
- Breadcrumb
  - 路径导航
  - 可点击链接

## 5. 状态管理

### 5.1 Redux Store
```typescript
interface RootState {
  auth: {
    user: User | null;
    token: string | null;
    loading: boolean;
    error: string | null;
  };
  books: {
    list: Book[];
    current: Book | null;
    filters: BookFilters;
    pagination: Pagination;
    loading: boolean;
    error: string | null;
  };
  tasks: {
    list: Task[];
    status: Record<string, TaskStatus>;
    loading: boolean;
    error: string | null;
  };
  series: {
    list: Series[];
    current: Series | null;
    loading: boolean;
    error: string | null;
  };
  ui: {
    theme: Theme;
    sidebar: boolean;
    modal: Record<string, boolean>;
  };
}
```

### 5.2 API集成
实现以下API功能：
- 认证API：登录、注册、密码重置
- 书籍API：列表、详情、搜索、筛选
- 系列API：列表、详情、订阅管理
- 任务API：创建、查询、状态更新
- 用户API：信息管理、订阅管理
- 管理API：系统管理、任务监控

## 6. 响应式设计

### 6.1 断点设计
```typescript
const breakpoints = {
  sm: '640px',   // 手机
  md: '768px',   // 平板
  lg: '1024px',  // 小屏幕
  xl: '1280px',  // 大屏幕
  '2xl': '1536px' // 超大屏幕
};
```

### 6.2 布局适配
- 移动端：单列布局，折叠菜单
- 平板端：双列布局，可展开菜单
- 桌面端：多列布局，固定菜单

## 7. 性能优化

### 7.1 代码分割
- 路由级别代码分割
- 组件懒加载
- 第三方库按需加载

### 7.2 缓存策略
- API数据缓存
- 状态持久化
- 静态资源缓存

## 8. 开发规范

### 8.1 代码规范
- 文件命名：PascalCase组件，camelCase其他
- 组件结构：
  ```typescript
  interface Props {
    // 属性定义
  }
  
  const Component: React.FC<Props> = () => {
    // 组件实现
  };
  ```
- 类型定义：优先使用interface
- 状态管理：遵循Redux最佳实践

### 8.2 Git规范
- 分支：feature/*, bugfix/*, release/*
- 提交：feat, fix, docs, style, refactor
- 版本：遵循语义化版本 