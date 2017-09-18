from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormMixin
from django.conf import settings

from products.models import Variation
from .models import Cart, CartItem
from orders.models import UserCheckout, Order, UserAddress
from orders.forms import GuestCheckoutForm

from orders.mixins import CartOrdermixin
# Create your views here.


class CartView(SingleObjectMixin, View):
    model = Cart
    template_name = "carts/view.html"

    def get_object(self, *args, **kwargs):
        # This will end the session when the user closes their browser.
        self.request.session.set_expiry(0)
        cart_id = self.request.session.get("cart_id")
        if cart_id == None:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart.id
        cart = Cart.objects.get(id=cart_id)
        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        item_id = request.GET.get("item")
        # Default for deleted items will be set to False.
        delete_item = request.GET.get("delete", False)
        item_added = False  # Default for added items
        if item_id:
            item_instance = get_object_or_404(Variation, id=item_id)
            # Giving the quantity a default value of 1
            qty = request.GET.get("qty", 1)
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                raise Http404
            # We will either have a created item, or an item that is already in the cart
            cart_item, created_item = CartItem.objects.get_or_create(
                cart=cart, item=item_instance)
            if created_item:
                item_added = True  # If a new item is added to the cart it will return as True
            if delete_item:
                cart_item.delete()
            else:
                cart_item.quantity = qty
                cart_item.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse("cart"))
        if request.is_ajax():  # If an AJAX call happens then...
            # Then print out what the request gives back
            print(request.GET.get("item"))
            try:
                total = cart_item.line_item_total
            except:
                total = None
            try:
                subtotal = cart_item.cart_subtotal
            except:
                subtotal = None
            data = {
                "deleted": delete_item,
                "item_added": item_added,
                "line_total": total,
                "subtotal": subtotal,
                "cart_total": cart_total,
                "tax_total": tax_total,
                "total_items": total_items,
            }
            return JsonResponse(data)  # Return a JSON Response.
        context = {
            "object": self.get_object()
        }
        template = self.template_name
        return render(request, template, context)


class CheckoutView(CartOrdermixin,FormMixin, DetailView):
    model = Cart
    template_name = "carts/checkout_view.html"
    form_class = GuestCheckoutForm

    # def get_order(self, *args, **kwargs):
    #     cart = self.get_object()
    #     new_order_id = self.request.session.get("order_id")
    #     if new_order_id is None:
    #         new_order = Order.objects.create(cart=cart)
    #         self.request.session["order_id"] = new_order.id
    #     else:
    #         new_order = Order.objects.get(id=new_order_id)
    #     return new_order

    def get_object(self, *args, **kwargs):
        cart = self.get_cart()
        if cart == None:
            return None
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        user_can_continue = False
        user_check_id = self.request.session.get("user_checkout_id")
        # or if request.user.is_guest:
        if not self.request.user.is_authenticated() or user_check_id == None:
            context["login_form"] = AuthenticationForm()
            context["next_url"] = self.request.build_absolute_uri()
        elif self.request.user.is_authenticated() or user_check_id != None:
            user_can_continue = True
            # return redirect "address select view"
        else:
            pass
        if self.request.user.is_authenticated():
            user_checkout, created = UserCheckout.objects.get_or_create(
                email=self.request.user.email)
            user_checkout.user = self.request.user
            user_checkout.save()
            self.request.session["user_checkout_id"] = user_checkout.id

        elif not self.request.user.is_authenticated() and user_check_id == None:
            context["login_form"] = AuthenticationForm()
            context["next_url"] = self.request.build_absolute_uri()
        else:
            pass
        if user_check_id != None:
            user_can_continue = True
        # This will allow use to show the order in the html.
        context["order"] = self.get_order()
        context["user_can_continue"] = user_can_continue
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user_checkout, created = UserCheckout.objects.get_or_create(
                email=email)
            request.session["user_checkout_id"] = user_checkout.id
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("checkout")

    def get(self, request, *args, **kwargs):
        get_data = super(CheckoutView, self).get(request, *args, **kwargs)
        cart = self.get_object()
        if cart == None:
            return redirect("cart")
        new_order = self.get_order()
        user_checkout_id = request.session.get("user_checkout_id")
        if user_checkout_id != None:
            user_checkout = UserCheckout.objects.get(id=user_checkout_id)
            if new_order.billing_address == None or new_order.shipping_address == None:
                return redirect("address_form")
            new_order.user = user_checkout
            new_order.save()
        return get_data

import stripe
stripe.api_key = settings.STRIPE_API_KEY
class CheckoutFinalView(CartOrdermixin,View):
    def post(self,request,*args,**kwargs):
        order = self.get_order()
        token = request.POST.get("stripeToken")
        # print(token)
        if token is not None:
            order.mark_completed()
            del request.session["cart_id"]
            del request.session["order_id"]
            charge = stripe.Charge.create(
              amount=order.order_total_in_cents,
              currency="usd",
              description="Two Decades Order #{}".format(order.id),
              source=token,
            )
            # print(charge)
        return redirect("checkout")

    def get(self,request,*args,**kwargs):
        """This GET call will redirect us back to the checkout URL
        otherwise we would raise a 405 Forbidden Error"""
        return redirect("checkout")
