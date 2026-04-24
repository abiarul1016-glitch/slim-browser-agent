# NOTE: Too many tools can cause the model to get confused and not know which one to call, so it's best to start with a few and then add more as needed.
# Navigate to url and extract text from page are the most useful tools, as the model is able to reason, that it can utilize parameters within the url to access different parts of a site.
# Adding the extra tools makes the agent much slower.


# == CORE TOOLS ==
def navigate_to_url(page, url: str):
    """
    Args:
        page: The Playwright page object. This is already passed in when it is called as a tool, so you don't need to worry about it when calling the function.
        url: The URL to navigate to. This you will need to pass in when calling the function as a tool.

    Returns:
        A success message if the url was successfully accessed.

    """

    page.goto(url)
    return f"Successfully navigated to {url}!"


def extract_text_from_page(page):
    """
    Args:
        page: The Playwright page object. This is already passed in when it is called as a tool, so you don't need to worry about it when calling the function as a tool.

    Returns:
        All the text from the current url.
    """
    # Extract all visible text from the page body
    text = page.inner_text("body")
    return text


# == EXTRA BUT HEAVY ==
def click_button_with_text(page, text):
    """
    Args:
        page: The Playwright page object. This is already passed in when it is called as a tool, so you don't need to worry about it when calling the function as a tool.
        text: The text of the button to click. This you will need to pass in when calling the function as a tool.

    Returns:
        A success message if the button was successfully clicked.
    """

    page.get_by_text(text).first.click()
    return f"Clicked the button with text {text}!"


def extract_html_from_page(page):
    """
    Args:
        page: The Playwright page object. This is already passed in when it is called as a tool, so you don't need to worry about it when calling the function as a tool.

    Returns:
        All the HTML from the current url.
    """
    # Extract all visible HTML from the page body
    text = page.inner_html("body")
    return text


def click_button_with_name(page, name):
    """
    Args:
        page: The Playwright page object. This is already passed in when it is called as a tool, so you don't need to worry about it when calling the function as a tool.
        name: The name of the button to click. This you will need to pass in when calling the function as a tool.

    Returns:
        A success message if the button was successfully clicked.
    """

    page.get_by_role("button", name=name).first.click()
    return f"Clicked the button with name {name}!"


def fill_textbox(page, name, text):
    """
    Args:
        page: The Playwright page object. This is already passed in when it is called as a tool, so you don't need to worry about it when calling the function as a tool.
        name: The name of the textbox to fill. This you will need to pass in when calling the function as a tool.
        text: The text to fill in the textbox. This you will need to pass in when calling the function as a tool.

    Returns:
        A success message if the textbox was successfully filled.
    """

    page.get_by_role("textbox", name=name).first.fill(text)
    return f"Filled the textbox with name {name} with text {text}!"
