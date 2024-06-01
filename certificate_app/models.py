from django.db import models
from django.utils import timezone


# Model representing different authorities.
class Authority(models.Model):
    auth_id = models.IntegerField(null=True)
    organization = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    designation = models.CharField(max_length=255)
    signature = models.ImageField(upload_to='signatures/')
    
    def __str__(self):
        return self.name


# Model representing different courses.
class Course(models.Model):
    course_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.course_name if self.course_name else ''
    
    class Meta:
        verbose_name ="Courses of Certificates"
        verbose_name_plural = "Courses of Certificates"



# Model representing different types of certificates.
class CertificateTypes(models.Model):
    certify_type_id=models.IntegerField(null=True)
    certificate_type = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, related_name='certificate_types')
    
    def __str__(self):
        course_list = ', '.join([course.course_name for course in self.courses.all()])
        return f"{self.certificate_type} - Courses: {course_list}"

    def get_certificate(self):
        self.certificate_type

    class Meta:
        verbose_name ="Certificate Types"
        verbose_name_plural = "Certificate Types"



# model for partner that related to tronix
class Partner(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='media/partners/')  # Field to store partner logo images
    width = models.FloatField(default=80)  # Field to store the width of the logo
    height = models.FloatField(default=40)  # Field to store the height of the logo

    def __str__(self):
        return self.name
    
    


# model representing items of tronix
class TronixItems(models.Model):
    items =models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.items
    
    class Meta:
        verbose_name ="Tronix items"
        verbose_name_plural = "Tronix Items"





# model for tronix details
class Tronix(models.Model):
    season = models.CharField(max_length=100, null=True)
    date = models.DateField(default=timezone.now)
    item = models.ForeignKey(TronixItems, on_delete=models.CASCADE, null=True)
    partner_logos = models.ManyToManyField(Partner)  # Field to associate partner logos with each student
    
    def __str__(self):
        return self.season
    
    def get_partners(self):
        """
        Get partners associated with this Tronix season.
        """
        return self.partner_logos.all()

    class Meta:
        verbose_name ="Tronix Certificate "
        verbose_name_plural = "Tronix Certificate"


# model for student of tronix
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
    
    class Meta:
        verbose_name ="Student Tronix Data"
        verbose_name_plural = "Student Tronix Data"


# model for student of  workshop
class StudentWorkshop(models.Model):
    name = models.CharField(max_length=255, blank=True, default='')
    college_name = models.CharField(max_length=255, blank=True, default='')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    mentor_name = models.CharField(max_length=255, blank=True, default='')
    issued_date = models.DateField(default=timezone.now)
    certificate_type = models.ForeignKey(CertificateTypes, on_delete=models.CASCADE, related_name='student', null=True)
    course= models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_student', null=True)
    created_at = models.DateTimeField( default=timezone.now)  # Add this field to store creation time
    certificate_number = models.CharField(max_length=20, null=True, blank=True)  # Changed field name to certificate_number

    def save(self, *args, **kwargs):
        # Set issued_date to the current date if it's not already set
        if not self.issued_date:
            self.issued_date = timezone.now().date()
        if not self.pk:  # If the instance is being created (not updated)
            self.created_at = self.issued_date  # Set created_at to issued_date
        super().save(*args, **kwargs)


    def get_certificatenumber(self):
        if self.certificate_number:
            return True  # Certificate is valid
        else:
            return False  # Certificate is invalid    

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name ="Student Workshop Data"
        verbose_name_plural = "Student Workshop Data"
    

# model for student of internship and workshop
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


    def get_certificatenumber(self):
        if self.certificate_number:
            return True  # Certificate is valid
        else:
            return False  # Certificate is invalid    

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name ="Student Internship Data"
        verbose_name_plural = "Student Internship Data"
  

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
    
    class Meta:
        verbose_name ="Student IV Data"
        verbose_name_plural = "Student IV Data"
  

# Model representing the relationship between students and authorities.
class StudentRelatedAuthority(models.Model):
    std = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    std_workshop = models.ForeignKey(StudentWorkshop, on_delete=models.CASCADE, null=True)
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



