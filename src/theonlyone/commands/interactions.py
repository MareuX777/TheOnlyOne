import discord
from discord import app_commands, ui
from discord.ext import commands
from theonlyone.utils.logger import logger


class TicketModal(ui.Modal, title="Criar Ticket"):
    """Modal para criar um novo ticket com título e descrição"""
    
    titulo = ui.TextInput(
        label="Título do Ticket",
        placeholder="Descreva brevemente seu problema",
        max_length=100,
    )
    
    descricao = ui.TextInput(
        label="Descrição do Problema",
        placeholder="Forneça mais detalhes sobre o seu problema",
        style=discord.TextStyle.paragraph,
        max_length=1000,
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📋 Novo Ticket Criado",
            description=f"**Título:** {self.titulo.value}\n\n**Descrição:** {self.descricao.value}",
            color=discord.Color.green(),
        )
        embed.set_footer(text=f"Criado por {interaction.user}", icon_url=interaction.user.avatar)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"Ticket criado | Usuário: {interaction.user} | Título: {self.titulo.value}")


class ConfirmButton(ui.View):
    """Buttons para confirmar/cancelar ações"""
    
    def __init__(self, timeout=180):
        super().__init__(timeout=timeout)
        self.confirmed = None
    
    @ui.button(label="✅ Confirmar", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: ui.Button):
        self.confirmed = True
        await interaction.response.defer()
        self.stop()
    
    @ui.button(label="❌ Cancelar", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: ui.Button):
        self.confirmed = False
        await interaction.response.defer()
        self.stop()


class TicketCategorySelect(ui.View):
    """Select Menu (Dropdown) para categorizar tickets"""
    
    def __init__(self, timeout=180):
        super().__init__(timeout=timeout)
        self.category = None
    
    @ui.select(
        placeholder="Escolha a categoria do seu ticket",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="🐛 Bug Report", value="bug", description="Reportar um bug"),
            discord.SelectOption(label="💡 Sugestão", value="suggestion", description="Enviar uma sugestão"),
            discord.SelectOption(label="❓ Suporte", value="support", description="Pedir suporte"),
            discord.SelectOption(label="🎮 Gameplay", value="gameplay", description="Problema de gameplay"),
            discord.SelectOption(label="💳 Pagamento", value="payment", description="Questão de pagamento"),
        ]
    )
    async def select_category(self, interaction: discord.Interaction, select: ui.Select):
        self.category = select.values[0]
        
        category_names = {
            "bug": "🐛 Bug Report",
            "suggestion": "💡 Sugestão",
            "support": "❓ Suporte",
            "gameplay": "🎮 Gameplay",
            "payment": "💳 Pagamento",
        }
        
        embed = discord.Embed(
            title="Categoria Selecionada",
            description=f"Você selecionou: **{category_names.get(self.category, 'Desconhecida')}**",
            color=discord.Color.blue(),
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"Categoria selecionada | Usuário: {interaction.user} | Categoria: {self.category}")
        self.stop()


class RoleSelectMenu(ui.View):
    """Select Menu para escolher roles (Reaction Roles simplificado)"""
    
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)
    
    @ui.select(
        placeholder="Clique para escolher seus roles",
        min_values=0,
        max_values=5,
        options=[
            discord.SelectOption(label="🎮 Gamer", value="gamer", emoji="🎮"),
            discord.SelectOption(label="🎨 Artista", value="artista", emoji="🎨"),
            discord.SelectOption(label="🎵 Músico", value="musico", emoji="🎵"),
            discord.SelectOption(label="📚 Leitor", value="leitor", emoji="📚"),
            discord.SelectOption(label="⚙️ Dev", value="dev", emoji="⚙️"),
        ]
    )
    async def select_roles(self, interaction: discord.Interaction, select: ui.Select):
        try:
            guild = interaction.guild
            user = interaction.user
            
            # Mapa de nomes de roles para seus valores
            role_map = {
                "gamer": "Gamer",
                "artista": "Artista",
                "musico": "Músico",
                "leitor": "Leitor",
                "dev": "Dev",
            }
            
            added_roles = []
            removed_roles = []
            
            # Procura pelos roles no servidor
            for role_value in role_map:
                role = discord.utils.get(guild.roles, name=role_map[role_value])
                
                if role:
                    if role_value in select.values:
                        if role not in user.roles:
                            await user.add_roles(role)
                            added_roles.append(role.name)
                    else:
                        if role in user.roles:
                            await user.remove_roles(role)
                            removed_roles.append(role.name)
            
            # Cria mensagem de resposta
            response_text = ""
            if added_roles:
                response_text += f"✅ Roles adicionados: {', '.join(added_roles)}\n"
            if removed_roles:
                response_text += f"❌ Roles removidos: {', '.join(removed_roles)}\n"
            if not response_text:
                response_text = "Nenhuma mudança foi feita."
            
            await interaction.response.send_message(response_text, ephemeral=True)
            logger.info(f"Roles atualizados | Usuário: {user} | Adicionados: {added_roles} | Removidos: {removed_roles}")
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao atualizar roles: {e}", ephemeral=True)
            logger.error(f"Erro ao atualizar roles: {e}")


