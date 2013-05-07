
var checkUserStatus = function(){

	var username = $('#phro_username').html()

    if ( username !== "" && typeof(user) === "undefined" ) {
		console.log("username but no user object")
    	// get user data
		 $.when( $.getJSON('v1/users/pdarche') )    
          .done(
            function(data){

            	console.log("the data is", data)

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

                // var traits = new app.Traits({
                //     firstPriority : undefined,
                //     firstPriorityActiveSpecific : data.adjectives.first_priority_specific,
                //     secondPriority : new Trait({ name : "sustainable" }),
                //     secondPriorityActiveSpecific : data.adjectives.second_priority_specific,
                //     thirdPriority : new Trait({ name : "educated" }),
                //     thirdPriorityActiveSpecific : data.adjectives.third_priority_specific
                // })

				var traits = new app.Traits()

                traits.set({ firstPriority : new Trait({ name : "healthy" }) })     
                traits.set({ firstPriorityActiveSpecific : "cardiovascular"})
                traits.set({ secondPriority : new Trait({ name : "sustainable" }) })
                traits.set({ secondPriorityActiveSpecific : "carbon" })
                traits.set({ thirdPriority : new Trait({ name : "educated" }) })
                traits.set({ secondPriorityActiveSpecific : "mathematical" })

                window.user = new User()

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
                    'traits' : traits
                })

                user.get('traits').get('firstPriority').get('traitSpecifics').fetch().then(
                    function(){
                        _.each( user.get('traits').get('firstPriority').get('traitSpecifics').models, function( model ){
                            model.get('recommendedBehaviors').fetch().then(
                                function(){
                                    _.each( model.get('recommendedBehaviors').models, function( subModel ){
                                        subModel.get('actions').fetch()
                                        subModel.get('currentStatus').fetch()
                                    })
                                }
                            )
                        })
                    }
                )
           
        })


		$('#heading').fadeIn()
		$('#adjective_1').addClass("healthy-accent")

    } else if ( username === "" ) {
    	window.location = '/'
    }
}

var priorities = [ "first_priority", "second_priority", "third_priority" ]

var categoryAttributes = {

	"physicalActivity" : {
		"steps" : "steps",
		"distance" : "distance", 
		"minutes sedentary" : "mins_sedentary",			 
		"minutes lightly active" : "mins_lightly_active",
		"minutes fairly active" : "mins_fairly_active",
		"minutes very active" : "mins_very_active", 
		"floors climbed" : "floors",
		"calories burned" : "calories_out"
	},

	"sleep" : {
		"total sleep zq points" : "total_z_zq_points",
		"time in rem zq points" : "time_in_rem_zq_points",
		"day feel" : "day_feel", 
		"zq" : "zq",
		"time in wake percentage" : "time_in_wake_percentage",
		"time to z" : "time_to_z",
		"total sleep" : "total_z",
		"time in deep percentage" : "time_in_deep_percentage",
		"time in wake zq points" : "time_in_wake_zq_points",
		"time in rem" : "time_in_rem",
		"time in wake" : "time_in_wake",
		"time in rem percentage" : "time_in_wake_rem_percentage",
		"time in deep zq points" : "time_in_deep_zq_points",
		"awakenings" : "awakenings",
		"time in light" : "time_in_light",
		"morning feel" : "morning_feel",
		"time in deep" : "time_in_deep",
		"time in light percentage" : "time_in_light_percentage"
	},

	"nutrition" : {
		"vitamin a" : "vit_a",
		"vitamin c" : "vit_c",
		"venue" : "venue",
		"total carbs" : "total_carbs",
		"calcium" : "calcium",
		"trans fat" : "trans_fat",
		"saturated fat" : "saturated_fat",
		"protein" : "protein",
		"calories from fat" : "calories_from_fat",
		"total fat" : "total_fat",
		"meal name" : "meal_item_name",
		"calories" : "calories",
		"sugar" : "sugar",
		"fiber" : "fiber",
		"cholesterol" : "cholesterol"
	}

}

var pieValues = {
	"sleep" : [ 
		"time_in_light", "time_in_deep", "time_in_rem", "time_in_wake", "time_to_z"
	 ],

	"physicalActivity" : [
		"mins_sedentary", "mins_fairly_active", "mins_lightly_active", "mins_very_active"
	],

	"nutrition" : [
		"total_fat", "total_carbs", "protein"
	]
}

