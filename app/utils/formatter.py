from typing import Any, Dict, List


def format_analysis_result(data: Dict[str, Any]) -> str:
    """
    AI dan kelgan tahlil natijasini Telegram foydalanuvchisi uchun
    juda aniq, tushunarli va tekshirish holati bilan chiroyli formatda shakllantiradi.
    """
    questions: List[Dict[str, Any]] = data.get("questions", [])
    if not questions:
        return "⚠️ Savollar aniqlanmadi yoki tahlil qilib bo'lmadi. Iltimos, savolni to'liqroq yozib qayta yuboring."

    output_parts = []
    test_summary_items = []

    for idx, q in enumerate(questions, start=1):
        num = q.get("number", idx)
        q_text = (q.get("question_text") or "").strip()
        correct_ans = (q.get("correct_answer") or "").strip()
        explanation = (q.get("explanation") or "").strip()
        is_unclear = q.get("is_unclear", False)
        unclear_reason = q.get("unclear_reason") or ""
        selected_option = q.get("selected_option")
        is_multiple_choice = q.get("is_multiple_choice", False)

        # Foydalanuvchi javobini tekshirish maydonlari
        has_user_answer = q.get("has_user_answer", False)
        user_answer = q.get("user_answer")
        is_user_correct = q.get("is_user_correct")

        block = []

        # Savol matni
        if len(questions) > 1:
            block.append(f"📚 <b>{num}-Savol:</b> {q_text}")
        else:
            block.append(f"📚 <b>Savol:</b> {q_text}")

        # Savol noaniq bo'lsa
        if is_unclear:
            block.append("⚠️ <b>Holat:</b> Savol noaniq yoki to‘liq berilmagan!")
            if unclear_reason:
                block.append(f"📝 <b>Sababi:</b> {unclear_reason}")
            else:
                block.append("📝 <b>Sababi:</b> Savolda yetarli ma'lumot yo'q yoki shart noaniq tuzilgan.")
        else:
            # Agar foydalanuvchi o'z javobini ham birga yuborgan bo'lsa (TEKSHIRISH)
            if has_user_answer and user_answer:
                if is_user_correct is True:
                    block.append(f"🎯 <b>Sizning javobingiz:</b> {user_answer} ➡️ <b>TO‘G‘RI!</b> ✅")
                elif is_user_correct is False:
                    block.append(f"🎯 <b>Sizning javobingiz:</b> {user_answer} ➡️ <b>NOTO‘G‘RI!</b> ❌")
                    block.append(f"✅ <b>Asl to‘g‘ri javob:</b> {correct_ans}")
                else:
                    block.append(f"🎯 <b>Sizning javobingiz:</b> {user_answer}")
                    block.append(f"✅ <b>To‘g‘ri javob:</b> {correct_ans}")
            else:
                block.append(f"✅ <b>To‘g‘ri javob:</b> {correct_ans}")

            # Aniq va tushunarli izoh
            if explanation:
                block.append(f"📝 <b>Aniq tushuntirish:</b>\n{explanation}")

        output_parts.append("\n".join(block))

        # Test xulosasi uchun
        if (is_multiple_choice or selected_option) and not is_unclear and selected_option:
            test_summary_items.append(f"{num}-savol — {selected_option.upper()} ✅")

    result_text = "\n\n────────────────────\n\n".join(output_parts)

    # Test savollari xulosasi
    if test_summary_items:
        summary_header = "\n\n📌 <b>Test javoblari:</b>\n"
        summary_body = "  ".join(test_summary_items)
        result_text += summary_header + summary_body

    return result_text
