import discord
from discord.ext import commands
import datetime
import os
import urllib
import asyncio

from urllib import parse, request
import re

client = commands.Bot(command_prefix='>', description="This is a Helper Bot")

@client.event
async def on_ready():
  while 1:
    urllib.request.urlopen("https://kayane-bot.naoooo.repl.co")
    await asyncio.sleep(500)

@client.command()
async def ping(ctx):
	await ctx.send('pong')


@client.command()
async def sum(ctx, numOne: int, numTwo: int):
	await ctx.send(numOne + numTwo)


@client.command()
async def info(ctx):
	embed = discord.Embed(title=f"{ctx.guild.name}",
	                      description="Lorem Ipsum asdasd",
	                      timestamp=datetime.datetime.utcnow(),
	                      color=discord.Color.blue())
	embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
	embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
	embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
	embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
	# embed.set_thumbnail(url=f"{ctx.guild.icon}")
	embed.set_thumbnail(
	    url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")

	await ctx.send(embed=embed)


@client.command()
async def youtube(ctx, *, search):
	query_string = parse.urlencode({'search_query': search})
	html_content = request.urlopen('http://www.youtube.com/results?' +
	                               query_string)
	# print(html_content.read().decode())
	search_results = re.findall('href=\"\\/watch\\?v=(.{11})',
	                            html_content.read().decode())
	print(search_results)
	# I will put just the first result, you can loop the response to show more results
	await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])


# Events
@client.event
async def on_ready():
	await client.change_presence(activity=discord.Streaming(
	    name="how to be cute?", url="http://www.twitch.tv/accountname"))
	print('My Ready is Body')


@client.event
async def on_message_join(member):
	channel = member.get_channel(823615900384100372)
	embed = discord.Embed(
	    title=f"welcome {member.name}",
	    description=f"Thanks for Joining {member.guild.name}!")
	embed.set_thumbnail(url=member.avatar_url)

	await channel.send(embed=embed)


@client.command(aliases=['rules'])
async def rule(ctx, *, number):
	await ctx.send(rule[int(number) -1])


@client.command(aliases=['c'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=2):
	await ctx.channel.purge(limit=amount)

@client.command(aliases=['k'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="no reason provided"):
	await member.kick(reason=reason)

  
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason="none"):
    await member.ban(reason=reason)
    embed = discord.Embed(title="Gebannt!", description="**{0}** wurde von **{1}** gebannt!".format(member.mention, ctx.message.author), color=808080)
    embed.set_thumbnail(url="https://cdn.imgbin.com/20/20/7/imgbin-banhammer-discord-computer-icons-hammer-uU2ButFwmhE4hzGmKuffX3mYK.jpg")
    await ctx.send(embed=embed)



@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.member, *, reason=None):
	guild = ctx.guild
	mutedRole = discord.utils.get(guild.roles, name="Muted")

	if not mutedRole:
		mutedRole = await guild.create_role(name="Muted")

		for channel in guild.channels:
			await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

	await member.add_roles(mutedRole, reason=reason)
	await ctx.send(f"Muted {member.mention} for reason {reason}")
	await member.send(f"You were muted in the server {guild.name} for {reason}")


@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.member):
	mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

	await member.remove_roles(mutedRole)
	await ctx.send(f"Unmuted {member.mention}")
	await member.send(f"You were unmuted in the server {ctx.guild.name}")

client.run('YourToken')
