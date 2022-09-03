import scrapydo
from fastapi import FastAPI, status, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from src.spiders.xpath_spider import XpathSpider

app = FastAPI()


@app.get("/web-scraper/html", status_code=status.HTTP_200_OK)
async def get_element_html(url: str, element_xpath: str, search_string: str):
    """Given url, element_xpath and search_string, search for search_string within the element and return its HTML if
    found."""
    scrapydo.setup()

    spider_result = scrapydo.run_spider(
        XpathSpider,
        url=url,
        xpath=element_xpath,
        search_string=search_string,
    )[0]

    req_status = spider_result.get("status")
    req_status_detail = spider_result.get("status_detail")

    if req_status == "web_element_not_found" or req_status == "multiple_elements_found":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=req_status_detail,
        )
    if req_status == "string_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=req_status_detail,
        )
    if req_status == "string_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=req_status_detail,
        )

    json_compatible_item_data = jsonable_encoder(spider_result)
    return {JSONResponse(content=json_compatible_item_data)}
