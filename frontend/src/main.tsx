import React from 'react';
import ReactDOM from 'react-dom/client';
import { ConfigProvider } from 'antd';
import { Provider } from 'react-redux';
import zhCN from 'antd/locale/zh_CN';
import App from './App';
import { store } from './store';
import './index.css';
import { validateConfig } from './config';

// 验证环境配置
validateConfig();

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <Provider store={store}>
            <ConfigProvider locale={zhCN}>
                <App />
            </ConfigProvider>
        </Provider>
    </React.StrictMode>
); 