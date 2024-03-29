from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import add_pagination, Page, paginate

from src.models.data_models import Genre
from src.services.genres import GenreService, get_genre_service

router = APIRouter()


@router.get(
    "/{genre_id}",
    response_model=Genre,
    summary="Информация о жанре",
    description="Подробная информация по id жанра",
    response_description="Название и описание жанра",
)
async def genre_details(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service),
) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")

    return Genre(id=genre.id, name=genre.name, description=genre.description)


@router.get(
    "/",
    response_model=Page[Genre],
    description="Вывод списка жанров",
)
async def genre_list(
    genre_service: GenreService = Depends(get_genre_service),
):
    genres = await genre_service.get_list()
    return paginate(genres)


add_pagination(router)
