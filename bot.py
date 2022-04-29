import sys
import asyncio
from datetime import datetime
import discord
import re
import locale
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Greedy

bot = commands.Bot(command_prefix='?', activity=discord.Game(name='"?info" for help',))
GUILD = "CellGC"

#====================================================================================================================================================================================

calculationtype = 1
type = ""
totalcost = 0
totalPrestige = 0
wantPrestige = 0
totalcostperenchant = []

locale.setlocale(locale.LC_ALL, '')

typelist = {
    'locksmith' : 250,
    'lucky' : 100,
    'allegiance' : 250,
    'combo' : 250,
    'tokengreed' : 100,
    'gemfinder' : 300,
    'dragonburst' : 100,
    'fortune' : 75,
    'efficiency' : 50
}

beginningPrice = {
    'locksmith' : 7500,
    'lucky' : 5000,
    'allegiance' : 5000,
    'combo' : 5000,
    'tokengreed' : 2500,
    'gemfinder' : 25000,
    'dragonburst' : 5000,
    'fortune' : 2500,
    'efficiency' : 1000
}

limitCap = {
    'locksmith' : 1000,
    'lucky' : 1000,
    'allegiance' : 5000,
    'combo' : 1000,
    'tokengreed' : 5000,
    'gemfinder' : 1500,
    'dragonburst' : 5000,
    'fortune' : 10000,
    'efficiency' : 5000
}


def getPrice(currentCost, arg2 , arg3, arg4):
    actualcost = 0
    if (int(arg4) > limitCap.get(arg2)):
        arg4 = limitCap.get(arg2)
    for i in range(int(arg4) - int(arg3)):
        if i == 0:
            actualcost = currentCost
        else:
            currentCost += typelist.get(arg2)
            actualcost = actualcost + currentCost
    return locale.format_string("%d", actualcost, grouping=True)

def getItemPrice(currentCost):
    actualcost = 0
    global levelwant
    if (levelwant > limitCap.get(type)):
        levelwant = limitCap.get(type)
        print(levelwant)
    for i in range(levelwant - currentLevel):
        if i == 0:
            actualcost = currentCost
        else:
            currentCost += typelist.get(type)
            actualcost = actualcost + currentCost
    return actualcost

def getLevels(currentCost):
    actualcost = currentCost
    totalLevel = 1
    while True:
        if (totalToken - actualcost) > (currentCost + typelist.get(type)):
            totalLevel += 1
            currentCost += typelist.get(type)
            actualcost = actualcost + currentCost
        else:
            break
    print("Total Levels:" + str(totalLevel))


#gets current upgrade price
def getCurrentPrice(arg2, arg3):
    price = beginningPrice.get(arg2)
    for i in range(int(arg3)):
        price = price + typelist.get(arg2)
    return price

#prestige shit
def getCurrentPrestigePrice(arg2):
    currentPrestigePrice = 1000000.0
    prestigePrice = 1000000.0
    for i in range(int(arg2) - 1):
        if i == 0 and int(arg2) == 1:
            prestigePrice = 1000000.0
        else:
            prestigePrice = currentPrestigePrice * 1.05
            currentPrestigePrice *= 1.05    
    if arg2 == 0:
        prestigePrice = 0
    print(prestigePrice)
    return prestigePrice

def getPrestigePrice(currentPrestigePrice, arg2, arg3):
    currentPrestigePrice = currentPrestigePrice
    prestigePrice = 0.0
    for i in range(int(arg3) - int(arg2)):
        if currentPrestigePrice == 0:
            prestigePrice = 1000000.0
            currentPrestigePrice = 1000000.0
        else:
            prestigePrice = prestigePrice + currentPrestigePrice * 1.05
            currentPrestigePrice = currentPrestigePrice + (currentPrestigePrice * 1.05 - currentPrestigePrice)
    return locale.format_string("%d", round(prestigePrice), grouping=True)

#Checks if the enchant given is valid
def checkIfAEnchat(arg2):
    if beginningPrice.__contains__(str(arg2).lower()):
        return True
    else:
        return False

#====================================================================================================================================================================================

