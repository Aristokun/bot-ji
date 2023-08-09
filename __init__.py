from nonebot import on_command, get_driver, on_regex, require, get_bot, on_notice
from nonebot.log import logger
from io import BytesIO
from .browser import get_browser, shutdown_browser
from nonebot.adapters.onebot.v11 import MessageSegment as MS
from nonebot.adapters.onebot.v11 import Bot, GroupIncreaseNoticeEvent, \
    MessageSegment, Message, GroupMessageEvent,  MessageEvent
from nonebot.params import CommandArg
from nonebot.adapters import Message
from typing import Literal
from .browser import get_new_page
from PIL import Image
from pathlib import Path
from asyncio import sleep
from nonebot.permission import SUPERUSER
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
import random
import json
import sys
import os
sys.path.append("/bot2.0/ji/ji/src/plugins/inquire_bns/")
from test2 import create_character_image
driver = get_driver()
config = driver.config
file_path = Path() / 'data' / 'ac.json'




bangzhu2 = on_command("帮",aliases={"h","help","帮助","说明"},priority=3,block=True)
@bangzhu2.handle()
async def handle_bangzhu2():
    longtext=(
"""
长文字老出错 就截图了
# 发送 - 或 / 触发相应命令
# 如:-zx 中出无敌
# 目前有的功能：
# ********
# 资讯/咨询/查询/zx/+名字:
# ---查看角色资讯界面
# 黑神木/降临殿/千手/名刀/ 
# 黑蛇/殿堂/祠堂/九合一等:
# ---查看副本攻略（马服版机制一样）
# 圣神/金价 等
# 定时汇报火龙夏曼杀猪
# ********
# 新功能制作中 有想法可以艾特我 3Q

"""
    )
    await bangzhu2.finish(MS.image("file:///help.png"))

# 发送 - 或 / 触发相应命令
# 如:-zx 中出无敌
# 目前有的功能：
# ********
# 资讯/咨询/查询/zx/+名字:
# ---查看角色资讯界面
# 黑神木/降临殿/千手/名刀/ 
# 黑蛇/殿堂/祠堂/九合一等:
# ---查看副本攻略（马服版机制一样）
# 圣神/金价 等
# ********
# 新功能制作中 有想法可以艾特我 3Q




jianyi = on_command("建议",aliases={"建议"},priority=2,block=True)
@jianyi.handle()
async def handle_jianyi(event: MessageEvent, args: Message = CommandArg()):
    uids = event.get_user_id()    
    with open('data/jianyi.json', 'r', encoding='utf-8') as f:
        ac = json.load(f)
    # 将 uids 作为键，name 作为值，追加到 data 中
    ac[uids] = args.extract_plain_text()
    # 将更新后的 JSON 数据写入文件
    with open('data/jianyi.json', 'w', encoding='utf-8') as f:
        json.dump(ac, f, ensure_ascii=False)
    await jianyi.finish("已收集建议，感谢建议。")





def append_to_json(uids, name):
    with open('data/ac.json', 'r', encoding='utf-8') as f:
        ac = json.load(f)

    # 将 uids 作为键，name 作为值，追加到 data 中
    ac[uids] = name
    print(ac) 
    # 将更新后的 JSON 数据写入文件
    with open('data/ac.json', 'w', encoding='utf-8') as f:
        json.dump(ac, f, ensure_ascii=False)
    return f'用户 {name} 绑定成功'

bangding = on_command("绑",aliases={"bd","绑定"},priority=2,block=True)
@bangding.handle()
async def handle_bangding(event: MessageEvent, arg: Message = CommandArg()):
    uids = event.get_user_id()    
    msg = append_to_json(uids,arg.extract_plain_text())
    #msg = handle_msg(arg, 'add', 'userlist')
    await bangding.finish(msg)
