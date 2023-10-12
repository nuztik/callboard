from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse



class Post(models.Model):
    Tanks = 'TN'
    Healers = 'HL'
    DD = 'DD'
    Merchants = 'ME'
    GuildMasters = 'GM'
    QuestGivers = 'QG'
    Blacksmiths = 'BS'
    Tanners = 'TS'
    PotionMakers = 'PM'
    SpellMasters = 'SM'

    CATEGORIES = [
        (Tanks, 'Танки'),
        (DD, 'ДД'),
        (Healers, 'Хиллы'),
        (Merchants, 'Торговцы'),
        (GuildMasters, 'Гилдмастера'),
        (QuestGivers, 'Квестгиверы'),
        (Blacksmiths, 'Кузнецы'),
        (Tanners, 'Кожевники'),
        (PotionMakers, 'Зельевары'),
        (SpellMasters, 'Мастера заклинаний'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    context = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=2, choices= CATEGORIES)
    file = models.ImageField(upload_to='media/', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('post', args=[str(self.pk)])

    def __str__(self):
        return f'{self.title}: {self.category}: {self.context[:50]}: {self.file}: {self.author}'



class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='reply', on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    context = models.TextField()
    accept = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('r_update', args=[str(self.pk)])

    def __str__(self):
        return f'{self.context}: {self.author}: {self.data}'