from flask import redirect, render_template, url_for, request
from flask.views import MethodView
from flask_login import current_user, login_required
from wtforms import SubmitField, TextAreaField, HiddenField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, ValidationError

from app.models.order import Order
from app.models.product import Product

#移交中 領收中 已完成 已取消 全部
ORDER_STATUS = {"TRANSFERING" : "0", "RECEIPTING" : "1", "COMPLETE" : "2", "CANCEL" : "3", "ALL" : "4"}
class PurchaseListView(MethodView):
    def get(self):
        form = PerchaseListForm()
        status = request.args.get('status')

        '''test = Order.objects.aggregate(*[
            {
                '$lookup':
                {
                    'from': 'Product',
                    'localField': 'product_id',
                    'foreignField': 'id',
                    'as':'order2product',
                }
            },
        ])'''

        if status == ORDER_STATUS['TRANSFERING']:
            orders = Order.objects(buyer_id=current_user.id, status=ORDER_STATUS["TRANSFERING"])
        elif status == ORDER_STATUS['RECEIPTING']:
            orders = Order.objects(buyer_id=current_user.id, status=ORDER_STATUS["RECEIPTING"])
        elif status == ORDER_STATUS['COMPLETE']:
            orders = Order.objects(buyer_id=current_user.id, status=ORDER_STATUS["COMPLETE"])
        elif status == ORDER_STATUS['CANCEL']:
            orders = Order.objects(buyer_id=current_user.id, status=ORDER_STATUS["CANCEL"])
        else:
            status = ORDER_STATUS["ALL"]
            orders = Order.objects(buyer_id=current_user.id)
        print(orders)
        orders = sorted(orders, key=lambda k: k.create_time, reverse=False)


        return render_template('user/product/list.html', orders=orders, ORDER_STATUS=ORDER_STATUS, status=status, form=form)
    def post(self):
        form = PerchaseListForm()
        status = request.args.get('status')
        if status == ORDER_STATUS['TRANSFERING']:
            orders = Order.objects(buyer_id=current_user.id, status=ORDER_STATUS["TRANSFERING"])
        elif status == ORDER_STATUS['RECEIPTING']:
            orders = Order.objects(buyer_id=current_user.id, status=ORDER_STATUS["RECEIPTING"])
        elif status == ORDER_STATUS['COMPLETE']:
            orders = Order.objects(buyer_id=current_user.id, status=ORDER_STATUS["COMPLETE"])
        elif status == ORDER_STATUS['CANCEL']:
            orders = Order.objects(buyer_id=current_user.id, status=ORDER_STATUS["CANCEL"])
        else:
            status = ORDER_STATUS["ALL"]
            orders = Order.objects(buyer_id=current_user.id)
        #print(orders)
        orders = sorted(orders, key=lambda k: k.create_time, reverse=False)
        if form.validate_on_submit() and 'score' in request.form:   #correct
            order = Order.objects(product_id=request.values['commentProductID']).first()  # correct
            order.seller_comment = form.detail      # correct
            order.seller_rating = request.values['score']  # correct
            order.status = ORDER_STATUS['COMPLETE']
            order.save()
            print(request.values['score'])   
             
        return render_template('user/product/list.html', orders=orders, ORDER_STATUS=ORDER_STATUS, status=status, form=form)
        

# for comment
class PerchaseListForm(FlaskForm):
    detail = TextAreaField("評論", render_kw={'rows': 7}, validators=[InputRequired(), Length(max=4000)])
    submit = SubmitField('提交')
    
    