import discord
from discord.ext import commands
import os
TOKEN = os.getenv("TOKEN")

TOKEN = "MTQ4MTcxOTQwODYwNTc5NDUyNg.GjECN_.kIsVgrsbMnvBQBMbWQgnaB-cRaDfutohokl_1I"
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

    game_id = discord.ui.TextInput(label="In-game ID")
    nickname = discord.ui.TextInput(label="In-game Nickname")
    recruiter_name = discord.ui.TextInput(label="Recruiter Nickname")
    recruiter_id = discord.ui.TextInput(label="Recruiter ID")

    async def on_submit(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="Open Ticket",
            description=f"{interaction.user.mention} created a new ticket 📱 Recruitment..",
            color=discord.Color.green()
        )

        embed.add_field(name="In-game ID:", value=self.game_id.value, inline=False)
        embed.add_field(name="In-game Nickname:", value=self.nickname.value, inline=False)
        embed.add_field(name="Recruiter Nickname:", value=self.recruiter_name.value, inline=False)
        embed.add_field(name="Recruiter ID:", value=self.recruiter_id.value, inline=False)

        await interaction.channel.send(embed=embed, view=TicketButtons())

        await interaction.response.send_message(
            "✅ Ticket submitted!", ephemeral=True
        )


# ---------------- BUTTONS ----------------

class TicketButtons(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.claimed = False


    @discord.ui.button(label="Claim Ticket", style=discord.ButtonStyle.primary)
    async def claim_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not any(role.id in STAFF_ROLE_IDS for role in interaction.user.roles):
            await interaction.response.send_message(
                "❌ You are not allowed to claim tickets.", ephemeral=True
            )
            return

        if self.claimed:
            await interaction.response.send_message(
                "⚠️ This ticket is already claimed.", ephemeral=True
            )
            return

        self.claimed = True

        button.disabled = True
        button.label = f"Claimed by {interaction.user.display_name}"

        await interaction.response.edit_message(view=self)


    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not any(role.id in STAFF_ROLE_IDS for role in interaction.user.roles):
            await interaction.response.send_message(
                "❌ You are not allowed to close tickets.", ephemeral=True
            )
            return

        await interaction.message.delete()

        await interaction.response.send_message(
            "❌ Ticket closed", ephemeral=True
        )


    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not any(role.id in STAFF_ROLE_IDS for role in interaction.user.roles):
            await interaction.response.send_message(
                "❌ You are not allowed to close tickets.", ephemeral=True
            )
            return

        await interaction.message.delete()

        await interaction.response.send_message(
            "❌ Ticket closed", ephemeral=True
        )


# ---------------- CREATE TICKET BUTTON ----------------

class CreateTicket(discord.ui.View):

    @discord.ui.button(label="Open Recruitment Ticket", style=discord.ButtonStyle.green)
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_modal(TicketModal())


# ---------------- COMMAND ----------------

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    channel = bot.get_channel(1481492593048158331)

    if channel:
        await channel.send(
            "Press the button below to open a recruitment ticket",
            view=CreateTicket()
        )

@bot.command()
async def ticketpanel(ctx):
    await ctx.send(
        "Press the button below to open a recruitment ticket",
        view=CreateTicket()
    )


bot.run(TOKEN)
