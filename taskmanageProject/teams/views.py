from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse_lazy
from .models import Team, Task
from accounts.models import User
from django.shortcuts import get_object_or_404
from teams.forms import TeamModelForm, TasksModelForm
from django.core.paginator import Paginator


# 팀 생성하기
class TeamCreateView(View):
    # 모든 유저목록 가져와서 team_create.html로 렌더
    def get(self, request):
        form = TeamModelForm(current_user=request.user)
        users = User.objects.all().order_by('username')  # 모든 사용자를 가져옴
        return render(request, 'index_create.html', {'form': form, 'users': users})

    # 팀 생성한 후 team_list.html로 리다이렉트
    def post(self, request):
        if request.method == 'POST' or request.method == 'FILES':
            form = TeamModelForm(request.POST, request.FILES, current_user=request.user)
            if form.is_valid():
                # team = form.save()  # 폼 데이터를 DB에 저장하고 팀 객체 반환
                unfinished_team = form.save(commit=False)
                unfinished_team.creater = request.user
                unfinished_team.save()

                # 유저 맴버에 추가하기
                unfinished_team.members.add(request.user)

                member_ids = request.POST.getlist('members')  # 선택된 멤버들의 ID 리스트
                
                for member_id in member_ids:
                    user = User.objects.get(pk=member_id)
                    unfinished_team.members.add(user)
                
                return redirect('teams:team_list')
        else: 
            users = User.objects.all().order_by('username')
            form = TeamModelForm(current_user=request.user)  # 현재 로그인한 사용자 정보 전달
        return render(request, 'index_create.html', {'form': form, 'users': users})
       

# 팀 수정하기
def team_update(request, id):
    post = get_object_or_404(Team, pk=id)
    if request.method == 'POST' or request.method == 'FILES':
        form = TeamModelForm(request.POST, request.FILES, instance=post, current_user=request.user)
        if form.is_valid():
            unfinished_team = form.save(commit=False)
            unfinished_team.creater = request.user
            unfinished_team.save()

            # 유저 맴버에 추가하기
            unfinished_team.members.add(request.user)
            
            member_ids = request.POST.getlist('members')  # 선택된 멤버들의 ID 리스트
                
            for member_id in member_ids:
                user = User.objects.get(pk=member_id)
                unfinished_team.members.add(user)
            
            return redirect('teams:team_detail',  id=id)
    else:
        form = TeamModelForm(instance=post, current_user=request.user)
        return render(request, 'team_create.html', {'form':form, 'id':id})
    

# 팀 삭제하기
def team_delete(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team.delete()
    return redirect('accounts:base') 

# 팀 전체 조회
def team_list(request):
    if request.user.is_authenticated:
        liked_teams = Team.objects.filter(like_users=request.user)
        other_teams = Team.objects.exclude(like_users=request.user)
    else:
        liked_teams = Team.objects.none()
        other_teams = Team.objects.all()
    
    context = {
        'liked_teams': liked_teams,
        'other_teams': other_teams,
    }
    return render(request, 'index.html', context)

# def team_list(request):   
#     teams = Team.objects.all().order_by('-created_at')
#     paginator = Paginator(teams, 3)
#     pagnum = request.GET.get('page')
#     teams = paginator.get_page(pagnum)
#     return render(request, 'team_list.html', {'teams': teams})

# 팀 상세 조회
def team_detail(request, id):
    team = get_object_or_404(Team, pk=id)
    tasks = team.task_set.all().order_by('title')  # 팀에 할당된 모든 할일 조회
    paginator = Paginator(tasks, 5)
    pagnum = request.GET.get('page')
    tasks = paginator.get_page(pagnum)
    return render(request, 'team_detail.html', {'team': team, 'tasks': tasks})


# 팀 좋아요
def likes(request, team_id):
    if request.user.is_authenticated:
        team = get_object_or_404(Team, pk=team_id)

        if team.like_users.filter(pk=request.user.pk).exists():
            team.like_users.remove(request.user)
        else:
            team.like_users.add(request.user)
        return redirect('teams:team_detail',  id=team.id)
    return redirect('teams:team_detail',  id=team.id)

#--------------------------------------------------------------------------------

# 할 일

# 할 일 생성하기
def task_create(request, id):
    team = get_object_or_404(Team, pk=id)
    if request.method == 'POST':
        form = TasksModelForm(request.POST, team=team)
        manager_ids = request.POST.getlist('manager')
        if form.is_valid():
            task_create = form.save()
            task_create.team = team
            task_create.save()
            #task_create.manager = request.POST.get('manager')
            for manager_id in manager_ids:
                user = User.objects.get(pk=manager_id)
                task_create.manager.add(user)
                task_create.save()

            task_create.save()
            return redirect('teams:team_detail', id=id)
    else:
        form = TasksModelForm(team=team)
     # 팀 멤버들에 대한 할 일 목록
    tasks = Task.objects.filter(team=team)
    return render(request, 'task_create.html', {'form': form, 'team': team, 'tasks': tasks})

# 할 일 수정하기
def task_update(request, id):
    task_update = get_object_or_404(Task, pk=id)
    team = task_update.team
    if request.method == 'POST':
        manager_ids = request.POST.getlist('manager')
        form = TasksModelForm(request.POST, request.FILES, instance=task_update, team=team)
        if form.is_valid():
            task_update = form.save()
            task_update.manager.clear()
            for manager_id in manager_ids:
                user = User.objects.get(pk=manager_id)
                task_update.manager.add(user)
                task_update.save()
            task_update.save()
            return redirect('teams:team_detail', id=task_update.team.id)
    else:
        form = TasksModelForm(instance=task_update, team=task_update.team)

    manager_ids = list(task_update.manager.all().values_list('id', flat=True))
    return render(request, 'task_create.html', {'form': form, 'task_update': task_update, 'team': team, 'manager': manager_ids})

# 할 일 삭제하기
def task_delete(request, id):
    task = get_object_or_404(Task, pk=id)
    team_id = task.team.id  # 할일이 속한 팀의 id를 가져옴
    task.delete()
    return redirect('teams:team_detail', id=team_id)



'''
def task_detail(request, id):
    task_detail = get_object_or_404(Team, pk=id)
    tasks = task_detail.task_set.all().order_by('-deadline')  # 팀에 할당된 모든 할일 조회
    paginator = Paginator(tasks, 5)
    pagnum = request.GET.get('page')
    tasks = paginator.get_page(pagnum)
    return render(request, 'task_detail.html', {'tasks': tasks})
'''

# 유저 찾기
# def user_search(request):
#     form = UserSearchForm(request.GET)
#     users = []

#     if form.is_valid():
#         search_query = form.cleaned_data.get('search_query')
#         if search_query:
#             users = User.objects.filter(username__icontains=search_query)

#     return render(request, 'user_search.html', {'form': form, 'users': users})

