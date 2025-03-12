from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime

def generate_report(username):
    file_name = f"{username}_report_{datetime.date.today()}.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4

    c.drawString(100, height - 100, f"Report for {username}")
    c.drawString(100, height - 120, "Date: " + str(datetime.date.today()))
    c.drawString(100, height - 140, "Total Active Time: X seconds")  # اجمع الوقت الفعلي هنا

    c.save()
    return file_name
