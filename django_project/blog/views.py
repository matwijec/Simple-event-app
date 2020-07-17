from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Participants
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']




class PostDetailView(DetailView):
    model = Post
    context_object_name = 'posts'
    

    def get_context_data(self, **kwargs):
        data = super(PostDetailView,self).get_context_data(**kwargs)
        data['members'] = Post.objects.filter(id=self.object.id)[0].participants.participants.all()
        if self.request.user in data['members']:
            data['attend']='Miss'
        else:
            data['attend']='Attend'
        return data


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        member=Participants()
        member.save()
        member.participants.add(self.request.user)
        member.save()
        form.instance.participants = member
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def postAttend(request, pk):
    part = Post.objects.get(id=pk).participants.participants.all()  
    if request.user in part:
        Post.objects.get(id=pk).participants.participants.remove(request.user) 
    else:
        Post.objects.get(id=pk).participants.participants.add(request.user)  
    return redirect('post-detail', pk)


def about(request):
    return render(request, 'blog/about.html', {'title': 'about'})


def events(request):
    listPart = Participants.objects.filter(participants=request.user)
    listOfPost=[]
    for part in listPart:
        if len(Post.objects.filter(participants=part)) is not 0:
            listOfPost.append(Post.objects.filter(participants=part)[0])
    context = {
        'events': listOfPost
    }
    return render(request, 'blog/events.html', context)


          