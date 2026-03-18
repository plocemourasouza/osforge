# UX Guidelines — UI Design Intelligence

99 diretrizes de UX curadas: boas práticas, anti-patterns e regras de acessibilidade.
Organizadas por domínio para busca rápida.

---

## Layout & Espaçamento

✅ Use escala de espaçamento baseada em múltiplos de 4px (4, 8, 12, 16, 24, 32, 48, 64)  
✅ Espaçamento interno (padding) sempre maior que espaçamento externo entre elementos relacionados  
✅ Agrupar elementos relacionados com espaçamento menor; separar grupos com espaçamento maior  
✅ Linhas de conteúdo: max-width entre 60–80 caracteres para leitura confortável  
✅ Hierarquia visual clara: o elemento mais importante ocupa mais espaço/atenção  
❌ Nunca usar valores de espaçamento arbitrários (17px, 23px) — quebra a grid  
❌ Nunca encher todos os espaços disponíveis — espaço em branco é design  
❌ Evitar mais de 3 níveis de hierarquia visual na mesma tela  

---

## Formulários

✅ Labels sempre visíveis (nunca usar apenas placeholder como label)  
✅ Validação inline — mostrar erro logo abaixo do campo após o usuário sair dele  
✅ Mensagens de erro específicas: "Email inválido" não "Preencha corretamente"  
✅ Agrupar campos relacionados (endereço: rua + número + CEP juntos)  
✅ Botão de submit próximo ao último campo do formulário  
✅ Indicar campos obrigatórios com asterisco + legenda "* obrigatório"  
✅ Auto-focus no primeiro campo de formulários curtos  
✅ Desabilitar botão de submit durante processamento para evitar double-submit  
❌ Nunca limpar um formulário sem confirmação do usuário  
❌ Nunca exigir formato específico sem máscaras (CPF, telefone, CEP)  
❌ Evitar CAPTCHAs — usar honeypots ou rate limiting no backend  

---

## Navegação