def query_uids(uids):
    # 读取 JSON 文件内容
    with open('data/ac.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 查询 uids 是否存在于 JSON 数据中
    if uids in data:
        return data[uids]
    else:
        return None

def switch(arg):
    sw = {"丷未闻花名": "fangai.jpg", 1: "2", 3: "three"}
    picnum = random.randint(1, 4)
    return sw.get(arg, f"mai.jpg")


zixun = on_command("查看资讯",aliases={"资讯","zx","咨询","查询"},priority=2,block=True)
'''
@zixun.handle()
async def handle_zixun(event: MessageEvent,args: Message = CommandArg()):
    input_words = args.extract_plain_text()
    uids = event.get_user_id()
    if not input_words:
        if not query_uids(uids):
          await zixun.finish("你没有绑定角色哦 可以输入-bd xxx进行绑定\n 也可以-zx xxx直接查询")
        input_words = query_uids(uids)    
    await zixun.send("加载图片中")
    img_bytes = await capture_web(
        f"http://g.bns.tw.ncsoft.com/ingame/bs/character/profile?c={input_words}",
    )
    image1 = Image.open(BytesIO(img_bytes))
    picnum = random.randint(1,4)
    vip = switch(input_words)
    image2 = Image.open(f"{Path(__file__).parent}/{vip}")
    image1.paste(image2, (11, 111))
    img_bytesio = BytesIO()
    image1.save(img_bytesio, format="jpeg")
    await zixun.finish(MS.image(img_bytesio))
'''
@zixun.handle()
async def handle_zixun(event: MessageEvent,args: Message = CommandArg()):
    '''
    input_words = args.extract_plain_text()
    uids = event.get_user_id()
    if not input_words:
        if not query_uids(uids):
          await zixun.finish("你没有绑定角色哦 可以输入-bd xxx进行绑定\n 也可以-zx xxx直接查询")
        input_words = query_uids(uids)    
    create_character_image(input_words)
    await zixun.send(MS.image(f"file:///bot2.0/ji/ji/{input_words}.png"))
    os.remove(f"/bot2.0/ji/ji/{input_words}.png")
    '''
    await zixun.finish("梯子到期了 懒得续费了 下次一定")

touzi = on_command("骰子",aliases={"骰子","touzi"},priority=1,block=True)
@touzi.handle()
async def handle_touzi(args: Message = CommandArg()):
    input_words = args.extract_plain_text()
    if not input_words:
        await touzi.finish("请输入/骰子 数字A-数字B")
    numb = input_words.split("-")
    num = random.randint(int(numb[0]),int(numb[1]))
    await touzi.finish(str(num),at_sender=True)

jinjia = on_command("查看金价",aliases={"金价","jj"},priority=1,block=True)
@jinjia.handle()
async def handle_jinjia():
   # tmp = open('/jinjia.txt','r')
   # con = tmp.readline()
   # tmp.close()
    str1 = "懒得更新金价了 忘了这个功能吧"  #+ str(con) + "金\r\n金价参考来源：卖金头子---爱笑笑"
    await jinjia.finish(str1)

wj = on_command("wj", permission=SUPERUSER)
@wj.handle()
async def handle_wj(args: Message = CommandArg()):
    input_words = args.extract_plain_text()
    if not input_words:
        await wj.finish("命令格式 /wj 句子")
    tmp = open('/bot2/ji/config/违禁词.txt','a')
    tmp.write(input_words+"\n")
    tmp.close()
    await wj.finish("违禁词添加成功")


jin = on_command("j", permission=SUPERUSER)
@jin.handle()
async def handle_jin(args: Message = CommandArg()):
    input_words = args.extract_plain_text()
    if not input_words:
        await jin.finish("命令格式 /j 数字")
    tmp = open('/jinjia.txt','w')
    tmp.write(input_words)
    tmp.close()
    await jin.finish("金价更新成功")

yanjiusuo = on_command("黑龙教秘密研究所",aliases={"黑龙教秘密研究所","研究所","研究所攻略"},priority=1,block=True)
@yanjiusuo.handle()
async def handle_yanjiusuo():
    await yanjiusuo.finish( "赤花下的混沌与黑暗-封魔副本-黑龙教研究所\r\n \
    作者：可爱的倾城小姐姐\r\n \
    https://bns.qq.com/guide/details-news.htm?newsid=18118800")
    

jianglin = on_command("黑龙教降临殿",aliases={"黑龙教降临殿","降临殿","降临殿攻略"},priority=1,block=True)
@jianglin.handle()
async def handle_jianglin():
    await jianglin.finish( "魔气四溢的黑龙容器-封魔副本-黑龙教降临殿\r\n \
    作者：可爱的倾城小姐姐\r\n \
    https://bns.qq.com/guide/details-news.htm?newsid=18155196")


qianshou = on_command("千手罗汉阵",aliases={"千手罗汉阵","千手","千手攻略"},priority=1,block=True)
@qianshou.handle()
async def handle_qianshou():
    await qianshou.finish( "纳律禅师的挑战-千手罗汉阵详解\r\n \
    作者：可爱的倾城小姐姐\r\n \
    https://bns.qq.com/guide/details-news.htm?newsid=16206356")
    
heishenmu = on_command("黑神木",aliases={"黑神木","混沌黑神木","黑神木攻略"},priority=1,block=True)
@heishenmu.handle()
async def handle_heishenmu():
    #await heishenmu.finish( "黑枪族的神秘阴谋-封魔副本-混沌黑神木详解\r\n \
    #作者：可爱的倾城小姐姐\r\n \
    #https://bns.qq.com/gicp/news/485/17954579.html")
    await test.finish(MS.image("file:///heishenmu.jpg"))


nandao = on_command("殿堂",aliases={"殿堂","南道派试验殿堂","殿堂攻略"},priority=1,block=True)
@nandao.handle()
async def handle_nandao():
    await nandao.finish( "南道派的求助-南道派试验殿堂详解\r\n \
    作者：可爱的倾城小姐姐\r\n \
    https://bns.qq.com/guide/details-news.htm?newsid=15528131")

citang = on_command("祠堂",aliases={"祠堂","南道派祠堂","祠堂攻略"},priority=1,block=True)
@citang.handle()
async def handle_citang():
    await citang.finish(MS.image("file:///citang.jpg"))   

heishe = on_command("黑蛇",aliases={"黑蛇","小黑蛇","大黑蛇"},priority=1,block=True)
@heishe.handle()
async def handle_heishe():
    await heishe.finish( "黑蛇门的意志-黑蛇门隐秘地\r\n \
    作者：可爱的倾城小姐姐\r\n \
    https://bns.qq.com/guide/details-news.htm?newsid=14100241")
    
mingdao = on_command("名刀",aliases={"名刀","无形神剑","老女人"},priority=1,block=True)
@mingdao.handle()
async def handle_mingdao():
    await mingdao.finish( "无形神剑的教导－剑之记忆冥途殿\r\n \
    作者：可爱的倾城小姐姐\r\n \
    https://bns.qq.com/guide/details-news.htm?newsid=13186213")

fengdao = on_command("风岛",aliases={"疾风岛","扶风岛","摇风岛"},priority=1,block=True)
@fengdao.handle()
async def handle_fengdao():
    await fengdao.finish( "黑色疾风驻留的混沌之岛 - 封魔副本疾风岛\r\n \
    作者：可爱的倾城小姐姐\r\n \
    https://bns.qq.com/guide/details-news.htm?newsid=18183946")

shantui = on_command("闪退",aliases={"闪退","报错"},priority=1,block=True)
@shantui.handle()
async def handle_shantui():
    await shantui.finish( "闪退关GCD 其他看群公告和文件 再不懂重开 撒比")




jiuheyi = on_command("周本",aliases={"周本","九合一","周本顺序","九合一顺序"},priority=1,block=True)
@jiuheyi.handle()
async def handle_jiuheyi():
    await jiuheyi.finish( "     白青山脉-钢铁堡垒-钢铁堡垒秘密研究所（小钢铁）\r\n \
    天命宫-永生寺-安息庭院\r\n \
    天命宫-永生寺-贪欲密室\r\n \
    西洛-泰天王陵-日暮圣殿\r\n \
    西洛-泰天王陵-束缚之石室\r\n \
    西洛-泰天王陵-纪律之回廊\r\n \
    西洛-泰天王陵-太初的王座\r\n \
    建元成道-天之盆地-庶子安息所\r\n \
    建元成道-天命宫外苑-涡流寺\r\n \
    ------以上为9合1顺序------\r\n \
    白青山脉-钢铁堡垒-钢铁方舟（大钢铁）\r\n \
    天命宫-永生寺-赤梦秘苑（邪花）\r\n \
    白青山脉-黑蛇门隐居处-黑蛇门隐居处（小黑蛇）\r\n \
    ------以上为12合1------")

shengshen = on_command("圣神",aliases={"圣神","圣神路线","圣神武器"},priority=1,block=True)
@shengshen.handle()
async def handle_shengshen():
    await shengshen.finish(MS.image("file:///shengshen.jpg"))

kuaipao = on_command("快跑",aliases={"小鲨鱼","快跑","剑灵快跑"},priority=1,block=True)
@kuaipao.handle()
async def handle_kuaipao():
    await kuaipao.finish(MS.image("file:///shayu.jpg"))

san = on_command("快跑3",aliases={"小鲨鱼不能用","315","鲨鱼坏了"},priority=1,block=True)
@san.handle()
async def handle_san():
    await san.finish(MS.image("file:///315.png"))

test = on_command("test",aliases={"test"},priority=1,block=True)
@test.handle()
async def handle_test():
    await test.finish("小寄测试新功能")
'''
@scheduler.scheduled_job("cron", hour="0,12,15,18,21", minute=55, misfire_grace_time=60)
async def _():
    bot = get_bot()
    await bot.send_group_msg(group_id=859692736, message="小寄提醒 还有五分钟火龙嗷\n顺便6500出5300up琴 有意加769780364 么么哒")
    await bot.send_group_msg(group_id=435362340, message="[CQ:at,qq=1421212610][CQ:at,qq=750030400][CQ:at,qq=1315020837]小寄提醒 还有五分钟火龙嗷\n顺便6500出5300up琴 有意加769780364 么么哒")
    await bot.send_group_msg(group_id=475219032, message="小寄提醒 还有五分钟火龙嗷\n顺便6500出5300up琴 有意加769780364 么么哒")
    await bot.send_group_msg(group_id=301397392, message="小寄提醒 还有五分钟火龙嗷\n顺便6500出5300up琴 有意加769780364 么么哒")
    await bot.send_group_msg(group_id=585148616, message="小寄提醒 还有五分钟火龙嗷\n顺便6500出5300up琴 有意加769780364 么么哒")
    await bot.send_group_msg(group_id=514106873, message="小寄提醒 还有五分钟火龙嗷\n顺便6500出5300up琴 有意加769780364 么么哒")
    await bot.send_group_msg(group_id=609981831, message="[CQ:at,qq=1421212610][CQ:at,qq=1315020837]小寄提醒 还有五分钟火龙嗷\n顺便6500出5300up琴 有意加769780364 么么哒")
    await bot.send_group_msg(group_id=429645656, message="小寄提醒 还有五分钟火龙嗷\n顺便6500出5300up琴 有意加769780364 么么哒")

@scheduler.scheduled_job("cron", hour="1,13,16,19,22", minute=25, misfire_grace_time=60)
async def _():
    bot = get_bot()
    await bot.send_group_msg(group_id=859692736, message="小寄提醒 还有五分钟夏曼嗷\n顺便6500出5300up琴 有意加769780364 么么哒")
    await bot.send_group_msg(group_id=435362340, message="[CQ:at,qq=1421212610][CQ:at,qq=750030400][CQ:at,qq=1315020837]小寄提醒 还有五分钟夏曼嗷\n顺便6500出5300up琴 有意加769780364 么么哒")
    await bot.send_group_msg(group_id=475219032, message="小寄提醒 还有五分钟夏曼嗷\n顺便6500出5300up琴 有意加769780364 么么哒")
    await bot.send_group_msg(group_id=514106873, message="小寄提醒 还有五分钟夏曼嗷\n顺便6500出5300up琴 有意加769780364 么么哒")
    await bot.send_group_msg(group_id=585148616, message="小寄提醒 还有五分钟夏曼嗷\n顺便6500出5300up琴 有意加769780364 么么哒")
    await bot.send_group_msg(group_id=301397392, message="小寄提醒 还有五分钟夏曼嗷\n顺便6500出5300up琴 有意加769780364 么么哒")
    await bot.send_group_msg(group_id=609981831, message="[CQ:at,qq=1421212610][CQ:at,qq=1315020837]小寄提醒 还有五分钟夏曼嗷\n顺便6500出5300up琴 有意加769780364 么么哒")
    await bot.send_group_msg(group_id=426848785, message="小寄提醒 还有五分钟夏曼嗷\n顺便6500出5300up琴 有意加769780364 么么哒")
    await bot.send_group_msg(group_id=429645656, message="小寄提醒 还有五分钟夏曼嗷\n顺便6500出5300up琴 有意加769780364 么么哒")

notice_handle = on_notice(priority=5, block=True)
@notice_handle.handle()
async def GroupNewMember(bot: Bot, event: GroupIncreaseNoticeEvent):
    greet_emoticon = MessageBuild.Image(bg_file, mode='RGBA')
    if event.user_id == event.self_id:
        await bot.send_group_msg(group_id=event.group_id, message=Message(
            MessageSegment.text('爷是新来的机器人 输出-h查看帮助\n') + greet_emoticon))
    elif event.group_id not in config.paimon_greet_ban:
        await bot.send_group_msg(group_id=event.group_id, message=Message(
            MessageSegment.at(event.user_id) + MessageSegment.text("你好，我是你进群送的cp哦~\n") + greet_emoticon))

download_image = on_notice(priority=5)

@download_image.handle()
async def handle_at(bot: Bot, event: GroupMessageEvent):
    if event.message_type == "group":
        if "at" in event.raw_message and str(bot.self_id) in event.raw_message:
            message = Message(event.message)
            img_urls = []

            # 检查消息中的图片
            for segment in message:
                if segment.type == "image":
                    img_urls.append(segment.data["url"])

            # 检查引用的消息中的图片
            if "reply" in event.raw_message:
                reply_id = event.message[0].data["id"]
                reply_msg = await bot.get_msg(message_id=reply_id)
                reply_message = Message(reply_msg["message"])
                for segment in reply_message:
                    if segment.type == "image":
                        img_urls.append(segment.data["url"])

            # 下载并保存图片
            if img_urls:
                for img_url in img_urls:
                    async with httpx.AsyncClient() as client:
                        response = await client.get(img_url)
                        img_data = response.content
                        file_name = os.path.basename(img_url)
                        async with aiofiles.open(f"downloads/{file_name}", "wb") as f:
                            await f.write(img_data)
                await bot.send(event, "图片已下载成功！")
            else:
                await bot.send(event, "未找到图片，请确保消息中包含图片。")
'''
