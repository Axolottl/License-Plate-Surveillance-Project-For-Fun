from django.db import models

class Data(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name

class MapData(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f'{self.latitude}, {self.longitude}'

class AgentKeys(models.Model):
    key = models.CharField(max_length=100)
    agent = models.CharField(max_length=100)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.agent

class AgentData(models.Model):
    agent = models.CharField(max_length=100)
    data = models.CharField(max_length=100)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.agent
    