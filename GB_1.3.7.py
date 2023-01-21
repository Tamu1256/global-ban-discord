# インストールした discord.py を読み込む

from ast import alias
from pydoc import synopsis
from pyexpat.errors import messages
from secrets import randbits
from unicodedata import name
from discord import ui
from discord.ext import commands,tasks
import os
import discord
from discord import app_commands,Webhook
import random
import asyncio
import datetime
import json
import sys
import socket
import aiosqlite
import time
import psutil
import cv2
import requests
import platform
from PIL import Image, ImageDraw,ImageFont
from captcha.image import ImageCaptcha
def rr(min,max):
    return random.randint(min,max)


async def dtnow():
    dt = datetime.datetime.now()
    dt = dt.replace(microsecond = 0)
    return dt

async def timestamp():
    return "<t:"+ str(int(time.time()))+":d>" + "<t:"+ str(int(time.time()))+":T>"

key = ""
ver01 = '1.3.7'

emoji_YES = "<:YES>"
emoji_NO="<:NO>"

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True

async def determine_prefix(bot,message):
    mgi = message.guild.id
    mai = message.author.id
    Strike_user = "GB/Strike/S-" + str(mgi) + "/User/U-" + str(mai) + ".json"
    Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
    if os.path.isfile(Strike_guild + "/P-Prefix.json"):
        with open(Strike_guild + "/P-Prefix.json",'r',encoding="utf-8") as a:
            d = list(json.load(a))
        return d
    if not os.path.isfile(Strike_guild + "/P-Prefix.json"):
        return ["se!","se."]

bot = commands.Bot(command_prefix=determine_prefix,help_command=None,intents=intents)

@tasks.loop(minutes=1)
async def timeday():
    with open("GB/Directory/time.json",'r') as a:
        ti = json.load(a)
        day = ti[0]
        hour = ti[1]
        minutes = ti[2]
        start_time = ti[3]
    with open("GB/Directory/time.json",'w') as a:
        minutes = minutes + 1
        if minutes == 60:
            minutes = 0
            hour = hour + 1
        if hour == 24:
            hour = 0
            day = day + 1
        time =[day,hour,minutes,start_time]
        a.write(str(time))

# 起動時に動作する処理
@bot.listen()
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    #ch = bot.get_channel()
    #await ch.purge(limit=5)
    print("Succes")
    await bot.tree.sync()

    #activity = discord.Activity(name="1.0.0", type=discord.ActivityType.playing)
    #await bot.change_presence(activity=activity)
    #user = discord.utils.get(bot.users, id=831453621732245534)
    #await user.send("起動したよ！")
    dt = datetime.datetime.now()
    daytimes = [dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second]
    with open("GB/Directory/time.json",'w') as a:
        time =[0,0,0,daytimes]
        a.write(str(time))
    timeday.start()
    print(len(bot.guilds))
    while True:
        game_status = [
            '!AVO help |' + ' Ver ' + str(ver01),
            '!AVO help | ' + str(len(bot.guilds)) + ' SERVERS'
        ]
        await activity(game_status[0])
        await activity(game_status[1])
        
async def activity(status):
    activity = discord.Activity(name=status, type=discord.ActivityType.playing)
    await bot.change_presence(activity=activity,status=discord.Status.online) 
    await asyncio.sleep(30) 


@bot.listen()
async def on_member_join(member):
    mgi = member.guild.id
    mai = member.author.id
    Strike_user = "GB/Strike/S-" + str(mgi) + "/User/U-" + str(mai) + ".json"
    Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
    with open(Strike_guild + "/C-Notice.json",'r') as a:
        d = json.load(a)
        GBAN_BOOLEAN = d[3]
        GBAN_CHANNEL = d[0]
    if GBAN_BOOLEAN == 1:
        with open("GB/Directory/id.json",'r') as a:
            d = json.load(a)
        with open("GB/Directory/name.json",'r') as a:
            n = json.load(a)
        if member.id in d or any(x in member.name for x in n):
            embed=discord.Embed(title="BAN", color=0xff0000)
            embed.add_field(name="メンバー", value=str(member.mention), inline=False)
            embed.add_field(name="理由", value="グローバルBAN\nGBAN", inline=False)
            urll = member.display_avatar
            embed.set_thumbnail(url=str(urll))
            if not GBAN_CHANNEL == 0:
                with open(Strike_guild + "/C-Notice.json",'r',encoding="utf-8") as a:
                    Notice_list = json.load(a)
                    Notice=Notice_list[0]
                with open("GB/Directory/log.json",'r',encoding="utf-8") as a:
                    Notice_list = json.load(a)
                    log=Notice_list[0]
                if not Notice == 0: #GBAN通知
                    channel = bot.get_channel(Notice)
                    embed = discord.Embed(title="GBAN", description=
                    "**違反者**：" + str(member.author.mention)+ 
                    "\n**時間**　：" + str(await timestamp())+
                    "\n **内容**　：" + "GBAN"+
                    "\n **処罰**　：" + "BAN"+
                    "\n **理由**　：" + "GBANに登録されているため" 
                    ,color=0x330000)
                    
                    await channel.send(embed=embed)
                if not log == 0: #GBAN通知
                    channel = bot.get_channel(log)
                    embed = discord.Embed(title="GBAN", description=
                    "**違反者**：" + str(member.author.mention)+ 
                    "\n**時間**　：" + str(await timestamp())+
                    "\n **内容**　：" + "GBAN"+
                    "\n **処罰**　：" + "BAN"+
                    "\n **理由**　：" + "GBANに登録されているため" +
                    "\n **場所**　：" + str(member.guild.id) + "・" + str(member.guild.name)
                    ,color=0x330000)
                    
                    await channel.send(embed=embed)
            await ban(member,member.id)
            
            
            
            await member.ban(delete_message_days=7, reason="グローバルBAN")

# --- BAN ---
async def ban(member,idd):
    embed=discord.Embed(title="BAN", color=0xff0000)
    embed.add_field(name="メンバー", value=str(member.mention), inline=False)
    embed.add_field(name="理由", value="グローバルBAN\nIDBAN", inline=False)
    urll = member.display_avatar
    embed.set_thumbnail(url=str(urll))
    user = discord.utils.get(bot.users, id=idd)
    await user.send(embed=embed)       
# メッセージ受信時に動作する処理
@bot.listen()
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
        

    if message.author.bot:
        return
