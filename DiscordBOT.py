from discord.ext import commands
import discord
import config

client = commands.Bot(command_prefix = '/', help_command=None)

@client.event
#起動時
async def on_ready():
    print(f'{client.user} has Awoken!')

#テキストチャンネル削除
@client.command()
async def deltxtch(ctx, channel: discord.TextChannel):
    mbed = discord.Embed(
        title='Success',
        description=f'チャンネル {channel} を削除したよ',
    )
    if ctx.author.guild_permissions.manage_channels:
        await ctx.send(embed=mbed)
        await channel.delete()

#ボイスチャンネル削除
@client.command()
async def delvcch(ctx, channel: discord.VoiceChannel):
    mbed = discord.Embed(
        title='Success',
        description=f'チャンネル {channel} を削除したよ',
    )
    if ctx.author.guild_permissions.manage_channels:
        await ctx.send(embed=mbed)
        await channel.delete()

#テキストチャンネル作成
@client.command()
async def mktxt(ctx, channelName):
    guild = ctx.guild
    # DMであればguildはNone
    if guild == None:
        mbed = discord.Embed(
        title = 'Error',
        description = 'このコマンドはDMでは使えないよ'
        )
        await ctx.send(embed=mbed)
    else:
        cat = ctx.channel.category
        mbed = discord.Embed(
            title = 'Success',
            description = f'カテゴリ {cat} に チャンネル {channelName} を作成したよ'
        )
        if ctx.author.guild_permissions.manage_channels:
            await guild.create_text_channel(name='{}'.format(channelName), category=cat)    
            await ctx.send(embed=mbed)

#ボイスチャンネル作成
@client.command()
async def mkvc(ctx, channelName):
    guild = ctx.guild
     # DMであればguildはNone
    if guild == None:
        mbed = discord.Embed(
        title = 'Error',
        description = 'このコマンドはDMでは使えないよ'
        )
        await ctx.send(embed=mbed)
    else:
        cat = ctx.channel.category
        mbed = discord.Embed(
            title = 'Success',
            description = f'カテゴリ {cat} に チャンネル {channelName} を作成したよ'
        )
        if ctx.author.guild_permissions.manage_channels:
            await guild.create_voice_channel(name='{}'.format(channelName), category=cat)
            await ctx.send(embed=mbed)

#プライベートテキストチャンネル作成
@client.command()
async def mkprivtxt(ctx, channelName):
    guild = ctx.guild
    # DMであればguildはNone
    if guild == None:
        mbed = discord.Embed(
        title = 'Error',
        description = 'このコマンドはDMでは使えないよ'
        )
        await ctx.send(embed=mbed)
    else:
        cat = ctx.channel.category
        mbed = discord.Embed(
            title = 'Success',
            description = f'カテゴリ {cat} に チャンネル {channelName} を作成したよ'
        )
        if ctx.author.guild_permissions.manage_channels:
            member = ctx.author
            voice_channel = await guild.create_text_channel(name='{}'.format(channelName), category=cat)
            await voice_channel.set_permissions(guild.get_role(988118353128325142), connect=False, speak=False, move_members=False, manage_roles=False, manage_channels=False, view_channel=False)
            await ctx.send(embed=mbed)

#プライベートボイスチャンネル作成
@client.command()
async def mkprivvc(ctx, channelName):
    guild = ctx.guild
    # DMであればguildはNone
    if guild == None:
        mbed = discord.Embed(
        title = 'Error',
        description = 'このコマンドはDMでは使えないよ'
        )
        await ctx.send(embed=mbed)
    else:
        cat = ctx.channel.category
        mbed = discord.Embed(
            title = 'Success',
            description = f'カテゴリ {cat} に チャンネル {channelName} を作成したよ'
        )
        if ctx.author.guild_permissions.manage_channels:
            member = ctx.author
            voice_channel = await guild.create_voice_channel(name='{}'.format(channelName), category=cat)
            await voice_channel.set_permissions(guild.get_role(988118353128325142), connect=False, speak=False, move_members=False, manage_roles=False, manage_channels=False, view_channel=False)
            await ctx.send(embed=mbed)

