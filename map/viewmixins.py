from django.http import Http404

class AuthenticateLoginViewMixin(object):

	def dispatch(self, request, *args, **kwargs):
		self.authenticate()
		return super().dispatch(request, *args, **kwargs)

	def authenticate(self):
		if not self.request.user.is_authenticated():
			raise Http404 # for now returning 404, later prompt login
		return None