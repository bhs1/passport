import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("pb_token", help="Your pushbot token")
args = parser.parse_args()
pb_token_=args.pb_token

pass_url = "https://passportappointment.travel.state.gov/appointment/new/travelplans"
cookies = {
        '_ga': 'GA1.2.877864282.1623345960',
        '_gid': 'GA1.2.638118698.1623345960',
        '_rdt_uuid': '1623345959803.7b25c537-f084-43b9-a73b-7837b7d071b3',
        '_fbp': 'fb.1.1623345959907.2109566296',
        'ASP.NET_SessionId': 'di2ipqf4us25xjjrqaty5oiq',
        '__RequestVerificationToken': 'rYRmqDxlDqQpoFOcuRBj3kUvk9X2P68KJGCPauFsXNPu9Am5x9X6SRKycy7COqwkbqwiBwXXOa7aWYKdv1G11Zraotk1',
        'ADRUM': 's=1623349717464&r=https%3A%2F%2Fpassportstatus.state.gov%2FSearchResult%3F0',
        '_gat': '1',
        '_gat_GSA_ENOR0': '1',
        '_gat_gtag_UA_93487216_1': '1',
    }

headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        '__RequestVerificationToken': 'zlKkkfeSKeU4cKUb-IBiDhdiNYkzOTPDZas5_sW6qUttbmc41h21nhi_hfHwp2XsX7SceFTmgOKDi6wIYMQwP5nMP7g1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://passportappointment.travel.state.gov',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://passportappointment.travel.state.gov/appointment/new/findagency/BFDB6D7163B664C45ED429DA07054AA9',
        'Accept-Language': 'en-US,en;q=0.9',
    }

def pushbullet_message(title, body, url):
    msg = {"type": "link", "title": title, "body": body, "url": url}
    TOKEN = pb_token_
    resp = requests.post('https://api.pushbullet.com/v2/pushes',
                         data=json.dumps(msg),
                         headers={'Authorization': 'Bearer ' + TOKEN,
                                  'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Error',resp.status_code)
    else:
        print ('Message sent')

def run(date_str):
    data = {
        'latitude': '21.275055599999998',
        'longitude': '-157.818455',
        'dateTravel': '%s 12:00:00 AM' % (date_str),
        'dateVisaNeeded': '',
        '__RequestVerificationToken': 'zlKkkfeSKeU4cKUb-IBiDhdiNYkzOTPDZas5_sW6qUttbmc41h21nhi_hfHwp2XsX7SceFTmgOKDi6wIYMQwP5nMP7g1'
    }

    response = requests.post('https://passportappointment.travel.state.gov/appointment/new/findclosestagencies', headers=headers, cookies=cookies, data=data)

    try:
        results = json.loads(response.text)
    except:
        print(response.text)
        sys.exit()
    for result in results:
        name = result["Name"]
        is_avail = result["IsAvailable"]
        msg_base = name + " " + date_str
        if date_str == '7/3/2021' and name == 'Honolulu Passport Agency':
            continue
        if is_avail:
            msg = msg_base +  " is available"
            print(msg)
            pushbullet_message("Passport Bot", msg, pass_url)
        else:
            msg = msg_base + " is not available"
            print(msg)
            #### DOE NOT SUBMIT: For testing ###
            #        pushbullet_message("Passport Bot", msg, pass_url)
run('6/21/2021')
run('7/3/2021')