✅ Indicar localização atual no menu/breadcrumb sempre  
✅ Links visitados devem ter cor diferente de links não visitados  
✅ Âncoras de navegação principais: máximo 7 itens (Miller's Law)  
✅ Menu mobile: hamburger com label "Menu", não apenas ícone  
✅ Back button: sempre disponível em mobile — não confiar no botão do sistema  
✅ Breadcrumb para hierarquias com 3+ níveis  
❌ Nunca esconder a navegação principal em desktop sem razão clara  
❌ Evitar dropdowns com mais de 10 itens — usar search ou categorias  
❌ Nunca abrir links externos sem aviso  

---

## Feedback e Estados

✅ Todo action button precisa de estado de loading quando a ação é assíncrona  
✅ Feedback de sucesso: máximo 3 segundos, depois desaparecer automaticamente  
✅ Feedback de erro: permanecer visível até o usuário agir  
✅ Skeleton loaders para conteúdo que demora >300ms para carregar  
✅ Mensagens de erro devem sugerir a próxima ação ("Verifique sua conexão e tente novamente")  
✅ Confirmação antes de ações destrutivas (deletar, cancelar, arquivar)  
✅ Undo disponível por 5–10 segundos após ação destrutiva (quando possível)  
❌ Nunca usar spinners sem timeout — usuário fica esperando para sempre  
❌ Nunca usar alert() nativo do browser para feedback  
❌ Nunca exibir stack traces para o usuário final  

---

## Acessibilidade

✅ Contraste mínimo WCAG AA: 4.5:1 para texto normal, 3:1 para texto grande (>18px bold)  
✅ Todos os elementos interativos devem ter focus visible (outline ou ring)  
✅ Ordem de tab deve seguir a ordem visual de cima para baixo, esquerda para direita  
✅ Imagens decorativas: alt="" | Imagens informativas: alt com descrição  
✅ Ícones sem texto: aria-label obrigatório  
✅ Inputs: sempre associar com label via htmlFor/id  
✅ Tabelas: usar thead, th com scope, caption quando necessário  
✅ Modais: focar no primeiro elemento interativo ao abrir; retornar foco ao fechar  
✅ Animações: respeitar prefers-reduced-motion  
❌ Nunca usar cor como único indicador de estado (vermelho para erro SEM ícone/texto)  
❌ Nunca usar placeholder como substituto de label  
❌ Evitar "clique aqui" como texto de link — usar texto descritivo  

---

## Mobile

✅ Touch targets mínimos: 44x44px (Apple HIG) / 48x48px (Material)  
✅ Conteúdo crítico na metade superior da tela em mobile (acima do fold)  
✅ Inputs de telefone/número: type="tel" abre teclado numérico  
✅ Inputs de email: type="email" abre teclado com @  
✅ Swipe gestures: sempre ter alternativa por toque (swipe para deletar → botão delete)  
✅ Bottom navigation bar para apps mobile com 3–5 destinos principais  
❌ Nunca usar hover como único trigger de ação importante em mobile  
❌ Evitar modais que cobrem >80% da tela em mobile  
❌ Nunca esconder scroll de forma que o usuário não saiba que há mais conteúdo  

---

## Tabelas e Dados

✅ Alinhar números à direita, textos à esquerda  
✅ Colunas de status: usar badge colorido + texto (nunca só cor)  
✅ Tabelas longas: sticky header  
✅ Tabelas com muitas colunas: scroll horizontal com shadow indicador  
✅ Linhas alternadas (zebra) para tabelas densas  
✅ Paginação visível e com indicador de total ("Mostrando 1–20 de 156")  
✅ Ordenação: indicar coluna ativa e direção (ícone ↑↓)  
✅ Busca em tabelas: debounce de 300ms  
❌ Nunca paginar tabelas com menos de 20 linhas  
❌ Nunca usar tabelas para layouts — usar CSS Grid/Flex  

---

## Animação e Transição

✅ Duração padrão: 150–300ms para micro-interações  
✅ Entrada de elementos: fade + scale sutil (opacity 0→1, scale 0.95→1)  
✅ Saída de elementos: mais rápida que entrada (100–150ms)  
✅ Easing: ease-out para entradas, ease-in para saídas  
✅ Skeleton loader: animação shimmer suave (pulse)  
❌ Nunca animar mais de 3 propriedades simultaneamente  
❌ Evitar animações em loop que o usuário não pediu  
❌ Nunca usar animation-duration > 500ms para micro-interações  

---

## Performance Percebida

✅ Mostrar conteúdo o mais rápido possível — priorizar LCP  
✅ Otimistic updates: atualizar a UI antes da resposta do servidor para ações comuns  
✅ Skeleton loaders para listas e cards (nunca spinner centralizado para listas)  
✅ Imagens: usar next/image com lazy loading e placeholder blur  
✅ Fontes: preload as fontes críticas, usar font-display: swap  
❌ Nunca bloquear a UI para operações que podem ser feitas em background  
❌ Evitar redirects desnecessários — cada redirect adiciona 200–500ms  

---

## E-commerce específico

✅ Preço sempre em destaque — maior e mais bold que o restante do card  
✅ "Adicionar ao carrinho" deve confirmar visualmente (ícone animado, badge no cart)  
✅ Exibir estoque quando baixo ("Apenas 3 restantes")  
✅ Frete grátis acima de X: mostrar quanto falta para o usuário atingir  
✅ Carrinho persistente — sobrevive ao fechar o browser  
❌ Nunca cobrar frete surpresa no checkout — mostrar desde o product page  
❌ Evitar campos opcionais desnecessários no checkout  

---

## SaaS / Onboarding

✅ Onboarding: máximo 5 steps, com indicador de progresso  
✅ Empty states: sempre com imagem/ilustração + explicação + CTA  
✅ Trial: mostrar dias restantes no header/dashboard  
✅ Upgrade: mostrar o valor antes de pedir pagamento  
✅ Configurações: organizar em categorias, busca disponível se >15 items  
❌ Nunca redirecionar para pricing sem o usuário ter visto valor primeiro  
❌ Evitar feature gates sem explicar o que o usuário ganha ao fazer upgrade  
