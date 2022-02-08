import discord, textwrap, VocaroLyrics
from discord.ext import commands
from discord_slash import (
    SlashCommand,
    SlashContext,
    manage_components,
)

bot = commands.AutoShardedBot("/", None, None)
slash = SlashCommand(bot)

@slash.slash(name="검색")
async def 검색(ctx: SlashContext, title, artist: str = ""):
    t = title
    ar = artist
    
    try:
        d = VocaroLyrics.get_lyrics(song=t, artist=ar)
    except Exception as e:
        return await ctx.send(
            embed=discord.Embed(title="오류가 발생했습니다.", description="```\n{}\n```".format(e), color=discord.Color.red()),
            hidden=True
        ) 

    l = d.lyrics
    w = textwrap.wrap(l.replace("\n", "%n"), 500)

    cnt = 0
    wm = len(w) - 1

    s = manage_components.create_button(style=5, label="니코니코 동화", url=d.original_url.strip(), emoji=bot.get_emoji(940465967161565204))
    s = manage_components.create_actionrow(s)

    embed = discord.Embed(title="가사", description="```\n{}\n```".format(w[cnt].replace("%n", "\n")), color=discord.Color.blurple())
    embed.set_footer(text="{}/{}".format(cnt, wm))

    msg = await ctx.send(embed=embed, components=[s])

    await msg.add_reaction("◀")
    await msg.add_reaction("▶")    

    check = lambda reaction, user: str(reaction.emoji) in ("◀", "▶") and user == ctx.author and msg.id == reaction.message.id
        
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=120, check=check)
        except Exception as e:
            if type(e).__name__ == "TimeoutError":
                return msg.edit(embed=discord.Embed(title="Operation timed out", color=discord.Color.red()))

        if str(reaction.emoji) == "▶":
            if cnt < wm:
                await reaction.remove(user)
                cnt += 1
                embed = discord.Embed(title="가사", description="```\n{}\n```".format(w[cnt].replace("%n", "\n")), color=discord.Color.blurple())
                embed.set_footer(text="{}/{}".format(cnt, wm))
                await msg.edit(embed=embed, components=[s])
            else:
                await reaction.remove(user)
                cnt = 0
                embed = discord.Embed(title="가사", description="```\n{}\n```".format(w[cnt].replace("%n", "\n")), color=discord.Color.blurple())
                embed.set_footer(text="{}/{}".format(cnt, wm))
                await msg.edit(embed=embed, components=[s])
        
        if str(reaction.emoji) == "◀":
            if cnt > 0:
                await reaction.remove(user)
                cnt -= 1
                embed = discord.Embed(title="가사", description="```\n{}\n```".format(w[cnt].replace("%n", "\n")), color=discord.Color.blurple())
                embed.set_footer(text="{}/{}".format(cnt, wm))
                await msg.edit(embed=embed, components=[s])
            else:
                await reaction.remove(user)
                cnt = 0
                embed = discord.Embed(title="가사", description="```\n{}\n```".format(w[cnt].replace("%n", "\n")), color=discord.Color.blurple())
                embed.set_footer(text="{}/{}".format(cnt, wm))
                await msg.edit(embed=embed, components=[s])

bot.run("top secret")
