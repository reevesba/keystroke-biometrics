''' Key Logging Bot Driver

Author: Bradley Reeves
Date: 05/22/2021

'''

from kb_bot import KeyLoggerBot


def main():
    # Setup data to send
    field_names = ["sentence" + str(i) for i in range(10)]
    sentences = [
        "The quick brown fox jumped over the lazy dogs.",
        "Jackie will budget for the most expensive zoology equipment.",
        "A quick movement of the enemy will jeopardize six gunboats.",
        "Grumpy wizards make toxic brew for the evil queen and Jack.",
        "Watch 'Jeopardy!', Alex Trebek's fun TV quiz game.",
        "When zombies arrive, quickly fax Judge Pat.",
        "The quick onyx goblin jumps over the lazy dwarf.",
        "Cozy lummox gives smart squid who asks for job pen.",
        "As quirky joke, chefs won't pay devil magic zebra tax.",
        "Zelda might fix the job growth plans very quickly on Monday."
    ]

    # Execute bot
    bot = KeyLoggerBot(field_names=field_names, sentences=sentences)
    bot.execute()


if __name__ == "__main__":
    main()
