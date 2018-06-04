import requests


class FreshSalesApiBase(object):
    """
    Fresh Sales Api Base Class
    contains Base functions to interacting with freshsales api
    """

    def __init__(self, base_url, api_key):
        """
        Init function
        
        :param base_url: freshsales base URL https://domain.freshsales.io/api/
        :type base_url: str
        :param api_key: fresh sales APIKEY i.e, XXxxxXXXxxxxXX
        :type api_key: str
        """
        self.api_key = api_key
        self.base_url = base_url

        self.session = self.session = requests.Session()
        self.session.headers.update({
            "Authorization": "Token token={}".format(self.api_key),
            "Content-Type": "application/json"
        })
        

    def get_uri(self, uri):
        """
        Function to call GET method on given uri
        
        :param uri: <string> path i.e, leads, contacts, etc
        :type uri: str
        :return: dictionary contains response json
        :rtype: dict
        """

        try:
            response = self.session.get(uri)
            if not response.status_code == 200:
                print(response.json())
            return response.json()

        except Exception as e:
            raise(e)
    

    def post_uri(self, uri, data):
        """
        Function to call POST method on given uri
        
        :param uri: <string> path i.e, leads, contacts, etc
        :type uri: str
        :param data: dictonary containing data to be posted
        :type data: dict
        :return: dictionary contains response json
        :rtype: dict
        """

        try:
            response = self.session.post(uri, json=data)
            if not response.status_code == 200:
                print(response.json())
            return response.json()

        except Exception as e:
            raise(e)
    
    def search(self, func, entities, query):
        """[summary]
        
        :param func: namee of field against searching for
        :type func: str
        :param entities: list of entities against searching for
        :type entities: list
        :param query: search string
        :type query: str
        :return: response object
        :rtype: object

        https://domain.freshsales.io/api/
        lookup?q=janesampleton@gmail.com&f=email&entities=lead
        """

        uri = self.base_url + "lookup?q={}&f={}&entities={}".format(
            query, func, ",".join(entities)
        )
        #print(uri)
        return self.get_uri(uri)

    
    def create_lead(self, params):
        """
        Function to create Leads
        
        :param params: payload data
        :type params: dictionary
        :return: dictionary containg response data
        :rtype: dictionary
        """

        uri = self.base_url + "leads/"
        return self.post_uri(uri, params)
    
    def create_contact(self, params):
        """
        Function to create Contacts
        
        :param params: payload data
        :type params: dictionary
        :return: dictionary containg response data
        :rtype: dictionary
        """

        uri = self.base_url + "contacts/"
        return self.post_uri(uri, params)

    def create_note(self, params):
        """
        Function to create Leads
        
        :param params: payload data
        :type params: dictionary
        :return: dictionary containg response data
        :rtype: dictionary
        """

        uri = self.base_url + "notes/"
        return self.post_uri(uri, params)
    
    def convert_lead_to_contact(self, lead):
        """[summary]
        
        :param lead: lead data containg lead information
        :type lead: dictionary
        :return: response dictionary containg contacts data
        :rtype: dictionary
        """

        params = {}
        params["email"] = lead["email"]
        params["last_name"] = lead.get("last_name", "Unknown")
        params["first_name"] = lead.get("first_name", "Unknown")
        params["company"] = lead.get("company", "Unknown")

        uri = self.base_url + "leads/{}/convert".format(lead["id"])
        return self.post_uri(uri, params)
    

    def get_all(self, key):
        """function to return all leads
        
        :return: list of all leads
        :rtype: list
        """

        uri = self.base_url + "{}/filters/".format(key)
        data =  self.get_uri(uri)
        view = {}
        for i in data['filters']:
            if i['name'] == 'All {}'.format(key.title()):
                view = i
                break;
        if view:
            data = self.get_uri(
                self.base_url + '{}/view/{}'.format(key, view['id'])
            )
        return data
