# -----------------------------------------------------------------------------
# 文件: main.py
# 描述: 这是调用 Agent 的主程序入口。
# -----------------------------------------------------------------------------
from agent import SocialMediaAgent

def main():
    # 1. 初始化 Agent
    # Agent 会自动从 config.ini 读取配置
    try:
        my_agent = SocialMediaAgent('config.ini')
    except FileNotFoundError as e:
        print(e)
        return

    # 2. 准备要发布的内容
    image_to_post = "sunflower_necklace.jpg" # <-- 将你的图片放在同目录下

    post_captions = {
        "twitter": "Absolutely in love with this sunflower pendant necklace! 🌻 It's the perfect little piece of sunshine to brighten up any outfit. #jewelry #sunflower #necklace #style",
        "xhs_title": "OOTD点睛之笔✨｜戴在锁骨上的小太阳🌻",
        "xhs_caption": "姐妹们快看！今天挖到什么宝藏配饰了！✨\n这条向日葵项链也太有夏天的感觉了吧～戴上它感觉自己就是行走的阳光小甜妹！☀️\n#OOTD #配饰分享 #向日葵 #锁骨链"
    }

    # 3. 执行发布任务
    publish_results = my_agent.post(
        image_path=image_to_post,
        captions=post_captions,
        platforms=['twitter', 'xhs'] # <-- 指定要发布的平台
    )

    # 4. 打印结果
    print("\n--- 发布任务总结 ---")
    for platform, success in publish_results.items():
        status = "成功" if success else "失败"
        print(f"平台 '{platform}': 发布{status}")

if __name__ == "__main__":
    main()