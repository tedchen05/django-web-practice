import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from webapp.utils.home import get_navigation
from webapp.utils.invoice import (
    get_captcha_text,
    fill_login_form,
    select_invoice_date,
    crawl_pages,
    init_driver, invoices_to_dict
)

@login_required(login_url='/')
def invoice(request):
    nav_items = get_navigation()
    data = { 'nav_items': nav_items}
    return render(request, 'webapp/invoice.html', data)

def invoice_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        headless = data.get('headless')
        startDate = data.get('startDate')
        endDate = data.get('endDate')

        # 檢查日期格式是否正確
        try:
            start_dt = datetime.strptime(startDate, "%Y-%m-%d")
            end_dt = datetime.strptime(endDate, "%Y-%m-%d")
        except ValueError:
            return JsonResponse({'status': 'error', 'message': '日期格式錯誤'})

        # 檢查是否同一個月
        if start_dt.year != end_dt.year or start_dt.month != end_dt.month:
            return JsonResponse({'status': 'error', 'message': '起始日期與結束日期須為同一個月'})

        # 計算允許查詢的最早月份
        today = datetime.today()
        month = today.month
        year = today.year

        if month % 2 == 0:  # 雙月
            min_month = month - 7  # 最近4期
        else:  # 單月
            min_month = month - 8  # 最近5期

        if min_month <= 0:
            min_month += 12
            year -= 1

        min_date = datetime(year, min_month, 1)

        # 檢查 startDate 是否早於允許的最早日期
        if start_dt < min_date:
            return JsonResponse({'status': 'error', 'message': f'起始日期早於允許的查詢範圍 {min_date.strftime("%Y-%m-%d")}'})

        try:
            # 初始化
            driver = init_driver(headless)
            # 擷取驗證碼
            captcha_text = get_captcha_text(driver)
            # 填寫登入表單
            login_result = fill_login_form(driver, username, password, captcha_text)

            if login_result is not True:
                driver.quit()
                return JsonResponse({'status': 'error', 'message': login_result})

            select_invoice_date(driver, startDate, endDate)
            invoice_data = crawl_pages(driver)

            result = invoices_to_dict(invoice_data)
            return JsonResponse({'status': 'success', 'data': result})

        except Exception as e:
            driver.quit()
            return JsonResponse({'status': 'error', 'message': str(e)})
