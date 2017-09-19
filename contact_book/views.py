from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

#Contacts dictionary

contacts = {
    '1': dict(uid='1', name='Igor', adress='Pahkakuja 2, Kuopio, Finland', email='igor.bezerra96@gmail.com', phone='+5584999337801', birthday='1996-09-26'),
    '2': dict(uid='2', name='Dave', adress='Av. Sen. Salgado Filho, Natal/RN, Brasil', email='dave.grohl@foofighters.com', phone='+5584988888888', birthday='1992-12-16'),
    '3': dict(uid='3', name='Eric', adress='Springfield, EUA', email='eric.clapton@cream.com', phone='+5584912314142', birthday='1996-09-26')
}

#Class contact book

class ContactBook(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name='contact_book', renderer='contact_book.jinja2')
    def contact_book(self):
        return dict(contacts=contacts.values())

    #Function to add new contact
    @view_config(route_name='contact_add',
                 renderer='contact_addedit.jinja2')
    def contact_add(self):

        #Verify if it's a request to save a new contact, or to load the form
        if 'submit' in self.request.params:
            
            params = self.request.params

            last_uid = int(sorted(contacts.keys())[-1])
            new_uid = str(last_uid + 1)
            contacts[new_uid] = dict(uid=new_uid, 
                                     name=params['name'], 
                                     adress=params['adress'], 
                                     email=params['email'], 
                                     phone=params['phone'], 
                                     birthday=params['birthday'])

            # Redirect to view the new contact
            url = self.request.route_url('contact_view', uid=new_uid)
            return HTTPFound(url)

        return {}

    #Function that returns the contact data
    @view_config(route_name='contact_view', renderer='contact_view.jinja2')
    def contact_view(self):
        uid = self.request.matchdict['uid']
        contact = contacts[uid]
        return dict(contact=contact)

    #Return contact's data to fill the form to edit, and handles new data of contact 
    @view_config(route_name='contact_edit',
                 renderer='contact_addedit.jinja2')
    def contact_edit(self):
        uid = self.request.matchdict['uid']
        contact = contacts[uid]

        #Verify if it's a request to save new data of contact, or to load the form to edit it
        if 'submit' in self.request.params:
            params = self.request.params
            
            contacts[uid]['name'] = params['name']
            contacts[uid]['adress'] = params['adress']
            contacts[uid]['email'] = params['email']
            contacts[uid]['phone'] = params['phone']
            contacts[uid]['birthday'] = params['birthday']
            url = self.request.route_url('contact_view',
                                         uid=contact['uid'])
            return HTTPFound(url)

        return dict(contact=contact)

    #Delete contact from dictionary
    @view_config(route_name='contact_delete',
                 renderer='contact_delete.jinja2')
    def contact_delete(self):
        uid = self.request.matchdict['uid']
        del contacts[uid]
        #Verify if the contact was really deleted from dictionary
        if uid in contacts:
            message = "An error ocurred"
        else:
            message = "Contact succesfully deleted"
        return dict(message=message)