import os


session_name = "session"
if not os.path.exists("msg_divul.txt"):
    with open("msg_divul.txt", "+w") as file:
        file.write("mensagem teste, substitua pelo link do seu grupo junto com a mensagem personalizada")
with open("msg_divul.txt", "r") as file:
    msg = file.read()