var adjectives = [
	{ name : "healthy", attributes : [ "fun", "tasty", "pizza" ], wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=health" }, 
	{ name : "sustainable", attributes : [ "carbon-neutral", "cradel to cradel consumptions", "reduced energy use", "reduce consumption" ], wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=sustainability" }, 
	{ name : "intelligent", attributes : [ "working memory", "spatial reasoning", "abstract reasoning" ], wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=intelligence"},
	{ name : "generous", attributes : [ "microloans", "friends birthdays", "pizza time"], wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=generosity"}, 
	{ name : "productive", attributes : [ "don't run away when scary things happen"], wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=courage"},
	{ name : "focused", attributes : ["some things ", "stuff", "pizza" ], wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=focus"},
	{ name : "attentive", attributes : ["some things ", "stuff", "pizza" ], wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=attention"},
	{ name : "kind", attributes : ["some things ", "stuff", "pizza" ], wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=kindness" },
	{ name : "punctual", attributes : ["some things ", "stuff", "pizza" ], wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=puncutality"},
	{ name : "just", attributes : ["some things ", "stuff", "pizza" ], wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=justice"},
	{ name : "disciplined", attributes : ["some things ", "stuff", "pizza" ], wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=discipline"},
	{ name : "honest", attributes : ["some things ", "stuff", "pizza" ], wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=honesty"},
	{ name : "respectful", attributes : ["some things ", "stuff", "pizza" ], wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=respect"},
	{ name : "responsible", attributes : ["some things ", "stuff", "pizza" ], wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=responsibility"},
	{ name : "educated", attributes : ["some things ", "stuff", "pizza" ], wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=education"},
	{ name : "wise", attributes : ["some things ", "stuff", "pizza" ], wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=wisdom"}
]


var adj = {
	"healthy" : { 
		attributes : [ "improve my cardiovascular health", "improve my musculoskelatal health", "improve my mental health", "improve my respiratory health" ], 
		wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=health",
		actions : [ "exercise 45 minutes per day", "quite smoking", "limit saturated fat intake to less than 20 grams per day", "limit sodium intake to 2400mg per day", "limit alchohol consumption to 1 drink per day (average)", "reduce stress" ],
		actions_heading : "Experts in cardiovascular health recommend"
	}, 
	"sustainable" : { 
		attributes : [ "reduce carbon footprint", "reduce waste", "reduce energy use", "reduce meat consumption" ],
		wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=sustainability",
		actions : ["limit carbon footprint to 2 tons per year", "limit electricity consumption to 1000 Watts per year", "purchase primarily from B Corporations"],
		actions_heading : "Sustainability experts recommend"
	},
	"intelligent" : { 
		attributes : [ "working memory", "spatial reasoning", "abstract reasoning" ], 
		wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=intelligence",
		actions : []
	},
	"generous" : { 
		attributes : [ "microloans", "friends birthdays", "pizza time"], 
		wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=generosity", 
		actions : []
	},
	"productive" : { 
		attributes : [ "don't run away when scary things happen"], 
		wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=courage",
		actions : []
	},
	"focused" : { 
		attributes : ["some things ", "stuff", "pizza" ], 
		wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=focus",
		actiosn : []
	},
	"attentive" : { 
		attributes : ["some things ", "stuff", "pizza" ], 
		wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=attention",
		actiosn : []
	},
	"kind" : { 
		attributes : ["some things ", "stuff", "pizza" ], 
		wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=kindness",
		actiosn : []
	},
	"punctual" : { 
		attributes : ["some things ", "stuff", "pizza" ], 
		wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=puncutality",
		actiosn : []
	},
	"just" : { 
		attributes : ["some things ", "stuff", "pizza" ], 
		wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=justice",
		actiosn : []
	},
	"disciplined" : { 
		attributes : ["some things ", "stuff", "pizza" ], 
		wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=discipline",
		actiosn : []
	},
	"honest" : { 
		attributes : ["some things ", "stuff", "pizza" ], 
		wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=honesty",
		actiosn : []
	},
	"respectful" : { 
		attributes : ["some things ", "stuff", "pizza" ], 
		wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=respect",
		actiosn : []
	},
	"responsible" : { 
		attributes : ["some things ", "stuff", "pizza" ], 
		wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=responsibility",
		actiosn : []
	},
	"educated" : { 
		attributes : ["expand my literary knowledge", "expand my scientific knowledge", "expand my historical knowledge", "expand my mathematical knowledge", "expand my social scientific knowledge" ], 
		wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=education",
		actions : [ "eat pizza", "eat more pizza", "eat a lot of pizza" ],
		actions_heading : "Education experts recommend"
	},
	"wise" : { 
		attributes : ["some things ", "stuff", "pizza" ], 
		wiki_url : "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&titles=wisdom",
		actiosn : []
	}
}

var trackers = [
		{ name : "Fitbit" },
		{ name : "Zeo" },
		{ name : "Withings" },
		{ name : "Flickr" },
		{ name : "Foursquare" },
		{ name : "Facebook" },
		{ name : "Google" },
		{ name : "Twitter" },
		{ name : "Khan Academy" },
		{ name : "Good Reads" },
		{ name : "GitHub" },
		{ name : "WattVision" }		
	]

var accents = {
	sustainable : '#00B25C',
	healthy : '#FF8E00',
	educated : '#FF4100'
}



