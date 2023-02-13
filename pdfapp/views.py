from django.shortcuts import render
from django.http import FileResponse

import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.

def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        tgk_content = myfile.read().decode("utf-8")	

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter, bottomup=0)

        textobj = c.beginText()
        textobj.setTextOrigin(inch, inch)
        textobj.setFont("Courier", 10)

        lines = tgk_content.split("\n")
        for line in lines:
             textobj.textLine(line)

        img_file = 'static/pdfapp/header.jpg'
        x_start = 400
        y_start = 0
        c.drawImage(img_file, x_start, y_start, width=200, preserveAspectRatio=True)    

        c.drawText(textobj)  
        c.showPage()
        c.save()
        buffer.seek(0)
             
        new_name = myfile.name.replace('.tgk','.pdf')     
        return FileResponse(buffer, as_attachment=True, filename=new_name)
             
#        return render(request, 'pdfapp/index.html', {'tgk_content': tgk_content})

    return render(request, 'pdfapp/index.html', {})