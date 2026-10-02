export function criarCardsView({
    cardsGrid,
    cardsBox
}) {

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

    function renderizarSetas(
        pagination,
        prevCards,
        proxCards
    ) {
        // Remove as setas antigas
        cardsBox.querySelectorAll('.pagination-btn').forEach(btn => btn.remove());

        if (!pagination) {
            return;
        }

        // Botão página anterior
        if (pagination.page > 1) {

            const btnAnterior = document.createElement('button');
            btnAnterior.className = 'pagination-btn pagination-prev';
            btnAnterior.type = 'button';
            btnAnterior.innerHTML = '&#10094;';
            btnAnterior.title = 'Página anterior';
            btnAnterior.addEventListener(
                'click',
                prevCards
            );

            cardsBox.prepend(btnAnterior);
        }


        // Botão próxima página
        if (pagination.has_next) {

            const btnProxima = document.createElement('button');
            btnProxima.className = 'pagination-btn pagination-next';
            btnProxima.type = 'button';
            btnProxima.innerHTML = '&#10095;';
            btnProxima.title = 'Próxima página';
            btnProxima.addEventListener('click', proxCards);

            cardsBox.appendChild(btnProxima);
        }
    }

    function renderizarModal(criarCard) {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.id = 'card-modal';

        const modalContent = document.createElement('div');
        modalContent.className = 'modal-content';

        const modalHeader = document.createElement('div');
        modalHeader.className = 'modal-header';

        const titulo = document.createElement('h2');
        titulo.textContent = 'Novo card';

        const fecharBtn = document.createElement('button');
        fecharBtn.id = 'fechar-modal-btn';
        fecharBtn.textContent = '×';

        const form = document.createElement('form');
        form.id = 'card-form';

        const titleLabel = document.createElement('label');
        titleLabel.htmlFor = 'card-title';
        titleLabel.textContent = 'Título';

        const titleInput = document.createElement('input');
        titleInput.id = 'card-title';
        titleInput.type = 'text';
        titleInput.placeholder = 'Título do card';
        titleInput.required = true;

        const contentLabel = document.createElement('label');
        contentLabel.htmlFor = 'card-content';
        contentLabel.textContent = 'Conteúdo';

        const contentInput = document.createElement('textarea');
        contentInput.id = 'card-content';
        contentInput.placeholder = 'Conteúdo do card...';
        contentInput.required = true;

        const submitBtn = document.createElement('button');
        submitBtn.type = 'submit';
        submitBtn.textContent = 'Criar card';

        modalHeader.append(
            titulo,
            fecharBtn
        );

        form.append(
            titleLabel,
            titleInput,
            contentLabel,
            contentInput,
            submitBtn
        );

        modalContent.append(
            modalHeader,
            form
        );

        modal.append(modalContent);

        document.body.prepend(modal);

        function remover() {
            modal.remove();
        }

        fecharBtn.addEventListener('click', remover);

        form.addEventListener('submit', async (event) => {

            event.preventDefault();

            const title = titleInput.value;
            const content = contentInput.value;

            await criarCard(title, content);
            remover();
        });
    }

    function renderizarCards(
        cards,
        deletarCard,
        pagination,
        prevCards,
        proxCards
    ) {
        cardsGrid.innerHTML = '';

        if ((!cards || cards.length === 0 ) && pagination) {
            renderizarEstadoVazio();
            renderizarSetas(pagination, prevCards, proxCards);
            return;
        }

        cards.forEach(card => {
            renderizarCard(
                card,
                deletarCard
            );
        });

        renderizarSetas(pagination, prevCards, proxCards);
    }

    function limparCards() {
        cardsGrid.innerHTML = '';
        cardsBox.querySelectorAll('.pagination-btn').forEach(btn => btn.remove());
    }

    return {
        renderizarCard,
        renderizarCards,
        renderizarEstadoVazio,
        renderizarSetas,
        limparCards,
        renderizarModal
    };
}