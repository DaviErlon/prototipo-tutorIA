const CHAT_PATH = '/api/chat';
const CARDS_PATH = '/api/chat';

async function solicitar(url, options) {
    const response = await fetch(url, options);
    if (!response.ok) {
        throw new Error(`Erro na requisição: ${response.status}`);
    }
    return response;
}

export async function apiCriarChat() {
    const response = await solicitar(`${CHAT_PATH}/`, { method: 'POST' });
    return response.json();
}

export async function apiListarChats() {
    const response = await solicitar(`${CHAT_PATH}/`);
    return response.json();
}

export async function apiListarMensagens(id) {
    const response = await solicitar(`${CHAT_PATH}/${id}`);
    return response.json();
}

export async function apiDeletarChat(id) {
    const response = await solicitar(`${CHAT_PATH}/${id}`, { method: 'DELETE' });
    return response.json();
}

export async function apiEnviarPrompt(id, content) {
    const response = await solicitar(`${CHAT_PATH}/${id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content })
    });
    return response.json();
}

export async function apiGetCards(value, limit) {
    let url = `${CARDS_PATH}/?limit=${limit}`;

    if (value && value !== "") {
        url += `&key=${value}`;
    }
    const response = await solicitar(url);
    return response.json();
}

export async function apiCriarCard(card) {
    const response = await solicitar(`${CARDS_PATH}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ card })
    });
    return response.json();
}

export async function apiDeletarCard(id) {
    const response = await solicitar(`${CARDS_PATH}/${id}`, {method: 'DELETE'});
    return response.json();
}