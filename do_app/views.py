from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Task, Comment, CommentLike
from .forms import TaskForm, CommentForm, SignUpForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LogoutView 
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'
    next_page = reverse_lazy('task_list')

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = self.object
            comment.author = request.user
            comment.save()
        return self.get(request, *args, **kwargs)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

# Нові класи для редагування та видалення коментарів

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment_edit.html'

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse('task_detail', args=[self.object.task.id])

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comments/comment_confirm_delete.html'

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse('task_detail', args=[self.object.task.id])

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

# Функція для лайків коментарів
@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)
    
    if not created:
        like.delete()  # Якщо лайк вже існує, видаляємо його
        messages.info(request, "You've removed your like.")
    else:
        messages.success(request, "You've liked the comment.")
    
    return redirect('task_detail', pk=comment.task.id)
