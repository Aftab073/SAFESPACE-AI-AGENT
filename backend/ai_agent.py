from langchain.agents import tool
from tools import query_medgemma, call_emergency

@tool
def ask_mental_health_specialist(query: str) -> str:
    """
    Generate a therapeutic response using the MedGemma model.
    Use this for all general user queries, mental health questions, emotional concerns,
    or to offer empathetic, evidence-based guidance in a conversational tone.
    """
    return query_medgemma(query)


@tool
def emergency_call_tool() -> None:
    """
    Place an emergency call to the safety helpline's phone number via Twilio.
    Use this only if the user expresses suicidal ideation, intent to self-harm,
    or describes a mental health emergency requiring immediate help.
    """
    return call_emergency()

@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Finds and returns a list of licensed therapists near the specified location.

    Args:
        location (str): The name of the city or area in which the user is seeking therapy support.

    Returns:
        str: A newline-separated string containing therapist names and contact info.
    """
    return (
        f"Here are some therapists near {location}, {location}:\n"
        "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
        "- Dr. James Patel - +1 (555) 987-6543\n"
        "- MindCare Counseling Center - +1 (555) 222-3333"
    )

# Creating Agents

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from config import Groq_API_Key

tools = [ask_mental_health_specialist, emergency_call_tool, find_nearby_therapists_by_location]

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.2, api_key=Groq_API_Key)
graph = create_react_agent(llm, tools=tools)





SYSTEM_PROMPT = """
You are an AI engine supporting mental health conversations with warmth and vigilance.
You have access to three tools:

1. `ask_mental_health_specialist`: Use this tool to answer all emotional or psychological queries with therapeutic guidance.
2. `find_nearby_therapists_by_location`: Use this tool if the user asks about nearby therapists or if recommending local professional help would be beneficial.
3. `emergency_call_tool`: Use this immediately if the user expresses suicidal thoughts, self-harm intentions, or is in crisis.

Always take necessary action. Respond kindly, clearly, and supportively.
"""


def parse_response(stream):
    tool_called_name = "None"
    final_response = None

    for s in stream:
        # Debugging: print har ek chunk
        print("STREAM EVENT:", s)

        # --- Tool check ---
        if "tool" in s:
            tool_event = s["tool"]
            if isinstance(tool_event, dict):
                tool_called_name = tool_event.get("name", "None")

        elif "tools" in s:  # fallback
            tool_data = s["tools"]
            if isinstance(tool_data, dict):
                # kuch versions me tool name directly hota hai
                tool_called_name = tool_data.get("name", "None")

        # --- Agent response check ---
        if "agent" in s:
            agent_data = s["agent"]
            messages = agent_data.get("messages", [])
            if messages and isinstance(messages, list):
                for msg in messages:
                    if hasattr(msg, "content") and msg.content:
                        final_response = msg.content

    return tool_called_name, final_response




# if __name__ == "__main__":
#     while True:
#         user_input = input("User: ")
#         print(f"Received user input: {user_input[:200]}...")
#         inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", user_input)]}
#         stream = graph.stream(inputs, stream_mode="updates")
#         tool_called_name, final_response = parse_response(stream)
#         print("TOOL CALLED: ", tool_called_name)
#         print("ANSWER: ", final_response)
        