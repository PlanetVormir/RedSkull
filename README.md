# RedSkull

> _"I guide others to a treasure I cannot possess"_

RedSkull scrapes a media streaming website and provides its data in form of an API. This is merely an indexing API,
and so it does not host any illegal contents and simply provides the client with URL where the actual content is hosted.
This is why it's named RedSkull, because it guides you to a treasure that it itself can't possess. On that note, I think
that this project does not break any laws since it does not host anything illegal, if you think otherwise please feel
free to open an issue and I will delete this repository.

# Endpoints

|    Name     |    Parameters    | Remarks                                                              |
|:-----------:|:----------------:|:---------------------------------------------------------------------|
|   search    | keyword, page_no | To search for content (movies or series)                             |
|    movie    |     media_id     | To get m3u8 urls for a particular movie                              |
|   series    |     media_id     | To list the seasons and episodes of series.                          |
|   episode   |    episode_id    | To get m3u8 urls for a particular episode of a particular show       |
| clear_cache |  No parameters   | To force the server to clear cache, in future, it will need a reason |

### Search

> <your-api-instance>/search?keyword=<your-query>&page_no=<optional-page-no>

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

### Movie

> <your-api-instance>/movie?media_id=<media-id-from-search-result>

#### Parameters:

- `media_id`: The media_id as provided in the response by the search endpoint.

#### Response:

```json
{
  "X_server_name": "episode_id",
  "Y_server_name": "episode_id"
}
```

### Series

> <your-api-instance>/series?media_id=<media-id-from-search-result>

TODO
