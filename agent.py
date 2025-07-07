# -----------------------------------------------------------------------------
# 文件: agent.py
# 描述: 这是 Agent 的核心逻辑，负责处理与社交媒体平台的交互。
# -----------------------------------------------------------------------------
import tweepy
import configparser
import logging
import os

# --- 设置日志记录 ---
# 日志是部署后排查问题的关键
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SocialMediaAgent:
    """
    一个可复用、可部署的社交媒体发图 Agent。
    它从配置文件读取密钥，并提供向各平台发布的统一接口。
    """
    def __init__(self, config_file='config.ini'):
        """
        初始化 Agent，加载配置。
        """
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"错误: 配置文件 '{config_file}' 未找到。请先创建它。")
        
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.twitter_client = self._setup_twitter_client()

    def _setup_twitter_client(self):
        """
        根据配置文件初始化并验证 Twitter API v2 客户端。
        """
        try:
            consumer_key = self.config['twitter']['api_key']
            consumer_secret = self.config['twitter']['api_key_secret']
            access_token = self.config['twitter']['access_token']
            access_token_secret = self.config['twitter']['access_token_secret']
            
            # 使用 v1.1 API 进行媒体上传
            auth_v1 = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
            api_v1 = tweepy.API(auth_v1)

            # 使用 v2 API 进行推文发布
            client_v2 = tweepy.Client(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )
            logging.info("Twitter API 客户端初始化成功。")
            return {"v1": api_v1, "v2": client_v2}
        except KeyError as e:
            logging.error(f"配置文件中缺少 Twitter 密钥: {e}")
            return None
        except Exception as e:
            logging.error(f"初始化 Twitter 客户端时发生未知错误: {e}")
            return None

    def _post_to_twitter(self, image_path, caption):
        """
        处理发布到 Twitter 的核心逻辑。
        """
        if not self.twitter_client:
            logging.error("Twitter 客户端未初始化，无法发布。")
            return False

        try:
            logging.info(f"正在上传图片 '{image_path}' 到 Twitter...")
            # 1. 使用 v1.1 API 上传媒体文件
            media = self.twitter_client["v1"].media_upload(filename=image_path)
            media_id = media.media_id
            logging.info(f"图片上传成功，Media ID: {media_id}")

            # 2. 使用 v2 API 发布推文并附上媒体 ID
            logging.info(f"正在发布推文...")
            response = self.twitter_client["v2"].create_tweet(
                text=caption,
                media_ids=[media_id]
            )
            logging.info(f"成功发布到 Twitter! 推文 ID: {response.data['id']}")
            return True
        except FileNotFoundError:
            logging.error(f"图片文件未找到: {image_path}")
            return False
        except Exception as e:
            logging.error(f"发布到 Twitter 失败: {e}")
            return False

    def _post_to_xhs(self, image_path, caption, title):
        """
        处理发布到小红书的占位逻辑。
        """
        logging.warning("--- 小红书发布模块 ---")
        logging.warning("注意: 小红书官方API不向个人开发者开放。")
        logging.warning("这是一个占位函数。要实现自动化，需要自行探索模拟浏览器方案（如 Playwright/Selenium）。")
        logging.info(f"（模拟）准备发布到小红书...")
        logging.info(f"标题: {title}")
        logging.info(f"内容: {caption}")
        logging.info(f"图片: {image_path}")
        logging.info("（模拟）发布成功。")
        # 在实际的模拟浏览器方案中，这里会是调用 browser.goto(), browser.fill() 等操作。
        return True

    def post(self, image_path, captions, platforms):
        """
        公开发布方法，统一调度。
        :param image_path: 本地图片的路径
        :param captions: 一个字典，包含为不同平台定制的文案。
        :param platforms: 一个列表，指定要发布到的平台。例如: ['twitter', 'xhs']
        """
        results = {}
        logging.info(f"开始发布任务，目标平台: {platforms}")

        if "twitter" in platforms:
            caption = captions.get("twitter", "A beautiful image.")
            results["twitter"] = self._post_to_twitter(image_path, caption)

        if "xhs" in platforms:
            caption = captions.get("xhs_caption", "一条好看的笔记～")
            title = captions.get("xhs_title", "一个不错的标题")
            results["xhs"] = self._post_to_xhs(image_path, caption, title)
            
        logging.info("所有发布任务已完成。")
        return results