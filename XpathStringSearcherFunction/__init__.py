import azure.functions as func
from fastapi import FastAPI

from src.main import get_element_html

app = FastAPI()


async def main(req: func.HttpRequest) -> func.HttpResponse:
    url = req.params.get("url", "")  # Provide an empty string as the default value
    element_xpath = req.params.get(
        "element_xpath", ""
    )  # Provide an empty string as the default value
    search_string = req.params.get(
        "search_string", ""
    )  # Provide an empty string as the default value

    try:
        response = await get_element_html(
            url, element_xpath, search_string
        )  # Call the function directly
        return func.HttpResponse(
            status_code=response.status_code,
            body=response.body,
            headers=response.headers,
        )
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
