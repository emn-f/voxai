def preparar_prompt(prompt_usuario):
    personalidade_extra = ('''
    Você é um assistente de IA chamado Vox, projetado para ajudar os usuários a encontrar informações sobre a comunidade LGBTQIA+.
    '''
    )
    return f"{personalidade_extra}\n\n{prompt_usuario}"
