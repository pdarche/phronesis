import tornado.auth
import tornado.httputil
from tornado import httpclient
from tornado import escape
from tornado.httputil import url_concat

import logging
import urllib
import json

log = logging.info

def build_oauth_header(params):
    return "OAuth " + ", ".join(
            ['%s="%s"' % (k, urllib.quote(v)) for k, v in params.iteritems()])

class FitbitMixin(tornado.auth.OAuthMixin):
    """Fitbit OAuth authentication.

    To authenticate with Fitbit, register your application with
    Fitbit at https://dev.fitbit.com/apps. Then copy your Consumer Key and
    Consumer Secret to the application settings 'fitbit_consumer_key' and
    'fitbit_consumer_secret'. Use this Mixin on the handler for the URL
    you registered as your application's Callback URL.

    When your application is set up, you can use this Mixin like this
    to authenticate the user with Fitbit and get access to their stream::

        class FitbitHandler(tornado.web.RequestHandler,
                             tornado.auth.FitbitMixin):
            @tornado.web.asynchronous
            def get(self):
                if self.get_argument("oauth_token", None):
                    self.get_authenticated_user(self.async_callback(self._on_auth))
                    return
                self.authorize_redirect()

            def _on_auth(self, user):
                if not user:
                    raise tornado.web.HTTPError(500, "Fitbit auth failed")
                # Save the user using, e.g., set_secure_cookie()

    The user object returned by get_authenticated_user() includes the
    attributes 'user-id', 'name', and all of the custom Fitbit user
    attributes describe at
    https://wiki.fitbit.com/display/API/API-Get-User-Info
    in addition to 'access_token'. You should save the access token with
    the user; it is required to make requests on behalf of the user later
    with fitbit_request().
    """
    _OAUTH_REQUEST_TOKEN_URL = "http://api.fitbit.com/oauth/request_token"
    _OAUTH_ACCESS_TOKEN_URL = "http://api.fitbit.com/oauth/access_token"
    _OAUTH_AUTHORIZE_URL = "http://www.fitbit.com/oauth/authorize"
    _OAUTH_AUTHENTICATE_URL = "http://www.fitbit.com/oauth/authenticate"
    _OAUTH_NO_CALLBACKS = False
    _FITBIT_BASE_URL = "http://api.fitbit.com/1"
    _OAUTH_VERSION="1.0"

    def authenticate_redirect(self, callback_uri=None):
        """Just like authorize_redirect(), but auto-redirects if authorized.

        This is generally the right interface to use if you are using
        Fitbit for single-sign on.
        """
        http = self.get_auth_http_client()
        http.fetch(self._oauth_request_token_url(callback_uri=callback_uri), self.async_callback(
            self._on_request_token, self._OAUTH_AUTHENTICATE_URL, None))

    def fitbit_request(self, path, callback, access_token=None,
                           post_args=None, **args):
        """Fetches the given API path, e.g., "/user/-/activities/log/steps/date/today/7d"

        The path should not include the format (we automatically append
        ".json" and parse the JSON output).

        If the request is a POST, post_args should be provided. Query
        string arguments should be given as keyword arguments.

        All the Twitter methods are documented at
        http://apiwiki.twitter.com/Twitter-API-Documentation.

        Many methods require an OAuth access token which you can obtain
        through authorize_redirect() and get_authenticated_user(). The
        user returned through that process includes an 'access_token'
        attribute that can be used to make authenticated requests via
        this method. Example usage::

            class MainHandler(tornado.web.RequestHandler,
                              tornado.auth.FitbitMixin):
                @tornado.web.authenticated
                @tornado.web.asynchronous
                def get(self):
                    self.fitbit_request(
                        "/user/-/activities/log/steps/date/today/7d",
                        access_token=user["access_token"],
                        callback=self.async_callback(self._on_post))

                def _on_post(self, new_entry):
                    if not new_entry:
                        # Call failed; perhaps missing permission?
                        self.authorize_redirect()
                        return
                    self.finish("Posted a message!")

        """
        if path.startswith('http:') or path.startswith('https:'):
            # Raw urls are useful for e.g. search which doesn't follow the
            # usual pattern: http://search.twitter.com/search.json
            url = path
        else:
            url = self._FITBIT_BASE_URL + path + ".json"
        # Add the OAuth resource request signature if we have credentials
        if access_token:
            all_args = dict()
            all_args.update(args)
            if post_args is not None:
                all_args.update(post_args)
            method = "POST" if post_args is not None else "GET"
            oauth = self._oauth_request_parameters(
                url, access_token, all_args, method=method)
            # args.update(oauth)
        if args:
            url += "?" + urllib.urlencode(args)
        callback = self.async_callback(self._on_fitbit_request, callback)
        http = self.get_auth_http_client()
        log(build_oauth_header(oauth))
        if post_args is not None:
            print url
            http.fetch(url, method="POST", body=urllib.urlencode(args),
                       callback=callback,
                       headers={'Authorization': build_oauth_header(oauth)})
        else:
            print url
            http.fetch(url, callback=callback,
                    headers={'Authorization': build_oauth_header(oauth)})

    def _on_fitbit_request(self, callback, response):
        log("Got response %s fetching %s", (str(response), response.body))
        callback(json.loads(response.body))

    def _oauth_consumer_token(self):
        self.require_setting("fitbit_consumer_key", "Fitbit OAuth")
        self.require_setting("fitbit_consumer_secret", "Fitbit OAuth")
        return {
            'key': self.settings["fitbit_consumer_key"],
            'secret': self.settings["fitbit_consumer_secret"]
        }

    def _oauth_get_user(self, access_token, callback):
        callback = self.async_callback(self._parse_user_response, callback)

        self.fitbit_request(
            "/user/-/profile",       
            access_token=access_token,
            callback=callback
        )

    def _parse_user_response(self, callback, user):
        if user:
            user["username"] = user["user"]["encodedId"]
        callback(user)