# --- BAN ---
@bot.listen()
async def on_message(message):
    mgi = message.guild.id
    mai = message.author.id
    Strike_user = "GB/Strike/S-" + str(mgi) + "/User/U-" + str(mai) + ".json"
    Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
    with open("GB/Directory/id.json",'r') as b:
        dx = json.load(b)
    GBAN_BOOLEAN = GBAN_CHANNEL = 0
    if os.path.isfile(Strike_guild + "/C-Notice.json"):
        with open(Strike_guild + "/C-Notice.json",'r') as a:
            d = json.load(a)
            GBAN_BOOLEAN = d[3]
            GBAN_CHANNEL = d[0]
    
    with open("GB/Directory/name.json",'r') as a:
        n = json.load(a)
    if GBAN_BOOLEAN == 1:
        member = bot.get_user(message.author.id)
        try:
            guild = bot.get_guild(message.guild.id)  #idはint型で
        except AttributeError:
            print("小さなエラー発生")
        #IDBAN対象
        if message.author.id in dx :
            embed=discord.Embed(title="BAN", color=0xff0000)
            embed.add_field(name="メンバー", value=str(message.author.mention), inline=False)
            embed.add_field(name="理由", value="グローバルBAN\nIDBAN", inline=False)
            urll = member.display_avatar
            embed.set_thumbnail(url=str(urll))
            userr = discord.utils.get(bot.users, id=int(message.author.id))
            await userr.send(embed=embed)  
            if not GBAN_CHANNEL == 0:
                try:
                    with open(Strike_guild + "/C-Notice.json",'r',encoding="utf-8") as a:
                        Notice_list = json.load(a)
                        Notice=Notice_list[0]
                    with open("GB/Directory/log.json",'r',encoding="utf-8") as a:
                        Notice_list = json.load(a)
                        log=Notice_list[0]
                    if not Notice == 0: #レイド通知
                        channel = bot.get_channel(Notice)
                        embed = discord.Embed(title="GBAN", description=
                        "**違反者**：" + str(member.author.mention)+ 
                        "\n**時間**　：" + str(await timestamp())+
                        "\n **内容**　：" + "GBAN"+
                        "\n **処罰**　：" + "BAN"+
                        "\n **理由**　：" + "GBANに登録されているため" 
                        ,color=0x330000)
                        
                        await channel.send(embed=embed)
                    if not log == 0: #レイド通知
                        channel = bot.get_channel(log)
                        embed = discord.Embed(title="GBAN", description=
                        "**違反者**：" + str(member.author.mention)+ 
                        "\n**時間**　：" + str(await timestamp())+
                        "\n **内容**　：" + "GBAN"+
                        "\n **処罰**　：" + "BAN"+
                        "\n **理由**　：" + "GBANに登録されているため" +
                        "\n **サーバー場所**　：" + str(message.guild.id) + "・" + str(message.guild.name) + 
                        "\n **チャンネル場所**：" + str(message.channel.id) + "・" + str(message.channel.mention) +
                        "\n **サーバー所有者**：" + str(message.guild.owner.id) + "・" + str(message.guild.owner.mention)
                        ,color=0x330000)
                        
                        await channel.send(embed=embed)
                except AttributeError:
                    pass

            await message.author.ban(delete_message_days=7, reason="グローバル ID BAN")

        #名前BAN対象
        if member.name in n:
            embed=discord.Embed(title="BAN", color=0xff0000)
            embed.add_field(name="メンバー", value=str(mm.mention), inline=False)
            embed.add_field(name="理由", value="グローバルBAN\nあなたのユーザー名が禁止リストに入っていたため", inline=False)
            urll = member.display_avatar
            embed.set_thumbnail(url=str(urll))
            userr = discord.utils.get(bot.users, id=int(message.author.id))
            await userr.send(embed=embed)  
            if not GBAN_CHANNEL == 0:
                with open(Strike_guild + "/C-Notice.json",'r',encoding="utf-8") as a:
                    Notice_list = json.load(a)
                    Notice=Notice_list[0]
                with open("GB/Directory/log.json",'r',encoding="utf-8") as a:
                    Notice_list = json.load(a)
                    log=Notice_list[0]
                if not Notice == 0: #レイド通知
                    channel = bot.get_channel(Notice)
                    embed = discord.Embed(title="GBAN", description=
                    "**違反者**：" + str(member.author.mention)+ 
                    "\n**時間**　：" + str(await timestamp())+
                    "\n **内容**　：" + "GBAN"+
                    "\n **処罰**　：" + "BAN"+
                    "\n **理由**　：" + "GBANに登録されているため" 
                    ,color=0x330000)
                    
                    await channel.send(embed=embed)
                if not log == 0: #レイド通知
                    channel = bot.get_channel(log)
                    embed = discord.Embed(title="GBAN", description=
                    "**違反者**：" + str(member.author.mention)+ 
                    "\n**時間**　：" + str(await timestamp())+
                    "\n **内容**　：" + "GBAN"+
                    "\n **処罰**　：" + "BAN"+
                    "\n **理由**　：" + "GBANに登録されているため" +
                    "\n **サーバー場所**　：" + str(message.guild.id) + "・" + str(message.guild.name) + 
                    "\n **チャンネル場所**：" + str(message.channel.id) + "・" + str(message.channel.mention) +
                    "\n **サーバー所有者**：" + str(message.guild.owner.id) + "・" + str(message.guild.owner.mention)
                    ,color=0x330000)
                    
                    await channel.send(embed=embed)
                

            await mm.ban(delete_message_days=7, reason="グローバルBAN")
    uid = await admin_id()
    if message.content == "!Atest":
        a = socket.gethostname()
        embed = discord.Embed(title='Hey', description=str(a),color=0x0080ff)
        
        embed.add_field(name="TEST",value="test",inline=False)
        embed.add_field(name="TEST",value="test",inline=False)

        embed.set_footer(text=str(await dtnow()))
        #embed.set_author(name="Test",url=str(url),icon_url="TEST")
        await message.channel.send(embed=embed)
    if message.author.id in uid:
        if message.channel.id == 1051116779365208064:
            if message.content.startswith("nb"):
                name = message.content.split()
                try:
                    name = name[1]
                    with open("GB/Directory/name.json",'r') as a:
                        n = json.load(a)
                    if not "" == name:
                        if not name in n:
                            with open("GB/Directory/name.json",'r') as a:
                                n = json.load(a)
                            with open("GB/Directory/name.json",'w') as a:
                                nn = list(n)
                                nn.append(str(name))
                                j= json.dumps(nn)
                                a.write(j)
                            
                            embed = discord.Embed(title='成功', description="リストに`" + str(name) + "`を追加しました" ,color=0x00ff00)
                            embed.set_footer(text=str(await dtnow()))
                            await message.channel.send(embed=embed)
                            
                        if name in n:
                            with open("GB/Directory/name.json",'w') as a:
                                nn = list(n)
                                nn.remove(str(name))
                                j= json.dumps(nn)
                                a.write(j)
                            embed = discord.Embed(title='成功', description="リストに`" + str(name) + "`を削除しました" ,color=0xff0000)
                            embed.set_footer(text=str(await dtnow()))
                            await message.channel.send(embed=embed)
                except IndexError:
                    embed = discord.Embed(title='エラー', description="引数がないため実行できませんでした" ,color=0xff0000)
                    embed.set_footer(text=str(await dtnow()))
                    await message.channel.send(embed=embed)
            if message.content.startswith("ib"):
                id = message.content.split() # msg = ["!test", "123"]
                try:
                    id = int(id[1])

                    with open("GB/Directory/id.json",'r') as a:
                        d = json.load(a)
                    if id in d :
                        embed = discord.Embed(title='エラー', description="既にそのユーザーIDはGBANに登録しています" ,color=0xff0000)
                        embed.set_footer(text=str(await dtnow()))
                        await message.channel.send(embed=embed)
                    else:
                        with open("GB/Directory/id.json",'w') as a:
                            data = d
                            data.append(id)
                            a.write(str(data))
                        embed = discord.Embed(title='成功', description="リストに<@{}>を追加しました".format(int(id)) ,color=0x00ff00)
                        embed.set_footer(text=str(await dtnow()))
                        await message.channel.send(embed=embed)
                        member = bot.get_user(id)
                        guild = bot.get_guild(message.guild.id)  #idはint型で
                        mm = guild.get_member(member.id)
                        
                        embed=discord.Embed(title="BAN", color=0xff0000)
                        embed.add_field(name="メンバー", value=str(mm.mention), inline=False)
                        embed.add_field(name="理由", value="グローバルBAN\nIDBAN", inline=False)
                        urll = member.display_avatar
                        embed.set_thumbnail(url=str(urll))
                        userr = discord.utils.get(bot.users, id=int(id))
                        await userr.send(embed=embed)  
                        await message.channel.send(embed=embed) 
                        await mm.ban(delete_message_days=7, reason="グローバルBAN")  
                except IndexError:
                    embed = discord.Embed(title='エラー', description="引数がないため実行できませんでした" ,color=0xff0000)
                    embed.set_footer(text=str(await dtnow()))
                    await message.channel.send(embed=embed)

    #await message.channel.send(str(message.content))
    # 「/neko」と発言したら「にゃーん」が返る処理
    
    # メッセージ送信者がBotだった場合は無視する
    
    if message.author.bot:
        return
    with open("GB/Directory/ngword.json", "r",encoding="utf-8") as f:
        d = json.load(f)
    if os.path.isfile(Strike_guild + "/N-NGword.json"):
        with open(Strike_guild + "/N-NGword.json",'r',encoding="utf-8") as a:
            d = json.load(a)
    if any(x in message.content for x in d):
        
        if os.path.isdir(Strike_guild):
            if not os.path.isfile(Strike_user):
                with open(Strike_user,'w',encoding="utf-8") as a:
                    
                    setting = json.dumps([1,message.author.name], indent=4,ensure_ascii=False)
                    a.write(str(setting))
            if os.path.isfile(Strike_user):
                with open(Strike_user,'r') as a:
                    b = json.load(a)
                with open(Strike_user,'w',encoding="utf-8") as a:
                    
                    setting = json.dumps([b[0] +1,message.author.name], indent=4,ensure_ascii=False)
                    a.write(str(setting))
        if not os.path.isdir(Strike_guild):
            os.mkdir("GB/Strike/S-" + str(mgi))
            os.mkdir(Strike_guild)
            os.mkdir("GB/Strike/S-" + str(mgi) + "/User") #サーバーIDのフォルダー作成
            if not os.path.isfile(Strike_guild + "/S-Setting.json"):
                with open(Strike_guild + "/S-Setting.json",'w') as a:
                    Strike_list = {}
                    Strike_list["timeout_1m"]   = 1
                    Strike_list["timeout_5m"]   = 0
                    Strike_list["timeout_15m"]  = 3
                    Strike_list["timeout_30m"]  = 0
                    Strike_list["timeout_1h"]   = 5
                    Strike_list["timeout_3h"]   = 0
                    Strike_list["timeout_6h"]   = 0
                    Strike_list["timeout_12h"]  = 6
                    Strike_list["timeout_1d"]   = 8
                    Strike_list["timeout_3d"]   = 0
                    Strike_list["timeout_7d"]   = 0
                    Strike_list["timeout_14d"]  = 0
                    Strike_list["timeout_28d"]  = 0
                    Strike_list["kick"]         = 10
                    Strike_list["ban"]          = 15
                    
                    setting = json.dumps(Strike_list, indent=4,ensure_ascii=False)
                    a.write(str(setting))
            if not os.path.isfile(Strike_guild + "/N-NGword.json"):
                with open(Strike_guild + "/N-NGword.json",'w',encoding="utf-8") as a:
                    setting = json.dumps(["死ね"], indent=4,ensure_ascii=False)
                    a.write(str(setting))
            if not os.path.isfile(Strike_guild + "/C-Notice.json"):
                with open(Strike_guild + "/C-Notice.json",'w',encoding="utf-8") as a:
                    setting = json.dumps([0,0,0,1], indent=4,ensure_ascii=False)
                    a.write(str(setting))
            if not os.path.isfile(Strike_guild + "/R-Report.json"):
                with open(Strike_guild + "/R-Report.json",'w',encoding="utf-8") as a:
                    setting = json.dumps([0,0,0], indent=4,ensure_ascii=False)
                    a.write(str(setting))
            


            if not os.path.isfile(Strike_user):
                with open(Strike_user,'w',encoding="utf-8") as a:
                    setting = json.dumps([1,message.author.name], indent=4,ensure_ascii=False)
                    a.write(str(setting))
            if os.path.isfile(Strike_user):
                with open(Strike_user,'r') as a:
                    b = json.load(a)
                with open(Strike_user,'w',encoding="utf-8") as a:
                    setting = json.dumps([b[0] +1,message.author.name], indent=4,ensure_ascii=False)
                    a.write(str(setting))
        with open(Strike_guild + "/S-Setting.json",'r',encoding="utf-8") as a:
            c = json.load(a)
        with open(Strike_user,'r') as a:
            b = json.load(a)
            b = b[0]
        l = ["1m","5m","15m","30m","1h","3h","6h","12h","1d","3d","7d","14d","28d"]
        lt = [60,300,900,1800,3600,10800,21600.43200,86400,259200,604800,1209600,2419200]
        cl = 0xffff00
        if not b >= c["kick"]:
            for i in range(13):
                
                if int(b) >= c["timeout_" + l[i]]:
                    if not c["timeout_" + l[i]] == 0:
                        content = "タイムアウト(" + l[i] + ")"
                        await member_timeout(message.author,int(lt[i]))
                #await member_timeout(message.author,259200)
        await message.delete()
        if b >= c["kick"]:
            cl = 0xff8000
            content = "キック"
            
            await message.author.kick(reason="Test")
        if b >= c["ban"]:
            cl = 0xff0000
            content = "永久BAN"
            await message.author.ban(reason="Test")
        
        #await message.author
        
        with open(Strike_guild + "/C-Notice.json",'r',encoding="utf-8") as a:
            Notice_list = json.load(a)
            Notice=Notice_list[1]
        with open("GB/Directory/log.json",'r',encoding="utf-8") as a:
            Notice_list = json.load(a)
            log=Notice_list[1]
        if not Notice == 0: #レイド通知
            channel = bot.get_channel(Notice)
            embed = discord.Embed(title="NG Word", description=
            "**違反者**：" + str(message.author.mention)+ 
            "\n**時間**　：" + str(await timestamp())+
            "\n **内容**　：" + str(message.content)+
            "\n **処罰**　：" + str(content) +
            "\n **理由**　：" + "NGワード"+
            "\n **回数**　：" + str(b) + "回違反"

            ,color=cl)
            await channel.send(embed=embed)
        if not log == 0: #レイド通知
            channel = bot.get_channel(log)
            embed = discord.Embed(title="NG Word(log)", description=
            "**違反者**：" + str(message.author.mention)+ 
            "\n**時間**　：" + str(await timestamp())+
            "\n **内容**　：" + str(message.content)+
            "\n **処罰**　：" + str(content) +
            "\n **理由**　：" + "NGワード"+
            "\n **回数**　：" + str(b) + "回違反" +
            "\n **サーバー場所**　：" + str(message.guild.id) + "・" + str(message.guild.name) + 
            "\n **チャンネル場所**：" + str(message.channel.id) + "・" + str(message.channel.mention) +
            "\n **サーバー所有者**：" + str(message.guild.owner.id) + "・" + str(message.guild.owner.mention)
            ,color=cl)
            
            await channel.send(embed=embed)
        
    # 招待リンク
    if any(x in message.content for x in ["https://discord.gg"]):
        await member_timeout(message.author,int(2419200))
        await message.delete()
        with open(Strike_guild + "/C-Notice.json",'r',encoding="utf-8") as a:
            Notice_list = json.load(a)
            Notice=Notice_list[1]
        with open("GB/Directory/log.json",'r',encoding="utf-8") as a:
            Notice_list = json.load(a)
            log=Notice_list[1]
        if not Notice == 0: #レイド通知
            channel = bot.get_channel(Notice)
            embed = discord.Embed(title="通常レイド[招待リンク]", description=
            "**違反者**：" + str(message.author.mention)+ 
            "\n**時間**　：" + str(await timestamp())+
            "\n **内容**　：" + str(message.content)+
            "\n **処罰**　：" + "タイムアウト(28日)"+
            "\n **理由**　：" + "招待リンク" 
            ,color=0xaa0000)
            
            await channel.send(embed=embed)
        if not log == 0: #レイド通知
            channel = bot.get_channel(log)
            embed = discord.Embed(title="通常レイド[招待リンク](log)", description=
            "**違反者**：" + str(message.author.mention)+ 
            "\n**時間**　：" + str(await timestamp())+
            "\n **内容**　：" + str(message.content)+
            "\n **処罰**　：" + "タイムアウト(28日)"+
            "\n **理由**　：" + "招待リンク" +
            "\n **サーバー場所**　：" + str(message.guild.id) + "・" + str(message.guild.name) + 
            "\n **チャンネル場所**：" + str(message.channel.id) + "・" + str(message.channel.mention) +
            "\n **サーバー所有者**：" + str(message.guild.owner.id) + "・" + str(message.guild.owner.mention)
            ,color=0xaa0000)
            
            await channel.send(embed=embed)
            
    #緊急レイド検出
    with open("GB/Directory/ERP.json",'r',encoding="utf-8") as a:
        erp = json.load(a)
        erp = list(erp)
    if any(x in message.content for x in erp):
        await message.delete()
        await message.author.ban(reason="緊急レイド[荒らしの可能性]")
        
        with open(Strike_guild + "/C-Notice.json",'r',encoding="utf-8") as a:
            Notice_list = json.load(a)
            Notice=Notice_list[2]
        with open("GB/Directory/log.json",'r',encoding="utf-8") as a:
            Notice_list = json.load(a)
            log=Notice_list[2]
        if not Notice == 0: #緊急レイド通知
            channel = bot.get_channel(Notice)
            embed = discord.Embed(title="緊急レイド検出", description=
            "**違反者**：" + str(message.author.mention)+ 
            "\n**時間**　：" + str(await timestamp())+
            "\n **内容**　：" + str(message.content)+
            "\n **処罰**　：" + "BAN"+
            "\n **理由**　：" + "荒らしの可能性高" 
            ,color=0x550000)
            
            await channel.send(embed=embed)
        if not log == 0: #緊急レイド通知
            channel = bot.get_channel(log)
            embed = discord.Embed(title="緊急レイド検出(log)", description=
            "**違反者**：" + str(message.author.mention)+ 
            "\n**時間**　：" + str(await timestamp())+
            "\n **内容**　：" + str(message.content)+
            "\n **処罰**　：" + "BAN"+
            "\n **理由**　：" + "荒らしの可能性高" +
            "\n **サーバー場所**　：" + str(message.guild.id) + "・" + str(message.guild.name) + 
            "\n **チャンネル場所**：" + str(message.channel.id) + "・" + str(message.channel.mention) +
            "\n **サーバー所有者**：" + str(message.guild.owner.id) + "・" + str(message.guild.owner.mention)
            ,color=0x550000)
            
            await channel.send(embed=embed)
            
    # 
