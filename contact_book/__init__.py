from pyramid.config import Configurator
from pymongo import MongoClient
from urllib.parse import urlparse

def main(global_config, **settings):

	config = Configurator(settings=settings)

	db_url = urlparse(settings['mongo_uri'])
	config.registry.db = MongoClient(
		host=db_url.hostname,
		port=db_url.port,
	)

	def add_db(request):
		db = config.registry.db[db_url.path[1:]]
		if db_url.username and db_url.password:
			db.authenticate(db_url.username, db_url.password)
		return db
	
	config.add_request_method(add_db, 'db', reify=True)

	config.include('pyramid_jinja2')
	config.add_route('contact_book', '/')
	config.add_route('contact_add', '/add')
	config.add_route('contact_view', '/{uid}')
	config.add_route('contact_edit', '/{uid}/edit')
	config.add_route('contact_delete', '/{uid}/delete')
	config.add_route('test_mongo', '/test_mongo/mongo.json')

	config.scan('.views')
	return config.make_wsgi_app()