class FlickrMixin(tornado.auth.OAuthMixin):
    """Flickr OAuth authentication.

    To authenticate with Flickr, register your application with
    Flickr at http://www.flickr.com/services/apps/. Then copy your Consumer Key and
    Consumer Secret to the application settings 'flickr_consumer_key' and
    'flickr_consumer_secret'. Use this Mixin on the handler for the URL
    you registered as your application's Callback URL.

    When your application is set up, you can use this Mixin like this
    to authenticate the user with Flickr and get access to their data::

        class FlickrHandler(tornado.web.RequestHandler,
                             tornado.auth.FlickrMixin):
            @tornado.web.asynchronous
            def get(self):
                if self.get_argument("oauth_token", None):
                    self.get_authenticated_user(self.async_callback(self._on_auth))
                    return
                self.authorize_redirect( callback_url )

            def _on_auth(self, user):
                if not user:
                    raise tornado.web.HTTPError(500, "Flickr auth failed")
                # Save the user using, e.g., set_secure_cookie()

    Note that Flickr requres a callback url for authorize_redirect.  No
    URL is required when registering your app

    The user object returned by get_authenticated_user() includes the
    attributes '', 'name', and all of the custom Flickr user
    attributes describe at http://www.flickr.com/services/api/flickr.urls.getUserProfile.html
    
    in addition to 'access_token'. You should save the access token with
    the user; it is required to make requests on behalf of the user later
    with flickr_request().
    """
    _OAUTH_REQUEST_TOKEN_URL = "http://www.flickr.com/services/oauth/request_token"
    _OAUTH_ACCESS_TOKEN_URL = "http://www.flickr.com/services/oauth/access_token"
    _OAUTH_AUTHORIZE_URL = "http://www.flickr.com/services/oauth/authorize"
    _OAUTH_NO_CALLBACKS = False
    _OAUTH_VERSION="1.0a"
    _FLICKR_BASE_URL = "http://api.flickr.com/services/rest/?"

    def authenticate_redirect(self, callback_uri=None):
        """Just like authorize_redirect(), but auto-redirects if authorized.

        This is generally the right interface to use if you are using
        Flickr for single-sign on.
        """
        http = self.get_auth_http_client()
        http.fetch(self._oauth_request_token_url(callback_uri=callback_uri), self.async_callback(
            self._on_request_token, self._OAUTH_AUTHENTICATE_URL, None))

    def flickr_request(self, path, callback, access_token=None,
                                post_args=None, **args):
        """Fetches the given API path, e.g., "http://api.flickr.com/services/rest/?method=flickr.photosets.getPhotos"

        The path can be either the full url or just the desired method.

        If the request is a POST, post_args should be provided. Query
        string arguments should be given as keyword arguments.

        All the Flickr methods are documented at
        http://www.flickr.com/services/api/

        Many methods require an OAuth access token which you can obtain
        through authorize_redirect() and get_authenticated_user(). The
        user returned through that process includes an 'access_token'
        attribute that can be used to make authenticated requests via
        this method. Example usage::

            class MainHandler(tornado.web.RequestHandler,
                              tornado.auth.FitbitMixin):
                @tornado.web.authenticated
                @tornado.web.asynchronous
                def get(self):
                    self.flickr_request(
                        "method=flickr.urls.getUserProfile",
                        access_token=user["access_token"],
                        callback=self.async_callback(self._on_post))

                def _on_auth(self, user):
                    if not user:
                        raise tornado.web.HTTPError(500, "Flickr auth failed")
                    # Save the user using, e.g., set_secure_cookie()

        """
        if path.startswith('http:') or path.startswith('https:'):
            # Raw urls are useful for things queries don't follow the usual pattern
            url = path
        else:
            url_elems = []
            url_elems.append(self._FLICKR_BASE_URL)
            url_elems.append("&".join("%s=%s" % (k, str(v)) for k, v in sorted(args.items())))             
            url = "&".join(e for e in url_elems)
        
        # Add the OAuth resource request signature if web have credentials
        if access_token:
            all_args = dict()
            all_args.update(args)
            if post_args is not None:
                all_args.update(post_args)
            method = "POST" if post_args is not None else "GET"            
            oauth = self._oauth_request_parameters(
                url, access_token, all_args, method=method)
            # args.update(oauth)

        callback = self.async_callback(self._on_flickr_request, callback)
        http = self.get_auth_http_client()
        log(build_oauth_header(oauth))
        if post_args is not None:
            print "the post urls is: %s" % url
            http.fetch(url, method="POST", body=urllib.urlencode(args),
                       callback=callback,
                       headers={'Authorization': build_oauth_header(oauth)})
        else:
            print "the get urls is: %s" % url
            http.fetch(url, callback=callback,
                    headers={'Authorization': build_oauth_header(oauth)})

    def _on_flickr_request(self, callback, response):
        log("Got response %s fetching %s", (str(response), response.body))
        callback(json.loads(response.body))

    def _oauth_consumer_token(self):
        self.require_setting("flickr_consumer_key", "Flickr OAuth")
        self.require_setting("flickr_consumer_secret", "Flickr OAuth")
        return {
            'key': self.settings["flickr_consumer_key"],
            'secret': self.settings["flickr_consumer_secret"]
        }

    def _oauth_get_user(self, access_token, callback):
        callback = self.async_callback(self._parse_user_response, callback)

        self.flickr_request(
            "empty string",
            format="json",
            api_key=self.settings["flickr_consumer_key"],
            nojsoncallback="1", 
            method="flickr.urls.getUserProfile",
            access_token=access_token,
            callback=callback
        )

    def _parse_user_response(self, callback, user):
        if user:
            callback(user)


