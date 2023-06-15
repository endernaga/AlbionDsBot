import asyncio

import discord
from discord.ext import commands

from CRUD_comand import *
from model import *

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)


@bot.event
async def on_ready():
    print('Запуск')
    await bot.tree.sync()


@bot.command(name='test')
async def test(ctx: discord.Interaction, *args):
    print(args)


class BuildSelect(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=build.name, value=build.id) for build in read_object(BuildList)]
        super().__init__(options=options, placeholder="Selecct a build", max_values=len(read_object(BuildList)))

    async def callback(self, interaction: discord.Interaction):
        await self.view.respond_to_answer2(interaction, self.values)



class SurveyView(discord.ui.View):
    answer1 = None
    answer2 = None

    @discord.ui.select(
        placeholder="Select activities",
        options=[discord.SelectOption(label=activities.name, value=activities.id) for activities in read_object(ProfileList)]
    )
    async def select_age(self, interaction: discord.Interaction, select_item: discord.ui.Select):
        self.answer1 = select_item.values
        print(self.answer1)
        self.children[0].disabled = True
        build_select = BuildSelect()
        self.add_item(build_select)
        await interaction.message.edit(view=self)
        await interaction.response.defer()

    async def respond_to_answer2(self, interaction: discord.Interaction, choices):
        print(choices)
        self.answer2 = choices
        self.children[1].disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.defer()
        update_object(ProfileList, int(self.answer1[0]), build_lists=[read_object(BuildList, i) for i in self.answer2])
        await interaction.message.edit(content=f'Профіль створено, До активнсті {read_object(ProfileList, self.answer1[0])} додані білди {[read_object(BuildList, i) for i in self.answer2]}', view=None)
        await asyncio.sleep(5)
        await interaction.message.delete()
        self.stop()


@bot.tree.command(name='survey')
async def survey(ctx):
    view = SurveyView()
    await ctx.response.send_message(view=view)

    await view.wait()
    results = {
        "a1": view.answer1,
        "a2": view.answer2,
    }


bot.run('MTA4NzQ3NzkzODU2OTYxMzQ2NA.Gqapbe.xMFK6maRm9KRbEXLCL5SYfXf3XPviwDHLcuB3U')
