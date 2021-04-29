import requests
import sys
from colorama import Fore
import dateutil.parser

red = Fore.RED
yellow = Fore.YELLOW
light_yellow = Fore.LIGHTYELLOW_EX


class User:
    def __init__(self, user, id):
        self.tag = user
        self.id = id


def get_messages(user, token, channel_id):
    body = {
        "limit": 100
    }

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    messages = requests.get(f"https://discord.com/api/channels/{channel_id}/messages", headers=headers, params=body)
    messages_json = messages.json()
    for x in messages_json:
        date = dateutil.parser.parse(x["timestamp"])
        print(f"""{red}[{yellow}{date.strftime("%m/%d/%Y | %H:%M:%S")}{red}] ({light_yellow}{x["author"]["username"]}#{x["author"]["discriminator"]}{red}) {light_yellow}- {red}{x["content"]}""")

    opcion = input(f"{light_yellow}Ver otro chat? [y/n]: ")

    if opcion == "y":
        getRelationships(user, token)
    elif opcion == "n":
        sys.exit(0)
    else:
        getRelationships(user, token)


def create_md(user, token, friend_id):
    body = {
        "recipient_id": friend_id
    }
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    md = requests.post("https://discord.com/api/users/@me/channels", headers=headers, json=body)
    md_json = md.json()
    get_messages(user, token, md_json["id"])


def getRelationships(user, token):
    relationships = requests.get("https://discord.com/api/users/@me/relationships", headers={"Authorization": token})
    relationships_list = relationships.json()
    print(f"{light_yellow}Amigos de {user.tag}:")
    for x, i in enumerate(relationships_list):
        print(f"""{yellow}[{red}{x}{yellow}] {red}{i["user"]["username"]}#{i["user"]["discriminator"]}""")
    relationship = input(f"{light_yellow}Introduce el índice de la conversación a la que quieras acceder (VER 100 ÚLTIMOS MENSAJES): ")
    create_md(user, token, relationships_list[int(relationship)]["id"])


def getUser(token):
    user = requests.get("https://discord.com/api/users/@me", headers={"Authorization": token})
    user_info = user.json()
    new_user = User(f"""{user_info["username"]}#{user_info["discriminator"]}""", user_info["id"])
    getRelationships(new_user, token)


def show_ascii():
    print(f"""{light_yellow}
                            
{red} ██████╗██╗  ██╗██╗██████╗ ██╗██████╗  ██████╗ ███╗   ██╗███████╗███████╗
{red}██╔════╝██║  ██║██║██╔══██╗██║██╔══██╗██╔═══██╗████╗  ██║██╔════╝██╔════╝
{yellow}██║     ███████║██║██████╔╝██║██████╔╝██║   ██║██╔██╗ ██║█████╗  ███████╗
{yellow}██║     ██╔══██║██║██╔═══╝ ██║██╔══██╗██║   ██║██║╚██╗██║██╔══╝  ╚════██║
{red}╚██████╗██║  ██║██║██║     ██║██║  ██║╚██████╔╝██║ ╚████║███████╗███████║
{red}╚═════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚══════╝
    {light_yellow}- acc_l_b1 - Taxalo#8998                                                         
                                                                            
    """)


def main():
    show_ascii()
    token = input(f"{red}Introduce el token: ")
    getUser(token)


main()
