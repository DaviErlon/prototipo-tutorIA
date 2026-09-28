const API_URL = "/api/chat";

const textarea = document.querySelector('.text');
const sendBtn = document.getElementById('send_btn');
const newChatBtn = document.querySelector('.new-chat-btn');
const chatHistory = document.querySelector('.chat-history');
const chatHeader = document.querySelector('.chat-header');
const messagesInner = document.querySelector('.messages-inner');
const messagesBox = document.querySelector('.messages');

let chatAtualId = null;

/* ---------------------------------------------------------
   Utilitários
--------------------------------------------------------- */

if (window.marked) {
    marked.setOptions({ breaks: true, gfm: true });
}

// Links das respostas abrem em nova aba
if (window.DOMPurify) {
    DOMPurify.addHook('afterSanitizeAttributes', (node) => {
        if (node.tagName === 'A') {
            node.setAttribute('target', '_blank');
            node.setAttribute('rel', 'noopener noreferrer');
        }
    });
}

function markdownParaHTML(texto) {
    // Se as libs não carregarem, cai para texto puro (seguro)
    if (!window.marked || !window.DOMPurify) return escapeHTML(texto);
    return DOMPurify.sanitize(marked.parse(texto));
}

function escapeHTML(texto) {
    const div = document.createElement('div');
    div.textContent = texto;
    return div.innerHTML;
}

function rolarParaOFim() {
    messagesBox.scrollTop = messagesBox.scrollHeight;
}

function limparTextarea() {
    textarea.value = '';
    textarea.style.height = 'auto';
    sendBtn.disabled = true;
}

/* ---------------------------------------------------------
   Chamadas à API
--------------------------------------------------------- */

async function apiCriarChat() {
    const res = await fetch(`${API_URL}/`, { method: 'POST' });
    if (!res.ok) throw new Error('Erro ao criar chat');
    const data = await res.json();
    return data.id;
}

async function apiListarChats() {
    const res = await fetch(`${API_URL}/`);
    if (!res.ok) throw new Error('Erro ao listar chats');
    return await res.json();
}

async function apiListarMensagens(id) {
    const res = await fetch(`${API_URL}/${id}`);
    if (!res.ok) throw new Error('Erro ao listar mensagens');
    return await res.json();
}

async function apiDeletarChat(id) {
    const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Erro ao deletar chat');
    return await res.json();
}

/* ---------------------------------------------------------
   Renderização
--------------------------------------------------------- */

function renderizarMensagem(msg) {
    const isUser = msg.role === 'user';
    const classe = isUser ? 'user' : 'tutor';
    const rotulo = isUser ? 'você' : 'tutor';

    const el = document.createElement('div');
    el.className = `message ${classe}`;

    const role = document.createElement('span');
    role.className = 'role';
    role.textContent = rotulo;

    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    if (isUser) {
        bubble.textContent = msg.content;
    } else {
        bubble.classList.add('markdown');
        bubble.innerHTML = markdownParaHTML(msg.content);
    }

    el.appendChild(role);
    el.appendChild(bubble);
    messagesInner.appendChild(el);
}

function renderizarMensagens(mensagens) {
    messagesInner.innerHTML = '';
    mensagens.forEach(renderizarMensagem);
    rolarParaOFim();
}

function renderizarEstadoVazio() {
    messagesInner.innerHTML = `
        <div class="message tutor">
            <span class="role">tutor</span>
            <div class="bubble">Olá! Crie uma nova conversa ou selecione uma existente para começar.</div>
        </div>
    `;
}

function renderizarListaChats(chats) {
    chatHistory.innerHTML = '';

    // Mais recentes primeiro
    const ordenados = [...chats].sort((a, b) => b.id - a.id);

    ordenados.forEach((chat) => {
        const item = document.createElement('div');
        item.className = 'history-item';
        item.dataset.id = chat.id;
        if (chat.id === chatAtualId) item.classList.add('active');

        const titulo = document.createElement('span');
        titulo.textContent = `Chat: ${chat.id}`;

        const btnDeletar = document.createElement('button');
        btnDeletar.className = 'delete-chat-btn';
        btnDeletar.title = 'Deletar conversa';
        btnDeletar.innerHTML = '&times;';

        btnDeletar.addEventListener('click', (e) => {
            e.stopPropagation();
            deletarChat(chat.id);
        });

        item.appendChild(titulo);
        item.appendChild(btnDeletar);
        item.addEventListener('click', () => abrirChat(chat.id));

        chatHistory.appendChild(item);
    });
}