async def member_timeout(member,seconds):
    await member.timeout(discord.utils.utcnow() + datetime.timedelta(seconds=seconds))

@bot.listen()
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    mgi = message.guild.id
    mai = message.author.id
    Strike_user = "GB/Strike/S-" + str(mgi) + "/User/U-" + str(mai) + ".json"
    Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
    if message.author.bot:
        return
    if os.path.isdir(Strike_guild):
        if not os.path.isfile(Strike_user):
            with open(Strike_user,'w',encoding="utf-8") as a:
                setting = json.dumps([0,message.author.name], indent=4,ensure_ascii=False)
                a.write(str(setting))
        if not os.path.isfile(Strike_guild + "/S-Setting.json"):
            with open(Strike_guild + "/S-Setting.json",'w') as a:
                Strike_list = {}
                Strike_list["timeout_1m"]   = 1
                Strike_list["timeout_5m"]   = 0
                Strike_list["timeout_15m"]  = 3
                Strike_list["timeout_30m"]  = 0
                Strike_list["timeout_1h"]   = 5
                Strike_list["timeout_3h"]   = 0
                Strike_list["timeout_6h"]   = 0
                Strike_list["timeout_12h"]  = 6
                Strike_list["timeout_1d"]   = 8
                Strike_list["timeout_3d"]   = 0
                Strike_list["timeout_7d"]   = 0
                Strike_list["timeout_14d"]  = 0
                Strike_list["timeout_28d"]  = 0
                Strike_list["kick"]         = 10
                Strike_list["ban"]          = 15
                
                setting = json.dumps(Strike_list, indent=4,ensure_ascii=False)
                a.write(str(setting))
        if not os.path.isfile(Strike_guild + "/N-NGword.json"):
            with open(Strike_guild + "/N-NGword.json",'w',encoding="utf-8") as a:
                setting = json.dumps(["死ね"], indent=4,ensure_ascii=False)
                a.write(str(setting))
        if not os.path.isfile(Strike_guild + "/C-Notice.json"):
            with open(Strike_guild + "/C-Notice.json",'w',encoding="utf-8") as a:
                setting = json.dumps([0,0,0,1], indent=4,ensure_ascii=False)
                a.write(str(setting))
        if not os.path.isfile(Strike_guild + "/R-Report.json"):
            with open(Strike_guild + "/R-Report.json",'w',encoding="utf-8") as a:
                setting = json.dumps([0,0,0], indent=4,ensure_ascii=False)
                a.write(str(setting))
        if not os.path.isfile(Strike_guild + "/P-Prefix.json"):
            with open(Strike_guild + "/P-Prefix.json",'w',encoding="utf-8") as a:
                setting = json.dumps(["se!","se."], indent=4,ensure_ascii=False)
                a.write(str(setting))
        
    if not os.path.isdir(Strike_guild):
        os.mkdir("GB/Strike/S-" + str(mgi))
        os.mkdir(Strike_guild)
        os.mkdir("GB/Strike/S-" + str(mgi) + "/User") #サーバーIDのフォルダー作成
        if not os.path.isfile(Strike_user):
            with open(Strike_user,'w',encoding="utf-8") as a:
                setting = json.dumps([0,message.author.name], indent=4,ensure_ascii=False)
                a.write(str(setting))
        if not os.path.isfile(Strike_guild + "/S-Setting.json"):
            with open(Strike_guild + "/S-Setting.json",'w') as a:
                Strike_list = {}
                Strike_list["timeout_1m"]   = 1
                Strike_list["timeout_5m"]   = 0
                Strike_list["timeout_15m"]  = 3
                Strike_list["timeout_30m"]  = 0
                Strike_list["timeout_1h"]   = 5
                Strike_list["timeout_3h"]   = 0
                Strike_list["timeout_6h"]   = 0
                Strike_list["timeout_12h"]  = 6
                Strike_list["timeout_1d"]   = 8
                Strike_list["timeout_3d"]   = 0
                Strike_list["timeout_7d"]   = 0
                Strike_list["timeout_14d"]  = 0
                Strike_list["timeout_28d"]  = 0
                Strike_list["kick"]         = 10
                Strike_list["ban"]          = 15
            
                setting = json.dumps(Strike_list, indent=4,ensure_ascii=False)
                a.write(str(setting))
        if not os.path.isfile(Strike_guild + "/N-NGword.json"):
            with open(Strike_guild + "/N-NGword.json",'w',encoding="utf-8") as a:
                setting = json.dumps(["死ね"], indent=4,ensure_ascii=False)
                a.write(str(setting))
        if not os.path.isfile(Strike_guild + "/C-Notice.json"):
            with open(Strike_guild + "/C-Notice.json",'w',encoding="utf-8") as a:
                setting = json.dumps([0,0,0,1], indent=4,ensure_ascii=False)
                a.write(str(setting))
        if not os.path.isfile(Strike_guild + "/R-Report.json"):
            with open(Strike_guild + "/R-Report.json",'w',encoding="utf-8") as a:
                setting = json.dumps([0,0,0], indent=4,ensure_ascii=False)
                a.write(str(setting))
        if not os.path.isfile(Strike_guild + "/P-Prefix.json"):
            with open(Strike_guild + "/P-Prefix.json",'w',encoding="utf-8") as a:
                setting = json.dumps(["se!","se."], indent=4,ensure_ascii=False)
                a.write(str(setting))
        

@bot.tree.command(name="pc_info",description="PCの状態や情報")
async def pcinfo(ctx:discord.Interaction):
    

    # 直線の描画
    
    cpu_used = psutil.cpu_percent()
    hostname = socket.gethostname()
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    btr = psutil.sensors_battery()  
    cpu = {"GALLERIA":"Ryzen 5 5600X","Celeron":"Celeron 3865U"} 
    gpu = {"GALLERIA":"RX 6600 XT","Celeron":"Intel Graphics UHD 610"} 
    embed = discord.Embed(title='ホスト名：' + str(hostname), description=
    "CPU コア：" + str(psutil.cpu_count(logical=False)) + "\n" +
    "CPU スレッド：" + str(psutil.cpu_count()) + "\n" + 
    "CPU 個別使用率：" + str(psutil.cpu_percent(percpu=True)) + "\n" + 
    "RAM 合計：" + str(round(ram.total / 1024 ** 3,2)) + "GB\n" +
    "RAM 使用量：" + str(round(ram.used / 1024 ** 3,2)) + "GB\n" +
    "RAM 空き：" + str(round(ram.available / 1024 ** 3,2)) + "GB\n" + 
    "DISK 合計：" + str(round(disk.total / 1024 ** 3,2)) + "GB\n" +
    "DISK 使用量：" + str(round(disk.used / 1024 ** 3,2)) + "GB\n" +
    "DISK 空き：" + str(round(disk.free / 1024 ** 3,2)) + "GB\n" + 
    "CPU 名称：" + str(cpu[str(hostname)]) +  "\n" + 
    "GPU 名称：" + str(gpu[str(hostname)]) +  "\n"
    ,color=0x0080ff)
    img = Image.new("RGB", (500, 150), "White")
    font = ImageFont.truetype('GB/Directory/やさしさゴシック手書き.ttf', 24)
    draw = ImageDraw.Draw(img)

    c , r , d = cpu_used * 5 , ram.percent*5 , disk.percent*5
    for i in range(10):
        draw.line([(i*50 +50,0), (i*50 +50, 150)], fill = "Gray", width = 2)
    for i in range(2):
        draw.line([(0,i*50 +50), (500, i*50 +50)], fill = "Gray", width = 2)
    draw.line([(0, 25), (c, 25)], fill = "Red", width = 51)
    draw.line([(0, 75), (r, 75)], fill = "Green", width = 50)
    draw.line([(0, 125), (d, 125)], fill = "Blue", width = 50)
    
    draw.multiline_text((10, 12.5), "CPU使用率：" + str(cpu_used),"White",stroke_width=3,stroke_fill='black',spacing=10, align='center',font=font)
    draw.multiline_text((10, 62.5), "RAM使用率：" + str(ram.percent),"White",stroke_width=3,stroke_fill='black',spacing=10, align='center',font=font)
    draw.multiline_text((10, 112.5), "DISK使用率：" + str(disk.percent),"White",stroke_width=3,stroke_fill='black',spacing=10, align='center',font=font)
    # 画像の表示
    img.save("GB/Directory/pc_info.png")
    file = discord.File("GB/Directory/pc_info.png", filename="image.png")
    embed.set_footer(text=str(await dtnow()))
    embed.set_image(url="attachment://image.png")
    #embed.set_author(name="Test",url=str(url),icon_url="TEST")
    await ctx.response.send_message(file=file,embed=embed)





