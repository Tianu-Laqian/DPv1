import webbrowser
import threading
import time

def open_urls(file_path, batch_size=5, delay=1):
    """批量打开URL"""
    with open(file_path, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]
    
    print(f"共发现 {len(urls)} 个URL")
    
    # 使用多线程批量打开
    threads = []
    for i, url in enumerate(urls):
        # 验证URL格式
        if not url.startswith('http'):
            print(f"跳过无效URL: {url}")
            continue
        
        # 创建并启动线程
        t = threading.Thread(target=webbrowser.open, args=(url,))
        t.start()
        threads.append(t)
        
        # 控制批量打开速度
        if (i + 1) % batch_size == 0:
            print(f"已打开 {i+1}/{len(urls)} 个标签页")
            time.sleep(delay)  # 短暂延迟避免浏览器卡顿
    
    # 等待所有线程完成
    for t in threads:
        t.join()
    
    print("所有URL已打开！")

if __name__ == "__main__":
    url_file = "input.txt"  # 包含URL的文件
    open_urls(url_file, batch_size=10, delay=0.5)