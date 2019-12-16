from flask import redirect, render_template, url_for, request
from flask.views import MethodView
from flask_login import current_user, login_required

from app.models.order import Order
from app.models.product import Product

#移交中 領收中 已完成 已取消 全部
ORDER_STATUS = {"TRANSFERING" : "0", "RECEIPTING" : "1", "COMPLETE" : "2", "CANCEL" : "3", "ALL" : "4"}
class OrderListView(MethodView):
    def get(self):
        products = Product.objects(seller_id=current_user.id)

        status = request.args.get('status')
        if status == ORDER_STATUS['TRANSFERING']:
            orders = Order.objects(product_id__in=products, status=ORDER_STATUS["TRANSFERING"])
        elif status == ORDER_STATUS['RECEIPTING']:
            orders = Order.objects(product_id__in=products, status=ORDER_STATUS["RECEIPTING"])
        elif status == ORDER_STATUS['COMPLETE']:
            orders = Order.objects(product_id__in=products, status=ORDER_STATUS["COMPLETE"])
        elif status == ORDER_STATUS['CANCEL']:
            orders = Order.objects(product_id__in=products, status=ORDER_STATUS["CANCEL"])
        else:
            status = ORDER_STATUS["ALL"]
            orders = Order.objects(product_id__in=products)

        orders = sorted(orders, key=lambda k: k.create_time, reverse=False)

        return render_template('user/selling/order.html', orders=orders, ORDER_STATUS=ORDER_STATUS, status=status)
    def post(self):
        products = Product.objects(seller_id=current_user.id)

        status = request.args.get('status')
        if status == ORDER_STATUS['TRANSFERING']:
            orders = Order.objects(product_id__in=products, status=ORDER_STATUS["TRANSFERING"])
        elif status == ORDER_STATUS['RECEIPTING']:
            orders = Order.objects(product_id__in=products, status=ORDER_STATUS["RECEIPTING"])
        elif status == ORDER_STATUS['COMPLETE']:
            orders = Order.objects(product_id__in=products, status=ORDER_STATUS["COMPLETE"])
        elif status == ORDER_STATUS['CANCEL']:
            orders = Order.objects(product_id__in=products, status=ORDER_STATUS["CANCEL"])
        else:
            status = ORDER_STATUS["ALL"]
            orders = Order.objects(product_id__in=products)

        orders = sorted(orders, key=lambda k: k.create_time, reverse=False)

        return render_template('user/selling/order.html', orders=orders, ORDER_STATUS=ORDER_STATUS, status=status)