# --- ID BAN ---
@bot.command(aliases=['gba'])
async def global_ban_add(ctx,ind:int):
    uid = await admin_id()
    if ctx.author.id in uid:
        await gba1(ctx,ind)
    if not ctx.author.id in uid:
        embed = discord.Embed(title='実行エラー', description="権限がないため実行できません" ,color=0xff0000)
        embed.set_footer(text=str(await dtnow()))
        await ctx.send(embed=embed)
# --- ID BAN List ---
@bot.command(aliases=['list'])
async def global_ban_list(ctx):
    uid = await admin_id()
    if ctx.author.id in uid:
        with open("GB/Directory/id.json",'r') as a:
            d = json.load(a)
            e = []
            for x in d:
                e.append("<@{}>\n".format(int(x)))
            e = ''.join(e)
        embed = discord.Embed(title='グローバルBANリスト', description=str(e) ,color=0x0080ff)
        embed.set_footer(text=str(await dtnow()))
        await ctx.send(embed=embed)
    if not ctx.id in uid:
        embed = discord.Embed(title='実行エラー', description="権限がないため実行できません" ,color=0xff0000)
        embed.set_footer(text=str(await dtnow()))
        await ctx.send(embed=embed)


# --- ID BAN 1 ---
async def gba1 (ctx,ind):
    with open("GB/Directory/id.json",'r') as a:
        d = json.load(a)
    if ind in d :
        embed = discord.Embed(title='エラー', description="既にそのユーザーIDはGBANに登録しています" ,color=0xff0000)
        embed.set_footer(text=str(await dtnow()))
        await ctx.send(embed=embed)
    else:
        class HButton(discord.ui.View):
            def __init__(self,args):
                super().__init__()

                for txt in args:
                    self.add_item(Button(txt))

        class Button(discord.ui.Button):
            def __init__(self,txt:str,):
                
                super().__init__(label=txt,style=discord.ButtonStyle.grey)
                if str(self.label) == 'はい':
                    self.style=discord.ButtonStyle.red
                if str(self.label) == 'いいえ':
                    self.style=discord.ButtonStyle.green
            async def callback(self, interaction: discord.Interaction):

                uid = await admin_id()
                if interaction.user.id in uid :
                    await interaction.response.edit_message(content=str(self.label))
                    if self.label == 'はい':
                        await bann(ctx,ind,d)
        await ctx.reply("GBANしますか？",view=HButton(("はい","いいえ")))
# --- ID BAN 2 ---
async def bann(ctx,ind,d):
    with open("GB/Directory/id.json",'w') as a:
        data = d
        data.append(ind)
        a.write(str(data))
        with open("GB/Directory/id.json",'r') as a:
            d = json.load(a)
            e = []
            for x in d:
                e.append("<@{}>\n".format(int(x)))
            e = ''.join(e)
    embed = discord.Embed(title='成功', description="リストに<@{}>を追加しました".format(int(ind)) ,color=0x00ff00)
    embed.set_footer(text=str(await dtnow()))
    await ctx.send(embed=embed)
    member = bot.get_user(ind)
    guild = bot.get_guild(ctx.guild.id)  #idはint型で
    mm = guild.get_member(member.id)
    
    embed=discord.Embed(title="BAN", color=0xff0000)
    embed.add_field(name="メンバー", value=str(mm.mention), inline=False)
    embed.add_field(name="理由", value="グローバルBAN\nIDBAN", inline=False)
    urll = member.display_avatar
    embed.set_thumbnail(url=str(urll))
    userr = discord.utils.get(bot.users, id=int(ind))
    await userr.send(embed=embed)  
    await ctx.send(embed=embed) 
    await mm.ban(delete_message_days=7, reason="グローバルBAN")    










# --- Channel ---
@bot.tree.command(name="channel", description="GBANチャンネル通知の設定 ")
async def channel_id(ctx:discord.Interaction,gban:discord.TextChannel):
    
    if ctx.user.guild_permissions.administrator:
        mgi = ctx.guild_id
        Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
        if os.path.isfile(Strike_guild + "/C-Notice.json"):
            with open(Strike_guild + "/C-Notice.json",'r',encoding="utf-8") as a:
                d = json.load(a)
            gban_id = 0
            gm =  "なし"
            if not gban == None:
                gban_id = gban.id
                gm = gban.mention
            
            with open(Strike_guild + "/C-Notice.json",'w',encoding="utf-8") as a:
                Notice_list = [gban_id,d[1],d[2],d[3]]
                setting = json.dumps(Notice_list, indent=4,ensure_ascii=False)
                a.write(str(setting))
            embed = discord.Embed(title='通知設定', description="変更しました。\n"
            +"通常Gban:"+str(gm)+"\n"
            +"通常Raid:<#"+str(d[1])+">\n"
            +"緊急Raid:<#"+str(d[2])+">"
            ,color=0x0080ff)
        if not os.path.isfile(Strike_guild + "/C-Notice.json"):
            embed = discord.Embed(title='通知設定(エラー)', description="通知のデータが見つかりませんでした。",color=0xff0000)

            
    else:
        embed = discord.Embed(title='権限エラー', description="あなたは実行することができません",color=0xff0000)
    await ctx.response.send_message(embed=embed)

#---------------------------------------------
# NAME Change
#---------------------------------------------
@bot.tree.command(name="name",description="名前フィルター機能に名前を追加",)
@discord.app_commands.describe(name="名前")
@discord.app_commands.rename(name="name")
async def gban_name(ctx:discord.Interaction,name:str):
    uid = await admin_id()
    if ctx.user.id in uid:
        with open("GB/Directory/name.json",'r') as a:
            n = json.load(a)
        if not "" == name:
            if not name in n:
                with open("GB/Directory/name.json",'r') as a:
                    n = json.load(a)
                with open("GB/Directory/name.json",'w') as a:
                    nn = list(n)
                    nn.append(str(name))
                    j= json.dumps(nn)
                    a.write(j)
                
                embed = discord.Embed(title='成功', description="リストに`" + str(name) + "`を追加しました" ,color=0x00ff00)
                embed.set_footer(text=str(await dtnow()))
                await ctx.response.send_message(embed=embed)
                
            if name in n:
                with open("GB/Directory/name.json",'w') as a:
                    nn = list(n)
                    nn.remove(str(name))
                    j= json.dumps(nn)
                    a.write(j)
                embed = discord.Embed(title='成功', description="リストに`" + str(name) + "`を削除しました" ,color=0xff0000)
                embed.set_footer(text=str(await dtnow()))
                await ctx.response.send_message(embed=embed)

@bot.command(aliases=['name'])
async def gban_name(ctx,name:str):
    uid = await admin_id()
    if ctx.author.id in uid:
        with open("GB/Directory/name.json",'r') as a:
            n = json.load(a)
        if not "" == name:
            if not name in n:
                with open("GB/Directory/name.json",'r') as a:
                    n = json.load(a)
                with open("GB/Directory/name.json",'w') as a:
                    nn = list(n)
                    nn.append(str(name))
                    j= json.dumps(nn)
                    a.write(j)
                
                embed = discord.Embed(title='成功', description="リストに`" + str(name) + "`を追加しました" ,color=0x00ff00)
                embed.set_footer(text=str(await dtnow()))
                await ctx.send(embed=embed)
                
            if name in n:
                with open("GB/Directory/name.json",'w') as a:
                    nn = list(n)
                    nn.remove(str(name))
                    j= json.dumps(nn)
                    a.write(j)
                embed = discord.Embed(title='成功', description="リストに`" + str(name) + "`を削除しました" ,color=0xff0000)
                embed.set_footer(text=str(await dtnow()))
                await ctx.send(embed=embed)


@bot.tree.command(name="name_list",description="名前リスト",)

async def name_listt(ctx:discord.Interaction):
    uid = await admin_id()
    if ctx.user.id in uid:
        with open("GB/Directory/name.json",'r') as a:
            d = json.load(a)
        embed = discord.Embed(title='グローバルBANリスト[name]', description=str(d) ,color=0x0080ff)
        embed.set_footer(text=str(await dtnow()))
        await ctx.response.send_message(embed=embed)
    if not ctx.id in uid:
        embed = discord.Embed(title='実行エラー', description="権限がないため実行できません" ,color=0xff0000)
        embed.set_footer(text=str(await dtnow()))
        await ctx.response.send_message(embed=embed)

@bot.tree.command(name="help",description="ヘルプコマンド")
async def help(ctx:discord.Interaction):
    mgi = ctx.guild.id
    mai = ctx.user.id
    Strike_user = "GB/Strike/S-" + str(mgi) + "/User/U-" + str(mai) + ".json"
    Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
    if os.path.isfile(Strike_guild + "/P-Prefix.json"):
        with open(Strike_guild + "/P-Prefix.json",'r',encoding="utf-8") as a:
            d = list(json.load(a))
        prefix_data =  d
    if not os.path.isfile(Strike_guild + "/P-Prefix.json"):
        prefix_data = ["se!","se."]
    text = ""
    for c,item in enumerate(prefix_data):
        text += "`" + str(item) + "`\n"
    embed = discord.Embed(title='HELP お困りですか？', description="接頭辞一覧:\n" + str(text) ,color=0x0080ff)
    
    embed.add_field(name="gbs",value="GBANの設定（GBAN無効/有効化・GBAN実行時の通知切り替え）",inline=False)
    embed.add_field(name="channel",value="GBAN実行時の通知チャンネルを設定する",inline=False)
    embed.add_field(name="info",value="Botの情報",inline=False)
    embed.set_footer(text=str(await dtnow()))
    await ctx.response.send_message(embed=embed)

@bot.command(aliases=['ha'])
async def help_admin(ctx):
    if ctx.author.id in await admin_id():
        embed = discord.Embed(title='HELP_ADMIN', description="接頭辞`!AVO`\n **`AVO階級３以上 限定のBot管理コマンド`**" ,color=0x0080ff)
        embed.add_field(name="gba - GBAN者追加",value="**使い方**\n❶`!AVO gba * `入力します\n❷ * はユーザーIDです `整数型` \n❸GBAN確認button[はい,いいえ]が出てきます\n❹それを押してください \n❺成功って表示されたらOKです",inline=False)
        embed.add_field(name="name - 名前フィルター機能に名前を追加",value="**使い方**\n❶`!AVO name * `入力します\n❷ * は名前です `文字型`\n❸ それで追加します　削除するときはもう一度同じように送信をします",inline=False)
        embed.set_footer(text=str(await dtnow()))
        embed.set_author(name="Tamu Home Page",url="https://sites.google.com/view/tamu1256tt/home",icon_url="https://cdn.discordapp.com/avatars/831453621732245534/a376406165e34fb16ad2f5ddc5f82e20.png?size=1024")
        await ctx.send(embed=embed)
    
