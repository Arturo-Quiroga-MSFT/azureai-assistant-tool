# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.

import json
import asyncio
from azure.ai.assistant.management.async_chat_assistant_client import AsyncChatAssistantClient
from azure.ai.assistant.management.ai_client_factory import AsyncAIClientType
from azure.ai.assistant.management.assistant_client_callbacks import AssistantClientCallbacks
from azure.ai.assistant.management.async_conversation_thread_client import AsyncConversationThreadClient


# Define a custom callback class that inherits from AssistantClientCallbacks
class MyAssistantClientCallbacks(AssistantClientCallbacks):
    def __init__(self, message_queue):
        self.message_queue = message_queue

    async def handle_message(self, action, message=""):
        await self.message_queue.put((action, message))

    def on_run_update(self, assistant_name, run_identifier, run_status, thread_name, is_first_message=False, message=None):
        if run_status == "streaming":
            asyncio.create_task(self.handle_message("start" if is_first_message else "message", message))

    def on_function_call_processed(self, assistant_name, run_identifier, function_name, arguments, response):
        asyncio.create_task(self.handle_message("function", function_name))

# Define a function to display streamed messages
async def display_streamed_messages(message_queue, assistant_name):
    while True:
        message_type, message = await message_queue.get()
        if message_type == "start":
            # At the start of a new message, include the assistant's name.
            print(f"{assistant_name}: {message}", end="")
        elif message_type == "message":
            # Print the streamed part of the message; `flush=True` ensures it's immediately displayed
            print(message, end="", flush=True)
        elif message_type == "function":
            # Print assistant's name and calling the function on the new line
            print(f"{assistant_name}: called {message} function.")
        message_queue.task_done()


# Define the main function
async def main():
    assistant_name = "PetTravelPlanChatAssistant"
    config_path = f"config/{assistant_name}_assistant_config.json"

    try:
        with open(config_path, "r") as file:
            config_json = json.load(file)
        ai_client_type = AsyncAIClientType[config_json["ai_client_type"]]
        message_queue = asyncio.Queue()
        callbacks = MyAssistantClientCallbacks(message_queue)
    except FileNotFoundError:
        print(f"Configuration file for {assistant_name} not found.")
        return
    except KeyError as e:
        print(f"Missing key in configuration file for {assistant_name}: {e}")
        return

    assistant_client = await AsyncChatAssistantClient.from_json(json.dumps(config_json), callbacks=callbacks)
    conversation_thread_client = AsyncConversationThreadClient.get_instance(ai_client_type)
    thread_name = await conversation_thread_client.create_conversation_thread()

    display_task = asyncio.create_task(display_streamed_messages(message_queue, assistant_name))

    try:
        while True:
            user_message = input("user: ").strip()
            if user_message.lower() == 'exit':
                print("Exiting chat.")
                break

            await conversation_thread_client.create_conversation_thread_message(user_message, thread_name)
            await assistant_client.process_messages(thread_name=thread_name, stream=True)

            print() # Add a newline for better readability

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await message_queue.join()
        display_task.cancel()
        await conversation_thread_client.close()

if __name__ == "__main__":
    asyncio.run(main())

