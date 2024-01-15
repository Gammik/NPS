from django.forms import ModelForm, Textarea, TextInput
from .models import project, projectfile, projectimage, projectmember, profile

class ProjectForm(ModelForm):
	class Meta:
		model = project
		fields = "__all__"
		widgets = {
            'description': Textarea(attrs={
                'style': 'width: 100%; height: 50%',
					 'class': 'autoresize'
                }),
				'date': TextInput(attrs={
					'style':'width: 95%'
				}),
				'Website': TextInput(attrs={
					'style':'width: 95%'
				}),
				'time': TextInput(attrs={
					'style':'width: 95%'
				}),
				'profit': TextInput(attrs={
					'style':'width: 95%'
				}),
				'cost': TextInput(attrs={
					'style':'width: 95%'
				}),
				'category': TextInput(attrs={
					'style':'width: 95%'
				}),
				'name': TextInput(attrs={
					'style':'margin-top: 20px'
				}),
        }
class Projectfileform(ModelForm):
	class Meta:
		model = projectfile
		fields = "__all__"
class Projectimageform(ModelForm):
	class Meta:
		model = projectimage
		fields = '__all__'
class Projectmemberform(ModelForm):
	class Meta:
		model = projectmember
		fields = '__all__'
class profileimg(ModelForm):
	class Meta:
		model = profile
		fields = ('profile_image',)