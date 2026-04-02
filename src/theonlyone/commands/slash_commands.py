from discord import app_commands
from discord.ext import commands
import discord
import datetime
from theonlyone.utils.logger import logger


class CmdSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando simples para verificar latência
    @app_commands.command(name="ping", description="Latência do bot")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! {latency}ms")

    # Comando para banir um usuário
    @app_commands.command(name="ban", description="Banir um usuário")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        motivo: str = "Não informado!",
    ):
        await user.ban(reason=motivo)

        await interaction.response.send_message(
            f"🔨 {user.mention} foi banido.\n"
            f"Motivo: {motivo}\n"
            f"Responsável: {interaction.user}"
        )

        logger.info(
            f"Ban | Usuário: {user} | ID: {user.id} | "
            f"Servidor: {interaction.guild.name} | Moderador: {interaction.user}"
        )

    # Comando de timeout com escolha de unidade de tempo
    @app_commands.command(name="timeout", description="Aplicar timeout em um membro")
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.choices(
        unidade=[
            app_commands.Choice(name="Segundos", value="s"),
            app_commands.Choice(name="Minutos", value="m"),
            app_commands.Choice(name="Horas", value="h"),
            app_commands.Choice(name="Dias", value="d"),
        ]
    )
    async def timeout(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        tempo: int,
        unidade: app_commands.Choice[str],
        motivo: str = "Não informado!",
    ):
        if tempo <= 0:
            return await interaction.response.send_message(
                "❌ Tempo inválido.",
                ephemeral=True
            )

        mapa_tempo = {
            "s": "seconds",
            "m": "minutes",
            "h": "hours",
            "d": "days",
        }

        delta = datetime.timedelta(**{mapa_tempo[unidade.value]: tempo})
        duracao = discord.utils.utcnow() + delta

        await user.timeout(duracao, reason=motivo)

        await interaction.response.send_message(
            f"⏳ {user.mention} ficou em timeout por {tempo}{unidade.value}\n"
            f"Motivo: {motivo}\n"
            f"Responsável: {interaction.user}"
        )

        logger.info(
            f"Timeout | Usuário: {user} | Tempo: {tempo}{unidade.value} | "
            f"Servidor: {interaction.guild.name} | Moderador: {interaction.user}"
        )
        
        # Comando para limpar chats
    @app_commands.command(
    name="clear",
    description="Limpa mensagens do chat (máx: 1000)"
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(
        self,
        interaction: discord.Interaction,
        quantidade: int
    ):
        # validação
        if quantidade <= 0 or quantidade > 1000:
            return await interaction.response.send_message(
                f"⚠️ Quantidade inválida: {quantidade} (use 1–1000).",
                ephemeral=True
            )

        # evita timeout da interação
        await interaction.response.defer(ephemeral=True)

        # remove mensagens (+1 para apagar o comando)
        deletadas = await interaction.channel.purge(limit=quantidade + 1)

        # resposta final
        await interaction.followup.send(
            f"🧹 {len(deletadas) - 1} mensagens foram apagadas.",
            ephemeral=True
        )

        # log estruturado
        logger.info(
            f"Clear | Autor: {interaction.user} | "
            f"Canal: {interaction.channel} | Quantidade: {quantidade}"
        )


async def setup(bot):
    await bot.add_cog(CmdSlash(bot))