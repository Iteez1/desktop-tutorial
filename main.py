import random
import time

from twitchio.ext import commands


class Bot(commands.Bot):
    ratings = {}
    cooldowns = {}

    def __init__(self):
        super().__init__(token='rg767kwfr707tucscmi4ehe7lc2l9i', prefix='++',
                         initial_channels=['iteez__', 'tastier_bot'])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.content == '123':
            await message.channel.send(f'321')
        await self.handle_commands(message)

    @commands.command()
    async def Tasty(self, ctx: commands.Context):
        aut = ctx.message.author.name
        rait = random.randint(-10, 10)

        current_time = time.time()

        if aut in Bot.ratings and current_time - Bot.ratings[aut][1] < 600:
            remaining_time = int(600 - (current_time - Bot.ratings[aut][1]))
            minutes, seconds = divmod(remaining_time, 60)
            if minutes > 0:
                await ctx.send(f"{aut} подожди еще {minutes} минут {seconds} секунд.")
            else:
                await ctx.send(f"{aut} подожди еще {seconds} секунд.")
            return

        if aut in Bot.ratings:
            user_rating, _ = Bot.ratings[aut]
            if user_rating < 0:
                rait = max(0, rait)  # Если у пользователя меньше 0 конфеток, увеличиваем шанс получить
            user_rating += rait
            Bot.ratings[aut] = (user_rating, current_time)
        else:
            Bot.ratings[aut] = (rait, current_time)

        with open('ratings.txt', 'w') as file:
            for user, (user_rating, last_used) in Bot.ratings.items():
                file.write(f'{user}:{user_rating}:{last_used}\n')
        await ctx.send(f'{aut} ты получил {rait} candy')

    @commands.command()
    async def tasty(self, ctx: commands.Context):
        aut = ctx.message.author.name
        rait = random.randint(-10, 10)

        current_time = time.time()

        if aut in Bot.ratings and current_time - Bot.ratings[aut][1] < 600:
            remaining_time = int(600 - (current_time - Bot.ratings[aut][1]))
            minutes, seconds = divmod(remaining_time, 60)
            if minutes > 0:
                await ctx.send(f"{aut} подожди еще {minutes} минут {seconds} секунд.")
            else:
                await ctx.send(f"{aut} подожди еще {seconds} секунд.")
            return

        if aut in Bot.ratings:
            user_rating, _ = Bot.ratings[aut]
            if user_rating < 0:
                rait = max(0, rait)  # Если у пользователя меньше 0 конфеток, увеличиваем шанс получить
            user_rating += rait
            Bot.ratings[aut] = (user_rating, current_time)
        else:
            Bot.ratings[aut] = (rait, current_time)

        with open('ratings.txt', 'w') as file:
            for user, (user_rating, last_used) in Bot.ratings.items():
                file.write(f'{user}:{user_rating}:{last_used}\n')
        if rait >= 0:
            await ctx.send(f'{aut} ты получил {rait} candy')
        if rait < 0:
            await ctx.send(f'{aut} ты потерял {rait} candy')

    @commands.command()
    async def candy(self, ctx: commands.Context, user: str = None):
        if user is None:
            user = ctx.message.author.name

        if user in Bot.ratings:
            user_rating, _ = Bot.ratings[user]
            await ctx.send(f'Пользователь {user} имеет {user_rating} candy')
        else:
            await ctx.send(f'{ctx.message.author.name} у тебя нет candy SAJ')


bot = Bot()
bot.run()