@bot.tree.command(name="ping",description="Ping!")
async def pinging(ctx:discord.Interaction):
    # ミリ秒に変換して丸めるPaPage
    ping = round(float(bot.latency) * 1000)
    embed = discord.Embed(title='Ping', description=str(ping) + "ms" ,color=0x0080ff)
    await ctx.response.send_message(embed=embed)

@bot.tree.command(name="info",description="Botについて")
async def info(ctx:discord.Interaction):
    url = "https://discord.com/api/oauth2/authorize?client_id=1038352771117744208&permissions=1100317060222&scope=bot%20applications.commands"
    # ミリ秒に変換して丸める
    #ping = round(float(bot.latency) * 1000)
    #embed = discord.Embed(title='Ping', description=str(ping) + "ms" ,color=0x0080ff)
    #await ctx.response.send_message(embed=embed)
    text001 = "このBotは反荒らし組織/AVOが開発・運営をしている、グローバルBANを主な機能とした荒らし対策BOTです。AVOのメンバーが登録した荒らしが導入サーバーで「サーバーに入室したとき」や「サーバーで発言したとき」に自動でBANしてくれます！"
    text002 = "\n✨Bot導入は[こちら](https://discord.com/api/oauth2/authorize?client_id=1038352771117744208&permissions=1100317060222&scope=bot%20applications.commands)✨"
    text003 = "\n👍反荒らし組織/AVOは[こちら](https://discord.gg/tZz5suP4my)👍"
    Text001 = str(text001)
    embed = discord.Embed(title='Bot info', description=str(Text001),color=0x0080ff)
    
    embed.add_field(name="✨Bot導入はこちら✨",value="[BOT招待リンク](" + str(url) + ")",inline=False)
    embed.add_field(name="👍反荒らし組織/AVOはこちら👍",value="[Discordサーバー](https://discord.gg/tZz5suP4my)",inline=False)

    embed.set_footer(text=str(await dtnow()))
    embed.set_author(name="/helpで他のコマンドを表示します",url=str(url),icon_url="https://cdn.discordapp.com/avatars/1038352771117744208/610f103baa2b90afc75aa654b7b63815.png?size=1024")
    await ctx.response.send_message(embed=embed)

@bot.command()
async def info(ctx):
    url = "https://discord.com/api/oauth2/authorize?client_id=1038352771117744208&permissions=1100317060222&scope=bot%20applications.commands"
    # ミリ秒に変換して丸める
    #ping = round(float(bot.latency) * 1000)
    #embed = discord.Embed(title='Ping', description=str(ping) + "ms" ,color=0x0080ff)
    #await ctx.response.send_message(embed=embed)
    text001 = "このBotは反荒らし組織/AVOが開発・運営をしている、グローバルBANを主な機能とした荒らし対策BOTです。AVOのメンバーが登録した荒らしが導入サーバーで「サーバーに入室したとき」や「サーバーで発言したとき」に自動でBANしてくれます！"
    text002 = "\n✨Bot導入は[こちら](https://discord.com/api/oauth2/authorize?client_id=1038352771117744208&permissions=1100317060222&scope=bot%20applications.commands)✨"
    text003 = "\n👍反荒らし組織/AVOは[こちら](https://discord.gg/tZz5suP4my)👍"
    Text001 = str(text001)
    embed = discord.Embed(title='Bot info', description=str(Text001),color=0x0080ff)
    
    embed.add_field(name="✨Bot導入はこちら✨",value="[BOT招待リンク](" + str(url) + ")",inline=False)
    embed.add_field(name="👍反荒らし組織/AVOはこちら👍",value="[Discordサーバー](https://discord.gg/tZz5suP4my)",inline=False)

    embed.set_footer(text=str(await dtnow()))
    embed.set_author(name="/helpで他のコマンドを表示します",url=str(url),icon_url="https://cdn.discordapp.com/avatars/1038352771117744208/610f103baa2b90afc75aa654b7b63815.png?size=1024")
    await ctx.send(embed=embed)

async def admin_id():
    list001 = [788962233375653901,8328609743356559964,831453621732245534]
    return list001

@bot.command()
async def annouce(ctx,num:str = 0):
    
    announcementChannel = bot.get_channel(1039502411292737568)
    cha = bot.get_channel(int(num))
    if num == 0:
        cha = ctx.channel
    await announcementChannel.follow(destination = cha, reason=None)
    await ctx.send("OK")

@bot.tree.command(name="annouce",description="アナウンス")
async def annouce(ctx:discord.Interaction,num:str = None):
    
    announcementChannel = bot.get_channel(1039502411292737568)
    cha = bot.get_channel(int(num))
    if num == None:
        cha = ctx.channel
    await announcementChannel.follow(destination = cha, reason=None)
    await ctx.response.send_message("OK")
    
@bot.tree.command(name="status",description="ステータス")
async def status(ctx:discord.Interaction):
    a = socket.gethostname()
    embed = discord.Embed(title='ホスト名', description=str(a),color=0x0080ff)
    with open("GB/Directory/time.json",'r') as a:
            ti = json.load(a)
            day = ti[0]
            hour = ti[1]
            minutes = ti[2]
            pen = ti[3]
            start_time = str(pen[0]) + "年" + str(pen[1]) + "月" + str(pen[2]) + "日" + str(pen[3]) + "時" + str(pen[4]) + "分" + str(pen[5]) + "秒"
    embed.add_field(name="稼働",value=str(day) + "日" + str(hour) + "時" + str(minutes) + "分",inline=False)
    embed.add_field(name="稼働開始時刻",value=str(start_time),inline=False)
    member = ctx.guild.get_member(1038352771117744208)
    if str(member.status) == "online":
        text = "オンライン"
    if str(member.status) == "offline":
        text = "オフライン"
    if str(member.status) == "idle":
        text = "退席中"
    if str(member.status) == "dnd":
        text = "取り込み中"
    embed.add_field(name="状況",value=str(text),inline=False)

    embed.set_footer(text=str(await dtnow()))
    #embed.set_author(name="Test",url=str(url),icon_url="TEST")
    await ctx.response.send_message(embed=embed)

class Modal(discord.ui.Modal):
    def __init__(self,text):
        super().__init__(title="お問い合わせ内容")
        self.t = text
        self.answer = ui.TextInput(label='本文', style=discord.TextStyle.paragraph)
        self.add_item(self.answer)
    
    async def on_submit(self, interaction: discord.Interaction):
        

        c = bot.get_channel(1051474147412291644)
        li = {"bug":"❗バグ報告","human":"🆔誤BAN報告（人物）","name":"🚹誤BAN報告（名前）","hey":"🈸機能提案"}

        embed = discord.Embed(title='問い合わせ' + str(li[str(self.t)]), description="",color=0xffff00)
        embed.add_field(name="本文",value=self.answer.value,inline=False)
        embed.add_field(name="送信者ユーザー",value="送信者：" + str(interaction.user.mention) ,inline=False)
        embed.add_field(name="送信元サーバー",value="送信元：" + str(interaction.guild.name) + "・" + str(interaction.guild.id),inline=False)

        embed.set_footer(text=str(await dtnow()))
        await c.send(embed=embed)
        await interaction.response.defer()



@bot.tree.command(name="inquiry",description="お問い合わせ")
@discord.app_commands.rename(text="type")
@discord.app_commands.choices(
    text=[
        discord.app_commands.Choice(name="バグ",value="bug"),
        discord.app_commands.Choice(name="誤BAN報告（人物）",value="human"),
        discord.app_commands.Choice(name="誤BAN報告（名前）",value="name"),
        discord.app_commands.Choice(name="機能提案",value="hey")
    ]
)
async def inquiry(ctx:discord.Interaction,text:str):
    
    embed = discord.Embed(title='inquiry', description=str(text),color=0x0080ff)
    await ctx.response.send_modal(Modal(text))
    await ctx.followup.send(content="問い合わせました")
    
    
@bot.tree.command(name="strike_setting",description="ストライキ設定")
@discord.app_commands.rename(type="type")
@discord.app_commands.choices(
    type=[
        discord.app_commands.Choice(name="タイムアウト(1分)",value="timeout_1m"),
        discord.app_commands.Choice(name="タイムアウト(5分)",value="timeout_5m"),
        discord.app_commands.Choice(name="タイムアウト(15分)",value="timeout_15m"),
        discord.app_commands.Choice(name="タイムアウト(30分)",value="timeout_30m"),
        discord.app_commands.Choice(name="タイムアウト(1時間)",value="timeout_1h"),
        discord.app_commands.Choice(name="タイムアウト(3時間)",value="timeout_3h"),
        discord.app_commands.Choice(name="タイムアウト(6時間)",value="timeout_6h"),
        discord.app_commands.Choice(name="タイムアウト(12時間)",value="timeout_12h"),
        discord.app_commands.Choice(name="タイムアウト(1日)",value="timeout_1d"),
        discord.app_commands.Choice(name="タイムアウト(3日)",value="timeout_3d"),
        discord.app_commands.Choice(name="タイムアウト(7日)",value="timeout_7d"),
        discord.app_commands.Choice(name="タイムアウト(14日)",value="timeout_14d"),
        discord.app_commands.Choice(name="タイムアウト(28日)",value="timeout_28d"),
        discord.app_commands.Choice(name="キック",value="kick"),
        discord.app_commands.Choice(name="BAN",value="ban")
    ]
)
async def strike_setting(ctx:discord.Interaction,type:str,value:app_commands.Range[int,0,None]):
    if ctx.user.guild_permissions.administrator:
        Strike_guild = "GB/Strike/S-" + str(ctx.guild_id)
        with open(Strike_guild + "/S-Setting.json",'r') as a:
            Strike_list = json.load(a)
        with open(Strike_guild + "/S-Setting.json",'w') as a:
            Strike_list[type] = value
            Strike_list = setting = json.dumps(Strike_list, indent=4,ensure_ascii=False)
            a.write(str(setting))
        with open(Strike_guild + "/S-Setting.json",'r') as a:
            New_strike_list = json.load(a)
        Second_strike_list = ""
        for list_key, list_value in New_strike_list.items():
            if not list_value == 0:
                Second_strike_list += "`" + str(list_key) + "`：" + "**" + str(list_value) + "**\n"
            if list_value == 0:
                pass
        embed = discord.Embed(title='ストライキ設定', description=str(Second_strike_list),color=0x0080ff)
    if not ctx.user.guild_permissions.administrator:
        embed = discord.Embed(title='権限エラー', description="あなたは`管理者権限`を持っていないため実行することができません",color=0xff0000)    
    await ctx.response.send_message(embed=embed)

