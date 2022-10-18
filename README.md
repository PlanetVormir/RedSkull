# RedSkull

> _"I guide others to a treasure I cannot possess"_

RedSkull scrapes a media streaming website and provides its data in form of an API. This is merely an indexing API,
and so it does not host any illegal contents and simply provides the client with URL where the actual content is hosted.
This is why it's named RedSkull, because it guides you to a treasure that it itself can't possess. On that note, I think
that this project does not break any laws since it does not host anything illegal, if you think otherwise please feel
free to open an issue and I will delete this repository.

# Endpoints

|    Name     |    Parameters    | Remarks                                                                      |
|:-----------:|:----------------:|:-----------------------------------------------------------------------------|
|   search    | keyword, page_no | To search for content (movies or series)                                     |
|    movie    |     media_id     | To get episode id for different servers, use this to get m3u8 url            |
|   series    |     media_id     | To list the seasons and episodes of a series along with it's episode id      |
|   episode   |    episode_id    | To get m3u8 urls for a particular episode of a particular show or a movie    |
| clear_cache |  No parameters   | (TODO): To force the server to clear cache, in future, it will need a reason |

## Search

> <your-api-instance>/search?keyword=&page_no=

Use this endpoint to search for a series or a movie. It won't provide all the results at once, you have to increment the
`page_no` parameter to get more results. Each result has a `media_id` parameter and a `type` parameter which can then be
used to request further details about a result. Use the `movie` endpoint if `type` is `Movie` or the `series` endpoint
if the type is `TV`.

#### Parameters:

- `keyword`: The name of the movie/series you want to watch.
- `page_no`: [Optional] Response does not provide all the results at once so increment this parameter for lazy loading

#### Response:

```json
{
  "max_page_no": "page_no parameter must be smaller than the number specified here",
  "results": [
    {
      "title": "Name of the movie/series",
      "poster": "A url to a poster of this media",
      "quality": "HD, SD, HDRip, etc",
      "rating": "IMDB rating",
      "type": "TV/Movie",
      "media_id": "use this parameter for further calls to movie/series endpoint"
    }
  ]
}
```

## Movie

> <your-api-instance>/movie?media_id=

This endpoint will provide you with an `episode_id` for different servers for the given movie. Pick any one of those and
use that to get an actual m3u8 url from the episode endpoint.

#### Parameters:

- `media_id`: The media_id as provided in the response by the search endpoint.

#### Response:

```json
{
  "X_server_name": "episode_id",
  "Y_server_name": "episode_id"
}
```

## Series

> <your-api-instance>/series?media_id=

This endpoint will provide you with an episode id of each episode from different server which can then be used to get an
actual m3u8 url from the episode endpoint.

#### Parameters:

- `media_id`: The media_id as provided in the response by the search endpoint.

#### Response:

```json
{
  "episodes": {
    "1": {
      "1": {
        "date": "Nov 16, 2004",
        "name": "Pilot",
        "sources": {
          "X_server_id": "X_server_episode_id",
          "Y_server_id": "Y_server_episode_id"
        }
      },
      "2": {
        "date": "Nov 23, 2004",
        "name": "First season, second episode",
        "sources": {
          "X_server_id": "X_server_episode_id",
          "Y_server_id": "Y_server_episode_id"
        }
      }
    },
    "2": {
      "1": {
        "date": "Sep 13, 2005",
        "name": "Second season, first episode",
        "sources": {
          "X_server_id": "X_server_episode_id",
          "Y_server_id": "Y_server_episode_id"
        }
      }
    }
  },
  "servers": {
    "X_server_name": "X_server_id",
    "Y_server_name": "Y_server_id"
  }
}
```

## Episode

> <your-api-instance>/episode?episode_id=

Use this endpoint to get a m3u8 url for either a movie on a particular server or an episode from a show on a particular
server.

#### Parameters:

- `episode_id`: The episode_id as provided in the response by the movie/series endpoint.

#### Response:

```json
{
  "url": "m3u8 url"
}
```