@bot.event
async def on_ready():
    print(f'{bot.user} has successfully connected!')




@bot.command(pass_context=True)
async def test(ctx, arg1, arg2, arg3, arg4):
    await ctx.reply(*arg)




@bot.command(pass_context=True)
async def info(ctx, arg1=None):
    if arg1 == None:
        embedhelp=discord.Embed(title="Commands", description="", color=0x660000)
        embedhelp.add_field(name="?upgradecost", value=f"To calculated the upgrade \ncosts on a enchant", inline=True)
        embedhelp.add_field(name="?prestigecost", value="To calculated the cost to prestige", inline=True)
        await ctx.reply(embed=embedhelp)

@bot.command(pass_context=True)
async def upgradecost(ctx, arg1=None, arg2=None, arg3=None):
    if arg1 != None:
        if checkIfAEnchat(arg1) == True:
            if arg2 != None:
                try:
                    currentLevel = int(arg2)
                    if arg3 != None:
                        try:
                            levelwant = int(arg3)
                            currentPrice = getCurrentPrice(arg1, arg2)
                            embedcalculator=discord.Embed(title="Results", description=f"The total cost for {arg1} is: {getPrice(currentPrice, arg1, arg2, arg3)}", color=0x660000)
                            await ctx.reply(embed=embedcalculator)
                        except ValueError:
                            embedcalculator=discord.Embed(title="Invalid level", description="Please enter your current level", color=0x660000)
                            await ctx.reply(embed=embedcalculator)
                    else:
                        embedcalculator=discord.Embed(title="Invalid level", description="Please enter the level you want", color=0x660000)
                        await ctx.reply(embed=embedcalculator)
                except ValueError:
                    embedcalculator=discord.Embed(title="Invalid level", description="Please enter your current level", color=0x660000)
                    await ctx.reply(embed=embedcalculator)
            else:
                embedcalculator=discord.Embed(title="Invalid level", description="Please enter your current level", color=0x660000)
                await ctx.reply(embed=embedcalculator)
        else:
            embedcalculator=discord.Embed(title="Invalid enchant", description="", color=0x660000)
            embedcalculator.add_field(name="Please enter a correct enchant", value="Please use one of the following 'locksmith', 'lucky', 'allegiance', 'combo', 'tokengreed', 'gemfinder', 'dragonburst', 'fortune', 'efficiency'", inline=True)
            await ctx.reply(embed=embedcalculator)
    else:
        embedcalculator=discord.Embed(title="No enchant provided", description="", color=0x660000)
        embedcalculator.add_field(name="Please enter a correct enchant", value="Please use one of the following 'locksmith', 'lucky', 'allegiance', 'combo', 'tokengreed', 'gemfinder', 'dragonburst', 'fortune', 'efficiency'", inline=True)
        await ctx.reply(embed=embedcalculator)

@bot.command(pass_context=True)
async def prestigecost(ctx, arg1=None, arg2=None):
    if arg1 != None:
        try:
            totalPrestige = int(arg1)
            if arg2 != None:
                wantPrestige = int(arg2)
                embedcalculator=discord.Embed(title="Results", description=f"The total cost to get from prestige {arg1} to {arg2} is: {getPrestigePrice(getCurrentPrestigePrice(arg1), arg1, arg2)}", color=0x660000)
                await ctx.reply(embed=embedcalculator)
            else:
                embedcalculator=discord.Embed(title="Missing Value", description="Please enter the prestige you want", color=0x660000)
                await ctx.reply(embed=embedcalculator)
        except ValueError:
            embedcalculator=discord.Embed(title="Invalid Prestige", description="Please enter your current level", color=0x660000)
            await ctx.reply(embed=embedcalculator)
    else:
        embedcalculator=discord.Embed(title="Missing Value", description="Please enter your current prestige", color=0x660000)
        await ctx.reply(embed=embedcalculator)

bot.run("OTY5Mzk5OTQ4NTgxOTQxMjU4.GbBrBi.U5Gyy7CE5ElFEhqHGU-nHbTYoDnkCPL7ht3x1E") 