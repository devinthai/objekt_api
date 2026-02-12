import logging
from objekt_api.http import ObjektHTTP 
from objekt_api.models import *
from objekt_api.exceptions import ObjektApiException
from typing import List, Dict
import concurrent.futures

class ObjektApi:
    def __init__(self, api_key: str = '', ssl_verify: bool = True, logger: logging.Logger = None):
        self._http = ObjektHTTP(api_key, ssl_verify, logger)

    def get_collection(self, params: Dict = None) -> List[Slug]:
        res = self._http.get('/collection', params = params)
        collection = Collection.model_validate_json(res.data)

        return collection.collections

    def get_metadata(self, slug: str) -> Metadata:
        metadata_endpoint = f'/objekts/metadata/{slug}'
        res = self._http.get(metadata_endpoint)

        slug_metadata = Metadata.model_validate_json(res.data)

        return slug_metadata

    def get_bulk_metadata(self, slugs: List[str]):
        """
        slugs: list of slugStrings to get metadata for 
        """
        endpoints = [f"/objekts/metadata/{slug}" for slug in slugs]

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            res = executor.map(self._http.get, endpoints)

        metadata_jsons = [row.data for row in res]

        validated_metadata_list = [Metadata.model_validate_json(metadata) for metadata in metadata_jsons]
        return validated_metadata_list
