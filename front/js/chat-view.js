function escapeHTML(texto) {
    const div = document.createElement('div');
    div.textContent = texto;
    return div.innerHTML;
}

function markdownParaHTML(texto) {
    if (!window.marked || !window.DOMPurify) return escapeHTML(texto);
    return window.DOMPurify.sanitize(window.marked.parse(texto));
}

function configurarMarkdown() {
    if (window.marked) {
        window.marked.setOptions({ breaks: true, gfm: true });
    }

    if (window.DOMPurify) {
        window.DOMPurify.addHook('afterSanitizeAttributes', (node) => {
            if (node.tagName === 'A') {
                node.setAttribute('target', '_blank');
                node.setAttribute('rel', 'noopener noreferrer');
            }
        });
    }
}

export function criarChatView({
    textarea,
    sendBtn,
    chatHistory,
    messagesInner,
    messagesBox
}) {
    configurarMarkdown();

    function rolarParaOFim() {
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    function renderizarMensagem(msg) {
        const isUser = msg.role === 'user';
        const el = document.createElement('div');
        el.className = `message ${isUser ? 'user' : 'tutor'}`;

        const role = document.createElement('span');
        role.className = 'role';
        role.textContent = isUser ? 'você' : 'tutor';

        const bubble = document.createElement('div');
        bubble.className = 'bubble';

        if (isUser) {
            bubble.textContent = msg.content;
        } else {
            bubble.classList.add('markdown');
            bubble.innerHTML = markdownParaHTML(msg.content);
        }

        el.append(role, bubble);
        messagesInner.appendChild(el);
    }

    function limparMensagens() {
        messagesInner.innerHTML = '';
    }

    function renderizarMensagens(mensagens) {
        messagesInner.innerHTML = '';
        mensagens.forEach(renderizarMensagem);
        rolarParaOFim();
    }

    function renderizarEstadoVazio() {
        messagesInner.innerHTML = '';

        const el = document.createElement('div');
        el.className = 'message tutor';

        const role = document.createElement('span');
        role.className = 'role';
        role.textContent = 'tutor';

        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.textContent = 'Olá! Crie uma nova conversa ou selecione uma existente para começar.';

        el.append(role, bubble);
        messagesInner.appendChild(el);
    }

    function renderizarItemChat(chat, chatAtualId, abrirChat, deletarChat) {
        const item = document.createElement('div');
        item.className = 'history-item';
        item.dataset.id = chat.id;
        if (chat.id === chatAtualId) item.classList.add('active');

        const titulo = document.createElement('span');
        titulo.textContent = `Chat: ${chat.id}`;

        const btnDeletar = document.createElement('button');
        btnDeletar.className = 'delete-btn';
        btnDeletar.title = 'Deletar conversa';
        btnDeletar.innerHTML = '&times;';
        btnDeletar.addEventListener('click', (event) => {
            event.stopPropagation();
            deletarChat(chat.id);
        });

        item.append(titulo, btnDeletar);
        item.addEventListener('click', () => abrirChat(chat.id));
        chatHistory.appendChild(item);
    }

    function renderizarListaChats(chats, chatAtualId, abrirChat, deletarChat) {
        chatHistory.innerHTML = '';
        const ordenados = [...chats].sort((a, b) => b.id - a.id);

        ordenados.forEach((chat) => { renderizarItemChat(chat, chatAtualId, abrirChat, deletarChat) });
    }

    function definirChatAtivo(id) {
        chatHistory.querySelectorAll('.history-item').forEach((item) => {
            item.classList.toggle('active', Number(item.dataset.id) === id);
        });
    }

    function limparTextarea() {
        textarea.value = '';
        textarea.style.height = 'auto';
        sendBtn.disabled = true;
    }

    function mostrarDigitando() {
        const el = document.createElement('div');
        el.className = 'message tutor';
        el.id = 'typing-indicator';

        const role = document.createElement('span');
        role.className = 'role';
        role.textContent = 'tutor';

        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.textContent = 'Pensando...';

        el.append(role, bubble);
        messagesInner.appendChild(el);
        rolarParaOFim();
    }

    function removerDigitando() {
        messagesInner.querySelector('#typing-indicator')?.remove();
    }

    function mostrarErro(texto) {
        const el = document.createElement('div');
        el.className = 'message tutor';

        const role = document.createElement('span');
        role.className = 'role';
        role.textContent = 'erro';

        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.textContent = texto;

        el.append(role, bubble);
        messagesInner.appendChild(el);
        rolarParaOFim();
    }

    return {
        renderizarMensagem,
        rolarParaOFim,
        mostrarErro,
        removerDigitando,
        mostrarDigitando,
        limparTextarea,
        definirChatAtivo,
        renderizarListaChats,
        renderizarEstadoVazio,
        limparMensagens,
        renderizarMensagens,
    };
}
