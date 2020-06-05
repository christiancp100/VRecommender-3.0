from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
# Healthcheck responsible endpoint
@api_view(["GET"])
@renderer_classes([JSONRenderer])
def healthcheck(request):
   # Here someone can put some more checks
   return Response({
      "django": "ok" 
   })