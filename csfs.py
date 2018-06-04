import json

import click

from fresh_sales_api import FreshSalesApiBase
import settings


class CsFsintegration(FreshSalesApiBase):
    """
    CloudSploit FreshSales Intergration Class
    """
    def __init__(self):
        """
        Init function
        """
        self.base_url = settings.BASE_URI
        self.api_key = settings.api_key
        self.view_id = settings.view_id
        
        # call super init
        super(CsFsintegration, self).__init__(self.base_url, self.api_key)
    

    def get_or_create_lead(self, email):
        """ Function to perform Operation on leads
        1) if leads not exists Create leads
        2) if leads exists again check if contacts exists
        3) if contacts not exists convert to contacts
        4) if contacts exists do nothing
        
        Arguments:
            email {[type]} -- [description]
        """
        # search email for lead / contact
        ret_data = {}

        search_response = self.search(
            "email", ["lead", "contact"], email
        )
        # check if contacts exists
        if len(search_response['contacts']['contacts']):
            print("contact exists do nothing")
            ret_data = search_response

        # check if leads exists convert to contact
        elif len(search_response['leads']['leads']):
            print("leads exists converting to contacts")
            ret_data = self.convert_lead_to_contact(
                search_response["leads"]["leads"][0]
            )
        else:
            print("creating new lead")
            params = {"lead":{
                "email": email, "last_name":"unknown"
            }}
            ret_data = self.create_lead(params)
        
        return ret_data
    
    def add_note(self, email, note):
        """[summary]
        
        Arguments:
            email string -- email of lead / contact
            note string  -- note
        """
        search_response = self.search(
            "email", ["lead", "contact"], email
        )
        # check if contacts exists create note for contact
        if len(search_response['contacts']['contacts']):
            contact = search_response['contacts']['contacts'][0]
            print("creating note for contact")
            
            params = {"note":{
                "description": note,
                "targetable_type": 'Contact',
                "targetable_id": contact['id']
            }}
            ret_data = self.create_note(params)

        # check if leads exists convert to contact
        elif len(search_response['leads']['leads']):
            lead = search_response['leads']['leads'][0]
            print("creating note for lead")
            
            params = {"note":{
                "description": note,
                "targetable_type": 'lead',
                "targetable_id": lead['id']
            }}
            ret_data = self.create_note(params)
        else:
            print('email not found updating nothing')
        
        return ret_data


@click.group()
@click.pass_context
def cli(ctx):
    pass

@click.command()
@click.pass_context
@click.option('--email', required=True)
def addlead(ctx, email):
    csfs = CsFsintegration()
    data = csfs.get_or_create_lead(email)
    if data.get('lead'):
        click.echo('New lead Created')
        click.echo(json.dumps(data, indent=2))
    elif data.get('contact'):
        click.echo('Converting to Contact')
        click.echo(json.dumps(data, indent=2))
    else:
        click.echo(json.dumps(data, indent=2))
        click.echo('Contacts Exists')

@click.command()
@click.pass_context
@click.option('--email', required=True)
@click.option('--note', required=True)
def addnote(ctx, email, note):
    csfs = CsFsintegration()
    data = csfs.add_note(email, note)

    click.echo(json.dumps(data, indent=2))
    click.echo('Note Added')

@click.command()
@click.pass_context
@click.option('--email', required=True)
def listlead(ctx, email):
    csfs = CsFsintegration()
    data = csfs.get_all_leads()
    import pdb; pdb.set_trace()

cli.add_command(addlead)
cli.add_command(addnote)

cli.add_command(listlead)


if __name__ == '__main__':
    cli()
