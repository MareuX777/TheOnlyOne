import discord
from discord import app_commands
from discord.ext import commands
import datetime
from theonlyone.utils.logger import logger


class Moderation(commands.Cog):
    """Cog para comandos de moderação"""
    
    def __init__(self, bot):
        self.bot = bot
        self.warns = {}  # {user_id: [{"motivo": str, "moderador": str, "data": datetime}]}

    # ==================== BAN ====================
    @app_commands.command(name="ban", description="Banir um usuário")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        motivo: str = "Não informado!",
    ):
        """Bane um membro do servidor"""
        await user.ban(reason=motivo)

        embed = discord.Embed(
            title="🔨 Usuário Banido",
            description=f"**Usuário:** {user.mention}\n**Motivo:** {motivo}",
            color=discord.Color.red(),
        )
        embed.set_footer(text=f"Responsável: {interaction.user}")
        await interaction.response.send_message(embed=embed)

        logger.info(
            f"Ban | Usuário: {user} | ID: {user.id} | "
            f"Servidor: {interaction.guild.name} | Moderador: {interaction.user}"
        )

    # ==================== UNBAN ====================
    @app_commands.command(name="unban", description="Desbanir um usuário")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(
        self,
        interaction: discord.Interaction,
        user: discord.User,
    ):
        """Desbanir um usuário do servidor"""
        await interaction.guild.unban(user)

        embed = discord.Embed(
            title="✅ Usuário Desbanido",
            description=f"**Usuário:** {user.mention}",
            color=discord.Color.green(),
        )
        embed.set_footer(text=f"Responsável: {interaction.user}")
        await interaction.response.send_message(embed=embed)

        logger.info(
            f"Unban | Usuário: {user} | Servidor: {interaction.guild.name} | "
            f"Moderador: {interaction.user}"
        )

    # ==================== KICK ====================
    @app_commands.command(name="kick", description="Expulsar um membro")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        motivo: str = "Não informado!",
    ):
        """Expulsa um membro do servidor"""
        await user.kick(reason=motivo)

        embed = discord.Embed(
            title="👢 Usuário Expulso",
            description=f"**Usuário:** {user.mention}\n**Motivo:** {motivo}",
            color=discord.Color.orange(),
        )
        embed.set_footer(text=f"Responsável: {interaction.user}")
        await interaction.response.send_message(embed=embed)

        logger.info(
            f"Kick | Usuário: {user} | ID: {user.id} | "
            f"Servidor: {interaction.guild.name} | Moderador: {interaction.user}"
        )

    # ==================== TIMEOUT ====================
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
        """Aplica timeout em um membro"""
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

        embed = discord.Embed(
            title="⏳ Timeout Aplicado",
            description=f"**Usuário:** {user.mention}\n**Duração:** {tempo}{unidade.value}\n**Motivo:** {motivo}",
            color=discord.Color.yellow(),
        )
        embed.set_footer(text=f"Responsável: {interaction.user}")
        await interaction.response.send_message(embed=embed)

        logger.info(
            f"Timeout | Usuário: {user} | Tempo: {tempo}{unidade.value} | "
            f"Servidor: {interaction.guild.name} | Moderador: {interaction.user}"
        )

    # ==================== CLEAR ====================
    @app_commands.command(name="clear", description="Limpar mensagens do chat (máx: 1000)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(
        self,
        interaction: discord.Interaction,
        quantidade: int,
    ):
        """Limpa mensagens do canal"""
        if quantidade <= 0 or quantidade > 1000:
            return await interaction.response.send_message(
                f"⚠️ Quantidade inválida: {quantidade} (use 1–1000).",
                ephemeral=True
            )

        await interaction.response.defer(ephemeral=True)
        deletadas = await interaction.channel.purge(limit=quantidade + 1)

        await interaction.followup.send(
            f"🧹 {len(deletadas) - 1} mensagens foram apagadas.",
            ephemeral=True
        )

        logger.info(
            f"Clear | Autor: {interaction.user} | "
            f"Canal: {interaction.channel} | Quantidade: {quantidade}"
        )

    # ==================== WARN ====================
    @app_commands.command(name="warn", description="Dar aviso a um membro")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        motivo: str = "Não informado!",
    ):
        """Adiciona um aviso a um membro"""
        user_id = str(user.id)
        if user_id not in self.warns:
            self.warns[user_id] = []
        
        self.warns[user_id].append({
            "motivo": motivo,
            "moderador": str(interaction.user),
            "data": datetime.datetime.now()
        })

        count = len(self.warns[user_id])
        
        embed = discord.Embed(
            title="⚠️ Aviso Registrado",
            description=f"**Usuário:** {user.mention}\n**Total de avisos:** {count}\n**Motivo:** {motivo}",
            color=discord.Color.orange(),
        )
        embed.set_footer(text=f"Responsável: {interaction.user}")
        await interaction.response.send_message(embed=embed)

        logger.info(
            f"Warn | Usuário: {user} | Moderador: {interaction.user} | Motivo: {motivo}"
        )

    # ==================== WARNINGS ====================
    @app_commands.command(name="warnings", description="Ver avisos de um membro")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warnings(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
    ):
        """Exibe todos os avisos de um membro"""
        user_id = str(user.id)
        if user_id not in self.warns or not self.warns[user_id]:
            embed = discord.Embed(
                title="✅ Sem Avisos",
                description=f"{user.mention} não possui avisos.",
                color=discord.Color.green(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title=f"⚠️ Avisos de {user}",
            color=discord.Color.orange(),
        )
        
        for i, w in enumerate(self.warns[user_id], 1):
            embed.add_field(
                name=f"Aviso {i}",
                value=f"**Motivo:** {w['motivo']}\n**Moderador:** {w['moderador']}\n**Data:** {w['data'].strftime('%d/%m/%Y %H:%M')}",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # ==================== MUTE ====================
    @app_commands.command(name="mute", description="Silenciar um membro")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def mute(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        motivo: str = "Não informado!",
    ):
        """Silencia um membro"""
        await interaction.response.defer(ephemeral=True)

        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await interaction.guild.create_role(
                name="Muted",
                color=discord.Color.dark_gray(),
                reason="Role de silenciamento automático"
            )
            for channel in interaction.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)

        await user.add_roles(muted_role, reason=motivo)
        
        embed = discord.Embed(
            title="🔇 Membro Silenciado",
            description=f"**Usuário:** {user.mention}\n**Motivo:** {motivo}",
            color=discord.Color.dark_grey(),
        )
        embed.set_footer(text=f"Responsável: {interaction.user}")
        await interaction.followup.send(embed=embed)

        logger.info(
            f"Mute | Usuário: {user} | Moderador: {interaction.user} | Motivo: {motivo}"
        )

    # ==================== UNMUTE ====================
    @app_commands.command(name="unmute", description="Dessilenciar um membro")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def unmute(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
    ):
        """Remove o silenciamento de um membro"""
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        
        if not muted_role or muted_role not in user.roles:
            embed = discord.Embed(
                title="❌ Não Silenciado",
                description=f"{user.mention} não está silenciado.",
                color=discord.Color.red(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await user.remove_roles(muted_role)
        
        embed = discord.Embed(
            title="🔊 Membro Dessilenciado",
            description=f"**Usuário:** {user.mention}",
            color=discord.Color.green(),
        )
        embed.set_footer(text=f"Responsável: {interaction.user}")
        await interaction.response.send_message(embed=embed)

        logger.info(
            f"Unmute | Usuário: {user} | Moderador: {interaction.user}"
        )


async def setup(bot):
    await bot.add_cog(Moderation(bot))
