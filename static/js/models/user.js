var app = app || {};

app.User = Backbone.Model.extend({
        defaults: {
            date_of_birth : undefined,
            username : undefined,
            user_since : undefined,
            facebook_user_info : {
                facebook_first_name : undefined,
                facebook_last_name : undefined,
                facebook_name : undefined,
                facebook_picture : undefined
            },
            flickr_user_info : {
                flickr_nsid : undefined,
                flickr_user_url : undefined
            },
            foursquare_user_info : {
                foursquare_bio : undefined,
                foursquare_home_city : undefined,
                foursquare_user_photo : undefined
            },
            ftbt_user_info : {
                ftbt_avatar : undefined,
                ftbt_gender : undefined,
                ftbt_nickname : undefined,
                ftbt_offset_from_utc_millis: undefined,
            },
            google_user_info : {
                google_claimed_id : undefined,
                google_email : undefined,
                google_first_name : undefined,
                google_last_name : undefined,
                google_locale : undefined,
                google_name : undefined
            },
            khanacademy_user_info : {
                khanacademy_key_email : undefined,
                khanacademy_profile_root : undefined
            },
            openpaths_user_info : {
                created_at : undefined
            },
            time_zone : undefined,
            twitter_user_info : {
                twitter_location : undefined,
                twitter_name : undefined,
                twitter_profile_image_url : undefined,
                twitter_time_zone : undefined,
            },
            zeo_user_info : {
                created_at : undefined
            }
        },
        initialize: function(){

            this.on("change", function(model){
                console.log("the user model has changed")
                // model.save()
            })
        }
});