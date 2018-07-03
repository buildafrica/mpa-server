from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import * 
from django.db.models import Q
from .models import *
from mapps.users.models import *
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED,
                                   HTTP_200_OK,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)

# Create your views here.

class PhysicalDescriptionViewSet(viewsets.ModelViewSet):

    """
    Returns a paginated list of all properties
    """
    serializer_class = PhysicalDescriptionSerializer
    queryset = PhysicalDescription.objects.all()

    @list_route(methods=['get'])
    def listAll(self, request, *args, **kwargs):
        """
        returns all properties
        """
        myqueryset = PhysicalDescription.objects.all()
      
        serializer = PhysicalDescriptionSerializer(myqueryset, context={'request': request}, many=True)
        return Response({ 'results': serializer.data}, status=HTTP_200_OK)

class CaseViewSet(viewsets.ModelViewSet):
    
    """
    Returns a paginated list of all Cases
    """
    serializer_class = CaseSerializer
    queryset = Case.objects.order_by('id')

    def create(self, request):
        """
        Create a case

        PARAMETERS

        full_name, date_missing=date_missing, missing_from=missing_from, address=address, mobile=mobile, description=description

        user = user

        handler = handler

        physical_description = physical_description

        """
        full_name = request.data.get('full_name', None)
        date_missing = request.data.get('date_missing', None)
        missing_from = request.data.get('missing_from', None)
        dob = request.data.get('dob', None)
        address = request.data.get('address', None)
        mobile = request.data.get('mobile', None)
        description = request.data.get('description', None)
        handler = request.data.get('handler', None)
        physical_description = request.data.get('physical_description', None)
       
      

        hand = None;

        # if(full_name is None):
        #     return Response({'detail': 'Please supply required parameter name'}, status=HTTP_400_BAD_REQUEST)

        # if(product_category is None):
        #     return Response({'detail': 'Please supply required parameter product category'}, status=HTTP_400_BAD_REQUEST)
        
        # if(product_type is None):
        #     return Response({'detail': 'Please supply required parameter product type'}, status=HTTP_400_BAD_REQUEST)

        try :
            hand = MPAUser.objects.get(id=int(handler))
        except MPAUser.DoesNotExist:
            return Response({'detail': 'Product type with id '+handler+' does not exist'}, status=HTTP_400_BAD_REQUEST)

        case = Case(
            full_name=full_name,
            date_missing=date_missing,
            missing_from=missing_from,
            dob=dob,
            address=address,
            mobile=mobile,
            description=description,
            user=request.user,
            handler=hand,
            physical_description=physical_description,
        )

        case.save()

        if(physical_description is not None):
            for p in physical_description:
                try :
                    physical=PhysicalDescription.objects.get(id=int(p['id']))
                    prodPro = PhysicalDescriptionValue(
                        physical=physical,
                        case=case,
                        value=p['value']
                    )

                    prodPro.save()
                except PhysicalDescription.DoesNotExist:
                    print('exception')
               

        else:
            print('Nothing')

        res = CaseAddSerializer(case, context={'request': request})
        return Response(res.data, status=HTTP_201_CREATED)
        # except:
        #     return Response({'detail': 'An error occured'}, status=HTTP_400_BAD_REQUEST)
     

    @list_route(methods=['get'])
    def listAll(self, request, *args, **kwargs):
        """
        returns all cases
        """
        myqueryset = Case.objects.all().extra(\
        select={'lower_full_name':'lower(full_name)'}).order_by('lower_full_name')
      
        serializer = CaseSerializer(myqueryset, context={'request': request}, many=True)
        return Response({ 'results': serializer.data}, status=HTTP_200_OK)

class CaseSearch(APIView):
    def get(self, request, *args, **kwargs):
        """
        Search an cases by name

        PARAMETERS:
        query = query params

        """
        query = self.request.query_params.get('query', None)
        if query is not None:
            cases= Case.objects.all().filter(Q(full_name__icontains=query) | Q(date_missing__icontains=query))
            results = CaseSerializer(cases, context={'request': request}, many=True)
            return Response(results.data, status=HTTP_200_OK)
        else:
            return  Response({'results': 'Query is empty'}, status=HTTP_400_BAD_REQUEST)

class CaseLatest(APIView):
    def get(self, request, *args, **kwargs):
        """
        get all recent cases whose ID are greater than the provided id

        PARAMETERS:
        id = query params

        """
        
        if self.request.query_params.get('id', None) is not None:
            id = int(self.request.query_params.get('id', None))
            cases= Case.objects.all().filter(id__gt=id)
            paginator = LargeResultsSetPagination()
            result_page = paginator.paginate_queryset(cases, request)
            results = CaseSerializer(result_page, context={'request': request}, many=True)
            return paginator.get_paginated_response(results.data)
        else:
            return  Response({'results': 'Query is empty'}, status=HTTP_400_BAD_REQUEST)


class SightingViewSet(viewsets.ModelViewSet):

    """
    Returns a paginated list of all hymns
    """
    serializer_class = SightingSerializer
    queryset = Sighting.objects.order_by('id')

   
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


class PrivacyPolicyViewSet(viewsets.ModelViewSet):

    """
    Returns a paginated list of all Events
    """
    serializer_class = PrivacyPolicySerializer
    queryset = PrivacyPolicy.objects.order_by('-id')

