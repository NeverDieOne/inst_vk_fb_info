import argparse
from fb_bot import get_facebook_statistic
from vk_bot import get_vk_statistic
from inst_bot import get_inst_statistic

parser = argparse.ArgumentParser(description='Анализ постов в социальных сетях')
parser.add_argument('social_network', choices=['vk', 'instagram', 'facebook'], help='Название социальной сети, которую нужно проанализировать')
args = parser.parse_args()

if args.social_network == 'instagram':
    print(get_inst_statistic('cocacolarus'))
if args.social_network == 'vk':
    print(get_vk_statistic('cocacola'))
if args.social_network == 'facebook':
    print(get_facebook_statistic())
