import discord
from discord.ext import commands
import datetime
from theonlyone.utils.logger import logger


class CommandsPrefix(commands.Cog):
    """Cog para comandos com prefixo"""
    
    def __init__(self, bot):
        self.bot = bot
        self.warns = {}  # {user_id: [{"motivo": str, "moderador": str, "data": datetime}]}

    # ==================== BAN ====================
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, membro: discord.Member, *, motivo="Não informado!"):
        """Bane um membro do servidor
        Uso: $ban @usuario motivo
        """
        await membro.ban(reason=motivo)

        embed = discord.Embed(
            title="🔨 Usuário Banido",
            description=f"**Usuário:** {membro.mention}\n**Motivo:** {motivo}",
            color=discord.Color.red(),
        )
        embed.set_footer(text=f"Responsável: {ctx.author}")
        await ctx.send(embed=embed)

        logger.info(
            f"Ban | Usuário: {membro} | ID: {membro.id} | "
            f"Servidor: {ctx.guild.name} | Moderador: {ctx.author}"
        )

    # ==================== UNBAN ====================
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, membro: discord.User):
        """Desbanir um usuário
        Uso: $unban @usuario
        """
        await ctx.guild.unban(membro)

        embed = discord.Embed(
            title="✅ Usuário Desbanido",
            description=f"**Usuário:** {membro.mention}",
            color=discord.Color.green(),
        )
        embed.set_footer(text=f"Responsável: {ctx.author}")
        await ctx.send(embed=embed)

        logger.info(
            f"Unban | Usuário: {membro} | Servidor: {ctx.guild.name} | "
            f"Moderador: {ctx.author}"
        )

    # ==================== KICK ====================
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, membro: discord.Member, *, motivo="Não informado!"):
        """Expulsa um membro do servidor
        Uso: $kick @usuario motivo
        """
        await membro.kick(reason=motivo)

        embed = discord.Embed(
            title="👢 Usuário Expulso",
            description=f"**Usuário:** {membro.mention}\n**Motivo:** {motivo}",
            color=discord.Color.orange(),
        )
        embed.set_footer(text=f"Responsável: {ctx.author}")
        await ctx.send(embed=embed)

        logger.info(
            f"Kick | Usuário: {membro} | ID: {membro.id} | "
            f"Servidor: {ctx.guild.name} | Moderador: {ctx.author}"
        )

    # ==================== TIMEOUT ====================
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def timeout(
        self,
        ctx,
        membro: discord.Member,
        tempo: int,
        unidade: str,
        *,
        motivo="Não informado!",
    ):
        """Aplica timeout em um membro
        Unidades: s (segundos), m (minutos), h (horas), d (dias)
        Uso: $timeout @usuario 5 m motivo
        """
        unidade = unidade.lower()

        mapa_tempo = {
            "s": "seconds",
            "m": "minutes",
            "h": "hours",
            "d": "days",
        }

        if tempo <= 0:
            return await ctx.send("❌ Tempo inválido.")

        if unidade not in mapa_tempo:
            return await ctx.send("❌ Use: s (segundos), m, h ou d.")

        delta = datetime.timedelta(**{mapa_tempo[unidade]: tempo})
        duracao = discord.utils.utcnow() + delta

        await membro.timeout(duracao, reason=motivo)

        embed = discord.Embed(
            title="⏳ Timeout Aplicado",
            description=f"**Usuário:** {membro.mention}\n**Duração:** {tempo}{unidade}\n**Motivo:** {motivo}",
            color=discord.Color.yellow(),
        )
        embed.set_footer(text=f"Responsável: {ctx.author}")
        await ctx.send(embed=embed)

        logger.info(
            f"Timeout | Usuário: {membro} | Tempo: {tempo}{unidade} | "
            f"Servidor: {ctx.guild.name} | Moderador: {ctx.author}"
        )

    # ==================== CLEAR ====================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, quantidade: int):
        """Limpa mensagens do canal
        Uso: $clear 10
        """
        if quantidade <= 0 or quantidade > 1000:
            return await ctx.send(f"⚠️ Quantidade inválida: {quantidade} (use 1–1000).")

        deletadas = await ctx.channel.purge(limit=quantidade + 1)

        embed = discord.Embed(
            title="🧹 Mensagens Limpas",
            description=f"**Quantidade:** {len(deletadas) - 1} mensagens deletadas",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed, delete_after=5)

        logger.info(
            f"Clear | Autor: {ctx.author} | Canal: {ctx.channel} | Quantidade: {quantidade}"
        )

    # ==================== WARN ====================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, membro: discord.Member, *, motivo="Não informado!"):
        """Adiciona um aviso a um membro
        Uso: $warn @usuario motivo
        """
        user_id = str(membro.id)
        if user_id not in self.warns:
            self.warns[user_id] = []
        
        self.warns[user_id].append({
            "motivo": motivo,
            "moderador": str(ctx.author),
            "data": datetime.datetime.now()
        })

        count = len(self.warns[user_id])
        
        embed = discord.Embed(
            title="⚠️ Aviso Registrado",
            description=f"**Usuário:** {membro.mention}\n**Total:** {count}\n**Motivo:** {motivo}",
            color=discord.Color.orange(),
        )
        embed.set_footer(text=f"Responsável: {ctx.author}")
        await ctx.send(embed=embed)

        logger.info(
            f"Warn | Usuário: {membro} | Moderador: {ctx.author} | Motivo: {motivo}"
        )

    # ==================== WARNINGS ====================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, ctx, membro: discord.Member):
        """Exibe todos os avisos de um membro
        Uso: $warnings @usuario
        """
        user_id = str(membro.id)
        if user_id not in self.warns or not self.warns[user_id]:
            embed = discord.Embed(
                title="✅ Sem Avisos",
                description=f"{membro.mention} não possui avisos.",
                color=discord.Color.green(),
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title=f"⚠️ Avisos de {membro}",
            color=discord.Color.orange(),
        )
        
        for i, w in enumerate(self.warns[user_id], 1):
            embed.add_field(
                name=f"Aviso {i}",
                value=f"**Motivo:** {w['motivo']}\n**Moderador:** {w['moderador']}\n**Data:** {w['data'].strftime('%d/%m/%Y %H:%M')}",
                inline=False
            )
        
        await ctx.send(embed=embed)

    # ==================== MUTE ====================
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, membro: discord.Member, *, motivo="Não informado!"):
        """Silencia um membro
        Uso: $mute @usuario motivo
        """
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(
                name="Muted",
                color=discord.Color.dark_gray(),
                reason="Role de silenciamento automático"
            )
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)

        await membro.add_roles(muted_role, reason=motivo)
        
        embed = discord.Embed(
            title="🔇 Membro Silenciado",
            description=f"**Usuário:** {membro.mention}\n**Motivo:** {motivo}",
            color=discord.Color.dark_grey(),
        )
        embed.set_footer(text=f"Responsável: {ctx.author}")
        await ctx.send(embed=embed)

        logger.info(
            f"Mute | Usuário: {membro} | Moderador: {ctx.author} | Motivo: {motivo}"
        )

    # ==================== UNMUTE ====================
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, membro: discord.Member):
        """Remove o silenciamento de um membro
        Uso: $unmute @usuario
        """
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        
        if not muted_role or muted_role not in membro.roles:
            embed = discord.Embed(
                title="❌ Não Silenciado",
                description=f"{membro.mention} não está silenciado.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        await membro.remove_roles(muted_role)
        
        embed = discord.Embed(
            title="🔊 Membro Dessilenciado",
            description=f"**Usuário:** {membro.mention}",
            color=discord.Color.green(),
        )
        embed.set_footer(text=f"Responsável: {ctx.author}")
        await ctx.send(embed=embed)

        logger.info(
            f"Unmute | Usuário: {membro} | Moderador: {ctx.author}"
        )

    # ==================== PING ====================
    @commands.command()
    async def ping(self, ctx):
        """Exibe a latência do bot
        Uso: $ping
        """
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 PONG!",
            description=f"Latência: **{latency}ms**",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)

    # ==================== USERINFO ====================
    @commands.command()
    async def userinfo(self, ctx, membro: discord.Member = None):
        """Exibe informações de um usuário
        Uso: $userinfo @usuario
        """
        membro = membro or ctx.author
        
        embed = discord.Embed(
            title=f"👤 Informações de {membro}",
            color=membro.color,
        )
        
        embed.add_field(name="ID", value=membro.id, inline=True)
        embed.add_field(name="Apelido", value=membro.nick or "Sem apelido", inline=True)
        embed.add_field(name="Status", value=str(membro.status).capitalize(), inline=True)
        
        embed.add_field(
            name="Entrou no servidor",
            value=membro.joined_at.strftime("%d/%m/%Y às %H:%M") if membro.joined_at else "Desconhecido",
            inline=True
        )
        embed.add_field(
            name="Conta criada em",
            value=membro.created_at.strftime("%d/%m/%Y às %H:%M"),
            inline=True
        )
        
        roles = [r.mention for r in membro.roles[1:]]
        embed.add_field(
            name=f"Roles ({len(roles)})",
            value=", ".join(roles) if roles else "Sem roles",
            inline=False
        )
        
        embed.set_thumbnail(url=membro.avatar.url if membro.avatar else membro.default_avatar.url)
        embed.set_footer(text=f"Solicitado por {ctx.author}")
        
        await ctx.send(embed=embed)

    # ==================== SERVERINFO ====================
    @commands.command()
    async def serverinfo(self, ctx):
        """Exibe informações do servidor
        Uso: $serverinfo
        """
        guild = ctx.guild
        
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
        embed.set_footer(text=f"Solicitado por {ctx.author}")
        
        await ctx.send(embed=embed)

    # ==================== HELP ====================
    @commands.command()
    async def help(self, ctx):
        """Lista de comandos com prefixo
        Uso: $help
        """
        embed = discord.Embed(
            title="📋 Comandos com Prefixo",
            description="Use `$` ou `!` para executar",
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
        
        embed.set_footer(text=f"Solicitado por {ctx.author}")
        
        await ctx.send(embed=embed)

    # ==================== ERROR HANDLER ====================
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Tratamento global de erros"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Você não tem permissão para esta ação.")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ Eu não tenho permissão para executar isso.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("❌ Membro não encontrado.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Argumento inválido. Verifique o uso do comando.")
        else:
            await ctx.send("❌ Ocorreu um erro inesperado.")
            logger.error(
                f"Erro | Servidor: {ctx.guild.name if ctx.guild else 'DM'} | Erro: {error}"
            )


async def setup(bot):
    await bot.add_cog(CommandsPrefix(bot))