class FoursquareMixin(object):
    """Foursquare API using Oauth2"""

    _OAUTH_ACCESS_TOKEN_URL = "https://foursquare.com/oauth2/access_token"
    _OAUTH_AUTHORIZE_URL    = "https://foursquare.com/oauth2/authorize"
    _OAUTH_AUTHENTICATE_URL = "https://foursquare.com/oauth2/authenticate"

    _BASE_URL = "https://api.foursquare.com/v2"

    @property
    def httpclient_instance(self):
        return httpclient.AsyncHTTPClient()


    def authorize_redirect(self, redirect_uri=None, client_id=None, **kwargs):
        """Redirects the user to obtain OAuth authorization for this service.

        Some providers require that you register a Callback
        URL with your application. You should call this method to log the
        user in, and then call get_authenticated_user() in the handler
        you registered as your Callback URL to complete the authorization
        process.
        """
        args = {
          "redirect_uri": redirect_uri,
          "client_id": client_id,
          "response_type": "code"
        }
        if kwargs: args.update(kwargs)
        self.redirect(url_concat(self._OAUTH_AUTHENTICATE_URL, args))       # Why _OAUTH_AUTHORIZE_URL fails?


    def get_authenticated_user(self, redirect_uri, client_id, client_secret, code, callback):
        """
        Handles the login for the Foursquare user, returning a user object.

        Example usage::

          class FoursquareLoginHandler(LoginHandler, FoursquareMixin):
              @tornado.web.asynchronous
              def get(self):
                  if self.get_argument("code", False):
                      self.get_authenticated_user(
                          redirect_uri='/auth/foursquare/connect',
                          client_id=self.settings["foursquare_client_id"],
                          client_secret=self.settings["foursquare_client_secret"],
                          code=self.get_argument("code"),
                          callback=self.async_callback(self._on_login)
                      )
                      return

                  self.authorize_redirect(
                      redirect_uri='/auth/foursquare/connect',
                      client_id=self.settings["foursquare_api_key"]
                  )

              def _on_login(self, user):
                  logging.error(user)
                  self.finish()
        """
        args = {
            "redirect_uri": redirect_uri,
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code"
        }

        self.httpclient_instance.fetch(
            url_concat(self._OAUTH_ACCESS_TOKEN_URL, args),
            self.async_callback(self._on_access_token, redirect_uri, client_id, client_secret, callback)
        )


    def _on_access_token(self, redirect_uri, client_id, client_secret, callback, response):
        if response.error:
            logging.warning('Foursquare auth error: %s' % str(response))
            callback(None)
            return

        session = escape.json_decode(response.body)

        self.foursquare_request(
            path="/users/self",
            callback=self.async_callback(self._on_get_user_info, callback, session),
            access_token=session["access_token"]
        )


    def _on_get_user_info(self, callback, session, user):
        if user is None:
            callback(None)
            return

        user.update({
            'first_name': user.get('firstName'),
            'last_name': user.get('lastName'),
            'home_city': user.get('homeCity'),
            'access_token': session['access_token']
        })
        callback(user)


    def foursquare_request(self, path, callback, access_token=None, post_args=None, **args):
        """
        If the request is a POST, post_args should be provided. Query
        string arguments should be given as keyword arguments.

        See: https://developer.foursquare.com/docs/
        """
        url = self.__class__._BASE_URL + path

        all_args = {}
        if access_token:
            all_args["access_token"] = access_token
            all_args["oauth_token"] = access_token
            all_args.update(args)

        if args:
            for k, v in args["args"].iteritems():
                all_args[k] = v
                all_args.update(args)

        if all_args: 
            url += "?" + urllib.urlencode(all_args)
            print "there are some args" + url

        callback = self.async_callback(self._on_foursquare_request, callback)
        if post_args is not None:
            self.httpclient_instance.fetch(url, method="POST", body=urllib.urlencode(post_args), callback=callback)
        else:
            self.httpclient_instance.fetch(url, callback=callback)


    def _on_foursquare_request(self, callback, response):
        response_body = escape.json_decode(response.body)
        if response.error:
            logging.warning(
                "Foursquare Error(%s) :: Detail: %s, Message: %s, URL: %s",
                response.error, response_body["meta"]["errorDetail"], response_body["meta"]["errorMessage"], response.request.url
            )
            callback(None)
            return
        callback(response_body)



