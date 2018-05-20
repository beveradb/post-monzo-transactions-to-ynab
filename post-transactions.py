import datetime
import json
import requests
from pymonzo import MonzoAPI

# Create your own personal hosted version of https://github.com/fintech-to-ynab/fintech-to-ynab, with secret parameter
fintechToYNABURL = 'https://{{YOUR_CHOSEN_APP_NAME}}.herokuapp.com/monzo?secret={{ARBITRARY_SECRET_YOU_SET_ON_HEROKU}}'

# Get these by creating a Monzo API client app: https://developers.monzo.com/apps/home
monzoClientID = ''
monzoClientSecret = ''

# Get this by authorizing your new client app using this URL:
# https://auth.monzo.com/?response_type=code&redirect_uri=https://github.com/pawelad/pymonzo&client_id={{monzoClientID}}
# Then check the URL you're redirected to for the "code" parameter
monzoClientAuthCode = ''

# Only needed when running on a new machine - this generates ~/.pymonzo-token which is then used when instantiating
# monzo = MonzoAPI(
#    client_id=monzoClientID,
#    client_secret=monzoClientSecret,
#    auth_code=monzoClientAuthCode,
# )
# exit(0)

# Instantiate Monzo API client normally, using tokens from ~/.pymonzo-token generated previously
monzo = MonzoAPI()


# Create method to handle non-serializable data types in transaction object
def json_default(value):
    if isinstance(value, datetime.date):
        return value.isoformat()
    else:
        return value.__dict__


# Loop through all transactions and post them all to YNAB via fintech-to-ynab app deployed on Heroku
for monzoTransactionSimple in monzo.transactions():
    # Fetch full transaction details including merchant, as otherwise merchant name etc. is missing
    monzoTransactionFull = monzo.transaction(monzoTransactionSimple.id, True)

    if monzoTransactionFull.merchant is None:
        merchantName = ""
    else:
        merchantName = monzoTransactionFull.merchant.name

    ynabTransaction = {
        "type": "transaction.created",
        "data": monzoTransactionFull
    }

    ynabTransactionCreationString = json.dumps(
        ynabTransaction,
        indent=4,
        default=json_default
    )

    print(
        "Processing transaction - Merchant: %s, Date: %s, Amount: %s" % (
            merchantName,
            monzoTransactionFull.created,
            monzoTransactionFull.amount)
    )

    fintechToYNABPOST = requests.post(
        fintechToYNABURL,
        data=ynabTransactionCreationString
    )

    print(fintechToYNABPOST.text)
