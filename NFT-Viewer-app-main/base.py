from flask import Flask, render_template, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from nft_policy_router import create_dict
from nft_policy_router import get_img_id
from nft_policy_router import nft_dict
from api_calls import ada_price_api, price_api
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

class InfoForm(FlaskForm):
    wallet_id = StringField('Please input your wallet address',validators=[DataRequired()])
    submit = SubmitField('Submit')


class here_now():

    def __init__(self,wallet_id):
        self.wallet_id= wallet_id
        self.nft_dict = {}

    def make_dict(wallet_id):

        create_dict(wallet_id)
        get_img_id(create_dict(wallet_id))

        for key, val in nft_dict.items():
            if val[3] == "https://miro.medium.com/max/1168/1*7MR5KsgkJad8QTo2e7DVjg.png":
                nft_price = "This is a native token"
                usd_price = "This is a native token"
                nft_dict[key].append(nft_price)
                nft_dict[key].append(usd_price)
            else:
                nft_price = price_api(val[2])
                usd_price = (nft_price*(ada_price_api()))
                nft_dict[key].append(nft_price)
                nft_dict[key].append(usd_price)
        return nft_dict


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/input_wallet', methods = ['GET','POST'])
def input_wallet():

    form = InfoForm()
    # If the form is valid on submission (we'll talk about validation next)
    if form.validate_on_submit():
        # Grab the data from the breed on the form.
        session['wallet_id'] = form.wallet_id.data
        # Reset the form's breed data to be False
        return redirect(url_for('viewer'))


    return render_template('input.html', form=form)


@app.route('/viewer',methods = ['GET','POST'])
def viewer():
    nft_dict = here_now.make_dict(session['wallet_id'])
    my_iter = nft_dict.items()
    dict_list = []
    for key,val in my_iter:
        dict_list.append(val)
    print(my_iter)
    print(dict_list)


    return render_template('viewer.html',here_now=here_now, dict_list = dict_list)


if __name__ == '__main__':
    app.run(debug=True)
