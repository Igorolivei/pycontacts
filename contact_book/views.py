from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from bson.json_util import loads, dumps, STRICT_JSON_OPTIONS
from bson.objectid import ObjectId
import pymongo
import re

#Class contact book

class ContactBook(object):
    def __init__(self, request):
        self.request = request

    #Function that list all contacts
    @view_config(route_name='contact_book', renderer='contact_book.jinja2')
    @view_config(route_name='contact_book_ordered', renderer='contact_book.jinja2')
    @view_config(route_name='search', renderer='contact_book.jinja2')
    def contact_book(self):
        if 'order' in self.request.matchdict:
            order = self.request.matchdict['order']
            contact = self.request.db['contacts'].find().sort([
                                                            (order, pymongo.ASCENDING)
                                                        ])
        elif 'search' in self.request.matchdict:
            search = self.request.matchdict['search']
            rgx = re.compile('.*'+search+'.*', re.IGNORECASE)
            contact = self.request.db['contacts'].find({"name":{"$regex": rgx}})
        else:
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
            #If the update worked
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

    #Send email to contact
    @view_config(route_name='email', renderer='email.jinja2')
    def send_email(self):
        import smtplib
        from email.mime.image import MIMEImage
        from email.mime.multipart import MIMEMultipart
        
        email = self.request.matchdict['email']
        uid = self.request.matchdict['uid']

        #Verify if the contact was really deleted from dictionary
        if 'submit' in self.request.params:

            '''server = smtplib.SMTP('smtp.gmail.com', 587)
            server.connect('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("igor.bezerra96@gmail.com", "xxxxxx")

            msg = "TEST"

            server.sendmail("igor.bezerra96@gmail.com", "igor.bezerra96@gmail.com", msg)

            server.quit'''

            url = self.request.route_url('contact_view',
                                             uid=uid)
            return HTTPFound(url)
        else:
            return dict(email=email, uid=uid)

    @view_config(route_name='test_mongo', renderer='json')
    def test_mongo(self):
        contacts = dumps(self.request.db['contacts'].find_one())
        return {'contacts':contacts}