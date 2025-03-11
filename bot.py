import discord
from discord.ext import commands
import youtube_dl
import os
from youtube_search import YoutubeSearch

client = commands.Bot(command_prefix='$')


@client.event
async def on_ready():
    print(f'We are logged in as {client.user}')


@client.command()
async def servidor(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title='Informações do Servidor: ' + name,
        description=description,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name='Dono', value=owner, inline=True)
    embed.add_field(name='ID do Servidor', value=id, inline=True)
    embed.add_field(name='Região', value=region, inline=True)
    embed.add_field(name='Membros', value=memberCount, inline=True)

    await ctx.send(embed=embed)

@client.command()
async def ajuda(ctx):
    bot_name = str(client.user.name)
    bot_icon = str(client.user.avatar_url)

    embed = discord.Embed(
        title=bot_name,
        description='Olá, eu sou o Rammus Bot! Aqui estão os meus comandos :grin:',
        color=discord.Color.gold()
    )
    embed.set_thumbnail(url=bot_icon)
    embed.add_field(name='Comandos: Gerais',
                    value='**$ajuda:** Mostra todos os comandos\n\n'
                          '**$servidor:** Mostra detalhes do servidor\n\n'
                          '**$oi:** Cumprimenta o usuário',
                    inline=True)
    embed.add_field(name='Comandos: DJ Rammus',
                    value='**$play:** Reproduz o aúdio de um vídeo do YouTube\n\n'
                          '**$stop:** Cancela a música em reprodução\n\n'
                          '**$pause:** Pausa a música\n\n'
                          '**$resume:** Despausa a música',
                    inline=True)

    await ctx.send(embed=embed)

# Música


@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    try:
        await channel.connect()
    except discord.ClientException:
        await ctx.send('O **DJ Rammus** já está em um Canal de Voz')
    else:
        await ctx.send(f'O **DJ Rammus** entrou no canal **{channel}**')


@client.command()
async def play(ctx, search):
    try:
        if os.path.exists('song.webm'):
            os.remove('song.webm')
    except PermissionError:
        await ctx.send('O **DJ Rammus** já está tocando uma música. Para parar, digite ´$stop´')
    else:
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            await ctx.send('O **DJ Rammus** não consegue te achar pois você não está em um Canal de Voz')
        else:
            ydl_opts = {'format': '249/250/251'}  # Download Preferences

            results = YoutubeSearch(search, max_results=1).to_dict()[0]

            videoUrl = 'https://www.youtube.com' + results['url_suffix']

            videoTitle = results['title']

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([videoUrl])  # Download the video
            for file in os.listdir('../'):
                if file.endswith('.webm'):
                    os.rename(file, 'song.webm')
                else:
                    print('Failed')
            source = discord.FFmpegPCMAudio('song.webm')

            if ctx.voice_client is None:
                voice = await channel.connect()
            else:
                voice = ctx.voice_client
            player = voice.play(source)

            await ctx.send(f'O **DJ Rammus** está tocando **{videoTitle}** no canal **{ctx.author.voice.channel}**')


@client.command()
async def leave(ctx):
    voice = ctx.voice_client
    try:
        await voice.disconnect()
    except AttributeError:
        await ctx.send("O **DJ Rammus** não está em nenhum Canal de Voz")
    else:
        await ctx.send(f'O **DJ Rammus** saiu do canal **{ctx.author.voice.channel}**')


@client.command()
async def pause(ctx):
    voice = ctx.voice_client
    try:
        voice.pause()
    except AttributeError:
        await ctx.send("O **DJ Rammus** não está tocando nada")
    else:
        await ctx.send('O **DJ Rammus** pausou a música')


@client.command()
async def resume(ctx):
    voice = ctx.voice_client
    try:
        voice.resume()
    except AttributeError:
        await ctx.send("O **DJ Rammus** não pausou nenhuma música")
    else:
        await ctx.send('O **DJ Rammus** despausou a música')


@client.command()
async def stop(ctx):
    try:
        voice = ctx.voice_client
        voice.stop()
    except AttributeError:
        await ctx.send('O **DJ Rammus** não está tocando nada')
    else:
        await ctx.send('O **DJ Rammus** parou a música')

token = '<TOKEN>'  # Insert your Discord Bot Token
client.run(token)
