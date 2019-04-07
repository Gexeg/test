from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
import text_comparison


class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    text_for_check = request.data['file'].read()
    file_checker = text_comparison.TextComparer(5, '/home/gex/git/projects/text_originality/file_filter/media', 60)
    similar_text_roster = file_checker.find_similar_text(text_for_check)

    if len(similar_text_roster) > 0:
      return Response('Base has similar text' + str(similar_text_roster), status=status.HTTP_403_FORBIDDEN)
    else:
      if file_serializer.is_valid():
        file_serializer.save()
        return Response(file_serializer.data, status=status.HTTP_201_CREATED)
