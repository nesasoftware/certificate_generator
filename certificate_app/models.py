from django.db import models
from django.utils import timezone

class Student(models.Model): 
    name = models.CharField(max_length=255,blank=True, default='')
    college_name = models.CharField(max_length=255, blank=True, default='')
    
    COURSE_CHOICES = [  
        ('embedded_system', 'Embedded System'),
        ('python_fullstack', 'Python Fullstack'),
        ('AI_ML', 'Artificial Intelligence & Machine Learning'),
        ('data_science', 'Data Science'),
        ('digital_marketing', 'Digital Marketing')
    ]
    
    course = models.CharField(max_length=100, choices=COURSE_CHOICES, blank=True, default='')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    mentor_name = models.CharField(max_length=255, blank=True, default='')

    