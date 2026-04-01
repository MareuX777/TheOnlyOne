import discord
from discord.ext import commands
import asyncio

class Mods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong🏓 {round(self.bot.latency * 1000)}ms")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, membro: discord.Member, *, motivo="Não informado!"):
        mod = ctx.author
        await membro.ban(reason=motivo)
        await ctx.send(f"Membro {membro.mention} foi banido com sucesso!")
        print(f"Usuario: {membro.name}\n id: {membro.id}\n Foi banido do servidor: {ctx.guild.name}\n Moderador: {mod}")

    @ban.error
    async def ban_erro(self, ctx, erro):
        if isinstance(erro, commands.MissingPermissions):
            await ctx.send("Você não tem permissão para realizar esta ação!")
        elif isinstance(erro, commands.BotMissingPermissions):
            await ctx.send(f"**Eu não tenho permissão para fazer isso!**")
        else:
            print(erro)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, membro: discord.User):
        mod = ctx.author
        try:
            await ctx.guild.unban(membro)
            await ctx.send(f"Usuario {membro} foi desbanido com sucesso!")
            print(f"Usuario: {membro.name} foi desbanido do servidor {ctx.guild.name}")
        except discord.NotFound:
            await ctx.send(f"{membro} não foi banido do servidor!")
            print(f"Moderador {mod} tentou desbanir um usuario não banido.")
        except Exception as e:
            await ctx.send(f"Ocorreu um erro: {e}")
            print(f"Ocorreu um erro: {e}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, msg: int):
        mod = ctx.author
        await ctx.channel.purge(limit=msg + 1)
        await asyncio.sleep(2)
        await ctx.send(f'{msg} mensagens apagadas, do canal {ctx.channel}!', delete_after=5)
        print(f"{mod} apagou {msg} mensagens no canal {ctx.channel}!")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("**Você não tem permissão para realizar esta operação!❌**")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"**Eu não tenho permissão para realizar esta ação!❌**")
        else:
            print(error)

async def setup(bot):
    await bot.add_cog(Mods(bot))