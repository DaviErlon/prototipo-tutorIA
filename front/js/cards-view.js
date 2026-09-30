export function criarCardsView(
    cardsGrid
) {

    function renderizarEstadoVazio() {
        cardsGrid.innerHTML = '';

        const el = document.createElement('div');
        el.className = 'message tutor';

        const role = document.createElement('span');
        role.className = 'role';
        role.textContent = 'tutor';

        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.textContent = 'Olá! Crie um card para me auxiliar nas suas perguntas!';

        el.append(role, bubble);

        cardsGrid.appendChild(el);
    }

    function renderizarCard(card, deletarCard) {
        const el = document.createElement('div');
        el.className = 'card';
        el.dataset.id = card.id;

        const header = document.createElement('div');
        header.className = 'card-header';

        const title = document.createElement('span');
        title.className = 'card-title';
        title.textContent = card.title;

        const btnDeletar = document.createElement('button');
        btnDeletar.className = 'delete-btn';
        btnDeletar.type = 'button';
        btnDeletar.title = 'Deletar card';
        btnDeletar.innerHTML = '&times;';

        btnDeletar.addEventListener('click', (event) => {
            event.stopPropagation();
            deletarCard(card.id);
        });

        const content = document.createElement('div');
        content.className = 'card-content';
        content.textContent = card.content;

        header.append(title, btnDeletar);
        el.append(header, content);

        cardsGrid.appendChild(el);
    }

    function renderizarCards(cards, deletarCard) {
        cardsGrid.innerHTML = '';

        if (!cards || cards.length === 0) {
            renderizarEstadoVazio();
            return;
        }

        cards.forEach(card => {
            renderizarCard(card, deletarCard);
        });
    }

    function limparCards() {
        cardsGrid.innerHTML = '';
    }

    return {
        renderizarCard,
        renderizarCards,
        renderizarEstadoVazio,
        limparCards
    };
}