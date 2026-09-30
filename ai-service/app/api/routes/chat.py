 
# ============================================================
# BLOCK 1 — IMPORTS
# ============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import Memory

from app.models.request import ChatRequest
from app.models.response import ChatResponse

from app.services.query_router import classify_query

from app.services.ai_service import generate_response

from app.services.page_detector import detect_page

from app.services.navigation_search import search_navigation

from app.services.navigation_intent import is_navigation_request

from app.services.account_service import (
    get_account_details
)

from app.services.balance_service import (
    get_current_balance
)

from app.services.transaction_service import (
    get_recent_transactions
)

from app.services.realtime_intent_service import (
    detect_realtime_intent,
    detect_interest_rate_type
)

from app.services.interest_rate_service import (
    get_fd_interest_rate,
    get_loan_interest_rate
)

from app.services.card_service import (
    get_card_status
)
from app.services.loan_service import (
    get_loan_status
)
from app.services.card_details_service import (
    get_card_details
)
from app.services.account_status_service import (
    get_account_status
)
from app.services.memory_service import (
    get_or_create_conversation,
    save_message,
    save_memory,
    get_history,
    replace_memory
)

from app.services.memory_extractor import (
    extract_memories
)

from app.services.embedding_service import (
    get_embedding
)

from app.services.chroma_service import (
    add_memory_to_chroma
)

from app.services.rag_service import (
    build_memory_context
)

from app.services.memory_lifecycle_service import (
    find_existing_memory
)

from app.services.memory_conflict_service import (
    classify_memory_conflict
)

from app.services.task_service import (
    get_active_task,
    has_active_task,
    start_fd_task,
    process_fd_task,
    start_emi_task,
    process_emi_task,
    clear_task
)


router = APIRouter()


# ============================================================
# BLOCK 2 — DATABASE DEPENDENCY
# ============================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# ============================================================
# BLOCK 3 — CHECK IF MESSAGE IS A PERSONAL MEMORY STATEMENT
# ============================================================

def is_memory_statement(message: str) -> bool:

    text = message.lower().strip()

    memory_patterns = [

        # Learning / skills
        "i am learning",
        "i'm learning",
        "i learn",
        "i know",
        "i'm good at",
        "i am good at",
        "i can",
        "i have learned",

        # Goals
        "my goal is",
        "my goal",
        "i want to become",
        "i want to learn",
        "i want to",
        "i plan to",
        "i'm planning to",
        "i am planning to",

        # Profession / work
        "i work as",
        "i work at",
        "i am working as",
        "i'm working as",
        "my profession is",
        "i am a",
        "i'm a",

        # Personal information
        "my name is",
        "i live in",
        "i am from",
        "i'm from",
        "my email is",
        "my phone is",

        # Preferences
        "i like",
        "i love",
        "i prefer",
        "i don't like",
        "i dislike",

        # Current state
        "i have",
        "i own",
        "i use",

        # Memory changes
        "no longer learning",
        "not learning",
        "don't learn",
        "do not learn",
        "no longer",
        "forget that",
        "remember that",

        # Future / recent
        "in the future",
        "recently i",
        "currently i"
    ]

    for pattern in memory_patterns:

        if pattern in text:

            return True

    return False


# ============================================================
# BLOCK 4 — CHAT ENDPOINT
# ============================================================

@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    # ========================================================
    # 4.1 — GET OR CREATE CONVERSATION
    # ========================================================

    conversation = get_or_create_conversation(
        db,
        request.user_id
    )

    # ========================================================
    # 4.2 — GET PREVIOUS CONVERSATION HISTORY
    # ========================================================

    history = get_history(
        db,
        conversation.id
    )

    # ========================================================
    # 4.3 — SAVE USER MESSAGE
    # ========================================================

    save_message(
        db,
        conversation.id,
        "user",
        request.message
    )
    # ========================================================
