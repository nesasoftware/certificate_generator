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


class Tronix_items(models.Model):
    items =models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.items


class Tronix(models.Model):
    season =models.CharField(max_length=100, null=True)
    date = models.DateField(default=timezone.now)
    item= models.ForeignKey(Tronix_items, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.season
    

class StudentTronix(models.Model):
    name= models.CharField(max_length=255, null=True)
    school= models.CharField(max_length=255, null=True)
    issued_date = models.DateField(default=timezone.now)
    place = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField( default=timezone.now)  # Add this field to store creation time
    certificate_number = models.CharField(max_length=20, null=True, blank=True)  # Changed field name to certificate_number
    tronix_details = models.ForeignKey(Tronix, on_delete=models.CASCADE, null=True)
    certificate_type = models.ForeignKey(CertificateTypes, on_delete=models.CASCADE, null=True)
    position = models.CharField(max_length=255, null=True)

    def save(self, *args, **kwargs):
        # Set issued_date to the current date if it's not already set
        if not self.issued_date:
            self.issued_date = timezone.now().date()
        if not self.pk:  # If the instance is being created (not updated)
            self.created_at = self.issued_date  # Set created_at to issued_date
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name


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
    certificate_number = models.CharField(max_length=20, null=True, blank=True)  # Changed field name to certificate_number

    def save(self, *args, **kwargs):
        # Set issued_date to the current date if it's not already set
        if not self.issued_date:
            self.issued_date = timezone.now().date()
        if not self.pk:  # If the instance is being created (not updated)
            self.created_at = self.issued_date  # Set created_at to issued_date
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
  

# model for Student of industrial visit(iv)
class StudentIV(models.Model):
    name = models.CharField(max_length=255, blank=True, default='')
    sem_year =models.CharField(max_length=100, blank=True, default='')
    dept =models.CharField(max_length=255, blank=True, null=True, default='')
    college_name = models.CharField(max_length=255, blank=True, default='')
    duration = models.CharField(max_length=255, blank=True, default='')
    mentor_name = models.CharField(max_length=255, blank=True, default='')
    conducted_date = models.DateField(default=timezone.now)
    issued_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField( default=timezone.now)  # Add this field to store creation time
    certificate_type = models.ForeignKey(CertificateTypes, on_delete=models.CASCADE,  null=True)
    course= models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    certificate_number = models.CharField(max_length=20, null=True, blank=True)  # Changed field name to certificate_number

    
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
    std = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    std_iv = models.ForeignKey(StudentIV, on_delete=models.CASCADE, null=True)
    std_tronix = models.ForeignKey(StudentTronix, on_delete=models.CASCADE, null=True)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, null=True)

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



