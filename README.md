# OCAL Collimator - Virtual Overlay Tool

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![PySide6](https://img.shields.io/badge/UI-PySide6-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

O **OCAL Collimator** é uma ferramenta open-source em Python projetada para auxiliar astrônomos amadores e astrofotógrafos no processo de colimação digital de alta precisão. O programa funciona como uma **máscara flutuante (overlay transparente)** que se sobrepõe a qualquer software de captura, permitindo alinhar perfeitamente os elementos ópticos do telescópio utilizando círculos concêntricos analógicos virtuais.

---

## 🌌 Como Funciona?

Diferente de sistemas proprietários travados a hardwares específicos, este colimador **funciona com qualquer câmera astronômica ou webcam**, desde que o sensor esteja precisamente centralizado no tubo do focalizador. 

Você pode utilizar o seu software de captura e exibição de imagem favorito (como **N.I.N.A., SharpCap, FireCapture, APT**, etc.). O script gera uma interface transparente que fica sempre no topo (*Always on Top*). Basta arrastar a interface sobre a imagem em tempo real da sua câmera e ajustar os círculos analógicos para coincidir com as bordas dos espelhos e reflexos ópticos.

### 🔭 Telescópios Compatíveis
A ferramenta é ideal para sistemas ópticos que exigem colimação rigorosa:
* **Ritchey-Chrétien (RC)**
* **Schmidt-Cassegrain (SCT)**
* **Maksutov-Cassegrain (Mak)**
* **Newtonianos Clássicos**

---

## ✨ Funcionalidades

* **Fundo 100% Translúcido:** O visualizador não interfere na exibição do software de captura que está por baixo.
* **Sempre no Topo (Window Stays on Top):** A máscara não desaparece quando você clica no software da câmera.
* **Controle Granular Independente:**
  * 3 Círculos concêntricos customizáveis (Azul Claro, Verde Claro e Amarelo).
  * Ajuste de **Raio** dinâmico baseado na resolução da sua tela.
  * Ajuste de **Espessura da linha** (1px a 30px) para facilitar a visualização contra fundos claros ou escuros.
  * Opção de ocultar/exibir cada círculo individualmente.
* **Cruz de Alinhamento Central:** Retículo vermelho fixo para marcação do centro geométrico.
* **Interface Responsiva:** Sidebar de controle com *Scroll Area*, garantindo que todos os controles fiquem acessíveis mesmo em telas de menor resolução (como notebooks em campo).
* **Mobilidade Total:** Sem bordas de janela (*Frameless*). Pode ser arrastado para qualquer lugar da tela clicando e puxando a barra lateral.

---

## 🛠️ Pré-requisitos e Instalação

### 1. Clonar o repositório (ou baixar o código)
```bash
git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)
cd NOME_DO_REPOSITORIO
2. Instalar as dependências
O projeto utiliza o PySide6 (framework oficial do Qt para Python). Instale-o via pip:

Bash
pip install PySide6
3. Solução de Problemas (Linux / Zorin OS / Ubuntu)
Se ao tentar executar o script no Linux você receber um erro clássico do plugin XCB do Qt6:

Plaintext
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
Isso ocorre porque o Qt 6.5+ exige a biblioteca gráfica de cursor do sistema. Corrija instalando a dependência ausente:

Bash
sudo apt update && sudo apt install -y libxcb-cursor0
🚀 Como Usar
Abra o seu software de astrofotografia/captura (Ex: N.I.N.A.) e ligue o Live View da sua câmera apontada para uma fonte de luz ou estrela desfocada (conforme o método de colimação escolhido).

Execute o script do colimador:

Bash
python ocal_colimator.py
A janela abrirá maximizada em modo overlay.

Para mover o overlay: Clique e arraste segurando o mouse em cima de qualquer área cinza da Sidebar lateral esquerda.

Use os sliders para ajustar os raios dos círculos até que eles tangenciem perfeitamente a borda do espelho secundário, primário e a sombra do secundário.

Faça os ajustes físicos nos parafusos de colimação do telescópio até que todos os elementos fiquem perfeitamente concêntricos com os círculos virtuais.

Para fechar o programa, clique no botão "Sair do Colimador" na parte inferior da barra lateral.

🎨 Layout e Cores Padrão
O software foi desenhado com cores de alto contraste para ambiente noturno/campo:

Círculo 1: Azul Claro (#ADD8E6)

Círculo 2: Verde Claro (#90EE90)

Círculo 3: Amarelo (#FFFFE0)

Retículo Central: Vermelho Claro (#FF6666)

📄 Licença
Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.

Desenvolvido para facilitar a vida de astrônomos amadores que buscam estrelas perfeitamente pontuais. 🌌