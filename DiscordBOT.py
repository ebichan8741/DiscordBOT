import discord
from discord.ext import commands
import interactions
import requests
#import asyncio
import os
#import keep_alive
from dotenv import load_dotenv

# 接続に必要なオブジェクトを生成
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', help_command=None, intents=intents)


@bot.event
#起動時
async def on_ready():
    print(f"ボットが起動しました! {bot.user}")


@bot.command()
async def sv(ctx):
    """BotのDMからプライベートボイスチャンネル作成(自分と管理者しか見えない部屋)
  
    """
    guild = ctx.guild
    # DMであればguildはNone
    if guild == None:
        guild = bot.get_guild(988118353128325142)
        #channel = bot.get_channel(988306406371360788)
        #cat = channel.category
        #サーバー内のコマンド用カテゴリを名前で検索
        for cat in guild.categories:
            if cat.name == ctx.me.name:
                category = cat
                break
        member = ctx.author
        mbed = discord.Embed(
            title='Success',
            description=f'カテゴリ {category} に {member.name}の部屋 を作成したよ')
        voice_channel = await guild.create_voice_channel(name='{0}の部屋'.format(
            member.name),
                                                         category=category)
        # @everyoneに対する権限追加(部屋を見えないようにするため)
        await voice_channel.set_permissions(guild.get_role(988118353128325142),
                                            connect=False,
                                            speak=False,
                                            move_members=False,
                                            manage_roles=False,
                                            manage_channels=False,
                                            view_channel=False)
        # VCにコマンド主用の権限を追加
        await voice_channel.set_permissions(member,
                                            connect=True,
                                            speak=True,
                                            move_members=False,
                                            manage_roles=False,
                                            manage_channels=False,
                                            view_channel=True,
                                            create_instant_invite=True,
                                            use_voice_activation=True)
        await ctx.send(embed=mbed)
    else:
        #サーバー内のコマンド用カテゴリを名前で検索
        for cat in guild.categories:
            if cat.name == ctx.me.name:
                category = cat
                break
        member = ctx.author
        mbed = discord.Embed(
            title='Success',
            description=f'カテゴリ {category} に {member.name}の部屋 を作成したよ')
        voice_channel = await guild.create_voice_channel(name='{0}の部屋'.format(
            member.name),
                                                         category=category)
        # @everyoneに対する権限追加(部屋を見えないようにするため)
        await voice_channel.set_permissions(guild.get_role(988118353128325142),
                                            connect=False,
                                            speak=False,
                                            move_members=False,
                                            manage_roles=False,
                                            manage_channels=False,
                                            view_channel=False)
        # VCにコマンド主用の権限を追加
        await voice_channel.set_permissions(member,
                                            connect=True,
                                            speak=True,
                                            move_members=False,
                                            manage_roles=False,
                                            manage_channels=False,
                                            view_channel=True,
                                            create_instant_invite=True,
                                            use_voice_activation=True)
        await ctx.send(embed=mbed)


@bot.command()
async def delch(ctx):
    """自分が今いるプライベートボイスチャンネルを削除
  
    """
    #特定カテゴリ内のボイスチャンネル群から、現在ユーザーが参加しているチャンネルを探して削除
    user = ctx.author
    guild = ctx.guild
    if guild == None:
        guild = bot.get_guild(988118353128325142)
    #サーバー内のコマンド用カテゴリを名前で検索
    for cat in guild.categories:
        if cat.name == ctx.me.name:
            category = cat
            break
    #サーバーに参加しているメンバーの中から自分(コマンドを打った人)を取得
    member = await guild.fetch_member(user.id)
    #カテゴリ内の自分が参加しているボイスチャンネルを検索し削除
    voiceState = member.voice
    if voiceState != None:
        for channel in category.voice_channels:
            if channel == voiceState.channel:
                mbed = discord.Embed(
                    title='Success',
                    description=f'チャンネル {channel} を削除したよ',
                )
                await ctx.send(embed=mbed)
                await channel.delete()


