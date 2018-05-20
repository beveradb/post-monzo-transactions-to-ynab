# post-monzo-transactions-to-ynab
Easily perform a one-off import of all existing Monzo transactions into YNAB.

Inline code comments are worth reading.

Usage:
1. Create your own personal hosted version of https://github.com/fintech-to-ynab/fintech-to-ynab, with secret parameter in URL as per the instructions in that project.
    - This will give you an app deployed on Heroku which accepts POST requests containing Monzo transaction data and interfaces with the YNAB API to create those transactions in YNAB.
    - Incidentally, this also allows you to then use Webhooks in the Monzo API to automatically get transactions into YNAB immediately!
    - Once you have your deployed APP URL, replace this in the `fintechToYNABURL` variable at the top of the script.

2. Create a Monzo API client app: https://developers.monzo.com/apps/home
    - This will give you a client ID and secret token - put these in the `monzoClientID` and `monzoClientSecret` variables.
    
3. Authorise your new Monzo API client app using your own Monzo login details, by replacing your real client ID in this URL and browsing to it: https://auth.monzo.com/?response_type=code&redirect_uri=https://github.com/pawelad/pymonzo&client_id={{monzoClientID}}
    - Once authorised, it should redirect you to the pymonzo Github project, but with a URL parameter named "code".
    - Copy this "code" value and insert it into the `monzoClientAuthCode` variable in the code.
    
4. Uncomment the "Only needed when running on a new machine" section and run the script once.
    - This generates a `.pymonzo-token` file in your home directory with auth tokens which are used for future runs.
    - Once this has been generated, comment this section back out - the normal `monzo = MonzoAPI` instantiation is all that is needed once you have a `.pymonzo-token` file.
    
5. Run the script normally! You should see output mentioning every transaction as it is imported into your YNAB.

Feel free to contact me if you have any issues, although this was hacked together in a couple of hours so I may not be much help!
