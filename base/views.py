from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import News, profile, Skills, project, projectfile, projectimage, projectmember
from django.contrib.auth.decorators import login_required
from .form import ProjectForm, Projectfileform, Projectimageform, Projectmemberform, profileimg
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
# Create your views here.
def home(request):
	last_five = News.objects.order_by('-created')[:5]
	last_three = project.objects.order_by('-date')[:3]
	try:
		user = User.get_username(request.user)
	except:
		user = None
	return render(request, 'index.html', {"last_five":last_five, "user":user, "last_three":last_three})

def projects(request):
	try:
		page = request.GET['page']
	except:
		return redirect('/projects/?page=1')
	projects = Paginator(project.objects.all().order_by('?'), 18).get_page(page)
	return render(request, 'projects.html', {'projects':projects})

def students(request):
	try:
		page = request.GET['page']
	except:
		return redirect('/students/?page=1')
	student = Paginator(profile.objects.exclude(id='5004ca7a-6adc-49fb-af9d-03e1ff8184cc').order_by('?'), 20)
	team = student.get_page(page)
	owner = profile.objects.get(id='5004ca7a-6adc-49fb-af9d-03e1ff8184cc')
	return render(request, 'team.html', {'students':team, 'owner':owner})


def loginpage(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		next = request.GET['next']
		if user is not None:
			login(request, user)
			return redirect(next)
		else:
			messages.error(request, "Username or password is incorrect")
	context = {}
	return render(request, 'login.html', context)
def logoutview(request):
	logout(request)
	next = request.GET['next']
	return redirect(next)
def news(request):
	try:
		page = request.GET['page']
	except:
		return redirect('/news/?page=1')
	allimg = Paginator(News.objects.all(), 15)
	allimages = allimg.get_page(page)
	try:
		user = User.get_username(request.user)
	except:
		user = None
	return render(request, 'news.html', {'news' : allimages, "user":user})
def new(request, pk):
	got = News.objects.all()
	new = None
	for i in got:
		if str(i.id) == pk:
			new = i
	try:
		user = User.get_username(request.user)
	except:
		user = None
	context = {'new' : new, "user":user}
	return render(request, 'new-1.html', context)

def profilepage(request, pk):
	person = User.objects.get(username=pk)
	ins = profile.objects.get(user=person)
	if request.method == "POST":
		try:
			last_file_path = ins.profile_image.path
		except:
			last_file_path = "None"
		if 'profile_image' in request.FILES:
			if default_storage.exists(last_file_path):
				default_storage.delete(last_file_path)
			ins.profile_image = request.FILES['profile_image']
			ins.save()
		try:
			create = Skills(host=person, skills=request.POST['skill'])
			create.save()
		except:
			pass
		return redirect("/profile/"+pk)
	prof = profile.objects.all()
	user1 = request.user
	user = None
	full_name = None
	email = None
	skill =None
	projects = None
	members = projectmember.objects.filter(project_id__host = person)
	for i in prof:
		if str(i.user) == pk:
			user = i
			full_name=i.user.get_full_name()
			email = i.user.email
			skill =Skills.objects.filter(host=i.user)
			projects = project.objects.filter(host=i.user)
	return render(request, 'profile.html', {'user':user, 'user1':user1,'members':members, "full":full_name, "email":email, "skill":skill, "projects":projects})
def projectpage(request, pk):
	form = Projectfileform()
	formimg = Projectimageform()
	formmember = Projectmemberform()
	if request.method == "POST":
		form = Projectfileform({'project_id': pk}, request.FILES)
		formimg = Projectimageform({'project_id': pk}, request.FILES)
		formmember = Projectmemberform({'member': request.POST.get('member'), 'job': request.POST.get('job'),'project_id': pk})
		print(formmember.errors.as_text)
		print(request.POST)
		if form.is_valid():
			form.save()
			return redirect("/project/"+pk)
		if formimg.is_valid():
			formimg.save()
			return redirect("/project/"+pk)
		if formmember.is_valid():
			formmember.save()
			return redirect("/project/"+pk)
	projects = project.objects.all()
	page = None
	images = projectimage.objects.filter(project_id=pk)
	files = projectfile.objects.filter(project_id=pk)
	members = None
	for i in projects:
		if str(i.id) == pk:
			page = i
			members = projectmember.objects.filter(project_id=i.id)
	return render(request, 'project.html', {'project':page, 'images':images, 'files':files, 'members':members, 'pk':pk, 'form':formmember})

@login_required(login_url='/login')
def profileredirect(request):
	return redirect('/profile/'+request.user.username)

@login_required(login_url='/login')
def newsedit(request, id):
	new1 = get_object_or_404(News, id=id)
	if request.method == "POST":
		try:
			last_face_path = new1.face_image.path
		except:
			last_face_path = "None"
		try:
			last_image_path = new1.images.path
		except:
			last_image_path = "None"
		if 'face-image' in request.FILES:
			new1.face_image = request.FILES['face-image']
			if default_storage.exists(last_face_path):
				default_storage.delete(last_face_path)
		new1.description = request.POST['description']
		new1.text = request.POST['text']
		new1.name = request.POST['name']
		if 'image' in request.FILES:
			new1.images = request.FILES['image']
			if default_storage.exists(last_image_path):
				default_storage.delete(last_image_path)
		new1.save()
		return redirect('/news/'+id)
	return render(request, 'news-edit.html', {'new':new1})

@login_required(login_url='/login')
def projectedit(request, pk):
	projectobj = get_object_or_404(project, id=pk)
	form = ProjectForm(instance=projectobj)
	print(form)
	formimg = Projectimageform()
	if request.method == 'POST':
			form = ProjectForm(request.POST,{"id":pk}, instance=projectobj)
			print(form.errors)
			if form.is_valid():
				form.save()
				return redirect("/project/"+pk)
	projects = project.objects.all()
	page = None
	images = projectimage.objects.filter(project_id=pk)
	files = projectfile.objects.filter(project_id=pk)
	members = None
	for i in projects:
		if str(i.id) == pk:
			if request.user != i.host:
				return render(request, 'notallowed.html')
			page = i
			members = projectmember.objects.filter(project_id=i.id)
	return render(request, 'project-edit.html', {'project':page, 'images':images, 'files':files, 'members':members, 'pk':pk, 'form':form, "formimg":formimg})

@login_required(login_url='/login')
def deleteimg(request, pk, id):
	img = get_object_or_404(projectimage, id=id)
	if request.user != img.project_id.host:
		return render(request, 'notallowed.html')
	img.delete()
	return redirect('/project/edit/'+pk)
def deleteskill(request, pk, id):
	skill = get_object_or_404(Skills, id=id)
	if request.user != skill.host:
		return render(request, 'notallowed.html')
	skill.delete()
	return redirect('/profile/'+pk)

@login_required(login_url='/login')
def deletenews(request, id):
	new = get_object_or_404(News, id=id)
	if request.user.is_superuser:
		pass
	else:
		if request.user != new.user:
			return render(request, 'notallowed.html')
	new.delete()
	return redirect('/news')
	
@login_required(login_url='/login')
def deletefile(request, pk, id):
	file = get_object_or_404(projectfile, id=id)
	if request.user != file.project_id.host:
		return render(request, 'notallowed.html')
	file.delete()
	return redirect('/project/edit/'+pk)

@login_required(login_url='/login')
def deletemember(request, pk, id):
	member = get_object_or_404(projectmember, id=id)
	if request.user != member.project_id.host:
		return render(request, 'notallowed.html')
	member.delete()
	return redirect('/project/edit/'+pk)

@login_required(login_url='/login')
def deleteproject(request, pk):
	projects = get_object_or_404(project, id=pk)
	if request.user != projects.host:
		return render(request, 'notallowed.html')
	projects.delete()
	return redirect('/profile/'+str(projects.host))

@login_required(login_url='/login')
def newscreate(request):
	if request.method == "POST":
		create = News(user=request.user, face_image=request.FILES['face-image'], description=request.POST['description'], name=request.POST['name'], text=request.POST['text'], images=request.FILES['image'])
		create.save()
		return redirect('/news')
	return render(request, 'news-create.html')

@login_required(login_url='login')
def projectcreate(request):
	form = ProjectForm()
	user = request.user
	if request.method == 'POST':
			form = ProjectForm(request.POST, request.FILES)
			print(form.errors)
			if form.is_valid():
				form.save()
				return redirect("/profile/"+str(request.user))
	return render(request, 'project-create.html', {"form":form, "host":user})
def about(request):
	return render(request, 'about.html')
def contact(request):
	return render(request, 'contact.html')