@bot.command()
async def join(ctx, mension):
    """メンションでプライベートボイスチャンネルへ招待（部屋を見えるように）
  
    Parameters
    ----------
    mension : str
      ディスコードのユーザー名が来る想定(タグ含む)
    """
    user = ctx.author
    guild = ctx.guild
    if guild == None:
        guild = bot.get_guild(988118353128325142)
    #サーバーに参加しているメンバーの中から自分(コマンドを打った人)を取得
    member = await guild.fetch_member(user.id)
    #サーバー内のコマンド用カテゴリを名前で検索
    for cat in guild.categories:
        if cat.name == ctx.me.name:
            category = cat
            break
    #特定カテゴリ内の自分が参加しているボイスチャンネルを検索
    if member.voice != None:
        for channel in category.voice_channels:
            if channel == member.voice.channel:
                joinChannel = channel
    #名前とタグが一致するメンバーの権限を変更する
    str = mension.split('#')
    if len(str) != 2:
        print('Error: Name and Tag Required!')
        mbed = discord.Embed(
            title='Error',
            description='名前とタグの入力が間違っているよ',
        )
        await ctx.send(embed=mbed)
        return
    name = str[0]
    tag = str[1]
    async for mem in guild.fetch_members():
        if name == mem.name:
            if tag == mem.discriminator:
                inviteMember = mem
                if inviteMember == None:
                    print(f'Error: {mension} doesn`t exist!')
                    return
                print(f'{inviteMember.name} found!')
                if joinChannel == None:
                    mbed = discord.Embed(
                        title='Error',
                        description='ボイスチャンネルに入ってないよ',
                    )
                    await ctx.send(embed=mbed)
                await joinChannel.set_permissions(inviteMember,
                                                  connect=True,
                                                  speak=True,
                                                  move_members=False,
                                                  manage_roles=False,
                                                  manage_channels=False,
                                                  view_channel=True,
                                                  create_instant_invite=True,
                                                  use_voice_activation=True)
                mbed = discord.Embed(
                    title='Success',
                    description=f'{inviteMember.name} さんを招待したよ',
                )
                await ctx.send(embed=mbed)
                mbed = discord.Embed(
                    title=f'{guild.name}',
                    description=f'{inviteMember.name} さんが秘密の部屋を用意してくれたよ！',
                )
                await inviteMember.send(embed=mbed)
                return
    #一致する名前がいなかった場合
    mbed = discord.Embed(
        title='Error',
        description='名前とタグの入力が間違っているよ',
    )
    await ctx.send(embed=mbed)


@bot.command()
async def set(ctx, guild: discord.Guild, category: discord.CategoryChannel):
    if guild == None & category == None:
        description = f'サーバーとカテゴリが見つからないよ'
    elif guild == None:
        description = f'サーバーがみつからないよ\nカテゴリ：{category.name}'
    elif category == None:
        description = f'サーバー：{guild.name}\nカテゴリが見つからないよ'
    mbed = discord.Embed(title='テスト', description=description)
    await ctx.send(embed=mbed)


@bot.command()
async def button(ctx):
    normal_url = "https://discordapp.com/api/channels/" + str(
        ctx.channel.id) + "/messages"
    json = {
        "content":
        "Hello World",
        "components": [{
            "type":
            1,
            "components": [
                {
                    "type": 2,
                    "label": "1st",
                    "style": 1,
                    "custom_id": "click_one",
                },
                {
                    "type": 2,
                    "label": "2nd",
                    "style": 3,
                    "custom_id": "click_two",
                },
            ]
        }]
    }
    requests.post(normal_url, headers=headers, json=json)


@bot.command()
async def cmd(ctx):
    """指定サーバーにBotコマンド用テキストチャンネルを作成する
  
    """
    guild = ctx.guild
    if guild == None:
        mbed = discord.Embed(title='Error', description='サーバーが見つからないよ')
        await ctx.send(embed=mbed)
        return
    # カテゴリ作成
    category = await guild.create_category(name=f'{ctx.me.name}')
    # テキストチャンネル作成
    command_ch = await guild.create_text_channel(name=f'{ctx.me.name}コマンド',
                                                 category=category)
    mbed = discord.Embed(
        title='Success',
        description=f'{category.name} カテゴリに{command_ch.name}が作成されたよ')
    await ctx.send(embed=mbed)


#---- 以下はテスト用のコマンド ----


#テキストチャンネル削除
@bot.command()
async def deltxtch(ctx, channel: discord.TextChannel):
    mbed = discord.Embed(
        title='Success',
        description=f'チャンネル {channel} を削除したよ',
    )
    if ctx.author.guild_permissions.manage_channels:
        await ctx.send(embed=mbed)
        await channel.delete()


