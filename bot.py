# Version 2.0 - 2026-13-03 - Updated to use discord.py 2.0 features and improved error handling. - Added support for multiple languages and enhanced the ticket management system. - Updated by SQRDIOS
import discord
from discord.ext import commands
import os
TOKEN = os.getenv("TOKEN")

CATEGORY_ID = 1481870388073070632  # Ticket category

STAFF_ROLE_IDS = [
    1481492592146255990,  # Admin
    1481492592146255989,  # LIDER 00
    1481492592146255988,   # 02
    1481492592146255987,   # 03
    1481492592146255986,   # SUB-LIDER 01
    1481492592146255984   # Gerente de farm
]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


# ---------------- MODAL ----------------

class TicketModal(discord.ui.Modal, title="Recruitment Ticket"):

    game_id = discord.ui.TextInput(label="ID IN-GAME")
    nickname = discord.ui.TextInput(label="NICK IN-GAME")
    recruiter_name = discord.ui.TextInput(label="NICK DO RECRUTADOR")
    recruiter_id = discord.ui.TextInput(label="ID DO RECRUTADOR")

    async def on_submit(self, interaction: discord.Interaction):

        guild = interaction.guild
        category = discord.utils.get(guild.categories, id=CATEGORY_ID)

        channel_name = f"{self.recruiter_name.value}-{self.recruiter_id.value}".lower().replace(" ", "-")

        overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        for role_id in STAFF_ROLE_IDS:
            role = guild.get_role(role_id)
            overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites
        )

        embed = discord.Embed(
            title="Ticket Aberto",
            description=f"{interaction.user.mention} criou um novo ticket 📞 Recrutamento.",
            color=discord.Color.green()
        )

        embed.add_field(name="ID IN-GAME:", value=self.game_id.value, inline=False)
        embed.add_field(name="NICK IN-GAME:", value=self.nickname.value, inline=False)
        embed.add_field(name="NICK DO RECRUTADOR:", value=self.recruiter_name.value, inline=False)
        embed.add_field(name="ID DO RECRUTADOR:", value=self.recruiter_id.value, inline=False)

        await ticket_channel.send(embed=embed, view=TicketButtons())

        await interaction.response.send_message(
            f"✅ Ticket created: {ticket_channel.mention}",
            ephemeral=True
        )


# ---------------- BUTTONS ----------------

class TicketButtons(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.claimed = False


    @discord.ui.button(label="📜 Reivindicar Ticket", style=discord.ButtonStyle.primary)
    async def claim_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not any(role.id in STAFF_ROLE_IDS for role in interaction.user.roles):
            await interaction.response.send_message(
                "❌ Você não tem permissão para retirar ingressos.", ephemeral=True
            )
            return

        if self.claimed:
            await interaction.response.send_message(
                "⚠️ Este bilhete já foi reservado.", ephemeral=True
            )
            return

        self.claimed = True

        button.disabled = True
        button.label = f"Reivindicado por {interaction.user.display_name}"

        await interaction.response.edit_message(view=self)


    @discord.ui.button(label="🔒 Fechar Ticket", style=discord.ButtonStyle.danger)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not any(role.id in STAFF_ROLE_IDS for role in interaction.user.roles):
            await interaction.response.send_message(
                "❌ Você não tem permissão para fechar chamados.", ephemeral=True
            )
            return

        await interaction.message.delete()

        await interaction.response.send_message(
            "❌ Bilhete fechado", ephemeral=True
        )


# ---------------- CREATE TICKET BUTTON ----------------

class CreateTicket(discord.ui.View):

    @discord.ui.button(label="Abrir ticket de recrutamento", style=discord.ButtonStyle.green)
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_modal(TicketModal())


# ---------------- COMMAND ----------------

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    channel = bot.get_channel(1481492593048158331)

    if channel:
        await channel.send(
            "Pressione o botão abaixo para abrir um formulário de recrutamento.",
            view=CreateTicket()
        )

@bot.command()
async def ticketpanel(ctx):
    await ctx.send(
        "Pressione o botão abaixo para abrir um formulário de recrutamento.",
        view=CreateTicket()
    )


bot.run(TOKEN)