@bot.tree.command(name="strike_user_show",description="ストライキユーザー情報")
async def strike_user(ctx:discord.Interaction,user:discord.Member):
    if ctx.user.guild_permissions.administrator:
        mgi = ctx.guild_id
        mai = user.id
        Strike_user = "GB/Strike/S-" + str(mgi) + "/User/U-" + str(mai) + ".json"
        if os.path.isfile(Strike_user):
            with open(Strike_user,'r') as a:
                b = json.load(a)
                b = b[0]
            l = {True:"はい",False:"いいえ"}
            embed = discord.Embed(title='ストライキユーザー', description=
            "**ユーザー**：" + str(user.mention) + 
            "\n**ストライキ回数**：" + str(b)+
            "\n**タイムアウト中**：" + str(l[user.is_timed_out()]),color=0x0080ff)
        if not os.path.isfile(Strike_user):
            embed = discord.Embed(title='ストライキユーザー(エラー)', description="そのユーザーのデータが見つかりませんでした。",color=0xff0000)
    if not ctx.user.id in await admin_id():
        embed = discord.Embed(title='権限エラー', description="あなたは実行することができません",color=0xff0000)    
    await ctx.response.send_message(embed=embed,ephemeral=True)

@bot.tree.command(name="strike_user_set",description="ストライキユーザーの点数を設定")
async def strike_user_set(ctx:discord.Interaction,user:discord.Member,strike_set:app_commands.Range[int,0,None]):
    if ctx.user.id in await admin_id():
        mgi = ctx.guild_id
        mai = user.id
        Strike_user = "GB/Strike/S-" + str(mgi) + "/User/U-" + str(mai) + ".json"
        if os.path.isfile(Strike_user):
            with open(Strike_user,'r',encoding="utf-8") as a:
                b = json.load(a)
                b = b[0]
            with open(Strike_user,'w',encoding="utf-8") as a:
                setting = json.dumps([strike_set,user.name], indent=4,ensure_ascii=False)
                a.write(str(setting))
            
            l = {True:"はい",False:"いいえ"}
            embed = discord.Embed(title='ストライキユーザー設定', description=
            "**ユーザー**：" + str(user.mention) + 
            "\n**ストライキ回数**：" + str(strike_set)+
            "\n**タイムアウト中**：" + str(l[user.is_timed_out()]),color=0x0080ff)
        if not os.path.isfile(Strike_user):
            embed = discord.Embed(title='ストライキユーザー設定(エラー)', description="そのユーザーのデータが見つかりませんでした。",color=0xff0000)
    if not ctx.user.id in await admin_id():
        embed = discord.Embed(title='権限エラー', description="あなたは実行することができません",color=0xff0000)    
    await ctx.response.send_message(embed=embed,ephemeral=True)

@bot.tree.command(name="ngword_change",description="NGワードを編集")
async def ngword(ctx:discord.Interaction,text:str):
    mgi = ctx.guild_id
    if ctx.user.guild_permissions.administrator:
        Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
        if os.path.isfile(Strike_guild + "/N-NGword.json"):
            with open(Strike_guild + "/N-NGword.json",'r',encoding="utf-8") as a:
                d = json.load(a)
                ngword_list = list(d)
            if not text in list(d):
                with open(Strike_guild + "/N-NGword.json",'w') as a:
                    ngword_list.append(text)
                    setting = json.dumps(ngword_list, indent=4,ensure_ascii=False)
                    a.write(str(setting))
                embed = discord.Embed(title='NGワード', description="NGワードを追加しました\n`" + str(text) + "`" ,color=0x00ff00)
            print(ngword_list)
            if text in list(d):
                with open(Strike_guild + "/N-NGword.json",'w',encoding="utf-8") as a:
                    ngword_list.remove(text)
                    setting = json.dumps(ngword_list, indent=4,ensure_ascii=False)
                    a.write(str(setting))
                embed = discord.Embed(title='NGワード', description="NGワードを削除しました\n`" + str(text) + "`" ,color=0xff0000)
        if not os.path.isfile(Strike_guild + "/N-NGword.json"):
            embed = discord.Embed(title='NGワード(エラー)', description="そのユーザーのデータが見つかりませんでした。",color=0xff0000)
    else:
        embed = discord.Embed(title='権限エラー', description="あなたは`管理者権限`を持っていないため実行することができません",color=0xff0000)

    await ctx.response.send_message(embed=embed)

@bot.tree.command(name="ngword_list",description="NGワードリスト")
async def ngword_list(ctx:discord.Interaction):
    if ctx.user.guild_permissions.administrator:
        mgi = ctx.guild_id
        Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
        if os.path.isfile(Strike_guild + "/N-NGword.json"):
            with open(Strike_guild + "/N-NGword.json",'r',encoding="utf-8") as a:
                d = json.load(a)
        ngword_list = ""
        for i in range(len(d)):
            ngword_list += "`" + d[i] + "`,"
        embed = discord.Embed(title='NGワードリスト', description=ngword_list,color=0x0080ff)
    else:
        embed = discord.Embed(title='権限エラー', description="あなたは`管理者権限`を持っていないため実行することができません",color=0xff0000)

        await ctx.response.send_message(embed=embed)

@bot.tree.command(name="erp_change",description="緊急レイドワードを編集")
async def erp(ctx:discord.Interaction,text:str):
    if ctx.channel_id == 1051116779365208064:
        if ctx.user.id in await admin_id():
            if os.path.isfile("GB/Directory/ERP.json"):
                with open("GB/Directory/ERP.json",'r',encoding="utf-8") as a:
                    d = json.load(a)
                    ngword_list = list(d)
                if not text in list(d):
                    with open("GB/Directory/ERP.json",'w',encoding="utf-8") as a:
                        ngword_list.append(text)
                        setting = json.dumps(ngword_list, indent=4,ensure_ascii=False)
                        a.write(str(setting))
                    embed = discord.Embed(title='ERPワード', description="ERPワードを追加しました\n`" + str(text) + "`" ,color=0x00ff00)
                print(ngword_list)
                if text in list(d):
                    with open("GB/Directory/ERP.json",'w',encoding="utf-8") as a:
                        ngword_list.remove(text)
                        setting = json.dumps(ngword_list, indent=4,ensure_ascii=False)
                        a.write(str(setting))
                    embed = discord.Embed(title='ERPワード', description="ERPワードを削除しました\n`" + str(text) + "`" ,color=0xff0000)
            if not os.path.isfile("GB/Directory/ERP.json"):
                embed = discord.Embed(title='ERPワード(エラー)', description="そのデータが見つかりませんでした。",color=0xff0000)
        else:
            embed = discord.Embed(title='権限エラー', description="あなたは実行することができません",color=0xff0000)

        await ctx.response.send_message(embed=embed)

@bot.tree.command(name="erp_list",description="ERPワードリスト")
async def erp_list(ctx:discord.Interaction):
    if ctx.user.id in await admin_id():
        if os.path.isfile("GB/Directory/ERP.json"):
            with open("GB/Directory/ERP.json",'r',encoding="utf-8") as a:
                d = json.load(a)
        ngword_list = ""
        for i in range(len(d)):
            ngword_list += "`" + d[i] + "`,"
        embed = discord.Embed(title='ERPワードリスト', description=ngword_list,color=0x0080ff)
    else:
        embed = discord.Embed(title='権限エラー', description="あなたは実行することができません",color=0xff0000)
    await ctx.response.send_message(embed=embed)

@bot.tree.command(name="setting",description="通知 GBAN実行設定")
@discord.app_commands.describe(
    gban="GBAN実行時の通知チャンネル",
    raid="通常レイド通知チャンネル",
    emergency_raid="緊急レイド通知チャンネル",
    boolean="GBAN実行")


async def setting(ctx:discord.Interaction,
    gban:discord.TextChannel=None,
    raid:discord.TextChannel=None,
    emergency_raid:discord.TextChannel=None,
    boolean:bool=True):

    if ctx.user.guild_permissions.administrator:
        mgi = ctx.guild_id
        Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
        if os.path.isfile(Strike_guild + "/C-Notice.json"):
            with open(Strike_guild + "/C-Notice.json",'r',encoding="utf-8") as a:
                d = json.load(a)
            gban_id = raid_id = er_id = 0
            gm = rm = em = "なし"
            if not gban == None:
                gban_id = gban.id
                gm = gban.mention
            if not raid == None:
                raid_id = raid.id
                rm = raid.mention
            if not emergency_raid == None:
                er_id = emergency_raid.id
                em = emergency_raid.mention
            with open(Strike_guild + "/C-Notice.json",'w',encoding="utf-8") as a:
                l = {True:1,False:0}
                Notice_list = [gban_id,raid_id,er_id,l[boolean]]
                setting = json.dumps(Notice_list, indent=4,ensure_ascii=False)
                a.write(str(setting))
            l = {True:emoji_YES,False:emoji_NO}
            embed = discord.Embed(title='通知設定', description="変更しました。\n"
            +"通常Gban:"+str(gm)+"\n"
            +"通常Raid:"+str(rm)+"\n"
            +"緊急Raid:"+str(em)+"\n"
            +"GBAN実行:"+str(l[boolean])
            ,color=0x0080ff)
        if not os.path.isfile(Strike_guild + "/C-Notice.json"):
            embed = discord.Embed(title='通知設定(エラー)', description="通知のデータが見つかりませんでした。",color=0xff0000)

            
    else:
        embed = discord.Embed(title='権限エラー', description="あなたは実行することができません",color=0xff0000)
    await ctx.response.send_message(embed=embed)

@bot.tree.command(name="log",description="全集通知設定")
@discord.app_commands.describe(
    gban="GBAN実行時の通知チャンネル",
    raid="通常レイド通知チャンネル",
    emergency_raid="緊急レイド通知チャンネル")
async def notice(ctx:discord.Interaction,
gban:discord.TextChannel=None,
raid:discord.TextChannel=None,
emergency_raid:discord.TextChannel=None):
    if ctx.user.id in await admin_id():
        Strike_guild = "GB/Directory/log"
        if os.path.isfile(Strike_guild + ".json"):
            with open(Strike_guild + ".json",'r',encoding="utf-8") as a:
                d = json.load(a)
            gban_id = raid_id = er_id = 0
            gm = rm = em = "なし"
            if not gban == None:
                gban_id = gban.id
                gm = gban.mention
            if not raid == None:
                raid_id = raid.id
                rm = raid.mention
            if not emergency_raid == None:
                er_id = emergency_raid.id
                em = emergency_raid.mention
            with open(Strike_guild + ".json",'w',encoding="utf-8") as a:
                Notice_list = [gban_id,raid_id,er_id]
                setting = json.dumps(Notice_list, indent=4,ensure_ascii=False)
                a.write(str(setting))
            embed = discord.Embed(title='全集通知設定', description="変更しました。\n"
            +"通常Gban:"+str(gm)+"\n"
            +"通常Raid:"+str(rm)+"\n"
            +"緊急Raid:"+str(em)
            ,color=0x0080ff)
        if not os.path.isfile("GB/Directory/log.json"):
            embed = discord.Embed(title='通知設定(エラー)', description="通知のデータが見つかりませんでした。",color=0xff0000)

            
    else:
        embed = discord.Embed(title='権限エラー', description="あなたは実行することができません",color=0xff0000)
    await ctx.response.send_message(embed=embed)

