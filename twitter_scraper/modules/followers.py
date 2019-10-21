import mechanicalsoup

from requests_html import HTMLSession

session = HTMLSession()

browser = mechanicalsoup.StatefulBrowser()
browser.addheaders = [('User-agent', 'Firefox')]

def get_followers(login, password, starting_user, pages):
    '''
        Get followers from a twitter user

        login:           username (without the @)
        password:        user password
        starting_user:   user to get the followers from

        Around 18 users per page
    '''

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
        'X-Twitter-Active-User': 'yes',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'en-US'
    }

    login_page = browser.get("https://twitter.com/login", headers=headers) # Login page
    login_form = login_page.soup.findAll("form")
    login_form = login_form[2]

    # Fills the login form then submits it
    login_form.find("input", {"name": "session[username_or_email]"})["value"] = login
    login_form.find("input", {"name": "session[password]"})["value"] = password
    login_response = browser.submit(login_form, login_page.url)
    login_response.soup()

    # Followers of the desired user
    browser.open("https://twitter.com/"+starting_user+"/followers")

    profile_link = browser.find_link()
    browser.follow_link(profile_link)

    followers_list = []

    # Adds each of the followers usernames to followers_list
    for page in range(pages):
        page = browser.get_current_page()

        for follower in page.find_all(class_="ProfileCard-screennameLink u-linkComplex js-nav"):
            txt = str(follower.find('b'))
            print(txt[32:-4])
            followers_list.append(txt[32:-4])

    return followers_list
