from __future__ import annotations

from fastapi import UploadFile
import pdfplumber


MAX_CHARS_DEFAULT = 20_000


def _clip(text: str, max_chars: int) -> str:
    """Evita mandar texto enorme pra IA e estourar custo/latência."""
    text = (text or "").strip()
    return text[:max_chars]


async def extract_email_text(
    upload: UploadFile | None,
    pasted_text: str | None,
    max_chars: int = MAX_CHARS_DEFAULT,
) -> str:
    """
    Prioridade:
      1) Se colou texto -> usa texto
      2) Senão, se enviou arquivo -> extrai do arquivo
    """
    if pasted_text and pasted_text.strip():
        return _clip(pasted_text, max_chars)

    if upload is None:
        return ""

    filename = (upload.filename or "").lower()

    if filename.endswith(".txt"):
        raw = await upload.read()
        # tenta utf-8, fallback latin-1 (comum em arquivos antigos)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("latin-1", errors="replace")
        return _clip(text, max_chars)

    if filename.endswith(".pdf"):
        raw = await upload.read()
        # pdfplumber trabalha com caminho/arquivo-like; aqui usamos bytes
        # abordagem simples: abrir via BytesIO
        from io import BytesIO

        text_parts: list[str] = []
        with pdfplumber.open(BytesIO(raw)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                if page_text.strip():
                    text_parts.append(page_text)

        return _clip("\n".join(text_parts), max_chars)

    # extensão não suportada
    return ""
