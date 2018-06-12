var FreshSales = require('./FreshSales');

Config = require(__dirname + '/config.json');

var get_client = function () {
    // Using API-KEY
    var authtentication = {
        api_key: Config.api_key
    };

    return new FreshSales(Config.domain, authtentication);

};

const Request = (method, options) => {
    var freshsales = get_client();
    return freshsales.request(method, options);
};

const GetAllLeads = function() {
    var options = {
        endpoint: 'api/leads/filters/',
        //payload: payload
    };
    Request('GET', options).then(function (result){
        console.log('GetAllLeads Success');
        // console.log(result)
    }).catch(function (err){
            console.log("GetAllLeads Error");
            console.log(err);
    });
}

const createContact = function(emailAddress) {
    var obj = {
        "contact": {
            "email": emailAddress,
            last_name: 'unknown '+ emailAddress
        }
    };

    var options = {
        endpoint: 'api/contacts',
        payload: obj
    };
    Request('POST', options).then(function (result){
        console.log('Contacts Created');
        // console.log(result)
    }).catch(function (err){
        console.log("createContact Error");
        console.log(err);
    });

}

const ConvertLeadToContact = function(ObjLead) {
    var obj = {
        "email": ObjLead.email,
        "last_name": ObjLead.last_name ,
        "first_name": ObjLead.first_name,
        "company": ObjLead.company,
        
    };

    var options = {
        endpoint: 'leads/' + ObjLead.id + '/convert',
        payload: obj
    };
    Request('POST', options).then(function (result){
        console.log('Converted to contacts');
        // console.log(result)
    }).catch(function (err){
        console.log("ConvertLeadToContact Error");
        console.log(err);
    });

}

const AddContact = function(emailAddress) {
    /* Function to perform Operation on leads
        1) if contact exist => do nothing
        2) if lead exist => convert to contact
        4) if not found => create contact
        
        Arguments:
            email {[type]} -- [description]
        
        uri = self.base_url + "lookup?q={}&f={}&entities={}".format(
            query, func, ",".join(entities)
        )
        lookup?q=janesampleton@gmail.com&f=email&entities=lead
    */


    var options = {
        endpoint: 'api/lookup',
        query: {
            f : 'email',
            entities: 'lead,contact',
            q: emailAddress
        }
    };
    Request('GET', options).then(function (result){
        //console.log('AddContact Success');
        if (result.body && result.body.contacts.contacts.length) {
            console.log('Contacts exists do nothing')
        } else if (result.body && result.body.leads.leads.length) {
            console.log('Lead found Converting to Contacts')
            ConvertLeadToContact(result.body.leads.leads[0])
        } else {
            console.log('Not Found creating Contacts')
            createContact(emailAddress)
        }
    }).catch(function (err){
            console.log("AddContact Error");
            console.log(err);
    });
}

const CreateNote = function(params){
    var options = {
        endpoint: 'api/notes',
        payload: params
    };
    Request('POST', options).then(function (result){
        console.log('Notes Created');
        // console.log(result)
    }).catch(function (err){
        console.log("CreateNote Error");
        console.log(err);
    });

};

const AddNote = function(emailAddress, note) {
    var options = {
        endpoint: 'api/lookup',
        query: {
            f : 'email',
            entities: 'lead,contact',
            q: emailAddress
        }
    };
    Request('GET', options).then(function (result){
        if (result.body && result.body.contacts.contacts.length) {
            console.log('Contacts exists Creating Note for Contacts')
            params = {
                "note": {
                    "description": note,
                    "targetable_type": 'Contact',
                    "targetable_id": result.body.contacts.contacts[0].id
                }
            };
            CreateNote(params)
        } else if (result.body && result.body.leads.leads.length) {
            console.log('leads exists Creating Note for Leads')
            params = {
                "note": {
                    "description": note,
                    "targetable_type": 'Lead',
                    "targetable_id": result.body.leads.leads[0].id
                }
            };
            CreateNote(params)
        }
    }).catch(function (err){
            console.log("AddNote Error");
            console.log(err);
    });
};

//AddContact('test1@gmail.com')
//AddNote('leadtest3@gmail.com', 'Note added')
// AddNote('lead1@test.com', 'new Note added')