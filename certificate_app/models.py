from django.db import models
from django.utils import timezone


class Authority(models.Model):
    organization = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    designation = models.CharField(max_length=255)
    signature = models.ImageField(upload_to='signatures/')
    
    def __str__(self):
        return self.name
    


class Course(models.Model):
    course_name = models.CharField(max_length=100)

    def __str__(self):
        return self.course_name



class CertificateTypes(models.Model):
    certificate_type = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, related_name='certificate_types')
    authorities = models.ManyToManyField(Authority, related_name='certificate_types')

    def __str__(self):
        return self.certificate_type
    


class Student(models.Model): 
    name = models.CharField(max_length=255, blank=True, default='')
    college_name = models.CharField(max_length=255, blank=True, default='')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    mentor_name = models.CharField(max_length=255, blank=True, default='')
    issued_date = models.DateField(default=timezone.now)
    certificate_type = models.ForeignKey(CertificateTypes, on_delete=models.CASCADE, related_name='students', default=None)
    authorities = models.ManyToManyField(Authority, related_name='students') 
    
    def save(self, *args, **kwargs):
        # Set issued_date to the current date if it's not already set
        if not self.issued_date:
            self.issued_date = timezone.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    # COURSE_CHOICES = [  
    #     ('embedded system', 'Embedded System'),
    #     ('python fullstack', 'Python Fullstack'),
    #     ('AI & ML', 'Artificial Intelligence & Machine Learning'),
    #     ('data science', 'Data Science'),
    #     ('digital marketing', 'Digital Marketing')
    # ]
    
    # course = models.CharField(max_length=100, choices=COURSE_CHOICES, blank=True, default='')
    # student_id = models.CharField(max_length=50, unique=True, editable=False)

    # def save(self, *args, **kwargs):
    #     # Generate the student ID in the format SRC/year/id
    #     current_year = timezone.now().strftime("%Y")
    #     last_student = Student.objects.last()
    #     if last_student:
    #         last_id = int(last_student.student_id.split('/')[-1]) + 1
    #     else:
    #         last_id = 1
    #     self.student_id = f'SRC/{current_year}/{last_id:04d}'
    #     super().save(*args, **kwargs)


