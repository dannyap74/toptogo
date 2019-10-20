from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
import json
from django.http import JsonResponse
from rest_framework import generics


from .models import Lesson, Profile, Note, Task
from .serializers import LessonSerializer, UserSerializer, ProfileSerializer, NoteSerializer
from .day_check import date_res
from .theme_check import theme_res
from .task_update import update


class NoteList(APIView):
    def get(self, request):
        user = request.user
        p = Profile.objects.get(user=user)
        notes = p.notes
        data = NoteSerializer(notes, many=True).data
        return Response(data)
    def post(self, request):
        user = request.user
        p = Profile.objects.get(user=user)
        data = json.loads(request.body)
        idea = data["idea"]
        task = data["task"]
        print(idea)
        t = Task.objects.get(num=task)
        note = Note(idea=idea, task=t)
        note.save()
        p.notes.add(note)
        return Response(status=status.HTTP_201_CREATED)

class Statistic(APIView):
    def get(self, request):
        user = request.user
        p = Profile.objects.get(user=user)
        update(p)
        days = date_res(p)
        compl = p.completed_tasks.count()
        tried = p.wa_tasks.count()
        theme_prog = theme_res(p)
        data = {
            "completed": compl,
            "tried": tried,
            "day_statistic": days,
            "theme_statistic": theme_prog,
        }
        return JsonResponse(data)


class LessonList(APIView):
    def get(self, request, theme):
        lessons = Lesson.objects.filter(theme=theme)
        data = LessonSerializer(lessons, many=True).data
        return Response(data)


class LessonDetail(APIView):
    def get(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        data = LessonSerializer(lesson).data
        return Response(data)


class UserCreate(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]
        username = data["username"]
        password = data["password"]
        judge_id = data["judge_id"]
        serializer = UserSerializer(data={"email": email, "username": username, "password": password})
        if serializer.is_valid():

            user = serializer.save()
            p = Profile(user=user, judge_id=judge_id)
            p.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





