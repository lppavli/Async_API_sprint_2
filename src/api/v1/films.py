import enum
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from src.models.data_models import Film, FilmForPerson
from src.services.films import FilmService, get_film_service

from fastapi_pagination import Page, add_pagination, paginate


router = APIRouter()


@router.get(
    "/search",
    response_model=Page[FilmForPerson],
    description="Полнотекстовый поиск по произведениям",
    summary="Поиск кинопроизведений",
    response_description="Название и рейтинг фильма",
)
async def films_search(
    query: str,
    film_service: FilmService = Depends(get_film_service),
):
    """
    Поиск по фильмам
    """
    films = await film_service.search(query)

    return paginate(films)


@router.get(
    "/{film_id}",
    response_model=Film,
    description="Подробная информация по id фильма",
    summary="Информация о фильме",
    response_description="Название, жанры и рейтинг фильма, актёры,"
    "режиссёры и сценаристы",
)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")

    return film


class EnumStrMixin(enum.Enum):
    def __str__(self) -> str:
        return self.value


class SortTypes(EnumStrMixin):
    rating = "rating"


class FilterGenres(EnumStrMixin):
    animation = "Animation"
    action = "Action"
    adventure = "Adventure"
    fantasy = "Fantasy"
    sci_fi = "Sci-Fi"
    drama = "Drama"
    music = "Music"
    romance = "Romance"
    thriller = "Thriller"
    mystery = "Mystery"
    comedy = "Comedy"
    family = "Family"
    biography = "Biography"
    musical = "Musical"
    crime = "Crime"
    short = "Short"
    western = "Western"
    documentary = "Documentary"
    history = "History"
    war = "War"
    game_show = "Game-Show"
    reality_tv = "Reality-TV"
    horror = "Horror"
    sport = "Sport"
    talk_show = "Talk-Show"
    news = "News"


@router.get(
    "/",
    response_model=Page[FilmForPerson],
    summary="Список фильмов",
    description="Список фильмов, отсортированных по рейтингу и жанру, если они переданы",
    response_description="Список фильмов, параметры сортировки, "
    "количество фильмов на странице, номер страницы",
)
async def get_all_films(
    sort: Optional[SortTypes] = None,
    filter: Optional[FilterGenres] = None,
    film_service: FilmService = Depends(get_film_service),
) -> Page[list[Film]]:

    if not sort:
        sort = ""
    else:
        sort = sort.value

    if not filter:
        filter = ""
    else:
        filter = filter.value

    films = await film_service.get_all_films(sort, filter)

    return paginate(films)


add_pagination(router)
