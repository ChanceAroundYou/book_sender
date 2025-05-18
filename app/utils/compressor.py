import py7zr
from pathlib import Path
from typing import Dict
import time
from loguru import logger

def compress_to_7z(input_path: str, compression_level: int = 9) -> Dict:
    """
    将文件压缩为7z格式并测试压缩效果
    
    Args:
        input_path: 输入文件路径
        compression_level: 压缩级别 (0-9)，默认9为最高压缩率
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"文件不存在: {input_path}")
        
    # 构建输出文件路径
    output_path = input_path.parent / f"{input_path.stem}.7z"
    
    # 记录开始时间
    start_time = time.time()
    
    try:
        # 配置7z压缩选项
        filters = [
            {
                "id": py7zr.FILTER_LZMA2,
                "preset": compression_level
            }
        ]
        
        # 执行压缩
        with py7zr.SevenZipFile(
            output_path,
            'w',
            filters=filters
        ) as archive:
            archive.write(input_path, input_path.name)
        
        # 计算压缩统计信息
        original_size = input_path.stat().st_size
        compressed_size = output_path.stat().st_size
        compression_ratio = compressed_size / original_size
        time_taken = time.time() - start_time
        
        result = {
            "status": "success",
            "input_path": str(input_path),
            "output_path": str(output_path),
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": compression_ratio,
            "time_taken_seconds": time_taken
        }
        
        # 打印结果
        logger.info(f"压缩结果:")
        logger.info(f"原始文件: {result['input_path']}")
        logger.info(f"压缩文件: {result['output_path']}")
        logger.info(f"原始大小: {result['original_size'] / 1024 / 1024:.2f} MB")
        logger.info(f"压缩大小: {result['compressed_size'] / 1024 / 1024:.2f} MB")
        logger.info(f"压缩比例: {result['compression_ratio']:.2%}")
        logger.info(f"耗时: {result['time_taken_seconds']:.2f} 秒")
        
        return result
        
    except Exception as e:
        logger.error(f"压缩失败: {str(e)}")
        raise e

# 测试代码
if __name__ == "__main__":
    # 测试不同压缩级别
    test_file = "downloads/The Economist Continental Europe Edition – 3-9 May 2025.pdf"  # 替换为你的PDF文件路径
    
    print("测试不同压缩级别的效果...")
    
    results = []
    for level in [9]:  # 测试低、中、高三种压缩级别
        print(f"\n使用压缩级别 {level}:")
        try:
            result = compress_to_7z(test_file, level)
            results.append(result)
        except Exception as e:
            print(f"级别 {level} 测试失败: {str(e)}")
            continue
    
    # 比较结果
    if results:
        print("\n压缩级别比较:")
        print("级别 | 压缩率 | 大小(MB) | 耗时(秒)")
        print("-" * 40)
        for i, result in enumerate([9]):
            if i < len(results):
                r = results[i]
                print(f"{result}    | {r['compression_ratio']:.2%} | {r['compressed_size_mb']:.2f} | {r['time_taken_seconds']:.2f}")