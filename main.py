import os, sys
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.types import Channel, Chat, User
from telethon.errors import SessionPasswordNeededError
import asyncio
import rich
import threading
from getpass import getpass
from settings import *

# Só pra nao colocar seus dados direto nesse arquivo
load_dotenv()
API_HASH = os.getenv("API_HASH")
API_ID = os.getenv("API_ID")

async def connect_to_telegram() -> TelegramClient:
    """
    Função responsável por conectar e autenticar o usuário no Telegram.

    Solicita o número de telefone, envia o código de verificação e, se necessário,
    solicita a senha de autenticação em duas etapas (2FA). Retorna uma instância 
    autenticada do TelegramClient pronta para uso.

    Returns:
        TelegramClient: Cliente autenticado do Telegram.

    Raises:
        Exception: Caso ocorra algum erro durante o processo de autenticação.
    """

    client = TelegramClient(session_name, api_id=API_ID, api_hash=API_HASH)
    await client.connect() # primeira conexão com o telegram
    if await client.is_user_authorized(): 
        print("\033[1;92mUsuário ja autorizado\033[m")
        await asyncio.sleep(2)
        return client
        # Se o usuário usou o telebot recentemente, ele ja está autorizado
    phone = input("Celular (+5512998765432): ")
    await client.send_code_request(phone=phone)
    while True: # Loop pra se conectar a sua conta telegram
        try:
            code = input("Código de verificação: ")
            await client.sign_in(phone=phone, code=code)
        except SessionPasswordNeededError: # Só entra aqui se tiver senha no telegram
            while True:
                passwd = getpass("Senha 2FA: ")
                try:
                    await client.sign_in(password=passwd)
                except:
                    print("\033[1;91mErro, senha inválida :(\033[m")
                    continue
                else:
                    print("\033[1;92mLogin efetuado com sucesso :)\033[m")
                    await asyncio.sleep(2)
                    break
                # Só vai sair do loop depois de digitar a senha certa
            break
        except Exception: # Só entra aqui se tiver algum outro erro
            print("\033[1;91mAlgo deu errado :(\033[m")
            continue
        else:
            print("\033[1;92mLogin efetuado com sucesso :)\033[m")
            await asyncio.sleep(2)
            break
    return client


async def telebot_divul(client: TelegramClient):
    groups = [group.entity for group in await client.get_dialogs() if type(group.entity) == Channel or type(group.entity) == Chat]
    for group in groups:
        try:
            # rich.print(group)
            await client.send_message(group, msg)
            await asyncio.sleep(1)
        except Exception as e:
            print("\n\033[1;91mErro ao enviar mensagem :(\033[m")
            print(f"\033[1;91m{str(e)}\033[m")
            await asyncio.sleep(1)
        else:
            print(f"\n\033[1;92mMensagem enviada para {group.title} :)\033[m")
        finally:
            print("\033[1;93m-=\033[m" * 40)


async def main(): 
    client = await connect_to_telegram() # Uso da função acima ja descrita, client instanciado
    while True:
        print("\033[2J\033[H1 - Iniciar")
        print("0 - Sair")
        try:
            res = int(input("Sua poção: "))
        except:
            print("\033[1;91mOpção inválida\033[m")
            await asyncio.sleep(2)
            continue
        else:
            match res:
                case 1:
                    while True:
                        await telebot_divul(client)
                        await asyncio.sleep(3600)
                    continue
                case 0:
                    print("\033[1;93mSaindo", end="", flush=True)
                    await client.disconnect()
                    await asyncio.sleep(0.75)
                    print(".", end="", flush=True)
                    await asyncio.sleep(0.75)
                    print(".", end="", flush=True)
                    await asyncio.sleep(0.75)
                    print(".\033[m", end="", flush=True)
                    await asyncio.sleep(0.75)
                    break
                case _:
                    print("\033[1;91mOpção inválida\033[m")
                    await asyncio.sleep(2)
                    continue
                

if __name__ == "__main__":
    asyncio.run(main())