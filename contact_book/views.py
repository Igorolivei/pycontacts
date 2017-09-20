from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from bson.json_util import loads, dumps, STRICT_JSON_OPTIONS
from bson.objectid import ObjectId

#Class contact book

class ContactBook(object):
    def __init__(self, request):
        self.request = request

    #Function that list all contacts
    @view_config(route_name='contact_book', renderer='contact_book.jinja2')
    def contact_book(self):
        contact = self.request.db['contacts'].find()
        return dict(contacts=contact)

    #Function to add new contact
    @view_config(route_name='contact_add', renderer='contact_addedit.jinja2')
    def contact_add(self):

        #Verify if it's a request to save a new contact, or to load the form
        if 'submit' in self.request.params:
            
            params = self.request.params

            new_uid = self.request.db['contacts'].insert_one(
                {
                    "name": params['name'],
                    "birthday": params['birthday'],
                    "adress": params['adress'],
                    "city": params['city'],
                    "state": params['state'],
                    "country": params['country'],
                    "emails": [
                        {"emailAdress1": params['emailAdress1']},
                        {"emailAdress2": params['emailAdress2']}, 
                        {"emailAdress3": params['emailAdress3']}
                    ], 
                    "phones": [
                        {"phoneIdentifier1": params['phoneIdentifier1'], "number1": params['number1']}, 
                        {"phoneIdentifier2": params['phoneIdentifier2'], "number2": params['number2']}, 
                        {"phoneIdentifier3": params['phoneIdentifier3'], "number3": params['number3']}
                    ]
                }
            ).inserted_id

            # Redirect to view the new contact
            url = self.request.route_url('contact_view', uid=new_uid)
            return HTTPFound(url)

        return {}

    #Function that returns the contact data
    @view_config(route_name='contact_view', renderer='contact_view.jinja2')
    def contact_view(self):
        uid = self.request.matchdict['uid']
        contact = self.request.db['contacts'].find_one({"_id":ObjectId(uid)})
        return dict(contact=contact)

    #Return contact's data to fill the form to edit, and handles new data of contact 
    @view_config(route_name='contact_edit', renderer='contact_addedit.jinja2')
    def contact_edit(self):
        uid = self.request.matchdict['uid']
        contact = self.request.db['contacts'].find_one({"_id":ObjectId(uid)})

        #Verify if it's a request to save new data of contact, or to load the form to edit it
        if 'submit' in self.request.params:
            params = self.request.params
            
            result = self.request.db['contacts'].update_one({"_id": ObjectId(uid)},
                { 
                    "$set": { "name": params['name'],
                              "birthday": params['birthday'],
                              "adress": params['adress'],
                              "city": params['city'],
                              "state": params['state'],
                              "country": params['country'],
                              "emails": [
                                  {"emailAdress1": params['emailAdress1']},
                                  {"emailAdress2": params['emailAdress2']}, 
                                  {"emailAdress3": params['emailAdress3']}
                              ], 
                              "phones": [
                                  {"phoneIdentifier1": params['phoneIdentifier1'], "number1": params['number1']}, 
                                  {"phoneIdentifier2": params['phoneIdentifier2'], "number2": params['number2']}, 
                                  {"phoneIdentifier3": params['phoneIdentifier3'], "number3": params['number3']}
                              ]
                    }
                }
            ).matched_count
            if result == 1:
                url = self.request.route_url('contact_view',
                                             uid=uid)
                return HTTPFound(url)
            else:
                message="An error ocurred during updating"
                return dict(message=message)

        return dict(contact=contact)

    #Delete contact from dictionary
    @view_config(route_name='contact_delete', renderer='contact_delete.jinja2')
    def contact_delete(self):
        uid = self.request.matchdict['uid']
        contact =  self.request.db['contacts'].remove({"_id":ObjectId(uid)})
        #Verify if the contact was really deleted from dictionary
        message = "Contact succesfully deleted" if (self.request.db['contacts'].find_one({"_id":ObjectId(uid)}) is None) else "An error ocurred"

        return dict(message=message)

    @view_config(route_name='test_mongo', renderer='json')
    def test_mongo(self):
        contacts = dumps(self.request.db['contacts'].find_one())
        return {'contacts':contacts}