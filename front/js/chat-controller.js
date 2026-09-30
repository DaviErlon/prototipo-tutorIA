import {
    apiCriarChat,
    apiDeletarChat,
    apiEnviarPrompt,
    apiListarChats,
    apiListarMensagens
} from './api.js';

export function criarChatController(view, textarea, sendBtn) {
    let chatAtualId = null;
    let enviando = false;

    async function carregarChats() {
        try {
            const chats = await apiListarChats();
            view.renderizarListaChats(chats, chatAtualId, abrirChat, deletarChat);
            return chats;
        } catch (error) {
            console.error(error);
            return [];
        }
    }

    async function abrirChat(id) {
        try {
            chatAtualId = id;
            const mensagens = await apiListarMensagens(id);
            view.renderizarMensagens(mensagens);
            view.definirChatAtivo(id);
            textarea.focus();
        } catch (error) {
            console.error(error);
        }
    }

    async function novoChat() {
        try {
            const res = await apiCriarChat();
            await carregarChats();
            await abrirChat(res.id);
        } catch (error) {
            console.error(error);
        }
    }

    async function deletarChat(id) {
        try {
            await apiDeletarChat(id);
            const chats = await carregarChats();

            if (id === chatAtualId) {
                chatAtualId = null;
                if (chats.length > 0) {
                    const maisRecente = Math.max(...chats.map((chat) => chat.id));
                    await abrirChat(maisRecente.id);
                } else {
                    view.renderizarEstadoVazio();
                }
            }
        } catch (error) {
            console.error(error);
        }
    }

    async function enviarPrompt() {
        if (enviando) return;

        const mensagem = textarea.value.trim();
        if (mensagem.length === 0) return;

        enviando = true;
        sendBtn.disabled = true;

        try {
            if (chatAtualId === null) {
                chatAtualId = await apiCriarChat();
                view.limparMensagens();
                await carregarChats();
            }

            const idDoChat = chatAtualId;
            view.renderizarMensagem({ role: 'user', content: mensagem });
            view.limparTextarea();
            view.rolarParaOFim();
            view.mostrarDigitando();

            try {
                const data = await apiEnviarPrompt(idDoChat, mensagem);
                if (chatAtualId === idDoChat) {
                    view.removerDigitando();
                    view.renderizarMensagem({ role: 'tutor', content: data.content });
                    view.rolarParaOFim();
                }
            } catch (error) {
                console.error(error);
                if (chatAtualId === idDoChat) {
                    view.removerDigitando();
                    view.mostrarErro('Não foi possível obter a resposta. Tente novamente.');
                }
            }
        } catch (error) {
            console.error(error);
            view.mostrarErro('Não foi possível criar a conversa.');
        } finally {
            enviando = false;
            sendBtn.disabled = textarea.value.trim().length === 0;
            textarea.focus();
        }
    }

    async function inicializar() {
        const chats = await carregarChats();
        if (chats.length > 0) {
            const maisRecente = Math.max(...chats.map((chat) => chat.id));
            await abrirChat(maisRecente);
        } else {
            view.renderizarEstadoVazio();
        }
    }

    return {
        deletarChat,
        enviarPrompt,
        inicializar,
        novoChat
    };
}
