from django.conf import settings
from django.http import FileResponse, Http404


def home(request, page='home'):
    pages = {'home': 'index.html', 'products': 'products/index.html', 'support': 'support/index.html', 'contact': 'contact/index.html', 'about': 'about/index.html'}
    if page not in pages:
        raise Http404('页面不存在。')
    index = settings.BASE_DIR / 'frontend' / 'dist' / pages[page]
    if not index.is_file():
        raise Http404('请先构建 Vue 前端：在 frontend 目录运行 pnpm build。')
    return FileResponse(index.open('rb'), content_type='text/html; charset=utf-8')


from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from .forms import InquiryForm
import json
from .models import Product


@require_http_methods(['GET'])
def products(request):
    items = [{
        'id': item.pk, 'name': item.name, 'type': item.category,
        'code': item.code, 'desc': item.description,
        'features': [line.strip() for line in item.features.splitlines() if line.strip()],
        'selection_notes': item.selection_notes,
        'image': item.image.url if item.image else '',
    } for item in Product.objects.filter(is_published=True)]
    response = JsonResponse({'products': items})
    response['Cache-Control'] = 'no-store'
    return response


@ensure_csrf_cookie
@require_http_methods(['GET', 'POST'])
def inquiries(request):
    if request.method == 'GET':
        return JsonResponse({'ready': True, 'csrf_token': get_token(request)})
    if request.content_type != 'application/json':
        return JsonResponse({'message': '请使用 application/json 提交需求。'}, status=415)
    try:
        data = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({'message': '请求格式不正确。'}, status=400)
    if not isinstance(data, dict):
        return JsonResponse({'message': '请求格式不正确。'}, status=400)
    form = InquiryForm(data)
    if not form.is_valid():
        return JsonResponse({'message': '请检查表单信息。', 'errors': form.errors.get_json_data()}, status=400)
    inquiry = form.save()
    return JsonResponse({'message': '需求已提交成功。', 'id': inquiry.pk}, status=201)
