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
            },
            adjectives : {
                first_priority : undefined,
                first_priority_specifics : undefined,
                second_priority : undefined,
                second_priority_specifics : undefined,
                third_priority : undefined,
                third_priority_specifics : undefined
            }
        },
        initialize: function(){

            this.on("change", function(model){
                console.log("the user model has changed")
                // model.save()
            })
        
        }
});


app.Adjectives = Backbone.Model.extend({

    defaults : {
        first_priority : undefined,
        first_priority_specifics : [],
        second_priority : undefined,
        second_priority_specifics : [],
        third_priority : undefined,
        third_priority_specifics : []
    },
    initialize : function(){

        this.on("change:first_priority", function(model){
            
            var prevAdj = $('#adjective_1').html(),
                prevClass = prevAdj + "-accent",
                newAdj = this.get('first_priority'),
                newAccent = newAdj + "-accent",
                newClasses = newAdj + " " + newAccent

            $('#adjective_1').removeClass(prevAdj).removeClass(prevClass)        

            console.log("the first priority has changed")
            console.log("the new first priority", newAdj)

            if ( newAdj !== null ){

                $('#adjective_1').addClass(newAdj)
                $('#adjective_1').html( newAdj )

            }

        })

        this.on("change:second_priority", function(model){
            
            var prevAdj = $('#adjective_2').html(),
                prevClass = prevAdj + "-accent",
                newAdj = this.get('second_priority'),
                newAccent = newAdj + "-accent",
                newClasses = newAdj + " " + newAccent
            
            $('#adjective_2').removeClass(prevAdj)
                .removeClass(prevClass)
            
            if ( newAdj !== null ){

                $('#adjective_2').addClass(newAdj)
                $('#adjective_2').html( newAdj )

            }
            console.log("the second priority has changed")

        })

        this.on("change:third_priority", function(model){
            
            var prevAdj = $('#adjective_3').html(),
                prevClass = prevAdj + "-accent",            
                newAdj = this.get('third_priority'),
                newAccent = newAdj + "-accent",
                newClasses = newAdj + " " + newAccent

            $('#adjective_3').removeClass(prevAdj)
                .removeClass(prevClass)
            
            if ( newAdj !== null ){

                $('#adjective_3').addClass(newAdj)
                $('#adjective_3').html( newAdj )

            }

            console.log("the thrid priority has changed")

        })

    }

})



