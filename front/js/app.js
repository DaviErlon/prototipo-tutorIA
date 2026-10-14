import { criarChatController } from './chat-controller.js';
import { criarChatView } from './chat-view.js';
import { criarChunksController } from './chunks-controller.js';
import { criarChunksView } from './chunks-view.js';

function selecionarSeletor(seletor) {
    const elemento = document.querySelector(seletor);
    if (!elemento) {
        throw new Error(`Elemento obrigatório não encontrado: ${seletor}`);
    }
    return elemento;
}

export function inicializarApp() {
    const textarea = selecionarSeletor('.text');
    const sendBtn = selecionarSeletor('#send-btn');
    const newChunkBtn = selecionarSeletor('#new-chunk-btn');
    const lupaIcon = selecionarSeletor('.lupa');
    const setaIcon = selecionarSeletor('.seta');
    const sideBar = selecionarSeletor('.sidebar');
    const newChatBtn = selecionarSeletor('#new-chat-btn');
    const chatHeader = selecionarSeletor('.chat-header');
    const chunksBtn = selecionarSeletor('#header-btn');
    const messagesInner = selecionarSeletor('.messages-inner');
    const messagesBox = selecionarSeletor('.messages');
    const chunksBox = selecionarSeletor('.chunks');
    const chunksGrid = selecionarSeletor('.chunks-grid');
    const chatHistory = selecionarSeletor('.chat-history');

    let modoChunks = false;

    const chatView = criarChatView({
        textarea,
        sendBtn,
        chatHistory,
        chatHeader,
        messagesInner,
        messagesBox
    });
    const chatController = criarChatController({
        chatView,
        textarea,
        sendBtn
    });

    const chunksView = criarChunksView({
        chunksGrid,
        chunksBox
    });
    const chunksController = criarChunksController({
        chunksView,
        textarea
    });

    let timerPesquisa;

    textarea.addEventListener('input', () => {
        textarea.style.height = 'auto';
        textarea.style.height = `${textarea.scrollHeight}px`;

        sendBtn.disabled = textarea.value.trim().length === 0;

        if (!modoChunks) return;

        clearTimeout(timerPesquisa);

        if (textarea.value.trim() === '') {
            chunksController.carregarChunks();
            return;
        }

        timerPesquisa = setTimeout(() => {
            chunksController.buscarChunks();
        }, 1000);
    });

    textarea.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();

            if (!sendBtn.disabled) {
                sendBtn.click();
            }
        }
    });

    newChunkBtn.addEventListener('click', chunksController.novoChunk);
    newChatBtn.addEventListener('click', chatController.novoChat);

    sendBtn.addEventListener('click', () => {
        if (modoChunks) {
            chunksController.buscarChunks();
        } else {
            chatController.enviarPrompt();
        }
    });

    chunksBtn.addEventListener('click', () => {
        chatView.limparTextarea();

        modoChunks = !modoChunks;
        if (modoChunks) {
            textarea.placeholder = 'Pesquise por um chunk...';
        } else {
            textarea.placeholder = 'Envie uma mensagem...';
        }

        sideBar.classList.toggle('hidden');
        lupaIcon.classList.toggle('hidden');
        setaIcon.classList.toggle('hidden');
        messagesBox.classList.toggle('hidden');
        chunksBox.classList.toggle('hidden');
        newChunkBtn.classList.toggle('hidden');
    });


    chatController.inicializar();
    chunksController.inicializar();
}