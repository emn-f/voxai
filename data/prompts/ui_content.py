from datetime import datetime
from src.external_links import (
    INSTAGRAM_VOX,
    INSTAGRAM_MARIELLE,
    FORM_AVALIACAO,
    LINKTREE_VOX,
    LINKEDIN_VOX,
    EMAIL_CONTATO,
    GITHUB,
    HUGGING_FACE_SPACE,
    TERMS_OF_USE,
    POLICY_PRIVACY,
)
from src.utils import git_version

# Captura o ano atual dinamicamente
ANO_ATUAL = datetime.today().year

# CSS injetado para limpar o HTML e centralizar os efeitos de hover
SIDEBAR_STYLES = """
<style>
    .vox-sidebar-container {
        display: flex; 
        flex-direction: column; 
        margin-bottom: 1em;
    }
    .vox-sidebar-section {
        margin-bottom: 1em;
    }
    .vox-title-group {
        font-size: 0.85em; 
        color: var(--text-color, #888); 
        margin-bottom: 0.6em; 
        font-weight: bold;
    }
    .vox-icon-link {
        transition: transform 0.2s ease-in-out;
        display: inline-block;
    }
    .vox-icon-link:hover {
        transform: scale(1.15);
    }
    .footer-links a {
        display: block;
        margin-top: 0.3em;
    }
</style>
"""

SAUDACAO = """
Oi! Que bom te ver por aqui. Sou o Vox AI, seu espaço seguro para tirar dúvidas sobre saúde, direitos, acolhimento e tudo que envolve a nossa comunidade LGBTQIA+. 

Como posso te apoiar hoje?
"""

SIDEBAR_BODY = f"""
{SIDEBAR_STYLES}
<div class="vox-sidebar-container">
    <div>
        <div class="vox-sidebar-title">Sobre o Vox</div>
        <div class="vox-sidebar-section">
            <b>Vox AI</b> é um assistente de apoio e informação <b>LGBTQIA+</b>. Aqui você encontra acolhimento,
            informações e recursos confiáveis.
        </div>
        
            <div class="vox-title-group">Siga nosso trabalho</div>
            
            <ul class="vox-sidebar-links" style="padding-left: 0; list-style: none; line-height: 1.8em;">
                <li>
                    <a href="{INSTAGRAM_VOX}" target="_blank" class="link-insta">
                        <img src="https://img.icons8.com/?size=100&id=Xy10Jcu1L2Su&format=png" alt="Instagram"
                            style="height:1.2em; vertical-align:middle; margin-right:6px;" />
                        @projetovoxai
                    </a>
                </li>
                <li>
                    <a href="{INSTAGRAM_MARIELLE}" target="_blank" class="link-casa-marielle">
                        <img src="https://img.icons8.com/?size=100&id=Xy10Jcu1L2Su&format=png" alt="Instagram"
                             style="height:1.2em; vertical-align:middle; margin-right:6px;" />
                        @casamariellefrancobr
                    </a>
                </li>
                <li>
                    <a href="{FORM_AVALIACAO}" target="_blank" title="Avaliar o Vox">
                        <img src="https://img.icons8.com/?size=100&id=19417&format=png" alt="Avaliar"
                            style="height:1.2em; vertical-align:middle; margin-right:6px;" />
                        Avalie o Vox
                    </a>
                </li>
            </ul>

        <div class="vox-title-group">Conecte-se</div>
        <div style="display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 1em;">
            <a href="{LINKTREE_VOX}" target="_blank" title="Linktree" class="vox-icon-link">
                <img src="https://img.icons8.com/?size=100&id=GfTOMrwiax2M&format=png" alt="Linktree" style="height: 28px;" />
            </a>
            <a href="{LINKEDIN_VOX}" target="_blank" title="LinkedIn" class="vox-icon-link">
                <img src="https://img.icons8.com/?size=100&id=13930&format=png" alt="LinkedIn" style="height: 28px;" />
            </a>
            <a href="{EMAIL_CONTATO}" target="_blank" title="Enviar E-mail" class="vox-icon-link">
                <img src="https://img.icons8.com/?size=100&id=ho8QlOYvMuG3&format=png" alt="Email" style="height: 28px;" />
            </a>
        </div>
    </div>
    <hr style="margin: 1em 0; opacity: 0.2;">
</div>"""

SIDEBAR_FOOTER = f"""
    <div>
        <div style="text-align: center; margin-bottom: 1em;">
            <a href="{GITHUB}" target="_blank" title="Ver código fonte" class="vox-icon-link" style="margin-right: 12px;">
                <img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/github.svg" alt="GitHub"
                    style="height: 24px; filter: invert(0.6);" />
            </a>
            <a href="{HUGGING_FACE_SPACE}" target="_blank" title="Hugging Face Space" class="vox-icon-link">
                <img src="https://img.icons8.com/?size=100&id=sop9ROXku5bb&format=png" alt="Hugging Face" style="height: 24px;" />
            </a>
        </div>
        
        <div class="footer-links" style="text-align:center; font-size: 0.9em;">
            <a href="{TERMS_OF_USE}" target="_blank" style="text-decoration: none;" class="legal-link">Termos de Uso</a>
            <a href="{POLICY_PRIVACY}" target="_blank" style="text-decoration: none;" class="legal-link">Política de Privacidade</a>
        </div>
        
        <div class="copyright" style="text-align:center; color:#666; font-size:0.8em; margin-top:1.2em; font-weight: 500;">
            Copyright © {ANO_ATUAL} Vox AI
        </div>
        
        <div style='color: #88888866; text-align: center; margin-top: 0.5em; font-size: 0.75em; font-family: monospace;'>
            {git_version()}
        </div>
    </div>
"""
