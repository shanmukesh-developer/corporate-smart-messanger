import sys, os
from dotenv import load_dotenv # type: ignore
from groq import Groq # type: ignore

# Robust IDE-Proof Path Injection
CWD = os.getcwd()
if CWD not in sys.path: sys.path.insert(0, CWD)
BACKEND_DIR = os.path.join(CWD, "backend")
if BACKEND_DIR not in sys.path: sys.path.insert(0, BACKEND_DIR)

try:
    from database import get_messages, get_conversations_collection # type: ignore
except (ImportError, ModuleNotFoundError):
    try:
        from backend.database import get_messages, get_conversations_collection # type: ignore
    except:
        pass
load_dotenv()

# Initialize Groq client
groq_key = os.environ.get("GROQ_API_KEY")
if not groq_key or "your_groq_key_here" in groq_key:
    print("⚠️ GROQ_API_KEY is missing or using placeholder. AI features will be disabled.")
    groq_client = None
else:
    groq_client = Groq(api_key=groq_key)


def retrieve_context(query: str, user_id: str, top_k=15):
    """
    Lightweight context retrieval: Fetch recent messages from conversations the user is in.
    """
    try:
        convos_col = get_conversations_collection()
        # Find conversations the user is a participant in
        user_convos = list(convos_col.find({"participants": user_id}, {"conversation_id": 1}))
        convo_ids = [c["conversation_id"] for c in user_convos]

        if not convo_ids:
            return []

        # Fetch recent messages from these conversations
        from backend.database import get_messages_collection
        msgs_col = get_messages_collection()
        
        # Get last top_k messages across all user's conversations
        recent_msgs = msgs_col.find(
            {"conversation_id": {"$in": convo_ids}},
            {"sender_id": 1, "content": 1, "timestamp": 1}
        ).sort("timestamp", -1).limit(top_k)

        context = []
        for m in recent_msgs:
            sender = m.get("sender_id", "unknown")
            content = m.get("content", "")
            context.append(f"[{sender}]: {content}")
        
        # Reverse to keep chronological order for the LLM
        return list(reversed(context))
        
    except Exception as e:
        print(f"Error in retrieve_context: {e}")
        return []


def answer(query: str, user_id: str, llm_client=None) -> str:
    context_chunks = retrieve_context(query, user_id)

    if not context_chunks:
        context_str = "No relevant messages found in the chat history."
    else:
        context_str = "\n".join(context_chunks)

    system_prompt = """You are a workplace assistant for a corporate messaging app.
Your job is to help employees by reading their chat history and answering questions.

You can help with:
- Finding scheduled meetings or calls mentioned in chat
- Tracking project status from messages (blocked, in progress, done)
- Summarizing what was discussed in a conversation
- Finding who said what about a topic

Answer based only on the chat history provided. If there is no relevant information, say so clearly.
Be concise and specific — quote the relevant message if it helps."""

    user_prompt = f"""Chat history retrieved:
{context_str}

User question: {query}"""

    if not groq_client:
        return "AI response disabled: GROQ_API_KEY is missing or invalid."

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=1000,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error communicating with AI assistant: {str(e)}. Please check your GROQ_API_KEY in the .env file."