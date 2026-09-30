import {
    apiGetCards,
    apiCriarCard,
    apiDeletarCard,
} from './api.js';

export function criarCardsController(view) {
    async function carregarCards() {
        try {
            const cards = await apiGetCards('', 6);
            view.renderizarCards(cards.data, deletarCard);
            return cards;
        } catch (error) {
            console.error(error);
            return [];
        }
    }

    async function novoCard(card) {
        try {
            await apiCriarCard(card);
            await carregarCards();
        } catch (error) {
            console.error(error);
        }
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