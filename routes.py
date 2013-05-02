from webapp2_extras.routes import RedirectRoute
import handlers
import BaseHandlers
_routes = [
    RedirectRoute('/', BaseHandlers.MainHandler, name='home',strict_slash=True),
    RedirectRoute('/signup', BaseHandlers.SignupHandler,name='signup',strict_slash=True),
    RedirectRoute('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',
      handler=BaseHandlers.VerificationHandler, name='verification',strict_slash=True),
    RedirectRoute('/password', BaseHandlers.SetPasswordHandler,name = 'password',strict_slash=True),
    RedirectRoute('/login', BaseHandlers.LoginHandler, name='login',strict_slash=True),
    RedirectRoute('/logout', BaseHandlers.LogoutHandler, name='logout',strict_slash=True),
    RedirectRoute('/forgot', BaseHandlers.ForgotPasswordHandler, name='forgot',strict_slash=True),
    RedirectRoute('/authenticated', BaseHandlers.AuthenticatedHandler, name='authenticated',strict_slash=True),
    RedirectRoute('/getshifts', handlers.GetShiftsHandler, name='getshifts',strict_slash=True),
   RedirectRoute('/getshiftsbyuser', handlers.GetShiftsByUserHandler, name='getshiftsbyuser',strict_slash=True),
    RedirectRoute('/getuser', handlers.GetCurrentUser, name='getcurrentuser',strict_slash=True),
   RedirectRoute('/requestsub', handlers.RequestSubHandler, name='requestsub',strict_slash=True),
   RedirectRoute('/claimsub', handlers.ClaimSubHandler, name='claimsub',strict_slash=True)

]
def get_routes():
	return _routes

def add_routes(app):
	for r in _routes:
		app.router.add(r)
