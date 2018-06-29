from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import * 
from django.db.models import Q
from .models import *
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED,
                                   HTTP_200_OK,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)

# Create your views here.

class CaseViewSet(viewsets.ReadOnlyModelViewSet):
    
    """
    Returns a paginated list of all cases
    """
    serializer_class = CaseSerializer
    queryset = Case.objects.order_by('id')

    @list_route(methods=['post'])
    def search(self, request, *args, **kwargs):
        """
        return a pinated list of  Cases that satisfy the param query_text

        params query_text:  text to search against
        """

        query_text= request.data.get('query_text', None)

        if query_text is not None:
            myqueryset=Case.objects.all().filter(name__icontains=query_text).extra(\
            select={'lower_name':'lower(name)'}).order_by('lower_name')
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(myqueryset, request)
            serializer = CaseSerializer(result_page, context={'request': request}, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            myqueryset=Case.objects.all().extra(\
            select={'lower_name':'lower(name)'}).order_by('lower_name')
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(myqueryset, request)
            serializer = CaseSerializer(result_page, context={'request': request}, many=True)
            return paginator.get_paginated_response(serializer.data)


    @list_route(methods=['get'])
    def listAll(self, request, *args, **kwargs):
        """
        returns all product cases
        """
        myqueryset = Case.objects.all().extra(\
        select={'lower_first_name':'lower(first_name)'}).order_by('lower_first_name')
      
        serializer = CaseSerializer(myqueryset, context={'request': request}, many=True)
        return Response({ 'results': serializer.data}, status=HTTP_200_OK)

 
class SightingViewSet(viewsets.ModelViewSet):

    """
    Returns a paginated list of all hymns
    """
    serializer_class = SightingSerializer
    queryset = Sighting.objects.order_by('id')

    # def create(self, request, *args, **kwargs):
    #     """
    #     Sighting ~ create Sightings

    #     PARAMETERS:

    #     name , has_refrain, refrain, stanzas

    #     """
    #     hymns = request.data.get('results')
        
    #     for item in hymns:
    #         name = item['name']
    #         has_refrain = item['has_refrain']
    #         refrain = item['refrain']
    #         stanzas = item['stanzas']
    #         category = item['category']

    #         category = Category.objects.get(category)

    #         hymn = Hymn.objects.create(name=name, has_refrain=has_refrain, refrain=refrain, category=category)

    #         for stan in stanzas:
    #             stanza=Stanza.objects.create(content=stan['content'], hymn=hymn)

        
    #     post = HymnSerializer(hymn, context={'request': request}, many=False)
    #     return Response(post.data, status=HTTP_201_CREATED)
    
    # @list_route(methods=['post'])
    # def search(self, request, *args, **kwargs):
    #     """
    #     return a paginated list of  Products that satisfy the param query_text

    #     params query_text:  text to search against
    #     """

    #     query_text= request.data.get('query_text', None)

    #     if query_text is not None:
    #         myqueryset=Hymn.objects.all().filter(name__icontains=query_text).extra(\
    #         select={'lower_name':'lower(name)'}).order_by('lower_name')
    #         paginator = PageNumberPagination()
    #         result_page = paginator.paginate_queryset(myqueryset, request)
    #         serializer = HymnSerializer(result_page, context={'request': request}, many=True)
    #         return paginator.get_paginated_response(serializer.data)
    #     else:
    #         myqueryset=Hymn.objects.all().extra(\
    #         select={'lower_name':'lower(name)'}).order_by('lower_name')
    #         paginator = PageNumberPagination()
    #         result_page = paginator.paginate_queryset(myqueryset, request)
    #         serializer = HymnSerializer(result_page, context={'request': request}, many=True)
    #         return paginator.get_paginated_response(serializer.data)
       

    # def update(self, request, *args, **kwargs):
        
    #     name = request.data.get('name', None)
    #     has_refrain = request.data.get('has_refrain', None)
    #     refrain = request.data.get('refrain', None)
    #     category = request.data.get('category', None)
    #     stanzas = request.data.get('stanzas', None)

    #     category = None;
    #     type = None;
        
    #     try :
    #         hymn = self.get_object()
    #         if(category is not None):
    #             try :
    #                 category = Category.objects.get(id=int(category))
    #                 hymn.category=category
    #             except Category.DoesNotExist:
    #                 print('hymn_category does not exist')

    #         if(has_refrain is not None):
    #             hymn.has_refrain=has_refrain

    #         if(name is not None):
    #             hymn.name=name

    #         if(refrain is not None):
    #             hymn.refrain=refrain          
            
    #         hymn.save()
           

    #         if(stanzas is not None):
    #             for stan in stanzas:
    #                 try :
    #                     stanzas = Stanza(
    #                         content=p['content'],
    #                         hymn=hymn
    #                     )
    #                     stanzas.save()
    #                 except Stanza.DoesNotExist:
    #                     print('exception')
            
            
    #         res = HymnSerializer(hymn, context={'request': request})
    #         return Response(res.data, status=HTTP_200_OK)
    #     except Hymn.DoesNotExist:
    #         return Response({'detail': 'Hymn with id '+pk+' does not exist'}, status=HTTP_400_BAD_REQUEST)


    @list_route(methods=['get'])
    def listAll(self, request, *args, **kwargs):
        """
        returns all Sightings 
        """
        myqueryset = Sighting.objects.all().extra(\
        select={'lower_name':'lower(name)'}).order_by('lower_name')
      
        serializer = SightingSerializer(myqueryset, context={'request': request}, many=True)
        return Response({ 'results': serializer.data}, status=HTTP_200_OK)

class FAQViewSet(viewsets.ModelViewSet):

    """
    Returns a paginated list of all stanzas
    """
    serializer_class = FAQSerializer 
    queryset = FAQ.objects.order_by('id')

class AboutUsViewSet(viewsets.ModelViewSet):

    """
    Returns a paginated list of all App details text
    """
    serializer_class = AboutUsSerializer
    queryset = AboutUs.objects.all()

class TeamViewSet(viewsets.ModelViewSet):

    """
    Returns a paginated list of all Prayer requests
    """
    serializer_class = TeamSerializer
    queryset = Team.objects.order_by('-id')

    # def create(self, request, *args, **kwargs):
    #     """
    #     Prayer Requests ~ create Prayer Requests

    #     PARAMETERS:

    #     name , content

    #     """
    #     content = request.data.get('content')

    #     request = PrayerRequest.objects.create(content=content, user=request.user)
        
    #     request = PrayerRequestSerializer(request, context={'request': request}, many=False)
    #     return Response(request.data, status=HTTP_201_CREATED) 

    # @detail_route(methods=['post'])
    # def following(self, request, *args, **kwargs):
    #     this_post= self.get_object();
    #     this_post.following.add(request.user)
    #     return Response({'results': 'followed'}, status= HTTP_200_OK)

class PrivacyPolicyViewSet(viewsets.ModelViewSet):

    """
    Returns a paginated list of all Events
    """
    serializer_class = PrivacyPolicySerializer
    queryset = PrivacyPolicy.objects.order_by('-id')

# class SearchHymn(APIView):

#   def post(self, request, *args, **kwargs):
#     """
#     Enables user to search for Hymns

#     POST REQUEST:

#     Parameters:
#     - search_text = a string that will be search against the database and return results
    
#     Filters:
#     - Hymn name, Refrain and stanzas
#     """
#     search_text = request.data.get('search_text', None)
#     if search_text is not None:
#       qs = Hymn.objects.all()
#       for term in search_text.split():
#         qs = qs.filter(Q(name__icontains=term) |
#                        Q(refrain__icontains=term)
#         )
#       hymns = HymnSerializer(qs, context={'request': request}, many=True)
#       return Response({'results': hymns.data}, status=HTTP_200_OK)
#     return Response({'results': 'Search Text is none'}, status=HTTP_400_BAD_REQUEST)


# from django.shortcuts import render
# from rest_framework import viewsets
# from .serializers import *
# from .models import *

# # Create your views here.
# class LanguageView(viewsets.ModelViewSet):
#      queryset = Language.objects.all()
#      serializer_class = LanguageSerializer