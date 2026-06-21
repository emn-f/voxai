from datetime import datetime

from scripts.update_slogan import SLOGAN
from src.external_links import (
    INSTAGRAM_VOX,
    LINKTREE_VOX,
    LINKEDIN_VOX,
    EMAIL_CONTATO,
    GITHUB,
    CVV_LINK,
    DISQUE_100,
    POLICY_PRIVACY,
    TERMS_OF_USE,
)
from src.utils import git_version

ANO_ATUAL = datetime.today().year

SAUDACAO = """
Oi! Que bom te ver por aqui. Sou o Vox AI, seu espaço seguro para tirar dúvidas sobre saúde, direitos, acolhimento e tudo que envolve a comunidade LGBTQIA+. 

Como posso te ajudar agora?
"""

SIDEBAR_BODY = f"""<div style="display: flex; flex-direction: column; margin-bottom: 1em;">
<div class="vox-sidebar-card">
<div class="vox-sidebar-card-title">Sobre o Projeto</div>
<div class="vox-sidebar-section">
O <b>Vox AI</b> é um assistente de apoio e informação <b>LGBTQIA+</b>. Desenvolvido para oferecer um espaço seguro de acolhimento, orientação e acesso a informações confiáveis.
</div>
</div>
<div class="vox-sidebar-card">
<div class="vox-sidebar-card-title">Precisa de ajuda agora?</div>
<ul class="vox-sidebar-list">
<li class="vox-sidebar-list-item">
<a href="{CVV_LINK}" target="_blank" title="Centro de Valorização da Vida">
Ligue 188 (Apoio Emocional)
</a>
</li>
<li class="vox-sidebar-list-item">
<a href="{DISQUE_100}" target="_blank" title="Direitos Humanos">
Disque 100 (Direitos Humanos)
</a>
</li>
</ul>
</div>
<div class="vox-sidebar-card">
<div class="vox-sidebar-card-title">Redes Sociais do Vox</div>
<div class="vox-social-grid">
<a href="{INSTAGRAM_VOX}" target="_blank" class="vox-social-icon" title="Instagram">
<img src="https://img.icons8.com/?size=100&id=Xy10Jcu1L2Su&format=png" alt="Instagram" />
</a>
<a href="{LINKTREE_VOX}" target="_blank" class="vox-social-icon" title="Linktree (Todos os links)">
<img src="https://img.icons8.com/?size=100&id=GfTOMrwiax2M&format=png&color=000000" alt="Linktree" />
</a>
<a href="{LINKEDIN_VOX}" target="_blank" class="vox-social-icon" title="LinkedIn">
<img src="https://img.icons8.com/?size=100&id=13930&format=png&color=000000" alt="LinkedIn" />
</a>
<a href="{EMAIL_CONTATO}" target="_blank" class="vox-social-icon" title="E-mail de Contato">
<img src="https://img.icons8.com/?size=100&id=ho8QlOYvMuG3&format=png&color=000000" alt="Email" />
</a>
</div>
</div>
</div>"""

SIDEBAR_FOOTER = f"""
<div style="display: flex; gap: 16px; justify-content: center; margin-bottom: 12px;">
<a href="{GITHUB}" target="_blank" title="GitHub">
<img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/github.svg" alt="GitHub" style="height: 24px; filter: invert(0.5);" />
</a>
</div>
<div class="copyright" style="text-align: center; color: #888; font-size: 0.8em; margin-top: 10px; opacity: 0.8;">
Vox AI {git_version()}
</div>
<div class="footer-links" style="text-align:center; font-size: 0.9  em; ">
<a href="{TERMS_OF_USE}" target="_blank" style="text-decoration: none;"class="legal-link">Termos de Uso</a>
<br>
<a href="{POLICY_PRIVACY}" target="_blank" style="text-decoration: none;"class="legal-link">Política de Privacidade</a>
</div>
</div>

"""
