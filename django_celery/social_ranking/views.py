from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Rank, RankChange
from .tasks import check_score_out_of_range

@api_view(['POST',])
def add_score_change(request):
    data = request.data
    try:
        user_id = data['user_id']
        d_score = int(data['score'])
        info = data['info']

        rank, _ = Rank.objects.get_or_create(user_id=user_id)

        new_score = rank.score + d_score
        if new_score<0:
            new_score=0
        
        RankChange.objects.create(
            user_id = user_id,
            d_score=d_score,
            information = info
        )

        rank.score = new_score
        rank.save()

        check_score_out_of_range.delay(user_id, new_score)
        return Response(status=status.HTTP_200_OK)
    except KeyError:
        error = 'please make sure to send all fields'
        return Response({'error':error},status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        error = 'please make sure "d_score" is a number'
        return Response({'error':error},status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
