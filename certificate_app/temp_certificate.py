from reportlab.lib.units import inch
def my_temp(c):
    c.translate(inch,inch)
# define a large font
    c.setFont("Helvetica", 14)
# choose some colors
    c.setStrokeColorRGB(0.1,0.8,0.1)
    c.setFillColorRGB(0,0,1) # font colour
    c.drawImage('D:\\top2.jpg',-0.8*inch,9.3*inch) #change path
    c.drawString(0, 9*inch, "1234, ABCD Road")
    c.drawString(0, 8.7*inch, "Mycity, ZIP : 12345  ")
    c.setFillColorRGB(0,0.5,1) # font colour
    c.drawString(2*inch, 8.7*inch, " www.plus2net.com ")
    c.setFillColorRGB(0,0,0) # font colour
    c.line(0,8.6*inch,6.8*inch,8.6*inch)
    from  datetime import date
    dt = date.today().strftime('%d-%b-%Y') #current date as string
    c.drawString(5.6*inch,9.3*inch,dt) # print the date
    c.setFont("Helvetica", 8)
    c.drawString(3*inch,9.6*inch,'End Semester Examination')
    c.line(0,-0.7*inch,6.8*inch,-0.7*inch)
    c.setFillColorRGB(1,0,0) # font colour
    c.drawString(0, -0.9*inch, u"\u00A9"+" plus2net.com")
    c.rotate(45)
    c.setFillColorCMYK(0,0,0,0.08) # font colour
    c.setFont("Helvetica", 100)
    c.drawString(2*inch, 1*inch, "SAMPLE") # watermarking
    c.rotate(-45)
    return c
