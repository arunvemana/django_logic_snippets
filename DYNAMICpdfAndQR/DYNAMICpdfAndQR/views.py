from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from .utils import render_to_pdf #created in step 4
import datetime
import random
import qrcode
from django.conf import settings
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        tempalte = get_template('invoice.html')
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border = 4,
        )
        qr.add_data('website:-https://thisdomain.com/pdf/')
        qr.make(fit=True)
        path = f"{settings.MEDIA_ROOT}qrimage_{random.randint(0,10)}.png"
        img = qr.make_image(fill_color ="black", back_color="white")
        img.save(path)
        data = {
             'today': datetime.date.today(), 
             'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'invoice_id': 1233434,
            'image_url':path
        }
        pdf = render_to_pdf('invoice.html', data)
        # force download
        
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"Invoce_{random.randint(0,100)}.pdf"
            # to save manumal
            content = f"inline; filename='{filename}'"
            download = request.GET.get("download")
            if download:
                # to download when the parameter contain download
                content = f"attachment; filename='{filename}'"
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
        # html = tempalte.render(data)
        # return HttpResponse(html)