class BanConfirmView(ui.View):
    """Buttons customizados para confirmar/cancelar ban com contexto"""
    
    def __init__(self, user: discord.Member, reason: str, moderator: discord.User, timeout=60):
        super().__init__(timeout=timeout)
        self.user = user
        self.reason = reason
        self.moderator = moderator
        self.confirmed = None
    
    @ui.button(label="✅ Confirmar Ban", style=discord.ButtonStyle.green)
    async def confirm_ban(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user != self.moderator:
            await interaction.response.send_message("❌ Apenas o moderador pode confirmar!", ephemeral=True)
            return
        
        try:
            await self.user.ban(reason=self.reason)
            embed = discord.Embed(
                title="✅ Ban Confirmado",
                description=f"**Usuário:** {self.user.mention}\n**Razão:** {self.reason}",
                color=discord.Color.green(),
            )
            await interaction.response.send_message(embed=embed)
            logger.info(f"Ban confirmado | Usuário: {self.user} | Razão: {self.reason}")
            self.stop()
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao banir: {e}", ephemeral=True)
            logger.error(f"Erro ao banir usuário: {e}")
    
    @ui.button(label="❌ Cancelar", style=discord.ButtonStyle.red)
    async def cancel_ban(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user != self.moderator:
            await interaction.response.send_message("❌ Apenas o moderador pode cancelar!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="❌ Ban Cancelado",
            description="A ação foi cancelada.",
            color=discord.Color.red(),
        )
        await interaction.response.send_message(embed=embed)
        self.stop()


class InteractiveCommands(commands.Cog):
    """Cog para comandos interativos com Modals, Buttons e Select Menus"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ticket", description="Criar um novo ticket")
    async def ticket(self, interaction: discord.Interaction):
        """Abre um modal para criar um ticket"""
        await interaction.response.send_modal(TicketModal())
        logger.info(f"Modal de ticket aberto | Usuário: {interaction.user}")
    
    @app_commands.command(name="roles", description="Escolher seus roles")
    async def roles(self, interaction: discord.Interaction):
        """Envia um dropdown para escolher roles"""
        embed = discord.Embed(
            title="🎯 Escolha seus Roles",
            description="Selecione os roles que deseja ter abaixo:",
            color=discord.Color.purple(),
        )
        
        view = RoleSelectMenu()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        logger.info(f"Select menu de roles enviado | Usuário: {interaction.user}")
    
    @app_commands.command(name="report", description="Reportar um usuário")
    async def report(self, interaction: discord.Interaction, usuario: discord.Member, motivo: str):
        """Cria um modal para reportar um usuário com confirmação"""
        
        embed = discord.Embed(
            title="⚠️ Confirmar Reporte",
            description=f"Você tem certeza que deseja reportar **{usuario.mention}**?\n\n**Motivo:** {motivo}",
            color=discord.Color.orange(),
        )
        
        view = ConfirmButton()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
        await view.wait()
        
        if view.confirmed:
            confirmation = discord.Embed(
                title="✅ Reporte Enviado",
                description=f"Seu reporte de **{usuario.mention}** foi enviado para os moderadores.",
                color=discord.Color.green(),
            )
            await interaction.followup.send(embed=confirmation, ephemeral=True)
            logger.info(f"Reporte criado | Autor: {interaction.user} | Reportado: {usuario} | Motivo: {motivo}")
        else:
            cancellation = discord.Embed(
                title="❌ Reporte Cancelado",
                description="Seu reporte foi cancelado.",
                color=discord.Color.red(),
            )
            await interaction.followup.send(embed=cancellation, ephemeral=True)
    
    @app_commands.command(name="selectticket", description="Selecionar categoria do ticket")
    async def selectticket(self, interaction: discord.Interaction):
        """Envia um dropdown para categorizar tickets"""
        embed = discord.Embed(
            title="📋 Selecionar Categoria do Ticket",
            description="Escolha a categoria que melhor descreve seu problema:",
            color=discord.Color.blue(),
        )
        
        view = TicketCategorySelect()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        logger.info(f"Select menu de categoria enviado | Usuário: {interaction.user}")
    
    @app_commands.command(name="banreview", description="Ban com confirmação via buttons")
    @app_commands.checks.has_permissions(ban_members=True)
    async def banreview(self, interaction: discord.Interaction, usuario: discord.Member, motivo: str = "Sem motivo"):
        """Ban com confirmação visual via buttons"""
        
        view = BanConfirmView(usuario, motivo, interaction.user)
        
        embed = discord.Embed(
            title="🔨 Confirmar Ban",
            description=f"**Usuário:** {usuario.mention}\n**Razão:** {motivo}\n\nClique em um botão para confirmar ou cancelar.",
            color=discord.Color.red(),
        )
        
        await interaction.response.send_message(embed=embed, view=view)
        logger.info(f"Confirmação de ban solicitada | Moderador: {interaction.user} | Usuário: {usuario}")


async def setup(bot):
    await bot.add_cog(InteractiveCommands(bot))
