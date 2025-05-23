def processar_prompt(prompt, chat, info_adicional):
    full_prompt_for_model = prompt
    if info_adicional:
        full_prompt_for_model = f"{prompt}\n\nConsidere a seguinte informação complementar para sua resposta: {info_adicional}"
    resposta = ''
    for chunk in chat.send_message(full_prompt_for_model, stream=True):
        resposta += chunk.text
    return resposta