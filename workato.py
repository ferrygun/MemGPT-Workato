import random
import pandas as pd
import requests
from datetime import datetime, timedelta

def getWorkatoRecipe(self) -> str:
    """
    Retrieving the list of Workato recipes

    This function generates JSON data containing details for Workato recipes, structured as follows:

        id: recipe id
        description: recipe description
        successful_job_count: successful job count
        last_status_success: last success status
        last_status_cancelled: last cancelled status
        last_status_datetime: last status datetime
        last_status_text: last status text
        last_description: last description
        last_master_job_id: last master job id
        last_repeat_job_id: last repeat job id
        action_count: task usage
        active: active status
        folder_id: folder id

    Returns:
        string: Data in JSON format.

    Example:
        >>> getWorkatoRecipe()
        
        [
          {
            'id': 1096317,
            'description': 'Recipe A',
            'successful_job_count': 5825,
            'failed_job_count': 93,
            'last_status_success': True,
            'last_status_cancelled': False,
            'last_status_datetime': '2023-11-27T19:30:07.000+08:00',
            'last_status_text': 'Last job: Successful',
            'last_description': '',
            'last_master_job_id': 'j-AKPozrbX-F4YXJ8',
            'last_repeat_job_id': 'j-AKPozrbX-F4YXJ8',
            'action_count': 41645,
            'active': True,
            'folder_id': 141423
          },
          {
            'id': 1096318,
            'description': 'Recipe B',
            'successful_job_count': 5825,
            'failed_job_count': 93,
            'last_status_success': True,
            'last_status_cancelled': False,
            'last_status_datetime': '2023-11-27T19:30:07.000+08:00',
            'last_status_text': 'Last job: Successful',
            'last_description': '',
            'last_master_job_id': 'j-AKPozrgX-p8ktMQ',
            'last_repeat_job_id': 'j-AKPozrgX-p8ktMQ',
            'action_count': 50974,
            'active': True,
            'folder_id': 141423
          }
        ]  # This is an example output and may vary each time the function is called.

    """

    print('-executing function--')
    ''' get_sign_session '''
    options = {
        'method': 'GET',
        'url': 'https://app.workato.com/web_api/auth_user.json',
        'headers': {
            'Host': 'app.workato.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://app.workato.com/users/sign_in',
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }
    }
    
    response = requests.request(options['method'], options['url'], headers=options['headers'])
    
    if response.status_code != 200:
        raise Exception(f"Failed to get sign session: {response.status_code}")

    raw_cookies = response.headers['set-cookie']
    xsrf_token = ''
    workato_app_session = ''

    for cookie in raw_cookies.split(';'):
        cookie = cookie.strip()
        
        if cookie.startswith('XSRF-TOKEN'):
            xsrf_token = cookie.split('=')[1]
        elif cookie.startswith('secure, _workato_app_session'):

            workato_app_session = cookie.split('=')[1]

    print('xsrf_token:', xsrf_token)
    print('workato_app_session:', workato_app_session)
    ''' end of get_sign_session '''
    
    ''' get_session '''
    x_csrf_token_ = requests.utils.unquote(xsrf_token.replace('+', ' '))
    workato_app_session_ = workato_app_session
    print('xsrf_token:', x_csrf_token_)
    print('workato_app_session:', workato_app_session_)


    options = {
        'method': 'POST',
        'url': 'https://app.workato.com/users/sign_in.json',
        'headers': {
            'Host': 'app.workato.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://app.workato.com/users/sign_in',
            'X-CSRF-TOKEN': x_csrf_token_,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json',
            'Origin': 'https://app.workato.com',
            'Connection': 'keep-alive',
            'Cookie': f'_workato_app_session={workato_app_session_}',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        },
        'json': {
            'user': {
                'email': '',
                'password': ''
            }
        }
    }

    response = requests.request(options['method'], options['url'], headers=options['headers'], json=options['json'])

    if response.status_code != 200:
        raise Exception(f"Failed to get session: {response.status_code}")

    raw_cookies = response.headers['set-cookie']
    xsrf_token2 = ''
    workato_app_session2 = ''

    for cookie in raw_cookies.split(';'):
        cookie = cookie.strip()
        #print(cookie)
        if cookie.startswith('secure, XSRF-TOKEN'):
            xsrf_token2 = cookie.split('=')[1]
        elif cookie.startswith('secure, _workato_app_session'):
            workato_app_session2 = cookie.split('=')[1]

    print('xsrf_token2:', xsrf_token2)
    print('workato_app_session2:', workato_app_session2)
    ''' end of get_session '''

    # Get the current date and time
    date = datetime.now()

    # Format the current date and time
    today = date.strftime("%Y-%m-%dT%H:%M:%S%z")

    # Calculate one month ago from the current date
    one_month_ago = date - timedelta(days=30)

    # Format one month ago
    one_month_ago_formatted = one_month_ago.strftime("%Y-%m-%dT%H:%M:%S%z")

    
    options = {
        'method': 'GET',
        'url': f"https://app.workato.com/dashboard/flows.json?started_at_from={one_month_ago_formatted}&started_at_to={today}&sort_term=failed_job_count&sort_direction=asc&recipe_type=active&folder_id=450562",
        'headers': {
            'Host': 'app.workato.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Cookie': f'XSRF-TOKEN={xsrf_token2}; _workato_app_session={workato_app_session2};',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        }
    }


    response = requests.request(options['method'], options['url'], headers=options['headers'])

    body = response.json()
    df = pd.DataFrame(body['result']['flows'])
    print(df)

    symbol_txt = df.to_string(index=None)    
    return f"""
    
{symbol_txt}
    """.strip()