#ボイスチャンネル削除
@bot.command()
async def delvcch(ctx, channel: discord.VoiceChannel):
    mbed = discord.Embed(
        title='Success',
        description=f'チャンネル {channel} を削除したよ',
    )
    if ctx.author.guild_permissions.manage_channels:
        await ctx.send(embed=mbed)
        await channel.delete()


#テキストチャンネル作成
@bot.command()
async def mktxt(ctx, channelName):
    guild = ctx.guild
    # DMであればguildはNone
    if guild == None:
        mbed = discord.Embed(title='Error', description='このコマンドはDMでは使えないよ')
        await ctx.send(embed=mbed)
    else:
        cat = ctx.channel.category
        mbed = discord.Embed(
            title='Success',
            description=f'カテゴリ {cat} に チャンネル {channelName} を作成したよ')
        if ctx.author.guild_permissions.manage_channels:
            await guild.create_text_channel(name='{}'.format(channelName),
                                            category=cat)
            await ctx.send(embed=mbed)


#ボイスチャンネル作成
@bot.command()
async def mkvc(ctx, channelName):
    guild = ctx.guild
    # DMであればguildはNone
    if guild == None:
        mbed = discord.Embed(title='Error', description='このコマンドはDMでは使えないよ')
        await ctx.send(embed=mbed)
    else:
        cat = ctx.channel.category
        mbed = discord.Embed(
            title='Success',
            description=f'カテゴリ {cat} に チャンネル {channelName} を作成したよ')
        if ctx.author.guild_permissions.manage_channels:
            await guild.create_voice_channel(name='{}'.format(channelName),
                                             category=cat)
            await ctx.send(embed=mbed)


#プライベートテキストチャンネル作成
@bot.command()
async def mkprivtxt(ctx, channelName):
    guild = ctx.guild
    # DMであればguildはNone
    if guild == None:
        mbed = discord.Embed(title='Error', description='このコマンドはDMでは使えないよ')
        await ctx.send(embed=mbed)
    else:
        cat = ctx.channel.category
        mbed = discord.Embed(
            title='Success',
            description=f'カテゴリ {cat} に チャンネル {channelName} を作成したよ')
        if ctx.author.guild_permissions.manage_channels:
            member = ctx.author
            voice_channel = await guild.create_text_channel(
                name='{}'.format(channelName), category=cat)
            await voice_channel.set_permissions(
                guild.get_role(988118353128325142),
                connect=False,
                speak=False,
                move_members=False,
                manage_roles=False,
                manage_channels=False,
                view_channel=False)
            await ctx.send(embed=mbed)


#プライベートボイスチャンネル作成
@bot.command()
async def mkprivvc(ctx, channelName):
    guild = ctx.guild
    # DMであればguildはNone
    if guild == None:
        mbed = discord.Embed(title='Error', description='このコマンドはDMでは使えないよ')
        await ctx.send(embed=mbed)
    else:
        cat = ctx.channel.category
        mbed = discord.Embed(
            title='Success',
            description=f'カテゴリ {cat} に チャンネル {channelName} を作成したよ')
        if ctx.author.guild_permissions.manage_channels:
            member = ctx.author
            voice_channel = await guild.create_voice_channel(
                name='{}'.format(channelName), category=cat)
            await voice_channel.set_permissions(
                guild.get_role(988118353128325142),
                connect=False,
                speak=False,
                move_members=False,
                manage_roles=False,
                manage_channels=False,
                view_channel=False)
            await ctx.send(embed=mbed)


@bot.command()
async def init(ctx):
    guild = bot.get_guild(988118353128325142)
    if ctx.guild == None:
        cat = await guild.create_category(name='{}'.format('えびBot'))
        channel = await guild.create_text_channel(name='{}'.format('お部屋作成用'),
                                                  category=cat)
        mbed = discord.Embed(
            title='Success',
            description=f'カテゴリ [{cat}] に チャンネル [{channel}] を作成したよ')
        await ctx.send(embed=mbed)


#カテゴリ作成
@bot.command()
async def mkcat(ctx, categoryName):
    guild = ctx.guild

    mbed = discord.Embed(title='Success',
                         description="カテゴリ {} を作成したよ".format(categoryName))
    if ctx.author.guild_permissions.manage_channels:
        await guild.create_category(name='{}'.format(categoryName))
        await ctx.send(embed=mbed)


