import discord
from discord.ext import commands
from datetime import timedelta

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("bot onn {bot.user}")




@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"❌ {error}", delete_after=5)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} online")

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log(self, guild, **fields):
        if ch := discord.utils.get(guild.text_channels, name="mod-logs"):
            e = discord.Embed(color=discord.Color.orange())
            [e.add_field(name=k, value=v) for k, v in fields.items()]
            await ch.send(embed=e)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, n: int = 5):
        d = await ctx.channel.purge(limit=min(n, 100) + 1)
        await ctx.send(f"🗑️ {len(d)-1} apagadas.", delete_after=3)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, m: discord.Member, *, r="Sem motivo"):
        await m.kick(reason=r) or await ctx.send(f"👢 {m} expulso. *{r}*")
        await self.log(ctx.guild, Ação="Kick", Membro=str(m), Motivo=r, Mod=ctx.author.mention)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, m: discord.Member, *, r="Sem motivo"):
        await m.ban(reason=r) or await ctx.send(f"🔨 {m} banido. *{r}*")
        await self.log(ctx.guild, Ação="Ban", Membro=str(m), Motivo=r, Mod=ctx.author.mention)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, tag: str):
        if e := discord.utils.find(lambda e: str(e.user) == tag, [e async for e in ctx.guild.bans()]):
            await ctx.guild.unban(e.user) or await ctx.send(f"✅ {e.user} desbanido.")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, m: discord.Member, mins: int = 5, *, r="Sem motivo"):
        await m.timeout(discord.utils.utcnow() + timedelta(minutes=mins), reason=r)
        await ctx.send(f"⏱️ {m} em timeout por {mins}min.")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"🏓 `{round(bot.latency*1000)}ms`")

async def main():
    async with bot:
        await bot.add_cog(Moderation(bot))
        await bot.start("SEU_TOKEN_AQUI")

import asyncio; asyncio.run(main())