async def admin_id():
    list001 = [788962233375653901,8328609743356559964,831453621732245534]
    return list001

@bot.tree.command(name="create_invite",description="招待作成")
async def create_invite(ctx:discord.Interaction):
    await ctx.channel.create_invite(max_age=86400,max_uses =0,reason="荒らし復興")
    d = await ctx.channel.invites()
    ch = bot.get_channel(1060939552153415804)
    print(ch.available_tags[0])
    await ch.create_thread(name="荒らし復興",content=d[0],applied_tags=[ch.available_tags[0]])
    await ctx.response.send_message(d[0])


class Mo2(discord.ui.Modal):
    def __init__(self,guild_id,message):
        super().__init__(title="通報内容")
        self.g = guild_id
        self.m = message
        Strike_guild = "GB/Strike/S-" + str(self.g)
        with open(Strike_guild + "/R-Report.json",encoding="utf-8") as a:
            d = json.load(a)
            ch_1 = d[0]
            role_1 = d[1]
            avo_report = d[2]
        self.answer = ui.TextInput(label='通報理由', style=discord.TextStyle.paragraph)
        self.avo_report = ui.TextInput(label='AVO本部に通報', style=discord.TextStyle.short,default="",placeholder="通報する場合は「はい」と入力",required=False)
        self.add_item(self.answer)
        if avo_report == 1:
            self.add_item(self.avo_report)


    async def on_submit(self, interaction: discord.Interaction):
        Strike_guild = "GB/Strike/S-" + str(interaction.guild.id)
        if os.path.isfile(Strike_guild + "/R-Report.json"):
            with open(Strike_guild + "/R-Report.json",encoding="utf-8") as a:
                d = json.load(a)
                ch = d[0]
                role = d[1]
                avo_report = d[2]

            embed = discord.Embed(title='⚠通報', description="通報者:" + str(interaction.user.mention)+
            "```通報理由:" + str(self.answer.value) + "```",color=0xffff00)
            embed.add_field(name="投稿者",value=self.m.author.mention,inline=True)
            embed.add_field(name="投稿先",value=str(self.m.channel.mention) + "[リンク](" + str(self.m.jump_url) + ")" ,inline=True)
            embed.add_field(name="メッセージ",value=str(self.m.content),inline=False)
            embed.set_footer(text=str(await dtnow()))
            c = bot.get_channel(ch)
            await c.send(content="<@&"+str(role)+">",embed=embed)
            if self.avo_report.value == "はい":
                if avo_report == 1:
                    embed = discord.Embed(title='通報(AVO本部へ)', description=
                    "**本文**　　：" + str(self.answer.value) + "\n"
                    +"**通報者**　：" + str(interaction.user.mention) + "\n"
                    +"**通報者ID**：" + str(interaction.user.id) + "\n"
                    +"**通報元**　：" + str(interaction.guild.name) + "\n"
                    +"**通報元ID**：" + str(interaction.guild.id) + "\n"
                    +"**通報チャンネル**　：<#" + str(interaction.channel_id) + ">\n"
                    +"**通報チャンネルID**　：" + str(interaction.channel_id) + "\n"
                    ,color=0xffff00)
                    embed.set_footer(text=str(await dtnow()))
                    await interaction.channel.create_invite(max_age=86400,max_uses =0,reason="荒らし復興")
                    d = await interaction.channel.invites()
                    ch = bot.get_channel(1060939552153415804)
                    await ch.create_thread(name="荒らし復興" + str(interaction.guild.name),content=d[0],embed=embed,applied_tags=[ch.available_tags[0]])
                    #await interaction.response.send_message(d[0],embed=embed)
        await interaction.response.defer()
        