#カテゴリとチャンネル作成
@bot.command()
async def mkcatch(ctx, categoryName, channelName):
    guild = ctx.guild

    mbed = discord.Embed(title='Success',
                         description="カテゴリ {} に チャンネル {} を作成したよ".format(
                             categoryName, channelName))
    if ctx.author.guild_permissions.manage_channels:
        cat = await guild.create_category(name='{}'.format(categoryName))
        await guild.create_text_channel(name='{}'.format(channelName),
                                        category=cat)
        await ctx.send(embed=mbed)


#チャンネル複製
@bot.command()
async def copych(ctx):
    channel = ctx.guild.get_channel(ctx.channel.id)
    mbed = discord.Embed(title='Success',
                         description="チャンネル {} を複製したよ".format(channel.name))
    if ctx.author.guild_permissions.manage_channels:
        await channel.clone(name='{}'.format(channel.name))
        await ctx.send(embed=mbed)


#リアクションでのロール付与
@bot.command()
async def selectrole(ctx):
    embed = discord.Embed(title='ロールの選択', description='リアクションをつけてロールを割り振り')
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('✔️')
    await msg.add_reaction('❤️')


@bot.event
async def on_raw_reaction_add(payload):
    ourMessageID = 988471291646459944

    if ourMessageID == payload.message_id:
        member = payload.member
        guild = member.guild

        emoji = payload.emoji.name
        if emoji == '✔️':
            role = discord.utils.get(guild.roles, name="Check")
        elif emoji == '❤️':
            role = discord.utils.get(guild.roles, name="Heart")
        await member.add_roles(role)


#サーバー情報表示
@bot.event
async def on_raw_reaction_remove(payload):
    ourMessageID = 988471291646459944

    if ourMessageID == payload.message_id:
        guild = await (bot.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name
        if emoji == '✔️':
            role = discord.utils.get(guild.roles, name="Check")
        elif emoji == '❤️':
            role = discord.utils.get(guild.roles, name="Heart")
        member = await (guild.fetch_member(payload.user_id))
        if member is not None:
            await member.remove_roles(role)
        else:
            print("Member not found")


#サーバー情報表示
@bot.command()
async def info(ctx):
    if ctx.guild != None:
        channel = ctx.channel
        mbed = discord.Embed(
            title='インフォ',
            #description = "チャンネルID : {}\nチャンネル名 : {}".format(ctx.channel.id, ctx.channel.name)
            description=f"{'Category: {}'.format(channel.category.name)}")
        mbed.add_field(name="Channel Guild",
                       value=ctx.guild.name,
                       inline=False)
        mbed.add_field(name="Channel id", value=channel.id, inline=False)
        mbed.add_field(
            name="Channel Topic",
            value=f"{channel.topic if channel.topic else 'No topic.'}",
            inline=False)
        mbed.add_field(name="Channel Position",
                       value=channel.position,
                       inline=False)
        mbed.add_field(name="Channel Slowmode Delay",
                       value=channel.slowmode_delay,
                       inline=False)
        mbed.add_field(name="Channel is nsfw?",
                       value=channel.is_nsfw(),
                       inline=False)
        mbed.add_field(name="Channel is news?",
                       value=channel.is_news(),
                       inline=False)
        mbed.add_field(name="Channel Creation Time",
                       value=channel.created_at,
                       inline=False)
        mbed.add_field(name="Channel Permissions Synced",
                       value=channel.permissions_synced,
                       inline=False)
        mbed.add_field(name="Channel Hash", value=hash(channel), inline=False)
        if ctx.author.guild_permissions.manage_channels:
            await ctx.send(embed=mbed)
    else:
        mbed = discord.Embed(title='Error', description='このコマンドはDMでは使えないよ')
        await ctx.send(embed=mbed)

class CreateButton(discord.ui.View):
    def __init__(self, txt:str):
        super().__init__()

        self.add_item(Button(txt))
            

class CreateButtons(discord.ui.View):
    def __init__(self, args):
        super().__init__()

        for txt in args:
            self.add_item(Button(txt))

class Button(discord.ui.Button):
    def __init__(self, txt:str):
        super().__init__(label=txt, style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'{interaction.user.display_name}は{self.label}を押しました')

@bot.command()
async def makeButton(ctx: commands.context, *args):
    await ctx.send('Press!', view=CreateButtons(args))

@bot.command()
async def setbutton(ctx):
    await ctx.send('ボタンを作成しました', view=CreateButton('ボタン'))


load_dotenv()
# Botの起動
DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(DISCORD_BOT_TOKEN)
