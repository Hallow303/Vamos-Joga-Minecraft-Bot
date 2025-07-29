import discord
from discord.ext import commands
from discord import app_commands
from config import CANAL_PAINEL_ID, id_cargo_atendente, id_do_servidor


class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(value="denuncia", label="Denúncia", emoji="🚨"),
            discord.SelectOption(value="duvida", label="Dúvida", emoji="❓"),
            discord.SelectOption(value="pagamento", label="Pagamentos", emoji="💰"),
            discord.SelectOption(value="parceria", label="Parcerias", emoji="🤝"),
            discord.SelectOption(value="atendimento", label="Atendimento Geral", emoji="📨"),
        ]
        super().__init__(
            placeholder="Selecione uma opção...",
            min_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )

    async def callback(self, interaction: discord.Interaction):
        tipo = self.values[0]

        mensagens = {
            "denuncia": "🚨 Clique abaixo para abrir um ticket de denúncia. Forneça o máximo de detalhes possíveis e, se puder, provas (prints, IDs, etc).",
            "duvida": "❓ Clique abaixo para tirar uma dúvida. Seja específico e claro, isso agiliza a resposta.",
            "pagamento": "💰 Clique abaixo para relatar um problema com pagamentos. Explique o ocorrido e aguarde retorno.",
            "parceria": "🤝 Clique abaixo para tratar sobre parcerias. Diga com quem fala, qual a proposta e os dados básicos.",
            "atendimento": "📨 Clique abaixo para atendimento geral. Detalhe seu problema de forma direta.",
        }

        await interaction.response.send_message(
            content=mensagens[tipo],
            ephemeral=True,
            view=CreateTicket(tipo)
        )




class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())

class CreateTicket(discord.ui.View):
    def __init__(self, tipo: str):
        super().__init__(timeout=300)
        self.tipo = tipo
        self.value = None

    @discord.ui.button(label="Abrir Ticket", style=discord.ButtonStyle.blurple, emoji="➕")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

        ticket = None
        for thread in interaction.channel.threads:
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(ephemeral=True, content="Você já tem um atendimento em andamento!")
                    return

        async for thread in interaction.channel.archived_threads(private=True):
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.edit_original_response(content="Você já tem um atendimento em andamento!", view=None)
                    return

        nomes = {
            "denuncia": f"🚨 denúncia - {interaction.user.name} ({interaction.user.id})",
            "duvida": f"❓ dúvida - {interaction.user.name} ({interaction.user.id})",
            "pagamento": f"💰 pagamento - {interaction.user.name} ({interaction.user.id})",
            "parceria": f"🤝 parceria - {interaction.user.name} ({interaction.user.id})",
            "atendimento": f"📨 atendimento - {interaction.user.name} ({interaction.user.id})",
        }

        msg_inicial = {
            "denuncia": f"🚨 **|** Ticket de denúncia aberto. Detalhe o ocorrido e forneça provas se possível. <@&{id_cargo_atendente}>",
            "duvida": f"❓ **|** Ticket de dúvida aberto. Pergunte com clareza. <@&{id_cargo_atendente}>",
            "pagamento": f"💰 **|** Ticket de pagamento aberto. Relate o erro ocorrido com o máximo de detalhes. <@&{id_cargo_atendente}>",
            "parceria": "🤝 **|** Ticket de parceria aberto. Apresente sua proposta.",
            "atendimento": f"📨 **|** Ticket geral aberto. Envie as informações necessárias. <@&{id_cargo_atendente}>"
        }


        if ticket:
            await ticket.edit(archived=False, locked=False)
            await ticket.edit(name=nomes[self.tipo], auto_archive_duration=10080, invitable=False)
        else:
            ticket = await interaction.channel.create_thread(name=nomes[self.tipo], auto_archive_duration=10080)
            await ticket.edit(invitable=False)

        await interaction.response.send_message(ephemeral=True, content=f"Seu ticket foi criado: {ticket.mention}")
        await ticket.send(f"{msg_inicial[self.tipo]} {interaction.user.mention}")

class Ticket(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.add_view(DropdownView())

        canal = self.bot.get_channel(CANAL_PAINEL_ID)
        if canal:
            mensagens = []
            async for msg in canal.history(limit=10):
                mensagens.append(msg)
            for msg in mensagens:
                if msg.author == self.bot.user and msg.components:
                    return
            await canal.send("Mensagem do painel", view=DropdownView())

    @app_commands.command(name="setup", description="Envia o painel manualmente.")
    @app_commands.guilds(discord.Object(id_do_servidor))
    @app_commands.checks.has_permissions(manage_guild=True)
    async def setup(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)  # oculta a resposta do comando

        embed = discord.Embed(
            title="🎟️  | Central de Ajuda",
            description=(
                "❓ Nessa seção, você pode tirar suas dúvidas ou entrar em contato com a nossa equipe de suporte.\n\n"
                "🚫 Para evitar problemas, leia as opções com atenção e lembre-se de tentar pedir ajuda nos suportes comunitários antes de abrir um ticket.\n\n"
                "<:Discord:1144329364377448518>  | Tickets relacionados ao canal 🎮｜Vamos Jogar MINECRAFT??"
            ),
            color=discord.Color.blurple()
        )

        embed.set_author(
            name=interaction.guild.name,
            icon_url=interaction.guild.icon.url if interaction.guild.icon else None
        )

        embed.set_image(url="https://i.ibb.co/yFk7w0xX/9b617284-2865-4c57-877b-317716b46715.jpg")

        canal = self.bot.get_channel(CANAL_PAINEL_ID)
        if canal:
            await canal.send(embed=embed, view=DropdownView())

        await interaction.followup.send("Painel enviado com sucesso.", ephemeral=True)

    @app_commands.command(name="fecharticket", description="Feche um atendimento atual.")
    @app_commands.guilds(discord.Object(id_do_servidor))
    async def fecharticket(self, interaction: discord.Interaction):
        mod = interaction.guild.get_role(id_cargo_atendente)
        if str(interaction.user.id) in interaction.channel.name or (mod and mod in interaction.user.roles):
            await interaction.response.send_message(f"O ticket foi arquivado por {interaction.user.mention}, obrigado por entrar em contato!")
            await interaction.channel.edit(archived=True, locked=True)
        else:
            await interaction.response.send_message("Isso não pode ser feito aqui...")

async def setup(bot: commands.Bot):
    await bot.add_cog(Ticket(bot))
