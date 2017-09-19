from pyramid.config import Configurator

def main(global_config, **settings):
	config = Configurator(settings=settings)
	config.include('pyramid_jinja2')
	config.add_route('contact_book', '/')
	config.add_route('contact_add', '/add')
	config.add_route('contact_view', '/{uid}')
	config.add_route('contact_edit', '/{uid}/edit')
	config.add_route('contact_delete', '/{uid}/delete')
	config.add_static_view('deform_static', 'deform:static/')
	config.scan('.views')
	return config.make_wsgi_app()
