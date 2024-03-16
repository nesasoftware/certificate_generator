from django.db import models
from django.utils import timezone

class Student(models.Model): 
    name = models.CharField(max_length=255, blank=True, default='')
    college_name = models.CharField(max_length=255, blank=True, default='')
    
    COURSE_CHOICES = [  
        ('embedded system', 'Embedded System'),
        ('python fullstack', 'Python Fullstack'),
        ('AI & ML', 'Artificial Intelligence & Machine Learning'),
        ('data science', 'Data Science'),
        ('digital marketing', 'Digital Marketing')
    ]
    
    course = models.CharField(max_length=100, choices=COURSE_CHOICES, blank=True, default='')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    mentor_name = models.CharField(max_length=255, blank=True, default='')

    