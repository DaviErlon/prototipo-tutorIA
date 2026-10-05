import {
    apiCriarChat,
    apiDeletarChat,
    apiEnviarPromptStream,
    apiListarChats,
    apiListarMensagens
} from './api.js';

export function criarChatController({
    chatView,
    textarea,
    sendBtn
}) {
    let chatAtualId = null;
    let enviando = false;

    async function carregarChats() {
        try {
            const chats = await apiListarChats();
            chatView.renderizarListaChats(chats, chatAtualId, abrirChat, deletarChat);
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
            chatView.renderizarMensagens(mensagens);
            chatView.definirChatAtivo(id);
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
                    await abrirChat(maisRecente);
                } else {
                    chatView.renderizarEstadoVazio();
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
                const novo = await apiCriarChat();
                chatAtualId = novo.id;
                chatView.limparMensagens();
                await carregarChats();
            }

            const idDoChat = chatAtualId;
            chatView.renderizarMensagem({ role: 'user', content: mensagem });
            chatView.limparTextarea();
            chatView.rolarParaOFim();
            chatView.mostrarDigitando();

            let bolha = null;

            try {
                await apiEnviarPromptStream(idDoChat, mensagem, (_chunk, textoCompleto) => {
                    if (chatAtualId !== idDoChat) return;

                    if (!bolha) {
                        chatView.removerDigitando();
                        bolha = chatView.iniciarMensagemStream();
                    }

                    const seguirFim = chatView.estaPertoDoFim();
                    bolha.atualizar(textoCompleto);
                    if (seguirFim) chatView.rolarParaOFim();
                });

                // Se o stream terminou sem nenhum pedaço, tira o "Pensando..."
                if (!bolha && chatAtualId === idDoChat) {
                    chatView.removerDigitando();
                }
            } catch (error) {
                console.error(error);
                if (chatAtualId === idDoChat) {
                    chatView.removerDigitando();
                    chatView.mostrarErro('Não foi possível obter a resposta. Tente novamente.');
                }
            }
        } catch (error) {
            console.error(error);
            chatView.mostrarErro('Não foi possível criar a conversa.');
        } finally {
            enviando = false;
            sendBtn.disabled = textarea.value.trim().length === 0;
            textarea.focus();
        }
    }

    /*
    async function enviarPrompt() {
        if (enviando) return;

        const mensagem = textarea.value.trim();
        if (mensagem.length === 0) return;

        enviando = true;
        sendBtn.disabled = true;

        try {
            if (chatAtualId === null) {
                chatAtualId = await apiCriarChat();
                chatView.limparMensagens();
                await carregarChats();
            }

            const idDoChat = chatAtualId;
            chatView.renderizarMensagem({ role: 'user', content: mensagem });
            chatView.limparTextarea();
            chatView.rolarParaOFim();
            chatView.mostrarDigitando();

            try {
                const data = await apiEnviarPrompt(idDoChat, mensagem);
                if (chatAtualId === idDoChat) {
                    chatView.removerDigitando();
                    chatView.renderizarMensagem({ role: 'tutor', content: data.content });
                    chatView.rolarParaOFim();
                }
            } catch (error) {
                console.error(error);
                if (chatAtualId === idDoChat) {
                    chatView.removerDigitando();
                    chatView.mostrarErro('Não foi possível obter a resposta. Tente novamente.');
                }
            }
        } catch (error) {
            console.error(error);
            chatView.mostrarErro('Não foi possível criar a conversa.');
        } finally {
            enviando = false;
            sendBtn.disabled = textarea.value.trim().length === 0;
            textarea.focus();
        }
    }
    */

    async function inicializar() {
        const chats = await carregarChats();
        if (chats.length > 0) {
            const maisRecente = Math.max(...chats.map((chat) => chat.id));
            await abrirChat(maisRecente);
        } else {
            chatView.renderizarEstadoVazio();
        }
    }

    return {
        deletarChat,
        enviarPrompt,
        inicializar,
        novoChat
    };
}
