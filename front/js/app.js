import { criarChatController } from './chat-controller.js';
import { criarChatView } from './chat-view.js';
import { criarCardsController } from './cards-controller.js';
import { criarCardsView } from './cards-view.js';

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
    const newCardBtn = selecionarSeletor('#new-card-btn');
    const lupaIcon = selecionarSeletor('.lupa');
    const setaIcon = selecionarSeletor('.seta');
    const sideBar = selecionarSeletor('.sidebar');
    const newChatBtn = selecionarSeletor('#new-chat-btn');
    const chatHeader = selecionarSeletor('.chat-header');
    const cardsBtn = selecionarSeletor('#header-btn');
    const messagesInner = selecionarSeletor('.messages-inner');
    const messagesBox = selecionarSeletor('.messages');
    const cardsBox = selecionarSeletor('.cards');
    const cardsGrid = selecionarSeletor('.cards-grid');
    const chatHistory = selecionarSeletor('.chat-history');

    let modoCards = false;

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

    const cardsView = criarCardsView({
        cardsGrid,
        cardsBox
    });
    const cardsController = criarCardsController({
        cardsView,
        textarea
    });

    let timerPesquisa;

    textarea.addEventListener('input', () => {
        textarea.style.height = 'auto';
        textarea.style.height = `${textarea.scrollHeight}px`;

        sendBtn.disabled = textarea.value.trim().length === 0;

        if (!modoCards) return;

        clearTimeout(timerPesquisa);

        if (textarea.value.trim() === '') {
            cardsController.carregarCards();
            return;
        }

        timerPesquisa = setTimeout(() => {
            cardsController.buscarCards();
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

    newCardBtn.addEventListener('click', cardsController.novoCard);
    newChatBtn.addEventListener('click', chatController.novoChat);

    sendBtn.addEventListener('click', () => {
        if (modoCards) {
            cardsController.buscarCards();
        } else {
            chatController.enviarPrompt();
        }
    });

    cardsBtn.addEventListener('click', () => {
        chatView.limparTextarea();

        modoCards = !modoCards;
        if (modoCards) {
            textarea.placeholder = 'Pesquise por um card...';
        } else {
            textarea.placeholder = 'Envie uma mensagem...';
        }

        sideBar.classList.toggle('hidden');
        lupaIcon.classList.toggle('hidden');
        setaIcon.classList.toggle('hidden');
        messagesBox.classList.toggle('hidden');
        cardsBox.classList.toggle('hidden');
        newCardBtn.classList.toggle('hidden')
    });


    chatController.inicializar();
    cardsController.inicializar();
}