class KhanAcademyMixin(tornado.auth.OAuthMixin):
    """Khan Academy OAuth authentication.

    To authenticate with Khan Academy, register your application with
    Khan Academy at https://www.khanacademy.org/api-apps/register. 
    Then copy your Consumer Key and Consumer Secret to the application 
    settings 'khanacademy_consumer_key' and'khanacademy_consumer_secret'. 

    When your application is set up, you can use this Mixin like this
    to authenticate the user with KhanAcademy and get access to their stream::

        class KhanAcademyHandler(tornado.web.RequestHandler,
                             tornado.auth.FitbitMixin):
            @tornado.web.asynchronous
            def get(self):
                if self.get_argument("oauth_token", None):
                    self.get_authenticated_user(self.async_callback(self._on_auth))
                    return
                self.authorize_redirect()

            def _on_auth(self, user):
                if not user:
                    raise tornado.web.HTTPError(500, "Khan Academy auth failed")
                # Save the user using, e.g., set_secure_cookie()

    The user object returned by get_authenticated_khanacademy_user() includes the
    attributes 'user-id', 'name', and all of the custom Khan Academy user
    attributes describe at
    https://github.com/Khan/khan-api/wiki/Khan-Academy-API-Methods#wiki-users
    in addition to 'access_token'. You should save the access token with
    the user; it is required to make requests on behalf of the user later
    with khanacademy_request().
    """
    _KHANACADEMY_BASE_URL = "http://www.khanacademy.org"
    _OAUTH_REQUEST_TOKEN_URL = _KHANACADEMY_BASE_URL + "/api/auth/request_token"
    _OAUTH_ACCESS_TOKEN_URL = _KHANACADEMY_BASE_URL + "/api/auth/access_token"
    _OAUTH_AUTHORIZE_URL = _KHANACADEMY_BASE_URL + "/api/auth/authorize"
    _OAUTH_NO_CALLBACKS = False
    _OAUTH_VERSION="1.0"
    _DEFAULT_CALLBACK = "/api/auth/default_callback" 

    def authenticate_redirect(self, callback_uri=None):
        """Just like authorize_redirect(), but auto-redirects if authorized.

        This is generally the right interface to use if you are using
        Khan Academy for single-sign on.
        """
        http = self.get_auth_http_client()
        http.fetch(self._oauth_request_token_url(callback_uri=callback_uri), self.async_callback(
            self._on_request_token, self._OAUTH_AUTHENTICATE_URL, None))
    
    def khanacademy_authorize_redirect(self, callback_uri=None, extra_params=None,
                           http_client=None):
        """Builds the authorization url and redirects user to request token
        """
        if callback_uri and getattr(self, "_OAUTH_NO_CALLBACKS", False):
            raise Exception("This service does not support oauth_callback")
        if http_client is None:
            http_client = self.get_auth_http_client()
        if getattr(self, "_OAUTH_VERSION", "1.0a") == "1.0a":
            http_client.fetch(
                self._oauth_request_token_url(callback_uri=callback_uri,
                                              extra_params=extra_params),
                self.async_callback(
                    self._on_request_token,
                    self._OAUTH_AUTHORIZE_URL,
                callback_uri))
        else: 
            extra_params = { "oauth_callback" : callback_uri }
            self.redirect( self._oauth_request_token_url(extra_params=extra_params) ),

    def get_authenticated_khanacademy_user(self, callback, http_client=None):
        """Makes initial authenticated request to get Khan Academy user 
            information
        """
        key = escape.utf8(self.get_argument("oauth_token"))
        verifier = self.get_argument("oauth_verifier", None)
        secret = self.get_argument("oauth_token_secret")

        token = { 'secret' : secret, 'verifier' : verifier, 'key' : key }

        if http_client is None:
            http_client = self.get_auth_http_client()

        http_client.fetch(self._oauth_access_token_url(token),
                  self.async_callback(self._on_access_token, callback))

    def khanacademy_request(self, path, callback, access_token=None,
                           post_args=None, **args):
        """Fetches the given API path, e.g., "/user"

        If the request is a POST, post_args should be provided. Query
        string arguments should be given as keyword arguments.

        All the Khan Academy methods are documented at
        https://github.com/Khan/khan-api/wiki/Khan-Academy-API-Methods

        Many methods require an OAuth access token which you can obtain
        through khanacademy_authorize_redirect() and 
        get_authenticated_khanacademy_user(). The
        user returned through that process includes an 'access_token'
        attribute that can be used to make authenticated requests via
        this method. Example usage::

            class MainHandler(tornado.web.RequestHandler,
                              tornado.auth.KhanAcademyMixin):
                @tornado.web.authenticated
                @tornado.web.asynchronous
                def get(self):
                    self.flickr_request(
                        "/videos/<youtube_id>",
                        access_token=user["access_token"],
                        callback=self.async_callback(self._on_post))

                def _khanacdemy_on_user(self, user):
                    if not user:
                        self.clear_all_cookies()
                        raise tornado.web.HTTPError(500, "Couldn't retrieve user information")

                    self.render('index.html', user=user)

        """
        if path.startswith('http:') or path.startswith('https:'):
            # Raw urls are useful for e.g. search which doesn't follow the
            # usual pattern: http://search.twitter.com/search.json
            url = path
        else:
            url = self._KHANACADEMY_BASE_URL + '/api/v1' + path 
        # Add the OAuth resource request signature if we have credentials
        if access_token:
            all_args = dict()
            all_args.update(args)
            if post_args is not None:
                all_args.update(post_args)
            method = "POST" if post_args is not None else "GET"
            oauth = self._oauth_request_parameters(
                url, access_token, all_args, method=method)
            # args.update(oauth)
        if args:
            url += "?" + urllib.urlencode(args)
        callback = self.async_callback(self._on_khanacademy_request, callback)
        http = self.get_auth_http_client()
        log(build_oauth_header(oauth))
        if post_args is not None:
            print url
            http.fetch(url, method="POST", body=urllib.urlencode(args),
                       callback=callback,
                       headers={'Authorization': build_oauth_header(oauth)})
        else:
            print "wer're doin it motherfuckers %r" % url
            http.fetch(url, callback=callback,
                    headers={'Authorization': build_oauth_header(oauth)})

    def _on_khanacademy_request(self, callback, response):
        log("Got response %s fetching %s", (str(response), response.body))
        callback(json.loads(response.body))

    def _oauth_consumer_token(self):
        self.require_setting("khanacademy_consumer_key", "Khan Academy OAuth")
        self.require_setting("khanacademy_consumer_secret", "Khan Academy OAuth")
        return {
            'key': self.settings["khanacademy_consumer_key"],
            'secret': self.settings["khanacademy_consumer_secret"]
        }

    def _oauth_get_user(self, access_token, callback):
        callback = self.async_callback(self._parse_user_response, callback)

        self.khanacademy_request(
            "/user",
            access_token=access_token,
            callback=callback
        )

    def _parse_user_response(self, callback, user):
        if user:
            callback(user)

