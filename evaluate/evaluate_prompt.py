import json
from datetime import datetime
from pathlib import Path

from config import API_BASE_URL, QUESTIONS_FILE, RESULTS_DIR
from api_client import TutorIAClient

def _load_questions():
    questions = [
        line.strip()
        for line in Path(QUESTIONS_FILE)
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]

    if not questions:
        raise ValueError(
            f"Nenhuma pergunta encontrada em: {QUESTIONS_FILE}"
        )

    return questions


def _run_questions_in_chat(client, chat_id, questions, start_index):
    results = []

    for i, question in enumerate(questions, start_index):
        print(f"[{i}] {question[:60]}")

        try:
            answer = client.send_message(chat_id, question)

            results.append({
                "numero": i,
                "chat_id": chat_id,
                "pergunta": question,
                "resposta": answer["content"],
                "contexto": answer["context"],
                "status": "sucesso"
            })

        except Exception as error:
            print(f"Erro na pergunta {i}: {error}")

            results.append({
                "numero": i,
                "chat_id": chat_id,
                "pergunta": question,
                "resposta": None,
                "contexto": None,
                "status": "erro",
                "erro": str(error)
            })

    return results


def _save_results(name, questions, results, mode,
                  questions_per_chat=None):
    output_dir = Path(RESULTS_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not name:
        name = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_file = output_dir / f"{name}.json"

    successes = sum(
        result["status"] == "sucesso"
        for result in results
    )

    data = {
        "data_avaliacao": datetime.now().isoformat(),
        "modo": mode,
        "total_perguntas": len(questions),
        "respostas_capturadas": successes,
        "falhas": len(results) - successes,
        "resultados": results
    }

    if questions_per_chat is not None:
        data["perguntas_por_chat"] = questions_per_chat

    output_file.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"\nAvaliação concluída: {output_file}")
    print(f"Respostas capturadas: {successes}")
    print(f"Falhas: {len(results) - successes}")

    return output_file


def evaluate_single_chat(name=None):
    client = TutorIAClient(API_BASE_URL)
    questions = _load_questions()

    print(f"Total de perguntas: {len(questions)}")
    print("Modo: um único chat")

    chat_id = client.create_chat()

    results = _run_questions_in_chat(
        client=client,
        chat_id=chat_id,
        questions=questions,
        start_index=1
    )

    return _save_results(
        name=name,
        questions=questions,
        results=results,
        mode="single_chat"
    )


def evaluate_multiple_chats(questions_per_chat, name=None):
    if questions_per_chat < 1:
        raise ValueError(
            "O número de perguntas por chat deve ser maior que zero."
        )

    client = TutorIAClient(API_BASE_URL)
    questions = _load_questions()
    results = []

    print(f"Total de perguntas: {len(questions)}")
    print(f"Perguntas por chat: {questions_per_chat}")

    for start in range(0, len(questions), questions_per_chat):
        batch = questions[start:start + questions_per_chat]
        chat_number = (start // questions_per_chat) + 1

        print(f"\n--- Chat {chat_number} ---")

        chat_id = client.create_chat()

        try:
            batch_results = _run_questions_in_chat(
                client=client,
                chat_id=chat_id,
                questions=batch,
                start_index=start + 1
            )

            results.extend(batch_results)

        finally:
            try:
                client.delete_chat(chat_id)
                print(f"Chat {chat_id} excluído.")
            except Exception as error:
                print(
                    f"Erro ao excluir o chat {chat_id}: {error}"
                )

    return _save_results(
        name=name,
        questions=questions,
        results=results,
        mode="multiple_chats",
        questions_per_chat=questions_per_chat
    )
