
""" ## explantion -->
# 👉 AbstractUser means:You are creating your own user model it already has: username, email, password.
### 🍔 ConsumeCalories: This stores what user eats. Fields: item_name → food name, calorie → calories, consumed_by → which user, created_by → date. Relationship: ForeignKey(User) 👉 Means: One user → many food entries. """
""" Think:
User	Food
Rony	Rice
Rony	Egg
Rony	Apple

👉 One user → many foods
👉 Each food → one user

🔧 Now break each part
1️⃣ ForeignKey(User)

👉 This creates a many-to-one relationship

Many ConsumeCalories → one User

✔ Like:

Food → belongs to → User """



from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'
    
    
class BasicInfoModel(models.Model):
    GENDER_TYPE =[
        ('Male','Male'),
        ('Female','Female'),
    ]
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_info',
        null=True,
    )
    
    name=models.CharField(max_length=100,null=True)
    age=models.PositiveIntegerField(null=True)
    gender= models.CharField(max_length=10, null=True, choices=GENDER_TYPE)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    bmr=models.FloatField(null=True)
    def __str__(self):
        return f'{self.name}'
    
class ConsumedCalories(models.Model):
    item_name= models.CharField(max_length=200,null=True)
    calorie = models.FloatField(null=True)
    created_by=models.DateField(auto_now_add=True,null=True)
    consumed_by=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='user_calorie'
    )
    def __str__(self):
        return f'{self.item_name}-{self.consumed_by.username}'