#DMからプライベートボイスチャンネル作成
@client.command()
async def secretvc(ctx, channelName):
    guild = ctx.guild
    # DMであればguildはNone
    if guild == None:
        guild = client.get_guild(988118353128325142)
        channel = client.get_channel(988306406371360788)
        cat = channel.category
        mbed = discord.Embed(
            title = 'Success',
            description = f'カテゴリ {cat} に チャンネル {channelName} を作成したよ'
        )
        voice_channel = await guild.create_voice_channel(name='{}'.format(channelName), category=cat)
        await voice_channel.set_permissions(guild.get_role(988118353128325142), connect=False, speak=False, move_members=False, manage_roles=False, manage_channels=False, view_channel=False)
        await ctx.send(embed=mbed)
            

#カテゴリ作成
@client.command()
async def mkcat(ctx, categoryName):
    guild = ctx.guild

    mbed = discord.Embed(
        title = 'Success',
        description = "カテゴリ {} を作成したよ".format(categoryName)
    )
    if ctx.author.guild_permissions.manage_channels:
        await guild.create_category(name='{}'.format(categoryName))
        await ctx.send(embed=mbed)
        
#カテゴリとチャンネル作成
@client.command()
async def mkcatch(ctx, categoryName, channelName):
    guild = ctx.guild

    mbed = discord.Embed(
        title = 'Success',
        description = "カテゴリ {} に チャンネル {} を作成したよ".format(categoryName, channelName)
    )
    if ctx.author.guild_permissions.manage_channels:
        cat = await guild.create_category(name='{}'.format(categoryName))
        await guild.create_text_channel(name='{}'.format(channelName), category=cat)
        await ctx.send(embed=mbed)

#チャンネル複製
@client.command()
async def copych(ctx):
    channel = ctx.guild.get_channel(ctx.channel.id)
    mbed = discord.Embed(
        title = 'Success',
        description = "チャンネル {} を複製したよ".format(channel.name)
    )
    if ctx.author.guild_permissions.manage_channels:
        await channel.clone(name='{}'.format(channel.name))
        await ctx.send(embed=mbed)

#リアクションでのロール付与
@client.command()
async def selectrole(ctx):
    embed = discord.Embed(
        title='ロールの選択',
        description='リアクションをつけてロールを割り振り'
    )
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('✔️')
    await msg.add_reaction('❤️')

#サーバー情報表示
@client.event
async def on_raw_reaction_add(payload):
    ourMessageID = 988471291646459944

    if ourMessageID == payload.message_id:
        member = payload.member
        guild = member.guild

        emoji = payload.emoji.name
        if emoji == '✔️':
            role = discord.utils.get(guild.roles, name="Check")
        elif emoji ==  '❤️':
            role = discord.utils.get(guild.roles, name="Heart") 
        await member.add_roles(role)

#サーバー情報表示
@client.event
async def on_raw_reaction_remove(payload):
    ourMessageID = 988471291646459944

    if ourMessageID == payload.message_id:
        guild = await(client.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name
        if emoji == '✔️':
            role = discord.utils.get(guild.roles, name="Check")
        elif emoji ==  '❤️':
            role = discord.utils.get(guild.roles, name="Heart") 
        member = await(guild.fetch_member(payload.user_id))
        if member is not None:
            await member.remove_roles(role)
        else:
             print("Member not found")

#サーバー情報表示
@client.command()
async def info(ctx):
    channel = ctx.channel
    mbed = discord.Embed(
        title = 'インフォ',
        #description = "チャンネルID : {}\nチャンネル名 : {}".format(ctx.channel.id, ctx.channel.name)
        description = f"{'Category: {}'.format(channel.category.name)}"
    )
    mbed.add_field(name="Channel Guild", value = ctx.guild.name, inline=False)
    mbed.add_field(name="Channel id", value = channel.id, inline=False)
    mbed.add_field(name="Channel Topic", value = f"{channel.topic if channel.topic else 'No topic.'}", inline=False)
    mbed.add_field(name="Channel Position", value = channel.position, inline=False)
    mbed.add_field(name="Channel Slowmode Delay", value = channel.slowmode_delay, inline=False)
    mbed.add_field(name="Channel is nsfw?", value = channel.is_nsfw(), inline=False)
    mbed.add_field(name="Channel is news?", value = channel.is_news(), inline=False)
    mbed.add_field(name="Channel Creation Time", value = channel.created_at, inline=False)
    mbed.add_field(name="Channel Permissions Synced", value = channel.permissions_synced, inline=False)
    mbed.add_field(name="Channel Hash", value = hash(channel), inline=False)
    if ctx.author.guild_permissions.manage_channels:    
        await ctx.send(embed=mbed)


token = config.DISCORD_TOKEN
client.run(token)