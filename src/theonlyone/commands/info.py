import discord
from discord import app_commands
from discord.ext import commands
from theonlyone.utils.logger import logger


class Info(commands.Cog):
    """Cog para comandos de informação"""
    
    def __init__(self, bot):
        self.bot = bot

    # ==================== PING ====================
    @app_commands.command(name="ping", description="Verificar latência do bot")
    async def ping(self, interaction: discord.Interaction):
        """Exibe a latência do bot em ms"""
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 PONG!",
            description=f"Latência: **{latency}ms**",
            color=discord.Color.green(),
        )
        await interaction.response.send_message(embed=embed)

    # ==================== USERINFO ====================
    @app_commands.command(name="userinfo", description="Informações de um usuário")
    async def userinfo(
        self,
        interaction: discord.Interaction,
        user: discord.Member = None,
    ):
        """Exibe informações detalhadas de um usuário"""
        user = user or interaction.user
        
        embed = discord.Embed(
            title=f"👤 Informações de {user}",
            color=user.color,
        )
        
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Apelido", value=user.nick or "Sem apelido", inline=True)
        embed.add_field(name="Status", value=str(user.status).capitalize(), inline=True)
        
        embed.add_field(
            name="Entrou no servidor",
            value=user.joined_at.strftime("%d/%m/%Y às %H:%M") if user.joined_at else "Desconhecido",
            inline=True
        )
        embed.add_field(
            name="Conta criada em",
            value=user.created_at.strftime("%d/%m/%Y às %H:%M"),
            inline=True
        )
        
        roles = [r.mention for r in user.roles[1:]]  # Exclui @everyone
        embed.add_field(
            name=f"Roles ({len(roles)})",
            value=", ".join(roles) if roles else "Sem roles",
            inline=False
        )
        
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed.set_footer(text=f"Solicitado por {interaction.user}")
        
        await interaction.response.send_message(embed=embed)

    # ==================== SERVERINFO ====================
    @app_commands.command(name="serverinfo", description="Informações do servidor")
    async def serverinfo(self, interaction: discord.Interaction):
        """Exibe informações detalhadas do servidor"""
        guild = interaction.guild
        
        embed = discord.Embed(
            title=f"🏠 Informações de {guild.name}",
            color=discord.Color.blue(),
        )
        
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Dono", value=guild.owner.mention, inline=True)
        embed.add_field(name="Membros", value=guild.member_count, inline=True)
        
        embed.add_field(name="Canais", value=len(guild.channels), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Emojis", value=len(guild.emojis), inline=True)
        
        embed.add_field(
            name="Criado em",
            value=guild.created_at.strftime("%d/%m/%Y às %H:%M"),
            inline=False
        )
        
        boost_level = guild.premium_tier
        boost_count = guild.premium_subscription_count or 0
        embed.add_field(
            name="Boosts",
            value=f"Nível {boost_level} ({boost_count} boosts)",
            inline=True
        )
        
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.set_footer(text=f"Solicitado por {interaction.user}")
        
        await interaction.response.send_message(embed=embed)

    # ==================== HELP ====================
    @app_commands.command(name="help", description="Lista de comandos do bot")
    async def help(self, interaction: discord.Interaction):
        """Exibe a lista de comandos disponíveis"""
        embed = discord.Embed(
            title="📋 Comandos do Bot",
            description="Use `/comando` para executar",
            color=discord.Color.blurple(),
        )
        
        embed.add_field(
            name="🔨 Moderação",
            value="`ban` `unban` `kick` `timeout` `clear` `warn` `warnings` `mute` `unmute`",
            inline=False
        )
        
        embed.add_field(
            name="📊 Informações",
            value="`ping` `userinfo` `serverinfo` `help`",
            inline=False
        )
        
        embed.add_field(
            name="🎫 Sistema de Tickets",
            value="`ticket` `ticket_panel` `ticket_close` `ticket_add` `ticket_remove`",
            inline=False
        )
        
        embed.add_field(
            name="🎨 Reaction Roles",
            value="`reaction_role_setup` `reaction_role_add`",
            inline=False
        )
        
        embed.add_field(
            name="⚙️ Interativo",
            value="`ticket` `roles` `report` `selectticket` `banreview`",
            inline=False
        )
        
        embed.set_footer(text=f"Solicitado por {interaction.user}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Info(bot))
