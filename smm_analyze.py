import argparse
from instabot import Bot
from fb_bot import get_facebook_statistic
from vk_bot import get_vk_statistic
from inst_bot import get_inst_statistic
from dotenv import load_dotenv
import os


load_dotenv()

parser = argparse.ArgumentParser(description='Анализ постов в социальных сетях')
parser.add_argument('social_network', choices=['vk', 'instagram', 'facebook'], help='Название социальной сети, которую нужно проанализировать')
parser.add_argument('-n, --name', help='Имя группы в vk или instagram')
args = parser.parse_args()


fb_access_token = os.getenv('FB_ACCESS_TOKEN')
vk_access_token = os.getenv('SERVICE_VK_TOKEN')
bot = Bot(base_path='./inst')
bot.login(username=os.getenv('INST_LOGIN'), password=os.getenv('INST_PASSWORD'))


if args.social_network == 'instagram':
    print(get_inst_statistic(bot, args.name or os.getenv('INST_GROUP_NAME')))
if args.social_network == 'vk':
    print(get_vk_statistic(vk_access_token, args.name or os.getenv('VK_GROUP_NAME')))
if args.social_network == 'facebook':
    print(get_facebook_statistic(fb_access_token))
