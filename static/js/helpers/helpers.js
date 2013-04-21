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

