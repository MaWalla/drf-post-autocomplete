from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from post_autocomplete.serializer import SearchBuildingsSerializer
from post_autocomplete.tools import search_buildings


__all__ = ['SearchBuildingsView']


class SearchBuildingsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        serializer = SearchBuildingsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        return Response(search_buildings(**serializer.validated_data))
