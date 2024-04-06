from django.db import models
from django.utils import timezone


class Authority(models.Model):
    auth_id = models.IntegerField(null=True)
    organization = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    designation = models.CharField(max_length=255)
    signature = models.ImageField(upload_to='signatures/')
    
    def __str__(self):
        return self.name


class Course(models.Model):
    course_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.course_name if self.course_name else ''


class CertificateTypes(models.Model):
    certify_type_id=models.IntegerField(null=True)
    certificate_type = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, related_name='certificate_types')
    
    def __str__(self):
        course_list = ', '.join([course.course_name for course in self.courses.all()])
        return f"{self.certificate_type} - Courses: {course_list}"

class Student(models.Model): 
    name = models.CharField(max_length=255, blank=True, default='')
    college_name = models.CharField(max_length=255, blank=True, default='')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    mentor_name = models.CharField(max_length=255, blank=True, default='')
    issued_date = models.DateField(default=timezone.now)
    certificate_type = models.ForeignKey(CertificateTypes, on_delete=models.CASCADE, related_name='students', null=True)
    course= models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_students', null=True)
    created_at = models.DateTimeField( default=timezone.now)  # Add this field to store creation time
    
    def save(self, *args, **kwargs):
        # Set issued_date to the current date if it's not already set
        if not self.issued_date:
            self.issued_date = timezone.now().date()
        if not self.pk:  # If the instance is being created (not updated)
            self.created_at = self.issued_date  # Set created_at to issued_date
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class StudentRelatedAuthority(models.Model):
    std = models.ForeignKey(Student, on_delete=models.CASCADE)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)

    def __str__(self):
        return self.std
    

# class StudentRelatedCourse(models.Model):
#     std = models.ForeignKey(Student, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.std
   

    # COURSE_CHOICES = [  
    #     ('embedded system', 'Embedded System'),
    #     ('python fullstack', 'Python Fullstack'),
    #     ('AI & ML', 'Artificial Intelligence & Machine Learning'),
    #     ('data science', 'Data Science'),
    #     ('digital marketing', 'Digital Marketing')
    # ]
    
    # course = models.CharField(max_length=100, choices=COURSE_CHOICES, blank=True, default='')
    # student_id = models.CharField(max_length=50, unique=True, editable=False)