@bot.tree.context_menu(name="サーバー運営に通報")
async def report(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_modal(Mo2(interaction.guild_id,message))
    await interaction.followup.send(content="通報完了",ephemeral=True)

@bot.tree.command(name="report_setting",description="通報受信チャンネル設定")
async def report_setting(ctx:discord.Interaction,ch:discord.TextChannel,role:discord.Role,avo_report:bool):
    mgi = ctx.guild.id
    Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
    if os.path.isfile(Strike_guild + "/R-Report.json"):
        with open(Strike_guild + "/R-Report.json",'w',encoding="utf-8") as a:
            l = {True:1,False:0}
            setting = json.dumps([ch.id,role.id,l[avo_report]], indent=4,ensure_ascii=False)
            a.write(str(setting))
        with open(Strike_guild + "/R-Report.json",encoding="utf-8") as a:
            d = json.load(a)
            ch_1 = d[0]
            role_1 = d[1]
            avo_report = d[2]
        l = {True:"はい",False:"いいえ"}
        embed = discord.Embed(title='通報受信設定', description="変更しました。\n"
        +"管理者ロール:<@&"+str(role_1)+">\n"
        +"通報受信チャンネル:<#"+str(ch_1)+">\n"
        +"AVO本部に通報:<#"+str(l[avo_report])
        ,color=0x0080ff)
        
    if not os.path.isfile(Strike_guild + "/R-Report.json"):
        embed = discord.Embed(title='通知設定(エラー)', description="通知のデータが見つかりませんでした。",color=0xff0000)

        embed = discord.Embed(title='権限エラー', description="あなたは実行することができません",color=0xff0000)
    await ctx.response.send_message(embed=embed)

@bot.tree.command(name="prefix_change",description="コマンドプレフィックス")
async def prefix_change(ctx:discord.Interaction,text:str):
    mgi = ctx.guild_id
    if True == True:#ctx.user.guild_permissions.administrator:
        Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
        if os.path.isfile(Strike_guild + "/P-Prefix.json"):
            with open(Strike_guild + "/P-Prefix.json",'r',encoding="utf-8") as a:
                d = json.load(a)
                ngword_list = list(d)
            if not text in list(d):
                with open(Strike_guild + "/P-Prefix.json",'w') as a:
                    ngword_list.append(text)
                    setting = json.dumps(ngword_list, indent=4,ensure_ascii=False)
                    a.write(str(setting))
                embed = discord.Embed(title='コマンドプレフィックス', description="コマンドプレフィックスを追加しました\n`" + str(text) + "`" ,color=0x00ff00)
            print(ngword_list)
            if text in list(d):
                with open(Strike_guild + "/P-Prefix.json",'w',encoding="utf-8") as a:
                    ngword_list.remove(text)
                    setting = json.dumps(ngword_list, indent=4,ensure_ascii=False)
                    a.write(str(setting))
                embed = discord.Embed(title='コマンドプレフィックス', description="コマンドプレフィックスを削除しました\n`" + str(text) + "`" ,color=0xff0000)
        if not os.path.isfile(Strike_guild + "/P-Prefix.json"):
            embed = discord.Embed(title='コマンドプレフィックス(エラー)', description="そのユーザーのデータが見つかりませんでした。",color=0xff0000)
    else:
        embed = discord.Embed(title='権限エラー', description="あなたは`管理者権限`を持っていないため実行することができません",color=0xff0000)

    await ctx.response.send_message(embed=embed)

@bot.command()
async def verify(ctx):
    mgi = ctx.guild.id
    Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
    

    
    if os.path.isfile(Strike_guild + "/C-Captcha.json"):
        with open(Strike_guild + "/C-Captcha.json",'r',encoding="utf-8") as a:
            d = json.load(a)
            d = dict(d)
        embed = discord.Embed(title='認証コマンド', description="初期設定\n送信",color=0x0080ff)
        await ctx.send(embed=embed,view=Initial_Send())
        
    if not os.path.isfile(Strike_guild + "/C-Captcha.json"):
        embed = discord.Embed(title='認証[初期設定]', description="どちらの認証方式にしますか？",color=0x0080ff)
        await ctx.send(embed=embed,view=Initial_Stting())
        
    
class Initial_Send(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Initial_Send_1("初期設定",discord.ButtonStyle.green))
        self.add_item(Initial_Send_1("送信",discord.ButtonStyle.blurple))
        
class Initial_Send_1(discord.ui.Button):
    def __init__(self,text,c):
        super().__init__(label=text,style=c)

    async def callback(self,interaction:discord.Interaction):
        mgi = interaction.guild.id
        Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
        if os.path.isfile(Strike_guild + "/M-MessageID.json"):
            with open(Strike_guild + "/M-MessageID.json",'r',encoding="utf-8") as a:
                de = json.load(a)
        with open(Strike_guild + "/C-Captcha.json",'r',encoding="utf-8") as a:
            d = json.load(a)
            d = dict(d)
        
        if self.label == "初期設定":
            embed = discord.Embed(title='認証[初期設定]', description="どちらの認証方式にしますか？",color=0x0080ff)
            await interaction.response.send_message(embed=embed,view=Initial_Stting())
        if self.label == "送信":
            if d["type"] == "calc":
                channel = bot.get_channel(d["channel"])
                m = await channel.send("計算問題認証",view=Calc_Button_1(interaction))
            if d["type"] == "image":
                channel = bot.get_channel(d["channel"])
                m = await channel.send("画像認証",view=Image_Button_1())
            await interaction.response.defer()
            with open(Strike_guild + "/M-MessageID.json",'w',encoding="utf-8") as a:
                setting = json.dumps([m.id], indent=4,ensure_ascii=False)
                a.write(str(setting))
        
            try:
                old_msg = await channel.fetch_message(de[0])
                await old_msg.delete()
            except:
                pass
class Initial_Stting(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Initial_Stting_1("画像方式",discord.ButtonStyle.green))
        self.add_item(Initial_Stting_1("計算方式",discord.ButtonStyle.red))
        
class Initial_Stting_1(discord.ui.Button):
    def __init__(self,text,c):
        super().__init__(label=text,style=c)

    async def callback(self,interaction:discord.Interaction):
        mgi = interaction.guild.id
        Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
        
        
        with open(Strike_guild + "/C-Captcha.json",'w',encoding="utf-8") as a:
            d = {}
            if self.label == "計算方式":
                d["type"] = "calc"
            if self.label == "画像方式":
                d["type"] = "image"
            setting = json.dumps(d, indent=4,ensure_ascii=False)
            a.write(str(setting))
        embed = discord.Embed(title='認証[初期設定]', description="認証するチャンネルを選択してください",color=0x0080ff)
        await interaction.response.send_message(embed=embed,view=Initial_Stting_2())

class Initial_Stting_2(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Initial_Stting_3())

class Initial_Stting_3(discord.ui.ChannelSelect):
    def __init__(self):
        super().__init__(min_values=1,max_values=1,placeholder="チャンネルを選択",channel_types=[discord.ChannelType.text])

    async def callback(self, interaction: discord.Interaction):
        
        mgi = interaction.guild.id
        Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
        with open(Strike_guild + "/C-Captcha.json",'r',encoding="utf-8") as a:
            d = json.load(a)
            d = dict(d)
        d["channel"] = self.values[0].id
        with open(Strike_guild + "/C-Captcha.json",'w',encoding="utf-8") as a:
            setting = json.dumps(d, indent=4,ensure_ascii=False)
            a.write(str(setting))
        embed = discord.Embed(title='認証[初期設定]', description="認証成功の時につけるロールを選択してください",color=0x0080ff)
        await interaction.response.send_message(embed=embed,view=Initial_Stting_4())

class Initial_Stting_4(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Initial_Stting_5())

class Initial_Stting_5(discord.ui.RoleSelect):
    def __init__(self):
        super().__init__(min_values=1,max_values=1,placeholder="ロール")

    async def callback(self, interaction: discord.Interaction):
        
        mgi = interaction.guild.id
        Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
        with open(Strike_guild + "/C-Captcha.json",'r',encoding="utf-8") as a:
            d = json.load(a)
            d = dict(d)
        d["role"] = self.values[0].id
        with open(Strike_guild + "/C-Captcha.json",'w',encoding="utf-8") as a:
            setting = json.dumps(d, indent=4,ensure_ascii=False)
            a.write(str(setting))
        embed = discord.Embed(title='認証[初期設定]', description="難易度を選択してください",color=0x0080ff)
        await interaction.response.send_message(embed=embed,view=Initial_Stting_6())

class Initial_Stting_6(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Initial_Stting_7("低",discord.ButtonStyle.blurple))
        self.add_item(Initial_Stting_7("高",discord.ButtonStyle.green))
        self.add_item(Initial_Stting_7("最高" ,discord.ButtonStyle.red))
class Initial_Stting_7(discord.ui.Button):
    def __init__(self,text,c, timeout=None):
        super().__init__(label=text,style=c)

    async def callback(self,interaction:discord.Interaction):
        mgi = interaction.guild.id
        Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
        
        with open(Strike_guild + "/C-Captcha.json",'r',encoding="utf-8") as a:
            d = json.load(a)
            d = dict(d)
        with open(Strike_guild + "/C-Captcha.json",'w',encoding="utf-8") as a:
            if self.label == "低":
                d["difficulty"] = "低"
            if self.label == "高":
                d["difficulty"] = "高"
            if self.label == "最高":
                d["difficulty"] = "最高"
                
            setting = json.dumps(d, indent=4,ensure_ascii=False)
            a.write(str(setting))
        embed = discord.Embed(title='認証[初期設定]', description="認証失敗の時に処罰するかを選択してください",color=0x0080ff)
        await interaction.response.send_message(embed=embed,view=Initial_Stting_8())

class Initial_Stting_8(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Initial_Stting_9())
class Initial_Stting_9(discord.ui.Select):
    def __init__(self):
        options =[discord.SelectOption(label="無し", description=""),
        discord.SelectOption(label="有り", description='キック'),
        discord.SelectOption(label="厳しく", description="キック+タイムアウト1時間")]
        super().__init__(options=options,min_values=1,max_values=1)

    async def callback(self,interaction:discord.Interaction):
        mgi = interaction.guild.id
        Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
        
        with open(Strike_guild + "/C-Captcha.json",'r',encoding="utf-8") as a:
            d = json.load(a)
            d = dict(d)
        with open(Strike_guild + "/C-Captcha.json",'w',encoding="utf-8") as a:
            if self.values[0] == "無し":
                d["punishment"] = "無し"
            if self.values[0] == "有り":
                d["punishment"] = "キック"
            if self.values[0] == "厳しく":
                d["punishment"] = "タイムアウト"
                
            setting = json.dumps(d, indent=4,ensure_ascii=False)
            a.write(str(setting))
        with open(Strike_guild + "/C-Captcha.json",'r',encoding="utf-8") as a:
            d = json.load(a)
            d = dict(d)
        type = {"image":"画像","calc":"計算"}
        type = type[d["type"]]
        role = interaction.guild.get_role(d["role"])
        embed = discord.Embed(title='認証[設定完了]' + str(emoji_YES), description=
        "**タイプ**：" + str(type) +"\n" +
        "**チャンネル**：" + str(d["channel"]) +"\n" +
        "**ロール**：" + str(role.mention) +"\n" +
        "**難易度**：" + str(d["difficulty"]) +"\n" +
        "**失敗時**：" + str(d["punishment"])
        ,color=0x00ff00)
        await interaction.response.send_message(embed=embed)

class Calc_Button_1(discord.ui.View):
    def __init__(self,inter):
        super().__init__(timeout=None)
        self.add_item(Calc_Button(inter))
class Calc_Button(discord.ui.Button):
    def __init__(self,inter):
        self.inter = inter
        super().__init__(label="計算問題認証",style=discord.ButtonStyle.green)

    async def callback(self,interaction:discord.Interaction):
        await interaction.response.send_modal(Mo3(self.inter))
    
class Image_Button_1(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Image_Button())
class Image_Button(discord.ui.Button):
    def __init__(self):
        
        super().__init__(label="画像認証",style=discord.ButtonStyle.green)

    async def callback(self,interaction:discord.Interaction):
        mgi = interaction.guild.id
        Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
        with open(Strike_guild + "/C-Captcha.json",'r',encoding="utf-8") as a:
            d = json.load(a)
            d = dict(d)
        if d["difficulty"] == "低":
            number=rr(1000,9999)
            k = 15
        if d["difficulty"] == "高":
            number=rr(123456,999999)
            k = 25
        if d["difficulty"] == "最高":
            number=rr(123456,999999)
            k =45
        img = Image.new('RGBA', (200, 150), (128, 128, 128))
        draw = ImageDraw.Draw(img)
        H=rr(20,70)
        W=rr(0,100)

       
        H = rr(20,70)
        num1 = list(str(number))
        print(len(num1))
        for i in range(len(num1)):
            font = ImageFont.truetype('GB/Directory/やさしさゴシック手書き.ttf',rr(20,35),)
            num = num1[i]
            print(num)
            draw.text((H + i*rr(14,16),W + rr(-10,10)),str(num),(255,255,255),stroke_width=3,stroke_fill='black',font=font)
        for i in range(k):
            draw.line((rr(0,200), rr(0,150), rr(0,200), rr(0,150)), fill=(255,255,255), width=3)
        # Create an image instance of the given size
        image = ImageCaptcha(width = 280, height = 90)
        
        # Image captcha text
        captcha_text = str(number)
        
        # generate the image of the given text
        data = image.generate(captcha_text) 
        
        # write the image on the given file and save it
        image.write(captcha_text, 'GB/Directory/auth.png')
        #img.save("GB/Directory/auth.png")
        file = discord.File("GB/Directory/auth.png", filename="image.png")
        await interaction.response.send_message(file=file,content="下の数字を打ってください。",ephemeral=True)
        bools = True
        while bools:
            user_msg: discord.Message = await bot.wait_for("message",check=lambda m: m.channel == interaction.channel)
            await user_msg.delete()
            if user_msg.author.id == interaction.user.id:
                bools = False
        
        mgi = interaction.guild_id
        Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"

        with open(Strike_guild + "/C-Captcha.json",'r',encoding="utf-8") as a:
            data = json.load(a)
            data = dict(data)
        if str(number) == user_msg.content:
            
            role = interaction.guild.get_role(data["role"])
            await interaction.user.add_roles(role,reason="認証")
            embed = discord.Embed(title='認証成功' + str(emoji_YES), description=str(interaction.user.mention) + "が認証成功しました"
            + str(role.mention),color=0x00ff00)
            embed.set_footer(text=str(await dtnow()))
            await interaction.followup.send(embed=embed,ephemeral=True)
        else:
            embed = discord.Embed(title='認証失敗' + str(emoji_NO), description="回答が違います",color=0xff0000)
            if data["punishment"] == "キック":
                embed = discord.Embed(title='認証失敗' + str(emoji_NO), description="回答が違います\n5秒後にキックされます",color=0xff0000)
            if data["punishment"] == "タイムアウト":
                await interaction.user.timeout(discord.utils.utcnow() + datetime.timedelta(seconds=3600),reason="認証失敗の時にタイムアウトされたため")
                embed = discord.Embed(title='認証失敗' + str(emoji_NO), description="回答が違います\n5秒後にキックとタイムアウトされます",color=0xff0000)
            await interaction.followup.send(embed=embed,ephemeral=True)
            if not data["punishment"] == "無し":
                await asyncio.sleep(5)
            if data["punishment"] == "キック":
                await interaction.user.kick(reason="認証失敗の時にキックされたため")
            if data["punishment"] == "タイムアウト":
                await interaction.user.kick(reason="認証失敗の時にキックされたため")
class Mo3(discord.ui.Modal):
    def __init__(self,inter):
        super().__init__(title="計算問題")
        mgi = inter.guild.id
        Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"
        with open(Strike_guild + "/C-Captcha.json",'r',encoding="utf-8") as a:
            d = json.load(a)
            d = dict(d)
        if d["difficulty"] == "低":
            num = [random.randint(1,9),random.randint(1,9)]
            total = num[0] + num[1]
            text = str(num[0])
            text += "+"
            text += str(num[1])
            text += "="
            self.t = total
        if d["difficulty"] == "高":
            num = [random.randint(5,50),random.randint(6,49)]
            total = num[0] + num[1]
            text = str(num[0])
            text += "+"
            text += str(num[1])
            text += "="
            self.t = total
        if d["difficulty"] == "最高":
            num = [rr(30,99),rr(100,999),rr(1,9)]
            total = num[0] + num[1] * num[2]
            print(total)
            text = str(num[0])
            text += "+"
            text += str(num[1])
            text += "×"
            text += str(num[2])
            text += "="
            self.t = total
        self.answer = ui.TextInput(label=str(text), style=discord.TextStyle.short)
        self.add_item(self.answer)
    async def on_submit(self, interaction: discord.Interaction):
        mgi = interaction.guild_id
        Strike_guild = "GB/Strike/S-" + str(mgi) + "/Data"

        with open(Strike_guild + "/C-Captcha.json",'r',encoding="utf-8") as a:
            data = json.load(a)
            data = dict(data)
        if str(self.t) == self.answer.value:
            
            role = interaction.guild.get_role(data["role"])
            await interaction.user.add_roles(role,reason="認証")
            embed = discord.Embed(title='認証成功' + str(emoji_YES), description=str(interaction.user.mention) + "が認証成功しました"
            + str(role.mention),color=0x00ff00)
            embed.set_footer(text=str(await dtnow()))
        else:
            embed = discord.Embed(title='認証失敗' + str(emoji_NO), description="回答が違います",color=0xff0000)
            if data["punishment"] == "キック":
                embed = discord.Embed(title='認証失敗' + str(emoji_NO), description="回答が違います\n5秒後にキックされます",color=0xff0000)
            if data["punishment"] == "タイムアウト":
                await interaction.user.timeout(discord.utils.utcnow() + datetime.timedelta(seconds=3600),reason="認証失敗の時にタイムアウトされたため")
                embed = discord.Embed(title='認証失敗' + str(emoji_NO), description="回答が違います\n5秒後にキックとタイムアウトされます",color=0xff0000)
            if not data["punishment"] == "無し":
                await asyncio.sleep(5)
            if data["punishment"] == "キック":
                await interaction.user.kick(reason="認証失敗の時にキックされたため")
            if data["punishment"] == "タイムアウト":
                await interaction.user.kick(reason="認証失敗の時にキックされたため")
        await interaction.response.send_message(embed=embed)
bot.run(key)