class ZeoMixin(tornado.auth.OAuthMixin):
    """Zeo OAuth authentication.

    To authenticate with Zeo, register your application with
    Zeo at https://dev.zeo.com/apps. Then copy your Consumer Key and
    Consumer Secret to the application settings 'zeo_consumer_key' and
    'zeo_consumer_secret'. Use this Mixin on the handler for the URL
    you registered as your application's Callback URL.

    When your application is set up, you can use this Mixin like this
    to authenticate the user with Zeo and get access to their data::

        class ZeoHandler(tornado.web.RequestHandler,
                             tornado.auth.ZeoMixin):
            @tornado.web.asynchronous
            def get(self):
                if self.get_argument("oauth_token", None):
                    self.get_authenticated_user(self.async_callback(self._on_auth))
                    return
                self.authorize_redirect()

            def _on_auth(self, user):
                if not user:
                    raise tornado.web.HTTPError(500, "Zeo auth failed")
                # Save the user using, e.g., set_secure_cookie()

    The user object returned by get_authenticated_user() includes the
    attributes 'user-id', 'name', and all of the custom Fitbit user
    attributes describe at
    https://wiki.zeo.com/display/API/API-Get-User-Info
    in addition to 'access_token'. You should save the access token with
    the user; it is required to make requests on behalf of the user later
    with zeo_request().
    """
    _OAUTH_REQUEST_TOKEN_URL = "https://mysleep.myzeo.com:8443/zeows/oauth/request_token"
    _OAUTH_ACCESS_TOKEN_URL = "https://mysleep.myzeo.com:8443/zeows/oauth/access_token"
    _OAUTH_AUTHORIZE_URL = "https://mysleep.myzeo.com:8443/zeows/oauth/confirm_access"
    _OAUTH_NO_CALLBACKS = False
    _ZEO_BASE_URL = "https://api.myzeo.com"
    _OAUTH_VERSION ="1.0"
    _ZEO_API_KEY = '64DD3496BF4D5E090DE4542A5C39F06F'
    _REFERER = 'http://stu.itp.nyu.edu/~pmd299'
    

    def authenticate_redirect(self, callback_uri=None):
        """Just like authorize_redirect(), but auto-redirects if authorized.

        This is generally the right interface to use if you are using
        Zeo for single-sign on.
        """

        http = self.get_auth_http_client()
        http.fetch(self._oauth_request_token_url(callback_uri=callback_uri), self.async_callback(
            self._on_request_token, self._OAUTH_AUTHORIZE_URL, None))

    def zeo_request(self, path, callback, referer, access_token=None,
                           post_args=None, **args):
        """Fetches the given API path, e.g., #example query

        The path should not include the format (we automatically append
        ".json" and parse the JSON output).

        If the request is a POST, post_args should be provided. Query
        string arguments should be given as keyword arguments.

        All the Zeo methods are documented at
        http://mysleep.myzeo.com/api/api.shtml

        Many methods require an OAuth access token which you can obtain
        through authorize_redirect() and get_authenticated_user(). The
        user returned through that process includes an 'access_token'
        attribute that can be used to make authenticated requests via
        this method. Example usage::

            class MainHandler(tornado.web.RequestHandler,
                              tornado.auth.FitbitMixin):
                @tornado.web.authenticated
                @tornado.web.asynchronous
                def get(self):
                    self.zeo_request(
                        "/user/-/activities/log/steps/date/today/7d",
                        access_token=user["access_token"],
                        callback=self.async_callback(self._on_post))

	            def _on_auth(self, user):
	                if not user:
	                    raise tornado.web.HTTPError(500, "Zeo auth failed")
	                # Save the user using, e.g., set_secure_cookie()
        """
        
        if path.startswith('http:') or path.startswith('https:'):
            # Raw urls are useful for e.g. search which doesn't follow the
            # usual pattern: http://search.twitter.com/search.json
            url = path
        else:
            url = self._FITBIT_BASE_URL + path + ".json"
        # Add the OAuth resource request signature if we have credentials
        if access_token:
            all_args = dict()
            all_args.update(args)
            if post_args is not None:
                all_args.update(post_args)
            method = "POST" if post_args is not None else "GET"
            oauth = self._oauth_request_parameters(
                url, access_token, all_args, method=method)
            # args.update(oauth)
        if args:
            url += "?" + urllib.urlencode(args)
        callback = self.async_callback(self._on_zeo_request, callback)
        http = self.get_auth_http_client()
        log(build_oauth_header(oauth))
        if post_args is not None:
            print url
            http.fetch(url, method="POST", body=urllib.urlencode(args),
                       callback=callback,
                       headers={ 'Authorization': build_oauth_header(oauth), "Referer" : referer })
        else:
            print url
            http.fetch(url, callback=callback,
                    headers={ 'Authorization': build_oauth_header(oauth), 'Referer' : referer })

    def _on_zeo_request(self, callback, response):
        log("Got response %s fetching %s", (str(response), response.body))
        callback(json.loads(response.body))

    def _oauth_consumer_token(self):
        self.require_setting("zeo_consumer_key", "Zeo OAuth")
        self.require_setting("zeo_consumer_secret", "Zeo OAuth")
        return {
            'key': self.settings["zeo_consumer_key"],
            'secret': self.settings["zeo_consumer_secret"]
        }

    def _oauth_get_user(self, access_token, callback):
        print "getting the user stuff"
        callback = self.async_callback(self._parse_user_response, callback)

        self.zeo_request(
            "https://api.myzeo.com:8443/zeows/api/v1/sleeperService/getPreviousSleepStats?key=64DD3496BF4D5E090DE4542A5C39F06F",
            access_token=access_token,
            referer="http://stu.itp.nyu.edu/~pmd299",
            callback=callback
        )

    def _parse_user_response(self, callback, user):
        if user:
            user["username"] = user["user"]["encodedId"]
        callback(user)
