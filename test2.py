import os
import requests
import json
from PIL import Image, ImageDraw, ImageFont

current_y = 0
item_order = ['hand', 'finger_left', 'ear_left', 'neck', 'bracelet', 'belt','gloves', 'soul', 'soul_2', 'pet', 'nova', 'soul_badge', 'swift_badge', 'body', 'head', 'body_accessory']
font_new = "/bot2.0/TaipeiSansTCBeta-Bold.ttf"
png_name = ""
proxies = {'http':'http://127.0.0.1:24458'}
# 从API获取JSON数据
def get_json_from_api(url):
    response = requests.get(url,proxies=proxies)
    return response.json()

# 下载图片并保存到指定路径
def download_image(url, file_path):
    response = requests.get(url,proxies=proxies)
    with open(file_path, 'wb') as f:
        f.write(response.content)

# 创建图片并将其与已有图片合并
def create_image(icon_file_path, name, output_file_path):
    global current_y  # 使用全局变量current_y来记录当前图片的垂直位置
    icon = Image.open(icon_file_path)  # 打开装备图标文件
    width, height = icon.size  # 获取装备图标的宽度和高度
    new_width = width + 600  # 新图片的宽度为装备图标宽度加200
    new_height = height  # 新图片的高度与装备图标高度相同

    # 检查输出文件是否已存在，如果存在则打开它，否则创建一个新的空白图片
    if os.path.exists(output_file_path):
        new_image = Image.open(output_file_path)
    else:
        new_image = Image.new('RGB', (new_width, new_height * len(item_order)), color='white')

    # 将装备图标粘贴到新图片的当前垂直位置（current_y）
    new_image.paste(icon, (0, current_y))
    draw = ImageDraw.Draw(new_image)  # 创建一个绘图对象以在新图片上绘制文本
    # 加载字体文件，设置字体大小为20
    font = ImageFont.truetype(font_new, 20)
    # 在新图片上绘制装备名称，位置为装备图标右侧，垂直居中
    draw.text((width + 10, current_y + height // 2 - 30), name, font=font, fill='black')
    new_image.save(output_file_path, quality=95)  # 保存新图片到指定的输出文件路径，使用高质量压缩设置
    current_y += new_height  # 更新current_y以便下一个装备图标粘贴到正确的位置



# 提取物品名称和图标文件名
def print_items(data, key1='detail', key2='item', key3='name', key4='icon'):
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key1 and isinstance(v, dict):
                if key2 in v and isinstance(v[key2], dict):
                    if key3 in v[key2]:
                        if key4 in v[key2]:
                            icon_url = v[key2][key4]
                            icon_file_name = icon_url.split('/')[-1]
                            return (f'{v[key2][key3]}', icon_file_name)

# 创建合并后的图片
def create_combined_image(item_name, icon_file_name, icon_url):
    global current_y
    icon_folder = 'icon'
    icon_file_path = os.path.join(icon_folder, icon_file_name)
    if not os.path.exists(icon_file_path):
        print(f'下载图片 {icon_file_path}')
        download_image(icon_url, icon_file_path)
    output_file_path = os.path.join(png_name)
    create_image(icon_file_path, item_name, output_file_path)

# 创建宝石图片并将其与已有图片合并
def create_gem_image(icon_file_path, output_file_path, x_offset, y_offset):
    icon = Image.open(icon_file_path)
    width, height = icon.size
    icon.thumbnail((width // 2.5, height // 2.5))  # 缩放宝石图片为25%
    width, height = icon.size

    if os.path.exists(output_file_path):
        new_image = Image.open(output_file_path)
    else:
        new_image = Image.new('RGB', (width + x_offset, height + y_offset), color='white')

    new_image.paste(icon, (x_offset, y_offset))
    new_image.save(output_file_path)
    return width  # 返回缩放后的宝石图标的宽度

# 处理宝石并将其添加到图片中
def process_gems(item, json_data, gem_x_offset, gem_y_offset):
    for gem in json_data[item]['detail']['added_gems']:
        gem_icon_url = gem['icon']
        if gem_icon_url is not None:
            gem_icon_file_name = gem_icon_url.split('/')[-1]
            gem_icon_folder = 'icon'
            gem_icon_file_path = os.path.join(gem_icon_folder, gem_icon_file_name)
            if not os.path.exists(gem_icon_file_path):
                print(f'下载图片 {gem_icon_file_path}')
                download_image(gem_icon_url, gem_icon_file_path)
            gem_width = create_gem_image(gem_icon_file_path, png_name, gem_x_offset, gem_y_offset)
            gem_x_offset += gem_width  # 使用缩放后的宝石图标的宽度
        else:
            # 处理 gem_icon_url 为 None 的情况，例如设置一个默认值或跳过这个宝石
            pass
    return gem_x_offset

def get_status(account_id,character_id):
    url = f"http://g.bns.tw.ncsoft.com/ingame/api/characters.json?guid={account_id}"
    response = requests.get(url,proxies=proxies)
    data = json.loads(response.text)
    for item in data:
        if item.get("name") == character_id:
            if item.get("playing"):
                return "在线"
            else:
                return "离线"



def get_character_info(role_name: str):
    url = f"http://g.bns.tw.ncsoft.com/ingame/api/character/info.json?c={role_name}"

    response = requests.get(url,proxies=proxies)
    data = json.loads(response.text)
    status = get_status(data['account_id'],data['name'])
    info = {
        '角色昵称': data['name'],
        '是否在线': status,
        '地点': data['geo_zone_name'],
        '游戏服务器': data['server_name'],
        '角色种族': data['race_name'],
        '性别': data['gender_name'],
        '角色职业': data['class_name'],
        '角色等级': data['level'],
        '所属帮会': data['guild']['guild_name'] if data['guild'] else "无",
        '派别': data['faction_name'],
    }
    return info

def add_character_info_to_image(character_info, ability_data, output_file_path):
    if os.path.exists(output_file_path):
        new_image = Image.open(output_file_path)
    else:
        return

    draw = ImageDraw.Draw(new_image)
    font = ImageFont.truetype(font_new, 20)

    x_offset = 300
    y_offset = 20
    for key, value in character_info.items():
        text = f"{key}: {value}"
        draw.text((x_offset, y_offset), text, font=font, fill='black')
        y_offset += 30

    # 添加 ability_data 到图像中
    for key, value in ability_data.items():
        text = f"{key}: {value}"
        draw.text((x_offset, y_offset), text, font=font, fill='black')
        y_offset += 30

    new_image.save(output_file_path, quality=95)


def get_ability_data(url):
    response = requests.get(url,proxies=proxies)
    json_data = response.json()
    total_ability = json_data['total_ability']

    ability_data = {
        '攻击力': total_ability.get('attack_power_value', 0),
        '对人攻击力': total_ability.get('pc_attack_power_value', 0),
        '降魔攻击力': total_ability.get('boss_attack_power_value', 0),
        '穿透': total_ability.get('attack_pierce_value', 0),
        '命中': total_ability.get('attack_hit_value', 0),
        '暴击': total_ability.get('attack_critical_value', 0),
        '暴击伤害': total_ability.get('attack_critical_damage_value', 0),
        '额外伤害': total_ability.get('attack_damage_modify_diff', 0),
        '威胁': total_ability.get('hate_power_rate', 0),
        '异常状态伤害': total_ability.get('abnormal_attack_power_value', 0),
        '功力': total_ability.get('attack_attribute_value', 0),
        '功力提升率': total_ability.get('attack_attribute_rate',0),
        '生命力': total_ability.get('max_hp', 0),
        '防御力': total_ability.get('defend_power_value', 0),
        '对人防御力': total_ability.get('pc_defend_power_value', 0),
        '降魔防御力': total_ability.get('boss_defend_power_value', 0),
        '闪避': total_ability.get('defend_dodge_value', 0),
        '格挡': total_ability.get('defend_parry_value', 0),
        '暴击防御': total_ability.get('defend_critical_value', 0),
        '再生': total_ability.get('hp_regen', 0),
        '恢复': total_ability.get('heal_power_rate', 0),
        '异常状态防御力': total_ability.get('abnormal_defend_power_value', 0),
        '先凑合看吧测试中':total_ability.get('ab', "有空再优化")
    }

    return ability_data



def create_character_image(character_name):
    print(os.getcwd())
    global png_name
    global current_y
    current_y = 0
    png_name = f'{character_name}.png'
    character_info = get_character_info(character_name)
    url = f"http://g.bns.tw.ncsoft.com/ingame/api/character/abilities.json?c={character_name}"
    ability_data = get_ability_data(url)

    url = f"http://g.bns.tw.ncsoft.com/ingame/api/character/equipments.json?c={character_name}"
    json_data = get_json_from_api(url)

    # 遍历物品列表并创建合并后的图片
    for item in item_order:
        if item in json_data:
            print(f'{item}')
            item_name, icon_file_name = print_items(json_data[item])
            icon_url = json_data[item]['detail']['item']['icon']
            print(item_name, icon_file_name)
            create_combined_image(item_name, icon_file_name, icon_url)

            # 如果物品包含宝石，则将宝石添加到图片中
            if item in ['hand', 'pet']:
                gem_x_offset = 65  # 减小初始值以向左移动宝石图标
                gem_y_offset = current_y - 30
                gem_x_offset = process_gems(item, json_data, gem_x_offset, gem_y_offset)
    add_character_info_to_image(character_info, ability_data, png_name)

# 使用函数创建角色图片
#character_name = "别忘记晚风"
#create_character_image(character_name)
