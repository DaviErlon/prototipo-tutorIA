import {
    apiGetCards,
    apiCriarCard,
    apiDeletarCard,
} from './api.js';

export function criarCardsController({ cardsView }) {

    function pegarPagina() {
        const page = localStorage.getItem('tutor-ia-page');
        if (page === null) {
            localStorage.setItem('tutor-ia-page', '1');
            return 1;
        }
        return Number(page);
    }


    async function carregarCards() {
        try {
            const page = pegarPagina();

            const cards = await apiGetCards('', page, 6);

            // voltar a pagina
            if (cards.data.length === 0 && page > 1) {
                localStorage.setItem(
                    'tutor-ia-page',
                    String(page - 1)
                );
                return carregarCards();
            }

            cardsView.renderizarCards(
                cards.data,
                deletarCard,
                cards.pagination,
                prevCards,
                proxCards
            );
            return cards;
        } catch (error) {
            console.error(error);
            return [];
        }
    }


    async function prevCards() {
        const pageAtual = pegarPagina();
        localStorage.setItem('tutor-ia-page', String(pageAtual - 1));
        await carregarCards();
    }


    async function proxCards() {
        const pageAtual = pegarPagina();
        localStorage.setItem('tutor-ia-page', String(pageAtual + 1));
        await carregarCards();
    }


    async function criarCard(title, content) {
        try {
            await apiCriarCard(title, content);
            await carregarCards();
        } catch (error) {
            console.error(error);
        }
    }

    async function novoCard() {
        cardsView.renderizarModal(criarCard);
    }

    async function deletarCard(id) {
        try {
            await apiDeletarCard(id);
            await carregarCards();
        } catch (error) {
            console.error(error);
        }
    }

    async function inicializar() {
        await carregarCards();
    }

    return {
        carregarCards,
        novoCard,
        deletarCard,
        inicializar
    };
}