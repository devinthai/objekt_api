import logging
from objekt_api.http import ObjektHTTP 
from objekt_api.models import *
from objekt_api.exceptions import ObjektApiException
from typing import List, Dict

class ObjektApi:
    def __init__(self, api_key: str = '', ssl_verify: bool = True, logger: logging.Logger = None):
        self._http = ObjektHTTP(api_key, ssl_verify, logger)

    def get_collection(self, params: Dict = None) -> List[Slug]:
        res = self._http.get('/collection', params = params)
        collection = Collection.model_validate(res.data)

        return collection.collections

    def get_metadata(self, slug: str) -> Metadata:
        metadata_endpoint = f'/objekts/metadata/{slug}'
        res = self._http.get(metadata_endpoint)

        slug_metadata = Metadata.model_validate(res.data)

        return slug_metadata
