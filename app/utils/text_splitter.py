from typing import List


def split_message(text: str, max_chars: int = 4000) -> List[str]:
    """
    Telegramning xabar hajmi chegarasi (4096 belgi) dan oshib ketmasligi uchun
    matnni mantiqiy bloklar (qatorlar yoki ajratkichlar) bo'yicha bo'laklarga ajratadi.
    """
    if len(text) <= max_chars:
        return [text]

    chunks = []
    lines = text.split("\n")
    current_chunk = []
    current_length = 0

    for line in lines:
        line_len = len(line) + 1  # \n hisobga olingan

        if current_length + line_len > max_chars:
            if current_chunk:
                chunks.append("\n".join(current_chunk).strip())
                current_chunk = []
                current_length = 0

            # Agar alohida bitta qatorning o'zi ham max_chars dan katta bo'lsa
            if line_len > max_chars:
                while len(line) > max_chars:
                    chunks.append(line[:max_chars])
                    line = line[max_chars:]
                if line:
                    current_chunk.append(line)
                    current_length = len(line)
            else:
                current_chunk.append(line)
                current_length = line_len
        else:
            current_chunk.append(line)
            current_length += line_len

    if current_chunk:
        chunks.append("\n".join(current_chunk).strip())

    return chunks
