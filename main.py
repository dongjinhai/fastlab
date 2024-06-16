# -*- encofing:utf-8 -*-
from typing import Union

from fastapi import FastAPI, Depends, Header
import uvicorn
from pydantic import BaseModel


app = FastAPI()


def get_db():
    try:
        print('run yield')
        yield 'got!'
    finally:
        print('run finally')


class Pagination(object):
    """
    分页依赖
    
    如果请求参数中没有传递page_size和current_page, 则返回的实例为None
    只需检查pagination这个参数是否为None即可判断是否要分页查询
    """
    def __init__(
        self,
        current_page: Union[int, None] = None,
        page_size: Union[int, None] = None
    ) -> None:
        # 数据总数, 在查询数据库后主动赋值
        self.total = 0
        self.current_page = current_page
        self.page_size = page_size
    
    def __new__(
        cls,
        current_page: Union[int, None] = None,
        page_size: Union[int, None] = None
    ):
        if current_page is None or page_size is None:
            return None
        return super(Pagination, cls).__new__(cls)


def get_user(header: str = Header()):
    print(header)


# def pagination_params(
#     page_size: Union[int, None] = None,
#     current_page: Union[int, None] = None
# ) -> Union[Pagination, None]:
#     """
#     获取分页参数

#     如果获取不到分页参数则返回None
#     """
#     if not page_size or not current_page:
#         return None

#     return Pagination(page_size=page_size, current_page=current_page)


@app.get('/')
def hello(db: str = Depends(get_db), x = Depends(get_user)):
    return {"hello": "world"}


@app.get('/page')
def run_page(q:int, pagination: Pagination = Depends(Pagination)):
    """分页查询"""
    return {
        'q': q,
        'pagination': pagination
    }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
