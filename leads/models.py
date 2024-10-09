from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator



class User(AbstractUser):
    #userprofile : this attribute exists/accessible technically because of the OneToMany bi diretional nature
    #agent : same reason
    is_organizor = models.BooleanField(default=True)#organizors(yes it is miss spelled too late now haha) can see and manage agents and leads
    is_agent = models.BooleanField(default=False)#agents who are not organizors can read leads only



class UserProfile(models.Model):
    '''Model definition for UserProfile.'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)#now both this class and User can access each other

    class Meta:
        '''Meta definition for UserProfile.'''

        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

    def __str__(self):
        return self.user.email
    




class Lead(models.Model):
    '''Model definition for Lead.'''
    first_name = models.CharField(null=False, blank=False, max_length=50)
    last_name = models.CharField(null=False, blank=False, max_length=50)  
    age = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    email = models.EmailField(blank=True,null=True, max_length=254)
    description = models.TextField(blank=True,null=True,)
    date_added = models.DateField(blank=True,null=True,auto_now_add=True)
    phone_number = models.CharField(blank=True, null=True, max_length=8)
    
    agent = models.ForeignKey("Agent",null=True, blank=True, on_delete=models.SET_NULL)#when a related agent is gone its leads remain but his fk is sset to null
    organization =  models.ForeignKey(UserProfile, on_delete=models.CASCADE)#to keep track since agent is nullable
    category = models.ForeignKey("Category",null=True, blank=True, on_delete=models.SET_NULL)


    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    """     def fix_age(self):
            '''Ensure age is not negative.'''
            if self.age < 0:
                self.age = 0

        def save(self, *args, **kwargs):
            '''Override the save method to fix age before saving.'''
            self.fix_age()
            super().save(*args, **kwargs) """



class Agent(models.Model):
    '''Model definition for Agent.'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization =  models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'

    def __str__(self):
        return self.user.username
    

#to automate the creation of a OneToOne userprofile when a user instance is created
def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print(f'userprofile(organisation) named {instance.username} has been created')


post_save.connect(post_user_created_signal, sender=User)# when an instance of user model is saved  method gets triggered



class Category(models.Model):
    '''Model definition for Category.'''
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        '''Meta definition for Category.'''

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
       return self.name
    