# BLOCK 4.4 — DATA VS NAVIGATION DETECTION
# ========================================================

    is_navigation = is_navigation_request(
    request.message
)

    print(
    "\n========== NAVIGATION INTENT =========="
)

    print(
    f"Navigation request: {is_navigation}"
)


# Default value
    navigation = None


# ========================================================
# ONLY CHECK PAGE WHEN IT IS A NAVIGATION REQUEST
# ========================================================

    if is_navigation:

    # ----------------------------------------------------
    # First: exact page detection
    # ----------------------------------------------------

     navigation = detect_page(
        request.message
    )

    # ----------------------------------------------------
    # Second: natural language navigation search
    # ----------------------------------------------------

    if navigation is None:

        navigation = search_navigation(
            request.message
        )

    # ----------------------------------------------------
    # Navigation found
    # ----------------------------------------------------

    if navigation:

        print(
            "\n========== PAGE NAVIGATION DETECTED =========="
        )

        print(
            f"Page: {navigation['page']}"
        )

        print(
            f"Route: {navigation['route']}"
        )

        navigation_response = (
            f"Opening "
            f"{navigation['page'].replace('_', ' ')}."
        )

        save_message(
            db,
            conversation.id,
            "assistant",
            navigation_response
        )

        return ChatResponse(
            response=navigation_response,
            action=navigation["route"]
        )
    


    # ========================================================
    # BLOCK 5 — MEMORY PROCESSING
    # ========================================================

    try:

        # ====================================================
        # 5.1 — CHECK ACTIVE TASK
        # ====================================================

        active_task = get_active_task(
            request.user_id
        )

        if active_task:

            print(
                "\n========== ACTIVE TASK =========="
            )

            print(
                active_task
            )

            should_process_memory = False

        else:

            should_process_memory = is_memory_statement(
                request.message
            )


        # ====================================================
        # 5.2 — NORMAL QUESTION
        # ====================================================

        if not should_process_memory:

            print(
                "\n========== MEMORY PROCESSING SKIPPED ==========\n"
            )

            print(
                "Normal question detected."
            )


        # ====================================================
        # 5.3 — MEMORY STATEMENT
        # ====================================================

        else:

            print(
                "\n========== MEMORY PROCESSING ==========\n"
            )

            memory_result = extract_memories(
                request.message
            )

            print(
                "\n========== MEMORY EXTRACTION ==========\n"
            )

            print(
                memory_result
            )


            # ==================================================
            # 5.4 — CHECK SHOULD REMEMBER
            # ==================================================

            if memory_result.get("should_remember"):

                memories = memory_result.get(
                    "memories",
                    []
                )

                message_lower = (
                    request.message.lower()
                )


                # ==================================================
                # LEARNING REPLACEMENT DETECTION
                # ==================================================

                replacement_detected = False

                old_subject = None
                new_subject = None


                # --------------------------------------------------
                # CASE 1 — no longer learning
                # --------------------------------------------------

                if "no longer learning" in message_lower:

                    old_part = message_lower.split(
                        "no longer learning",
                        1
                    )[1]

                    old_subject = (
                        old_part
                        .split(".", 1)[0]
                        .strip()
                    )

                    replacement_detected = True


                # --------------------------------------------------
                # CASE 2 — not learning
                # --------------------------------------------------

                elif "not learning" in message_lower:

                    old_part = message_lower.split(
                        "not learning",
                        1
                    )[1]

                    old_subject = (
                        old_part
                        .split(".", 1)[0]
                        .strip()
                    )

                    replacement_detected = True


                # --------------------------------------------------
                # CASE 3 — don't learn
                # --------------------------------------------------

                elif "don't learn" in message_lower:

                    old_part = message_lower.split(
                        "don't learn",
                        1
                    )[1]

                    old_subject = (
                        old_part
                        .split(".", 1)[0]
                        .strip()
                    )

                    replacement_detected = True


                # --------------------------------------------------
                # CASE 4 — do not learn
                # --------------------------------------------------

                elif "do not learn" in message_lower:

                    old_part = message_lower.split(
                        "do not learn",
                        1
                    )[1]

                    old_subject = (
                        old_part
                        .split(".", 1)[0]
                        .strip()
                    )

                    replacement_detected = True


                # ==================================================
                # FIND NEW LEARNING SUBJECT
                # ==================================================

                if replacement_detected:

                    new_markers = [
                        "now learning",
                        "recently learning",
                        "currently learning",
                        "learning"
                    ]

                    for marker in new_markers:

                        if marker in message_lower:

                            new_part = message_lower.split(
                                marker,
                                1
                            )[1]

                            new_subject = (
                                new_part
                                .split(".", 1)[0]
                                .strip()
                            )

                            break


                # ==================================================
                # 5.5 — LEARNING REPLACEMENT
                # ==================================================

                if (
                    replacement_detected
                    and old_subject
                    and new_subject
                ):

                    print(
                        "\n========== LEARNING REPLACEMENT ==========\n"
                    )

                    print(
                        f"Old subject: {old_subject}"
                    )

                    print(
                        f"New subject: {new_subject}"
                    )


                    old_memory = (
                        db.query(Memory)
                        .filter(
                            Memory.user_id ==
                            request.user_id,

                            Memory.memory_type ==
                            "SKILL",

                            Memory.active == True,

                            Memory.content.ilike(
                                f"%{old_subject}%"
                            )
                        )
                        .order_by(
                            Memory.created_at.desc()
                        )
                        .first()
                    )


                    # ==============================================
                    # OLD MEMORY FOUND
                    # ==============================================

                    if old_memory:

                        print(
                            f"Old memory found: "
                            f"{old_memory.id}"
                        )

                        replaced_memory = replace_memory(
                            db=db,
                            user_id=request.user_id,
                            old_memory_id=old_memory.id,
                            new_content=(
                                f"User is learning "
                                f"{new_subject}"
                            ),
                            memory_type="SKILL",
                            importance=8
                        )

                        if replaced_memory:

                            embedding = get_embedding(
                                replaced_memory.content
                            )

                            add_memory_to_chroma(
                                memory_id=replaced_memory.id,
                                user_id=replaced_memory.user_id,
                                content=replaced_memory.content,
                                embedding=embedding,
                                memory_type=replaced_memory.memory_type,
                                importance=replaced_memory.importance,
                                created_at=replaced_memory.created_at,
                                active=replaced_memory.active
                            )

                            print(
                                "Old memory deactivated."
                            )

                            print(
                                f"New memory created: "
                                f"{replaced_memory.id}"
                            )

                            print(
                                "Learning memory replaced successfully."
                            )


                    # ==============================================
                    # OLD MEMORY NOT FOUND
                    # ==============================================

                    else:

                        print(
                            "Old active learning memory "
                            "was not found."
                        )

                        saved_memory = save_memory(
                            db=db,
                            user_id=request.user_id,
                            content=(
                                f"User is learning "
                                f"{new_subject}"
                            ),
                            memory_type="SKILL",
                            importance=8
                        )

                        embedding = get_embedding(
                            saved_memory.content
                        )

                        add_memory_to_chroma(
                            memory_id=saved_memory.id,
                            user_id=saved_memory.user_id,
                            content=saved_memory.content,
                            embedding=embedding,
                            memory_type=saved_memory.memory_type,
                            importance=saved_memory.importance,
                            created_at=saved_memory.created_at,
                            active=saved_memory.active
                        )

                        print(
                            "New learning memory created."
                        )

                    print(
                        "\n==========================================\n"
                    )


                # ==================================================
                # 5.6 — NORMAL MEMORY PROCESSING
                # ==================================================

                else:

                    for memory in memories:

                        new_content = memory["content"]

                        memory_type = memory.get(
                            "memory_type",
                            "GENERAL"
                        )

                        importance = memory.get(
                            "importance",
                            5
                        )


                        # ==========================================
                        # FIND EXISTING MEMORY
                        # ==========================================

                        existing = None


                        # ==========================================
                        # GOAL / PROFESSION CHECK
                        # ==========================================

                        if memory_type in [
                            "GOAL",
                            "PROFESSION"
                        ]:

                            existing_memory_for_type = (
                                db.query(Memory)
                                .filter(
                                    Memory.user_id ==
                                    request.user_id,

                                    Memory.memory_type ==
                                    memory_type,

                                    Memory.active == True
                                )
                                .order_by(
                                    Memory.created_at.desc()
                                )
                                .first()
                            )

                            if existing_memory_for_type:

                                existing = {
                                    "memory_id":
                                    existing_memory_for_type.id,

                                    "distance": 0
                                }


                        # ==========================================
                        # NORMAL SEMANTIC SEARCH
                        # ==========================================

                        if not existing:

                            existing = find_existing_memory(
                                content=new_content,
                                user_id=request.user_id
                            )


                        # ==========================================
                        # NO EXISTING MEMORY
                        # ==========================================

                        if not existing:

                            print(
                                "\nMemory decision: NEW"
                            )

                            saved_memory = save_memory(
                                db=db,
                                user_id=request.user_id,
                                content=new_content,
                                memory_type=memory_type,
                                importance=importance
                            )

                            embedding = get_embedding(
                                saved_memory.content
                            )

                            add_memory_to_chroma(
                                memory_id=saved_memory.id,
                                user_id=saved_memory.user_id,
                                content=saved_memory.content,
                                embedding=embedding,
                                memory_type=saved_memory.memory_type,
                                importance=saved_memory.importance,
                                created_at=saved_memory.created_at,
                                active=saved_memory.active
                            )

                            print(
                                "New memory saved successfully."
                            )

                            continue


                        # ==========================================
                        # EXISTING MEMORY FOUND
                        # ==========================================

                        existing_memory_id = existing[
                            "memory_id"
                        ]

                        print(
                            f"\nSimilar memory found: "
                            f"{existing_memory_id}"
                        )


                        existing_memory = (
                            db.query(Memory)
                            .filter(
                                Memory.id ==
                                existing_memory_id,

                                Memory.user_id ==
                                request.user_id,

                                Memory.active == True
                            )
                            .first()
                        )


                        if not existing_memory:

                            print(
                                "Existing active memory "
                                "not found in MySQL."
                            )

                            continue


                        # ==========================================
                        # MEMORY CONFLICT
                        # ==========================================

                        decision = classify_memory_conflict(
                            existing_memory=existing_memory.content,
                            new_memory=new_content
                        )

                        print(
                            f"Memory decision: "
                            f"{decision['decision']}"
                        )

                        print(
                            f"Reason: "
                            f"{decision['reason']}"
                        )


                        # ==========================================
                        # DUPLICATE
                        # ==========================================

                        if decision["decision"] == "DUPLICATE":

                            print(
                                "Duplicate memory ignored."
                            )

                            continue


                        # ==========================================
                        # UPDATE
                        # ==========================================

                        if decision["decision"] == "UPDATE":

                            replaced_memory = replace_memory(
                                db=db,
                                user_id=request.user_id,
                                old_memory_id=existing_memory_id,
                                new_content=new_content,
                                memory_type=memory_type,
                                importance=importance
                            )

                            if replaced_memory:

                                embedding = get_embedding(
                                    replaced_memory.content
                                )

                                add_memory_to_chroma(
                                    memory_id=replaced_memory.id,
                                    user_id=replaced_memory.user_id,
                                    content=replaced_memory.content,
                                    embedding=embedding,
                                    memory_type=replaced_memory.memory_type,
                                    importance=replaced_memory.importance,
                                    created_at=replaced_memory.created_at,
                                    active=replaced_memory.active
                                )

                                print(
                                    "Old memory deactivated."
                                )

                                print(
                                    f"New memory created: "
                                    f"{replaced_memory.id}"
                                )

                                print(
                                    "Memory replaced successfully."
                                )

                            continue


                        # ==========================================
                        # NEW SIMILAR MEMORY
                        # ==========================================

                        if decision["decision"] == "NEW":

                            print(
                                "Similar but different memory. "
                                "Saving as new."
                            )

                            saved_memory = save_memory(
                                db=db,
                                user_id=request.user_id,
                                content=new_content,
                                memory_type=memory_type,
                                importance=importance
                            )

                            embedding = get_embedding(
                                saved_memory.content
                            )

                            add_memory_to_chroma(
                                memory_id=saved_memory.id,
                                user_id=saved_memory.user_id,
                                content=saved_memory.content,
                                embedding=embedding,
                                memory_type=saved_memory.memory_type,
                                importance=saved_memory.importance,
                                created_at=saved_memory.created_at,
                                active=saved_memory.active
                            )

                            print(
                                "New memory saved successfully."
                            )


    except Exception as e:

        print(
            f"\nMemory processing failed: {e}"
        )


    # ========================================================
     # BLOCK 6 — MAIN QUERY ROUTER
    # ========================================================

    query_type = classify_query(
    request.message
  )

    print(
    "\n========== MAIN QUERY ROUTER =========="
    )

    print(
    f"Query type: {query_type}"
)

    print(
        f"User message: {request.message}"
)


    # ========================================================
    # BLOCK 7 — ACTIVE TASK PROCESSING
    # ========================================================

    if has_active_task(request.user_id):

        print(
            "\n========== ACTIVE TASK PROCESSING =========="
        )

        active_task = get_active_task(
            request.user_id
        )

        print(
            f"Active task: {active_task}"
        )

        task_name = active_task.get("task")


        # ====================================================
        # 7.1 — FD TASK
        # ====================================================

        if task_name == "FD_CALCULATOR":

            handled, task_response = process_fd_task(
                user_id=request.user_id,
                message=request.message
            )

            if handled:

                save_message(
                    db,
                    conversation.id,
                    "assistant",
                    task_response
                )

                active_task = get_active_task(
                    request.user_id
                )

                if active_task:

                    task_mode = active_task.get(
                        "mode"
                    )

                    message_lower = (
                        request.message
                        .lower()
                        .strip()
                    )

                    manual_words = [
                        "manual",
                        "manually",
                        "calculator",
                        "use calculator",
                        "open calculator",
                        "open tool"
                    ]

                    is_manual_selection = any(
                        word in message_lower
                        for word in manual_words
                    )

                    if (
                        task_mode == "manual"
                        and is_manual_selection
                    ):

                        return ChatResponse(
                            response=task_response,
                            action="OPEN_FD_CALCULATOR"
                        )

                return ChatResponse(
                    response=task_response
                )


        # ====================================================
        # 7.2 — EMI TASK
        # ====================================================

        elif task_name == "EMI_CALCULATOR":

            handled, task_response = process_emi_task(
                user_id=request.user_id,
                message=request.message
            )

            if handled:

                active_task = get_active_task(
                    request.user_id
                )

                if active_task:

                    task_mode = active_task.get(
                        "mode"
                    )

                    message_lower = (
                        request.message
                        .lower()
                        .strip()
                    )

                    manual_words = [
                        "manual",
                        "manually",
                        "open emi",
                        "open emi calculator",
                        "calculator",
                        "use calculator",
                        "open calculator",
                        "open tool"
                    ]

                    is_manual_selection = any(
                        word in message_lower
                        for word in manual_words
                    )

                    if (
                        task_mode == "manual"
                        and is_manual_selection
                    ):

                        print(
                            "\n========== OPENING EMI CALCULATOR =========="
                        )

                        clear_task(
                            request.user_id
                        )

                        save_message(
                            db,
                            conversation.id,
                            "assistant",
                            task_response
                        )

                        return ChatResponse(
                            response=task_response,
                            action="OPEN_EMI_CALCULATOR"
                        )

                save_message(
                    db,
                    conversation.id,
                    "assistant",
                    task_response
                )

                return ChatResponse(
                    response=task_response
                )


    # ========================================================
    # BLOCK 8 — QUERY TYPE PROCESSING
    # ========================================================

    memory_context = ""


    # ========================================================
    # 8.1 — RETRIEVAL
    # ========================================================

    if query_type == "RETRIEVAL":

        print(
            "\n========== RETRIEVAL ROUTE =========="
        )

        memory_context = build_memory_context(
            question=request.message,
            user_id=request.user_id,
            n_results=5
        )


    # ========================================================
    # 8.2 — REALTIME
    # ========================================================

    elif query_type == "REALTIME":

        print(
            "\n========== REALTIME QUERY =========="
        )

        realtime_intent = detect_realtime_intent(
            request.message
        )

        print(
            f"Realtime intent: {realtime_intent}"
        )


        # ====================================================
        # BALANCE
        # ====================================================

        if realtime_intent == "BALANCE":

            print(
                "\n========== BALANCE QUERY =========="
            )

            balance_data = get_current_balance(
                db=db,
                user_id=request.user_id
            )

            if balance_data is None:

                response_text = (
                    "I could not find an active bank account "
                    "for your user."
                )

            else:

                response_text = (
                    f"Your current "
                    f"{balance_data['account_type'].lower()} "
                    f"account balance is "
                    f"₹{balance_data['balance']:,.2f}."
                )

            save_message(
                db,
                conversation.id,
                "assistant",
                response_text
            )

            return ChatResponse(
                response=response_text
            )


        # ====================================================
        # TRANSACTIONS
        # ====================================================

        elif realtime_intent == "TRANSACTIONS":

            print(
                "\n========== TRANSACTIONS QUERY =========="
            )

            transactions = get_recent_transactions(
                db=db,
                user_id=request.user_id,
                limit=5
            )

            if not transactions:

                response_text = (
                    "I could not find any recent "
                    "transactions for your account."
                )

            else:

                lines = [
                    "Here are your recent transactions:"
                ]

                for transaction in transactions:

                    transaction_type = (
                        transaction["transaction_type"]
                    )

                    amount = transaction["amount"]

                    description = (
                        transaction["description"]
                        or "No description"
                    )

                    transaction_date = (
                        transaction["transaction_date"]
                    )

                    if transaction_date:

                        date_text = (
                            transaction_date.strftime(
                                "%d-%m-%Y %H:%M"
                            )
                        )

                    else:

                        date_text = "Unknown date"

                    lines.append(
                        f"{transaction_type}: "
                        f"₹{amount:,.2f} - "
                        f"{description} "
                        f"({date_text})"
                    )

                response_text = "\n".join(
                    lines
                )

            save_message(
                db,
                conversation.id,
                "assistant",
                response_text
            )

            return ChatResponse(
                response=response_text
            )

        elif realtime_intent == "INTEREST_RATE":

            rate_type = detect_interest_rate_type(
                request.message
            )

            if rate_type == "FD":

                fd_data = get_fd_interest_rate(
                    db,
                    request.user_id
                )

                if fd_data is None:

                    response_text = (
                        "You don't have an active fixed deposit, "
                        "so there is no FD interest rate available."
                    )

                else:

                    response_text = (
                        f"Your fixed deposit interest rate is "
                        f"{fd_data['interest_rate']:.2f}% "
                        f"for a tenure of "
                        f"{fd_data['tenure_months']} months."
                    )

            elif rate_type == "LOAN":

                loan_data = get_loan_interest_rate(
                    db,
                    request.user_id
                )

                if loan_data is None:

                    response_text = (
                        "You don't have an active loan, "
                        "so there is no loan interest rate available."
                    )

                else:

                    response_text = (
                        f"Your {loan_data['loan_type'].lower()} loan "
                        f"interest rate is "
                        f"{loan_data['interest_rate']:.2f}% "
                        f"for a tenure of "
                        f"{loan_data['tenure_months']} months."
                    )

            else:

                response_text = (
                    "Please specify whether you want "
                    "your FD or loan interest rate."
                )
            save_message(
                db,
                conversation.id,
                "assistant",
                response_text
            )

            return ChatResponse(
                response=response_text
            )

        # ====================================================
                # CARD STATUS
        # ====================================================

        elif realtime_intent == "CARD_STATUS":

            print(
                "\n========== CARD STATUS QUERY =========="
            )

            card_data = get_card_status(
                db=db,
                user_id=request.user_id
            )

            if card_data is None:

                response_text = (
                    "I could not find a card "
                    "for your user."
                )

            else:

                response_text = (
                    f"Your {card_data['card_type'].lower()} "
                    f"card ending in "
                    f"{card_data['card_number'][-4:]} "
                    f"is currently "
                    f"{card_data['status'].lower()}."
                )

            save_message(
                db,
                conversation.id,
                "assistant",
                response_text
            )

            return ChatResponse(
                response=response_text
            )

        elif realtime_intent == "CARD_DETAILS":

            print(
                "\n========== CARD DETAILS QUERY =========="
            )

            card_data = get_card_details(
                db=db,
                user_id=request.user_id
            )

            if card_data is None:

                response_text = (
                    "I could not find a card "
                    "for your user."
                )

            else:

                response_text = (
                    f"You have a "
                    f"{card_data['card_type'].lower()} card "
                    f"ending in "
                    f"{card_data['card_number'][-4:]}. "
                    f"The card is currently "
                    f"{card_data['status'].lower()}."
                )

            save_message(
                db,
                conversation.id,
                "assistant",
                response_text
            )

            return ChatResponse(
                response=response_text
            )


        elif realtime_intent == "LOAN_STATUS":

            print(
                "\n========== LOAN STATUS QUERY =========="
            )

            loan_data = get_loan_status(
                db=db,
                user_id=request.user_id
            )

            if loan_data is None:

                response_text = (
                    "I could not find an active loan "
                    "for your user."
                )

            else:

                response_text = (
                    f"Your {loan_data['loan_type'].lower()} loan "
                    f"is currently "
                    f"{loan_data['status'].lower()}. "
                    f"Your outstanding loan amount is "
                    f"₹{loan_data['outstanding_amount']:,.2f}."
                )

            save_message(
                db,
                conversation.id,
                "assistant",
                response_text
            )

            return ChatResponse(
                response=response_text
            )

      
        # ====================================================
        # ACCOUNT DETAILS
        # ====================================================

        elif realtime_intent == "ACCOUNT_DETAILS":

            print(
                "\n========== ACCOUNT DETAILS QUERY =========="
            )

            account_data = get_account_details(
                db=db,
                user_id=request.user_id
            )

            if account_data is None:

                response_text = (
                    "I could not find an account "
                    "for your user."
                )

            else:

                response_text = (
                    "Here are your account details:\n"
                    f"Account Number: "
                    f"{account_data['account_number']}\n"
                    f"Account Type: "
                    f"{account_data['account_type']}\n"
                    f"Branch: "
                    f"{account_data['branch_name']}\n"
                    f"IFSC Code: "
                    f"{account_data['ifsc_code']}"
                )

            save_message(
                db,
                conversation.id,
                "assistant",
                response_text
            )

            return ChatResponse(
                response=response_text
            )

        elif realtime_intent == "ACCOUNT_STATUS":

            print(
                "\n========== ACCOUNT STATUS QUERY =========="
            )

            account_data = get_account_status(
                db=db,
                user_id=request.user_id
            )

            if account_data is None:

                response_text = (
                    "I could not find a bank account "
                    "for your user."
                )

            else:

                response_text = (
                    f"Your "
                    f"{account_data['account_type'].lower()} "
                    f"account ending in "
                    f"{account_data['account_number'][-4:]} "
                    f"is currently "
                    f"{account_data['status'].lower()}."
                )

            save_message(
                db,
                conversation.id,
                "assistant",
                response_text
            )

            return ChatResponse(
                response=response_text
            )


        # ====================================================
        # UNKNOWN REALTIME QUERY
        # ====================================================

        else:

            response_text = (
                "I can currently check your account "
                "balance, recent transactions, and "
                "account details."
            )

            save_message(
                db,
                conversation.id,
                "assistant",
                response_text
            )

            return ChatResponse(
                response=response_text
            )


    # ========================================================
    # 8.3 — TASK
    # ========================================================

    elif query_type == "TASK":

        print(
            "\n========== TASK ROUTE =========="
        )

        message_lower = (
            request.message
            .lower()
            .strip()
        )


        # ====================================================
        # EMI
        # ====================================================

        emi_words = [
            "emi",
            "emi calculator",
            "calculate emi",
            "calculate loan emi",
            "loan emi",
            "calculate my emi",
            "calculate my loan emi"
        ]

        is_emi_task = any(
            word in message_lower
            for word in emi_words
        )

        if is_emi_task:

            print(
                "\n========== STARTING EMI TASK =========="
            )

            start_emi_task(
                request.user_id
            )

            handled, task_response = process_emi_task(
                user_id=request.user_id,
                message=request.message
            )

            if handled:

                active_task = get_active_task(
                    request.user_id
                )

                if active_task:

                    task_mode = active_task.get(
                        "mode"
                    )

                    manual_words = [
                        "manual",
                        "manually",
                        "open emi",
                        "open emi calculator",
                        "calculator",
                        "use calculator",
                        "open calculator",
                        "open tool"
                    ]

                    is_manual_selection = any(
                        word in message_lower
                        for word in manual_words
                    )

                    if (
                        task_mode == "manual"
                        and is_manual_selection
                    ):

                        print(
                            "\n========== OPENING EMI CALCULATOR =========="
                        )

                        clear_task(
                            request.user_id
                        )

                        save_message(
                            db,
                            conversation.id,
                            "assistant",
                            task_response
                        )

                        return ChatResponse(
                            response=task_response,
                            action="OPEN_EMI_CALCULATOR"
                        )

                save_message(
                    db,
                    conversation.id,
                    "assistant",
                    task_response
                )

                return ChatResponse(
                    response=task_response
                )


        # ====================================================
        # FD
        # ====================================================

        fd_words = [
            "fd",
            "fixed deposit",
            "fixed-deposit"
        ]

        is_fd_task = any(
            word in message_lower
            for word in fd_words
        )

        if is_fd_task:

            print(
                "\n========== STARTING FD TASK =========="
            )

            start_fd_task(
                request.user_id
            )

            response = (
                "Sure. Would you like to calculate "
                "it manually using the FD calculator, "
                "or should I calculate it for you here?"
            )

            save_message(
                db,
                conversation.id,
                "assistant",
                response
            )

            return ChatResponse(
                response=response
            )


        # ====================================================
        # FUTURE BANKING TASKS
        # ====================================================

        memory_context = (
            "BANKING TASK:\n"
            "Banking task tools are not connected yet."
        )


    # ========================================================
    # 8.4 — GENERAL
    # ========================================================

    else:

        print(
            "\n========== GENERAL ROUTE =========="
        )

        memory_context = ""


    # ========================================================
    # BLOCK 9 — GENERATE AI RESPONSE
    # ========================================================

    response = generate_response(
        message=request.message,
        history=history,
        memory_context=memory_context,
        query_type=query_type
    )


    # ========================================================
    # SAVE AI RESPONSE
    # ========================================================

    save_message(
        db,
        conversation.id,
        "assistant",
        response
    )


    # ========================================================
    # RETURN RESPONSE
    # ========================================================

    return ChatResponse(
        response=response
    )