/* ---------------------------------------------------------
   Ações
--------------------------------------------------------- */

async function carregarChats() {
    try {
        const chats = await apiListarChats();
        renderizarListaChats(chats);
        return chats;
    } catch (err) {
        console.error(err);
        return [];
    }
}

async function abrirChat(id) {
    try {
        chatAtualId = id;
        const mensagens = await apiListarMensagens(id);
        renderizarMensagens(mensagens);
        chatHeader.textContent = `Chat: ${id}`;

        document.querySelectorAll('.history-item').forEach((el) => {
            el.classList.toggle('active', Number(el.dataset.id) === id);
        });

        textarea.focus();
    } catch (err) {
        console.error(err);
    }
}

async function novoChat() {
    try {
        const id = await apiCriarChat();
        await carregarChats();
        await abrirChat(id);
    } catch (err) {
        console.error(err);
    }
}

async function deletarChat(id) {
    try {
        await apiDeletarChat(id);

        const chats = await carregarChats();

        if (id === chatAtualId) {
            chatAtualId = null;
            if (chats.length > 0) {
                const maisRecente = Math.max(...chats.map((c) => c.id));
                await abrirChat(maisRecente);
            } else {
                chatHeader.textContent = '';
                renderizarEstadoVazio();
            }
        }
    } catch (err) {
        console.error(err);
    }
}

/* ---------------------------------------------------------
   Prompt
--------------------------------------------------------- */

async function apiEnviarPrompt(id, content) {
    const res = await fetch(`${API_URL}/${id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content })
    });
    if (!res.ok) throw new Error('Erro ao enviar mensagem');
    return await res.json(); // { id: <id da mensagem do tutor> }
}

function mostrarDigitando() {
    const el = document.createElement('div');
    el.className = 'message tutor';
    el.id = 'typing-indicator';
    el.innerHTML = `
        <span class="role">tutor</span>
        <div class="bubble">Pensando...</div>
    `;
    messagesInner.appendChild(el);
    rolarParaOFim();
}

function removerDigitando() {
    document.getElementById('typing-indicator')?.remove();
}

function mostrarErro(texto) {
    const el = document.createElement('div');
    el.className = 'message tutor';
    el.innerHTML = `
        <span class="role">erro</span>
        <div class="bubble">${escapeHTML(texto)}</div>
    `;
    messagesInner.appendChild(el);
    rolarParaOFim();
}

let enviando = false;

async function enviar_promt() {
    if (enviando) return;

    const mensagem = textarea.value.trim();
    if (mensagem.length === 0) return;

    enviando = true;
    sendBtn.disabled = true;

    try {
        // Se não houver chat aberto, cria um antes de enviar
        if (chatAtualId === null) {
            chatAtualId = await apiCriarChat();
            messagesInner.innerHTML = '';
            chatHeader.textContent = `Chat: ${chatAtualId}`;
            await carregarChats();
        }

        const idDoChat = chatAtualId;

        renderizarMensagem({ role: 'user', content: mensagem });
        limparTextarea();
        rolarParaOFim();
        mostrarDigitando();

        try {
            const data = await apiEnviarPrompt(idDoChat, mensagem);

            // Só atualiza a tela se o usuário ainda estiver nesse chat
            if (chatAtualId === idDoChat) {
                removerDigitando();
                renderizarMensagem({ role: 'tutor', content: data.content });
                rolarParaOFim();
            }
        } catch (err) {
            console.error(err);
            if (chatAtualId === idDoChat) {
                removerDigitando();
                mostrarErro('Não foi possível obter a resposta. Tente novamente.');
            }
        }
    } catch (err) {
        console.error(err);
        mostrarErro('Não foi possível criar a conversa.');
    } finally {
        enviando = false;
        sendBtn.disabled = textarea.value.trim().length === 0;
        textarea.focus();
    }
}

/* ---------------------------------------------------------
   Eventos
--------------------------------------------------------- */

textarea.addEventListener('input', () => {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
    sendBtn.disabled = textarea.value.trim().length === 0;
});

textarea.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        if (!sendBtn.disabled) sendBtn.click();
    }
});

sendBtn.addEventListener('click', () => {
    enviar_promt();
});

newChatBtn.addEventListener('click', novoChat);

/* ---------------------------------------------------------
   Inicialização
--------------------------------------------------------- */

async function init() {
    const chats = await carregarChats();

    if (chats.length > 0) {
        const maisRecente = Math.max(...chats.map((c) => c.id));
        await abrirChat(maisRecente);
    } else {
        renderizarEstadoVazio();
    }
}

init();