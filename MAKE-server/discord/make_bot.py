import datetime
import discord
from discord.ext import tasks, commands

from db_schema import MongoDB

intents = discord.Intents.default()
intents.members = True

class MakeBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)

    async def setup_hook(self) -> None:
        # Register the persistent view for listening here.
        # Note that this does not send the view to any message.
        # In order to do this you need to first send a message with the View, which is shown below.
        # If you have the message_id you can also pass it as a keyword argument, but for this example
        # we don't have one.
        self.add_view(CollegeView())
        self.add_view(PronounView())
        self.add_view(YearView())

        self.no_steward_message_sent = False
        #self.announcement_channel_id = 857333481474097203
        self.announcement_channel_id = 526941847831183363
        self.check_shifts.start()

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        print('------')


    @tasks.loop(seconds=60)
    async def check_shifts(self):
        hour = datetime.datetime.now().hour
        day_of_week = datetime.datetime.now().weekday()

        day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][day_of_week]

        hour = 3 + 12;
        if hour == 0:
            hour = "12:00 AM"
        elif hour == 12:
            hour = "12:00 PM"
        elif hour > 12:
            hour = str(hour - 12) + ":00 PM"
        else:
            hour = str(hour) + ":00 AM"

        if self.no_steward_message_sent == hour:
            return
        else:
            self.no_steward_message_sent = False

        db = MongoDB()

        shifts = await db.get_collection("shifts")
        print("Checking shifts", hour, "...")
        shift = await shifts.find_one({"timestamp_start": hour})
        if shift is not None:
            if len(shift.stewards_dropped) == len(shift.stewards) and len(shift.stewards_picked_up) == 0:
                # send message to announcement channel
                channel = bot.get_channel(self.announcement_channel_id)

                if channel is not None:
                    await channel.send(f'''**CLOSURE**: The Makerspace will be closed for the next hour. Sorry for the inconvenience!''')
                    no_steward_message_sent = hour

bot = MakeBot()

class CollegeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Harvey Mudd', style=discord.ButtonStyle.blurple, custom_id='persistent_view:college:hmc')
    async def hmc(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role Harvey Mudd!', ephemeral=True)
        await grant_create_role(interaction.user, "Harvey Mudd", to_remove=["Pomona", "Pitzer", "Scripps", "Claremont McKenna", "Claremont Graduate University", "Keck Graduate Institute"])
    
    @discord.ui.button(label='Pitzer', style=discord.ButtonStyle.blurple, custom_id='persistent_view:college:pitzer')
    async def pitzer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role Pitzer!', ephemeral=True)
        await grant_create_role(interaction.user, "Pitzer", to_remove=["Harvey Mudd", "Pomona", "Scripps", "Claremont McKenna", "Claremont Graduate University", "Keck Graduate Institute"])

    @discord.ui.button(label='Pomona', style=discord.ButtonStyle.blurple, custom_id='persistent_view:college:pomona')
    async def pomona(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role Pomona!', ephemeral=True)
        await grant_create_role(interaction.user, "Pomona", to_remove=["Harvey Mudd", "Pitzer", "Scripps", "Claremont McKenna", "Claremont Graduate University", "Keck Graduate Institute"])
    
    @discord.ui.button(label='Scripps', style=discord.ButtonStyle.blurple, custom_id='persistent_view:college:scripps')
    async def scripps(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role Scripps!', ephemeral=True)
        await grant_create_role(interaction.user, "Scripps", to_remove=["Harvey Mudd", "Pitzer", "Pomona", "Claremont McKenna", "Claremont Graduate University", "Keck Graduate Institute"])

    @discord.ui.button(label='Claremont McKenna', style=discord.ButtonStyle.blurple, custom_id='persistent_view:college:cmc')
    async def cmc(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role Claremont McKenna!', ephemeral=True)
        await grant_create_role(interaction.user, "Claremont McKenna", to_remove=["Harvey Mudd", "Pitzer", "Pomona", "Scripps", "Claremont Graduate University", "Keck Graduate Institute"])

    @discord.ui.button(label='Claremont Graduate University', style=discord.ButtonStyle.blurple, custom_id='persistent_view:college:cgu')
    async def cgu(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role Claremont Graduate University!', ephemeral=True)
        await grant_create_role(interaction.user, "Claremont Graduate University", to_remove=["Harvey Mudd", "Pitzer", "Pomona", "Scripps", "Claremont McKenna", "Keck Graduate Institute"])
    
    @discord.ui.button(label='Keck Graduate Institute', style=discord.ButtonStyle.blurple, custom_id='persistent_view:college:kgi')
    async def kgi(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role Keck Graduate Institute!', ephemeral=True)
        await grant_create_role(interaction.user, "Keck Graduate Institute", to_remove=["Harvey Mudd", "Pitzer", "Pomona", "Scripps", "Claremont McKenna", "Claremont Graduate University"])


class PronounView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='He/Him', style=discord.ButtonStyle.blurple, custom_id='persistent_view:pronoun:he/him')
    async def he_him(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role He/Him!', ephemeral=True)
        await grant_create_role(interaction.user, "He/Him", to_remove=["She/Her", "They/Them", "He/They", "She/They", "Any Pronouns"])

    @discord.ui.button(label='She/Her', style=discord.ButtonStyle.blurple, custom_id='persistent_view:pronoun:she/her')
    async def she_her(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role She/Her!', ephemeral=True)
        await grant_create_role(interaction.user, "She/Her", to_remove=["He/Him", "They/Them", "He/They", "She/They", "Any Pronouns"])
        
    @discord.ui.button(label='They/Them', style=discord.ButtonStyle.blurple, custom_id='persistent_view:pronoun:they/them')
    async def they_them(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role They/Them!', ephemeral=True)
        await grant_create_role(interaction.user, "They/Them", to_remove=["He/Him", "She/Her", "He/They", "She/They", "Any Pronouns"])

    @discord.ui.button(label='He/They', style=discord.ButtonStyle.blurple, custom_id='persistent_view:pronoun:he/they')
    async def he_they(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role He/They!', ephemeral=True)
        await grant_create_role(interaction.user, "He/They", to_remove=["He/Him", "She/Her", "They/Them", "She/They", "Any Pronouns"])

    @discord.ui.button(label='She/They', style=discord.ButtonStyle.blurple, custom_id='persistent_view:pronoun:she/they')
    async def she_they(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role She/They!', ephemeral=True)
        await grant_create_role(interaction.user, "She/They", to_remove=["He/Him", "She/Her", "They/Them", "He/They", "Any Pronouns"])

    @discord.ui.button(label='Any Pronouns', style=discord.ButtonStyle.blurple, custom_id='persistent_view:pronoun:any pronouns')
    async def any_pronouns(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role Any Pronouns!', ephemeral=True)
        await grant_create_role(interaction.user, "Any Pronouns", to_remove=["He/Him", "She/Her", "They/Them", "He/They", "She/They"])
        
    @discord.ui.button(label='Other', style=discord.ButtonStyle.blurple, custom_id='persistent_view:pronoun:other')
    async def other(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role Other!', ephemeral=True)
        await grant_create_role(interaction.user, "Other", to_remove=["He/Him", "She/Her", "They/Them", "He/They", "She/They", "Any Pronouns"])
    
class YearView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='2024', style=discord.ButtonStyle.blurple, custom_id='persistent_view:year:2024')
    async def year_2021(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role 2024!', ephemeral=True)
        await grant_create_role(interaction.user, "2024", to_remove=["2025", "2026", "2027", "2028", "2029", "2030", "2031", "2032", "2033", "2034", "2035", "2036", "2037", "2038", "2039", "2040"])

    @discord.ui.button(label='2025', style=discord.ButtonStyle.blurple, custom_id='persistent_view:year:2025')
    async def year_2025(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role 2025!', ephemeral=True)
        await grant_create_role(interaction.user, "2025", to_remove=["2024", "2026", "2027", "2028", "2029", "2030", "2031", "2032", "2033", "2034", "2035", "2036", "2037", "2038", "2039", "2040"])

    @discord.ui.button(label='2026', style=discord.ButtonStyle.blurple, custom_id='persistent_view:year:2026')
    async def year_2026(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role 2026!', ephemeral=True)
        await grant_create_role(interaction.user, "2026", to_remove=["2024", "2025", "2027", "2028", "2029", "2030", "2031", "2032", "2033", "2034", "2035", "2036", "2037", "2038", "2039", "2040"])

    @discord.ui.button(label='2027', style=discord.ButtonStyle.blurple, custom_id='persistent_view:year:2027')
    async def year_2027(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role 2027!', ephemeral=True)
        await grant_create_role(interaction.user, "2027", to_remove=["2024", "2025", "2026", "2028", "2029", "2030", "2031", "2032", "2033", "2034", "2035", "2036", "2037", "2038", "2039", "2040"])

    @discord.ui.button(label='2028', style=discord.ButtonStyle.blurple, custom_id='persistent_view:year:2028')
    async def year_2028(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gained role 2028!', ephemeral=True)
        await grant_create_role(interaction.user, "2028", to_remove=["2024", "2025", "2026", "2027", "2029", "2030", "2031", "2032", "2033", "2034", "2035", "2036", "2037", "2038", "2039", "2040"])



@bot.command()
@commands.has_permissions(administrator=True)
async def send_reaction_message(ctx):
    await ctx.send('''***Reaction Roles***''')

    await ctx.send('''**Select your college**''', view=CollegeView())

    await ctx.send('''**Select your pronouns**''', view=PronounView())

    await ctx.send('''**Select your class year**''', view=YearView())

        

async def grant_create_role(user, role_name, to_remove=[]):
    guild = user.guild
    role = discord.utils.get(guild.roles, name=role_name)

    if role is None:
        role = await guild.create_role(name=role_name)

    await user.add_roles(role)

    if len(to_remove) > 0:
        for r in to_remove: 
            role = discord.utils.get(guild.roles, name=r)

            if role is not None:
                await user.remove_roles(role)

def run_discord_bot(TOKEN):
    if TOKEN == "":
        print("DISCORD_TOKEN is not set")
        return
    
    bot.run(TOKEN)