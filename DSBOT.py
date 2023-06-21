import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from CRUD_comand import *
from model import *

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)

#Класи створені для того щоб зробити випадаюче меню

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
        options=[discord.SelectOption(label=activities.name,
                                      value=activities.id) for activities in read_object(ProfileList)]
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


@bot.event
async def on_ready():
    print('Запуск')
    await bot.tree.sync()

@app_commands.choices(role=[
    app_commands.Choice(name='Tank', value='tank'),
    app_commands.Choice(name='Heal', value='heal'),
    app_commands.Choice(name='saport', value='saport'),
    app_commands.Choice(name='MDD', value='MDD'),
    app_commands.Choice(name='RDD', value='RDD'),
    app_commands.Choice(name='Battle Mount', value='Battle Mount')
])
@bot.tree.command(name='create_build') #створення білда
async def create_build(ctx: discord.Interaction, build_name: str, build_description: str, role: app_commands.Choice[str]):
    create_object(BuildList, name=build_name, description=build_description, role=role.value)
    await ctx.response.send_message(f'Білд {build_name} успішно створено!', ephemeral=True)


@bot.tree.command(name='delete_build') # видалення білда за id(В майбутньому зробити за іменем )
async def delete_build(ctx: discord.Interaction, build_id: int):
    delete_object(BuildList, object_id=build_id)
    await ctx.response.send_message(f'Білд {read_object(BuildList, build_id)} успішно вилучено!', ephemeral=True)


@bot.tree.command(name='create_profile') #Створення активності
async def create_profile(ctx: discord.Interaction, activities_name: str, activities_description: str,
                            tank_count: int,
                            heal_count: int,
                            support_count: int,
                            mdd_count: int,
                            rdd_count: int, battlemount_count: int,):
    if tank_count + heal_count + support_count + mdd_count+ rdd_count + battlemount_count > 20:
        await ctx.response.send_message('Не правильно вказана кількість ролів , впевніться що їх сума не більша за 20', ephemeral=True)
    else:
        create_object(ProfileList, name=activities_name, description=activities_description, tank_count=tank_count,
                      heal_count=heal_count, support_count=support_count, mdd_count=mdd_count,
                      rdd_count=rdd_count, battle_mount_count=battlemount_count)
        await ctx.response.send_message(f'Активність {activities_name} успішно створена', ephemeral=True)


@bot.tree.command(name='delete_activities') # вилучення активності
async def delete_activivtiess(ctx: discord.Interaction, activitie_id: int):
    delete_object(ProfileList, activitie_id)
    await ctx.response.send_message(f"Активність {read_object(ProfileList, activitie_id)} успішно вилучена",
                                    ephemeral=True)


@bot.tree.command(name='add_build_to_profile') #створення звязку між активностями та білдами ( Для цього використано класи )
async def add_build_to_profile(ctx):
    view = SurveyView()
    await ctx.response.send_message(view=view)

    await view.wait()


bot.run('MTA4NzQ3NzkzODU2OTYxMzQ2NA.Gqapbe.xMFK6maRm9KRbEXLCL5SYfXf3XPviwDHLcuB3U')
