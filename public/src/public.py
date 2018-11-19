import os
import sys
from logging import basicConfig, INFO, getLogger

from flask import Flask, Blueprint, redirect, url_for
from flask import render_template


basicConfig(format='%(asctime)s %(levelname)s [%(process)d/%(threadName)s %(pathname)s:%(lineno)d]: %(message)s',
            stream=sys.stderr, level=INFO)


logger = getLogger('makeradmin')


class Section(Blueprint):
    
    def __init__(self, name):
        super().__init__(name, name)
        self.context_processor(lambda: dict(url=self.url))

    def url(self, path):
        return f"/{self.name}{path}"

    def route(self, path, **kwargs):
        return super().route(self.url(path), **kwargs)


shop = Section("shop")


@shop.route("/")
def home() -> str:
    return render_template("shop.html")


@shop.route("/cart")
def cart() -> str:
    return render_template("cart.html")


@shop.route("/register")
def register_member():
    return render_template("register.html")


@shop.route("/member/history")
def purchase_history():
    return render_template("history.html")


@shop.route("/product/<product_id>")
def product_view(product_id: int):
    return render_template("product.html", product_id=product_id)


@shop.route("/product/<int:product_id>/edit")
def product_edit(product_id: int):
    return render_template("product_edit.html", product_id=product_id)


@shop.route("/product/create")
def product_create() -> str:
    return render_template("product_edit.html", product_id=0)


@shop.route("/receipt/<int:transaction_id>")
def receipt(transaction_id: int):
    return render_template("receipt.html", transaction_id=transaction_id)


@shop.route("/statistics")
def statistics() -> str:
    return render_template("statistics.html")


member = Section("member")


@member.route("/")
def show_member():
    return render_template("member.html")


@member.route("/login/<string:token>")
def login(token):
    return render_template("login.html", token=token)


app = Flask(__name__, static_url_path="/static", static_folder="../static")
app.register_blueprint(shop)
app.register_blueprint(member)


@app.route("/")
def root():
    return redirect(url_for("member.show_member"))


api_base_url = os.environ["HOST_BACKEND"]
if not api_base_url.startswith("http"):
    api_base_url = "https://" + api_base_url


@app.context_processor
def context():
    return dict(
        STATIC="/static",
        meta=dict(
            api_base_url=api_base_url,
            stripe_public_key=os.environ["STRIPE_PUBLIC_KEY"],
        )
    )