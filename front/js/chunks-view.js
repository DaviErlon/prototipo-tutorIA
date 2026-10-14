export function criarChunksView({
    chunksGrid,
    chunksBox
}) {

    function renderizarEstadoVazio() {
        chunksGrid.innerHTML = '';

        const el = document.createElement('div');
        el.className = 'message tutor';

        const role = document.createElement('span');
        role.className = 'role';
        role.textContent = 'tutor';

        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.textContent = 'Olá! Crie um chunk para me auxiliar nas suas perguntas!';

        el.append(role, bubble);
        chunksGrid.appendChild(el);
    }


    function renderizarChunk(chunk, deletarChunk) {
        const el = document.createElement('div');
        el.className = 'chunk';
        el.dataset.id = chunk.id;

        const header = document.createElement('div');
        header.className = 'chunk-header';

        const btnDeletar = document.createElement('button');
        btnDeletar.className = 'delete-btn';
        btnDeletar.type = 'button';
        btnDeletar.title = 'Deletar chunk';
        btnDeletar.innerHTML = '&times;';

        btnDeletar.addEventListener('click', (event) => {
            event.stopPropagation();
            deletarChunk(chunk.id);
        });

        const content = document.createElement('div');
        content.className = 'chunk-content';
        content.textContent = chunk.content;

        // A distância só vem nos resultados de busca (não na listagem paginada)
        if (typeof chunk.distance === 'number') {
            const distancia = document.createElement('span');
            distancia.className = 'chunk-distance';
            distancia.title = 'Distância semântica: quanto menor, mais parecido com a busca';
            distancia.textContent = `distância: ${chunk.distance.toFixed(3)}`;
            // fica direto no card (posição absoluta), fora do fluxo do texto
            el.append(distancia);
        }

        header.append(btnDeletar);
        el.append(header, content);

        chunksGrid.appendChild(el);
    }

    function renderizarSetas(
        pagination,
        prevChunks,
        proxChunks
    ) {
        // Remove as setas antigas
        chunksBox.querySelectorAll('.pagination-btn').forEach(btn => btn.remove());

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
                prevChunks
            );

            chunksBox.prepend(btnAnterior);
        }


        // Botão próxima página
        if (pagination.has_next) {

            const btnProxima = document.createElement('button');
            btnProxima.className = 'pagination-btn pagination-next';
            btnProxima.type = 'button';
            btnProxima.innerHTML = '&#10095;';
            btnProxima.title = 'Próxima página';
            btnProxima.addEventListener('click', proxChunks);

            chunksBox.appendChild(btnProxima);
        }
    }

    function renderizarModal(criarChunk) {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.id = 'chunk-modal';

        const modalContent = document.createElement('div');
        modalContent.className = 'modal-content';

        const modalHeader = document.createElement('div');
        modalHeader.className = 'modal-header';

        const titulo = document.createElement('h2');
        titulo.textContent = 'Novo chunk';

        const fecharBtn = document.createElement('button');
        fecharBtn.id = 'fechar-modal-btn';
        fecharBtn.textContent = '×';

        const form = document.createElement('form');
        form.id = 'chunk-form';

        const contentLabel = document.createElement('label');
        contentLabel.htmlFor = 'chunk-content';
        contentLabel.textContent = 'Conteúdo';

        const contentInput = document.createElement('textarea');
        contentInput.id = 'chunk-content';
        contentInput.placeholder = 'Conteúdo do chunk...';
        contentInput.required = true;

        const submitBtn = document.createElement('button');
        submitBtn.type = 'submit';
        submitBtn.textContent = 'Criar chunk';

        modalHeader.append(
            titulo,
            fecharBtn
        );

        form.append(
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

            const content = contentInput.value;

            await criarChunk(content);
            remover();
        });
    }

    function renderizarChunks(
        chunks,
        deletarChunk,
        pagination,
        prevChunks,
        proxChunks
    ) {
        chunksGrid.innerHTML = '';

        if ((!chunks || chunks.length === 0) && pagination) {
            renderizarEstadoVazio();
            renderizarSetas(pagination, prevChunks, proxChunks);
            return;
        }

        chunks.forEach(chunk => {
            renderizarChunk(
                chunk,
                deletarChunk
            );
        });

        renderizarSetas(pagination, prevChunks, proxChunks);
    }

    function limparChunks() {
        chunksGrid.innerHTML = '';
        chunksBox.querySelectorAll('.pagination-btn').forEach(btn => btn.remove());
    }

    return {
        renderizarChunk,
        renderizarChunks,
        renderizarEstadoVazio,
        renderizarSetas,
        limparChunks,
        renderizarModal
    };
}