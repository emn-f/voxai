def processar_prompt(prompt, chat, preparar_prompt, informacao_complementar):
    resposta = ''
    prompt_final = preparar_prompt(prompt)
    for chunk in chat.send_message(prompt_final, stream=True):
        resposta += chunk.text
    return resposta + informacao_complementar