import json
import requests

from llm_client import chat, execute_tool
from prompts import SYSTEM_PROMPT
from memory import load_memory, save_memory, clear_memory


conversation = load_memory()

if not conversation:
    conversation = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]
else:
    conversation = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ] + conversation


def start_chat():

    print("AI BUSINESS ASSISTANT")
    print("Ask about sales or business.")
    print("Commands: exit, clear")

    while True:

        question = input("\nYou: ").strip()

        if not question:
            continue

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if question.lower() == "clear":
            clear_memory()

            conversation.clear()
            conversation.append({
                "role": "system",
                "content": SYSTEM_PROMPT
            })

            print("Conversation history cleared.")
            continue

        conversation.append({
            "role": "user",
            "content": question
        })

        try:
            for _ in range(5):

                message = chat(conversation)

                tool_calls = message.get("tool_calls", [])

                conversation.append(message)

                if not tool_calls:
                    print("\nAssistant:", message.get("content", ""))
                    break

                for tool_call in tool_calls:

                    result = execute_tool(tool_call)

                    conversation.append({
                        "role": "tool",
                        "tool_name": tool_call["function"]["name"],
                        "content": json.dumps(result)
                    })

            else:
                print("Tool-call limit reached.")

            save_memory([
                item for item in conversation
                if item["role"] != "system"
            ])

        except requests.exceptions.RequestException as error:
            print("Connection error:", error)
            conversation.pop()

        except (ValueError, KeyError, TypeError) as error:
            print("Application error:", error)


if __name__ == "__main__":
    start_chat()