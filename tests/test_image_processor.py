import os
import logging
from app.utils.image_processor import ImageProcessor

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_checkbox_detection():
    """测试 checkbox 检测功能"""
    # 创建图像处理器实例
    processor = ImageProcessor(debug=True)
    
    # 测试图像目录
    test_dir = "cf_clicks"
    
    # 测试用例
    test_cases = [
        {
            "name": "正常 checkbox",
            "image": "click_20250509_181257_158469_full.png",
            "expected": True
        },
        {
            "name": "无 checkbox",
            "image": "click_20250509_181248_849958_full.png",
            "expected": False
        },
        {
            "name": "无 checkbox",
            "image": "click_20250509_181301_957887_full.png",
            "expected": False
        },
        {
            "name": "无 checkbox",
            "image": "click_20250509_181311_582642_full.png",
            "expected": False
        }
    ]
    
    # 运行测试
    for case in test_cases:
        print(f"\n测试用例: {case['name']}")
        image_path = os.path.join(test_dir, case['image'])
        
        if not os.path.exists(image_path):
            print(f"测试图像不存在: {image_path}")
            continue
            
        # 检测 checkbox
        result = processor.find_checkbox(image_path)
        
        # 验证结果
        if case['expected']:
            if result:
                print(f"✓ 成功找到 checkbox，位置: {result}")
            else:
                print("✗ 未找到 checkbox，但期望找到")
        else:
            if result:
                print(f"✗ 找到 checkbox，但期望未找到，位置: {result}")
            else:
                print("✓ 正确识别为无 checkbox")

if __name__ == "__main__":
    test_checkbox_detection() 