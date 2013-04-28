
var app = app || {}; 

app.Login = Backbone.View.extend({

    initialize: function(){

        var username = $('#phro_username').html()
        username !== "" ? window.location = 'http://localhost:8000/#profile' : null
        
        if ( !($.isFunction(this.template)) ){

            var self = this;
            $.get('/static/js/templates/landingpage.handlebars', function(tmpl){
                self.template = tmpl;
                self.render();
                $('#greeting p').removeClass('hidden-way-top')
                setTimeout(self.updateGreeting, 1800)
            })

        } else {

            console.log("gots the template");

        }

    },

    render: function(){

        var source = $(this.template).html();
        var template = Handlebars.compile(source);
        this.$el.html( template );

        return this;

    },

    events : {

        "click #signup_button" : "signup",
        "click .signup-container span a" : "signin"

    },

    signup : function() {

        // this.accept()
        var self = this,
            username = $('#username').val(),
            password = $('#password').val(),
            postData = { username : username, password : password }

        $.post('v1/login', postData, function(res){
            res === "success" ? self.accept() : self.reject
        })

    },

    signin : function( ev ){

        ev.preventDefault()
        $('#re-enter').fadeOut()
        $('.signup-container').addClass('signin')
        $('#signup_button').html("sign in")

    },

    accept : function() {

        var self = this

         $.when( $.getJSON('v1/users/pdarche') )    
          .done(
            function(data){

                if ( data.facebook_user_info !== null ) {          
                    var facebook_user_info = {
                        'facebook_first_name' : data.facebook_user_info.facebook_first_name,
                        'facebook_last_name' : data.facebook_user_info.facebook_last_name,
                        'facebook_name' : data.facebook_user_info.facebook_name,
                        'facebook_picture' : data.facebook_user_info.facebook_picture
                    } 
                } else {

                    facebook_user_info = undefined

                }

                if ( data.flickr_user_info !== null ) {
                    var flickr_user_info = {
                        'flickr_nsid' : data.flickr_user_info.flickr_nsid,
                        'flickr' : data.flickr_user_info.flickr_user_url
                    }
                } else {

                    flickr_user_info = undefined

                }

                var foursquare_user_info = {
                    'foursquare_bio' : data.foursquare_user_info.foursquare_bio,
                    'foursquare_home_city' : data.foursquare_user_info.foursquare_home_city,
                    'foursquare_user_photo' : data.foursquare_user_info.foursquare_user_photo
                }

                var ftbt_user_info = {
                    'ftbt_user_info' : data.ftbt_user_info.ftbt_avatar,
                    'ftbt_gender' : data.ftbt_user_info.ftbt_gender,
                    'ftbt_nickname' : data.ftbt_user_info.ftbt_nickname,
                    'ftbt_offset_from_utc_millis' : data.ftbt_offset_from_utc_millis
                }

                var google_user_info = {
                    'google_claimed_id' : data.google_user_info.google_claimed_id,
                    'google_email' : data.google_user_info.google_email,
                    'google_first_name' : data.google_user_info.google_first_name,
                    'google_last_name' : data.google_user_info.google_last_name,
                    'google_locale' : data.google_user_info.google_locale,
                    'google_name' : data.google_user_info.google_name
                }

                var khanacademy_user_info = {
                    'khanacademy_key_email' : data.khanacademy_user_info.khanacademy_key_email,
                    'khanacademy_profile_root' : data.khanacademy_user_info.khanacademy_profile_root
                }

                var openpaths_user_info = {
                    'created_at' : data.openpaths_user_info.created_at
                }

                if ( data.twitter_user_info !== null ) {
                    var twitter_user_info = {
                        'twitter_location' : data.twitter_user_info.twitter_location,
                        'twitter_name' : data.twitter_user_info.twitter_name,
                        'twitter_profile_image_url' : data.twitter_user_info.twitter_profile_image_url,
                        'twitter_time_zone' : data.twitter_user_info.twitter_time_zone
                    }
                } else {
                    twitter_user_info = undefined
                }

                var zeo_user_info = {
                    'created_at' : data.zeo_user_info.created_at
                }

                var adjectives = new app.Adjectives({
                    first_priority : data.adjectives.first_priority,
                    first_priority_specifics : data.adjectives.first_priority_specifics,
                    second_priority : data.adjectives.second_priority,
                    second_priority_specifics : data.adjectives.second_priority_specifics,
                    third_priority : data.adjectives.third_priority,
                    third_priority_specifics : data.adjectives.third_priority_specifics
                })  

                window.user = new app.User()
                user.set({
                    'date_of_birth' : data.date_of_birth,
                    'username' : data.username,
                    'user_since' : data.user_since,
                    'facebook_user_info' : facebook_user_info,
                    'flickr_user_info' : flickr_user_info,
                    'foursquare_user_info' : foursquare_user_info,
                    'ftbt_user_info' : ftbt_user_info,
                    'google_user_info' : google_user_info,
                    'khanacademy_user_info' : khanacademy_user_info,
                    'openpaths_user_info' : openpaths_user_info,
                    'time_zone' : data.time_zone,
                    'twitter_user_info' : twitter_user_info,
                    'zeo_user_info' : zeo_user_info,
                    'adjectives' : adjectives
                })

                var username = user.get('username')
                $('#phro_username').text( username )
                $('.signup-container').addClass('accept-top')
                $('.logo-container').addClass('accept-left')
                setTimeout( self.move, 500)
            })

    },

    reject : function() {

        d3.select('.signup_container')
            .style('box-shadow', '0px 2px 10px lightred')
            .style('border', '1px solid lightred')
          .transition()

    },

    move : function(){

        $('.signup_container').remove()
        window.location.hash = 'define'

    },

    updateGreeting : function() {

        $('#greeting').children().fadeOut('fast').queue( function(){
            $(this).remove()
            $('#greeting').append('<p>sign up <span> or <a href="#">sign in</a></span></p>')
                          .hide().fadeIn()
        })
        

    }

});