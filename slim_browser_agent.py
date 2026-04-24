from ollama import ResponseError, chat
from playwright.sync_api import sync_playwright

from browser_tools import (
    click_button_with_name,
    click_button_with_text,
    extract_html_from_page,
    extract_text_from_page,
    fill_textbox,
    navigate_to_url,
)

BROWSER_STATE_PATH = "playwright/.auth/state.json"
AVAILABLE_MODELS = {
    "qwen3.5": "qwen3.5:0.8b",
    "qwen3.6": "qwen3.6:35b-a3b-coding-nvfp4",
}
SELECTED_MODEL = AVAILABLE_MODELS.get("qwen3.6")


def main():

    available_functions = {
        "navigate_to_url": navigate_to_url,
        "extract_text_from_page": extract_text_from_page,
        "extract_html_from_page": extract_html_from_page,
        "click_button_with_name": click_button_with_name,
        "click_button_with_text": click_button_with_text,
        "fill_textbox": fill_textbox,
    }

    USING_FUNCTIONS = [navigate_to_url, extract_text_from_page]

    messages = [
        {
            "role": "system",
            "content": "You have access to many functions which allows you to access the browser and navigate pages. Also, you are in an agent loop, so you are free to use whatever function you wish, and as many you like. You won't need to pass in the browser or page object, as that is already passed in when you call the function as a tool.",
        }
    ]

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)

            # Create a new context with the saved storage state.
            try:
                context = browser.new_context(storage_state=BROWSER_STATE_PATH)
            except FileNotFoundError:
                print("Saved context not found. Creating new context.")
                context = browser.new_context()

            page = context.new_page()

            while True:
                user_input = input(
                    "What would you like Qwen to do next? (Type 'quit' to exit) "
                )

                if user_input == "quit":
                    break
                messages.append({"role": "user", "content": user_input})

                while True:
                    try:
                        response = chat(
                            model=SELECTED_MODEL,
                            messages=messages,
                            tools=USING_FUNCTIONS,
                            think=False,
                        )
                    except ResponseError as e:
                        print(f"Error: {e.error}")
                        return

                    messages.append(response.message)

                    if response.message.tool_calls:
                        for tc in response.message.tool_calls:
                            args = dict(tc.function.arguments)
                            args.pop(
                                "page", None
                            )  # Remove the page argument if it exists, since we are already passing it in

                            try:
                                function_to_call = available_functions[tc.function.name]
                                result = function_to_call(page=page, **args)
                                print(f"Called: {tc.function.name}!")
                            except KeyError:
                                result = f"Error: Unknown tool '{tc.function.name}'"
                            except Exception as e:
                                result = f"Error calling {tc.function.name}: {e}"

                            messages.append(
                                {
                                    "role": "tool",
                                    "tool_name": tc.function.name,
                                    "content": str(result),
                                }
                            )
                    else:
                        # No more tools to call
                        break

                print(response.message.content)

            # Save storage state into the file.
            storage = context.storage_state(path="state.json")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
