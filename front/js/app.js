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
    const sendBtn = selecionarSeletor('#send_btn');
    const lupaIcon = selecionarSeletor('.lupa');
    const setaIcon = selecionarSeletor('.seta');
    const sideBar = selecionarSeletor('.sidebar');
    const newChatBtn = selecionarSeletor('.new-chat-btn');
    const chatHeader = selecionarSeletor('.chat-header');
    const cardsBtn = selecionarSeletor('.header-btn');
    const messagesInner = selecionarSeletor('.messages-inner');
    const messagesBox = selecionarSeletor('.messages');
    const cardsBox = selecionarSeletor('.cards');
    const cardsGride = selecionarSeletor('.cards-grid');
    const chatHistory = selecionarSeletor('.chat-history');

    let modoCards = false;

    const chat_view = criarChatView({
        textarea,
        sendBtn,
        chatHistory,
        chatHeader,
        messagesInner,
        messagesBox
    });
    const chat_controller = criarChatController(chat_view, textarea, sendBtn);

    const card_view = criarCardsView(cardsGride);
    const card_controller = criarCardsController(card_view);

    textarea.addEventListener('input', () => {
        textarea.style.height = 'auto';
        textarea.style.height = `${textarea.scrollHeight}px`;
        sendBtn.disabled = textarea.value.trim().length === 0;
    });

    // se modoCards entao pesquisar dps de 1 segundos sem o user digitar
    textarea.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            if (!sendBtn.disabled) sendBtn.click();
        }
    });

    // se modo Cards entao cards_chat_controller.pesquisarCards()
    sendBtn.addEventListener('click', chat_controller.enviarPrompt);

    cardsBtn.addEventListener('click', () => {
        chat_view.limparTextarea();
        
        modoCards = !modoCards;
        if(modoCards){
            textarea.placeholder = 'Pesquise por um card...';

        } else {
            textarea.placeholder = 'Envie uma mensagem...';

        }

        sendBtn.classList.toggle('hidden');
        sideBar.classList.toggle('hidden');
        lupaIcon.classList.toggle('hidden');
        setaIcon.classList.toggle('hidden');
        messagesBox.classList.toggle('hidden');
        cardsBox.classList.toggle('hidden');
    });

    newChatBtn.addEventListener('click', chat_controller.novoChat);

    chat_controller.inicializar();
    card_controller.inicializar();
    
}
