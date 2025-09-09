import logging
from app.crawler.economist_crawler import EconomistCrawler
from app.core.database import get_db

# 配置日志
logging.basicConfig(
    level=logging.INFO,  # 设置为 DEBUG 级别以显示更多信息
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_crawler():
    """测试爬虫功能"""
    try:
        # 创建爬虫实例
        crawler = EconomistCrawler()
        
        # 测试获取杂志列表
        print("\n测试获取杂志列表...")
        issues = crawler.get_issue_list(page=1)
        print(f"找到 {len(issues)} 期杂志")
        
        if issues:
            print("\n杂志列表:")
            for issue in issues:
                print(f"标题: {issue['title']}")
                print(f"链接: {issue['link']}")
                print(f"日期: {issue['date']}")
                print("-" * 50)
            
            # 测试获取下载链接
            print("\n测试获取下载链接...")
            issue = issues[0]
            download_url = crawler.get_download_link(issue["link"])
            print(f"下载链接: {download_url}")
            
            if download_url:
                # 测试下载杂志
                print("\n测试下载杂志...")
                book = crawler.download_issue(download_url, issue["title"])
                if book:
                    print(f"成功下载: {book.title}")
                    print(f"文件路径: {book.file_path}")
        
        # # 测试爬取最新杂志
        # print("\n测试爬取最新杂志...")
        # books = crawler.crawl_latest_issues(num_issues=2)
        # print(f"成功下载 {len(books)} 期杂志")
        
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")
        import traceback
        print(traceback.format_exc())
    finally:
        # 清理资源
        if 'crawler' in locals():
            del crawler

if __name__ == "__main__":
    test_crawler() 