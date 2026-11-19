# Travus Reels Maker

*[Read in English](README.md)*

Uma **skill do Claude Code** que transforma um vídeo de fala, uma locução, uma abertura com avatar de IA ou só um tema em um **reels vertical** pronto e editado com cara profissional (Instagram Reels, TikTok, YouTube Shorts, Facebook Reels). Ela também agenda a publicação.

É construída sobre o [HyperFrames](https://hyperframes.heygen.com) (HTML + GSAP renderizado como vídeo): cada legenda, título e motion graphic é animação de verdade, não texto queimado com ffmpeg.

## O que ela faz

- **4 pontos de partida:**
  - vídeo bruto de fala (jump cuts + punch-ins);
  - locução em MP3 (motion graphics sobre b-roll);
  - um **tema**: pesquisa → roteiro com gancho comprovado → narração com a **sua voz clonada** (Fish Audio ou ElevenLabs);
  - **híbrido**: um clipe de abertura (ex.: avatar de IA) seguido de narração.
- **Legendas animadas:** palavra por palavra, frases curtas ou karaokê, com contorno ou pílula e palavras-chave em destaque, dentro das zonas seguras das plataformas.
- **5 estilos de edição** (clássico, canvas editorial, produto kinetic, terminal neon, cinematográfico 3D) e uma **biblioteca de motion** com ~70 recursos ligados a componentes prontos do HyperFrames: odômetros, gráficos, mockups de chat e celular, cursor clicando, transições whip, iris e corte diagonal, cards 3D flutuando, câmera percorrendo uma tela.
- **3 visuais + a sua marca:** bold-dark, clean-light, neon-retro, ou as suas cores sobre base escura ou clara.
- **Título fixo e gancho**, logos oficiais, b-roll sincronizado com cada frase e cenas prontas (card de empresa, comparação, checklist, produto em publi, CTA).
- **Som:** música livre de direitos (escolhida medindo o quanto ela compete com a voz), ducking, efeitos discretos e loudness em −14 LUFS.
- **Entregas:** MP4 em qualidade máxima, cópia < 30 MB para o celular, capa e legenda do post (limite de hashtags, fontes, aviso de IA e #publi).
- **Publicação opcional:** agenda Instagram, Facebook, TikTok e YouTube Shorts de uma vez pelo Social Planner do GoHighLevel. Sempre pergunta o dia e a hora antes.
- **Honesta por padrão:** confere as afirmações com fontes, nunca inventa números ou citações e credita material de terceiros.

## Como ela conversa com você

**Primeira execução: setup** (~2 minutos, uma vez só). Perguntas de múltipla escolha sobre idioma, visual padrão, estilo de legenda e provedor de voz; depois publicação, fuso horário, CTA padrão e onde parar para aprovação. Mais uma mensagem curta com seu @, nicho, pasta dos projetos e as palavras com que seus reels nunca podem começar. As chaves de API ficam no cofre do sistema, nunca em texto.

**Cada vídeo: um briefing curto.**

| Rodada | Quando | Perguntas |
| --- | --- | --- |
| 1 | sempre | legendas · visual · duração · personalizar mais? |
| 2 | se você quiser | ritmo e cortes · fonte do b-roll · estilo da música · CTA |
| 3 | se você quiser tudo | título fixo · estilo e posição da legenda · é publi? · tom da narração (ou entregáveis) |

Toda pergunta tem a opção "meu padrão", e o que o seu pedido já diz não é perguntado.

## Instalação

**Requisitos:**
- Node.js 18+
- FFmpeg no PATH
- Python 3.9+, mais `python -m pip install fonttools brotli keyring tzdata`
- um agente de IA que **rode comandos no seu computador** (veja a tabela de compatibilidade abaixo)

### Opção 1: plugin do Claude Code (recomendado)

Dentro do Claude Code:

```
/plugin marketplace add rodrigobsm/travus-reels-maker
/plugin install travus-reels-maker@travus
```

Ou pelo terminal:

```bash
claude plugin marketplace add rodrigobsm/travus-reels-maker
claude plugin install travus-reels-maker@travus
```

### Opção 2: manual (pasta de skills do Claude Code)

```bash
git clone https://github.com/rodrigobsm/travus-reels-maker ~/.claude/skills/travus-reels-maker
```

No Windows, a pasta é `%USERPROFILE%\.claude\skills\travus-reels-maker`. Funciona no Claude Code pelo terminal, nas extensões de IDE e na aba Code do app desktop do Claude.

### Opção 3: outros agentes (não testado)

O `SKILL.md` segue o formato aberto de Agent Skills, então agentes que leem skills podem rodá-la. Clone o repo na pasta de skills do seu agente e confira a documentação dele para o caminho exato. Exemplos: Codex CLI da OpenAI, Cursor, GitHub Copilot.

Diferenças fora do Claude Code:
- As perguntas de múltipla escolha chegam como lista numerada (responda assim: `1a 2c 3b`).
- Pode ser preciso instalar as skills do HyperFrames à mão.

### Depois de instalar

Rode `python <pasta da skill>/scripts/doctor.py`. No Claude Code, as skills do HyperFrames (`hyperframes`, `hyperframes-cli`, `media-use`) são oferecidas pelo `npx hyperframes init` na primeira vez.

### Compatibilidade

| Ferramenta | Situação |
| --- | --- |
| Claude Code (terminal, IDE, aba Code do app) | ✅ feita e testada nele |
| Codex CLI, Cursor, Copilot e outros agentes locais com skills | ⚠️ deve funcionar, não testado |
| ChatGPT, Gemini ou Claude **no navegador** | ❌ não: eles não rodam FFmpeg, Node e o renderizador na sua máquina |

## Uso

É só pedir ao Claude Code:

- "Edita o reels do `~/Videos/bruto.mov`"
- "Faz um reels de 45 segundos sobre o novo iPhone, tema claro"
- "Minha locução está em `./locucao`, monta o reels"
- "Usa o `abertura.mp4` como abertura e narra esse roteiro com a minha voz"
- "Cria a legenda do post" / "Agenda nas minhas 4 redes"

## Provedores opcionais

| Provedor | Para | Segredo | Config |
| --- | --- | --- | --- |
| Fish Audio | narração com voz clonada (s2.1-pro, tags de emoção livres) | `fish_api_key` | `voice.voiceId` |
| ElevenLabs | narração com voz clonada (audio tags do eleven_v3) | `elevenlabs_api_key` | `voice.voiceId` |
| GoHighLevel Social Planner | agendar IG, FB, TikTok e YouTube Shorts | `ghl_token` | `publish.ghl.locationId`, `publish.ghl.userId` |
| Google Gemini API | tomadas do seu avatar de IA (Gemini Omni Flash), capas e imagens de b-roll (Nano Banana) | `gemini_api_key` | `avatar.*`, `gemini.*` |

Guarde as chaves no seu próprio terminal: `python scripts/secrets_store.py set fish_api_key` e cole a chave. Para outro TTS ou agendador, acrescente um provedor em `scripts/tts.py` ou um `scripts/publish_<nome>.py`.

## Estrutura e licenças

A mesma do [README em inglês](README.md#repository-layout). A sua configuração fica em `~/.travus-reels/config.json` (ou em `TRAVUS_REELS_HOME`), nunca no repositório.

- Código: MIT.
- Fontes: SIL OFL 1.1.
- O HyperFrames e as mídias de banco (Mixkit etc.) seguem as licenças de cada um.
- Os direitos de material de terceiros que você usar nos vídeos são responsabilidade sua.
