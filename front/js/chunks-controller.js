import {
    apiBuscarChunks,
    apiCriarChunk,
    apiDeletarChunk,
} from './api.js';

export function criarChunksController({ chunksView, textarea }) {

    function pegarPagina() {
        const page = localStorage.getItem('tutor-ia-page');
        if (page === null) {
            localStorage.setItem('tutor-ia-page', '1');
            return 1;
        }
        return Number(page);
    }

    async function buscarChunks() {
        const mensagem = textarea.value.trim();
        if (mensagem.length === 0) return;

        try {
            const chunks = await apiBuscarChunks(mensagem, 1, 6);
            chunksView.renderizarChunks(
                chunks,
                deletarChunk,
                chunks.pagination,
                prevChunks,
                proxChunks
            );
            return chunks;
        } catch (error) {
            console.error(error);
            return [];
        }
    }

    async function carregarChunks() {
        try {
            const page = pegarPagina();
            const chunks = await apiBuscarChunks('', page, 6);

            // voltar a pagina
            if (chunks.data.length === 0 && page > 1) {
                localStorage.setItem(
                    'tutor-ia-page',
                    String(page - 1)
                );
                return carregarChunks();
            }

            chunksView.renderizarChunks(
                chunks.data,
                deletarChunk,
                chunks.pagination,
                prevChunks,
                proxChunks
            );
            return chunks;
        } catch (error) {
            console.error(error);
            return [];
        }
    }


    async function prevChunks() {
        const pageAtual = pegarPagina();
        localStorage.setItem('tutor-ia-page', String(pageAtual - 1));
        await carregarChunks();
    }


    async function proxChunks() {
        const pageAtual = pegarPagina();
        localStorage.setItem('tutor-ia-page', String(pageAtual + 1));
        await carregarChunks();
    }


    async function criarChunk(content) {
        try {
            await apiCriarChunk(content);
            await carregarChunks();
        } catch (error) {
            console.error(error);
        }
    }

    async function novoChunk() {
        chunksView.renderizarModal(criarChunk);
    }

    async function deletarChunk(id) {
        try {
            await apiDeletarChunk(id);
            await carregarChunks();
        } catch (error) {
            console.error(error);
        }
    }

    async function inicializar() {
        await carregarChunks();
    }

    return {
        carregarChunks,
        novoChunk,
        deletarChunk,
        inicializar,
        buscarChunks
    };
}