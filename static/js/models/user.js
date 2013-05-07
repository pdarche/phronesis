var app = app || {};

var User = Backbone.Model.extend({
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
            traits : undefined
        },
        initialize: function(){

            this.on("change", function(model){
                console.log("the user model has changed")
                // model.save()
            })
        
        }
});

app.Traits = Backbone.Model.extend({

    defaults : {
        firstPriority : undefined,
        firstPriorityActiveSpecific : undefined,
        secondPriority : undefined,
        secondPriorityActiveSpecific : undefined,
        thirdPriority : undefined,
        thirdPriorityActiveSpecific : undefined 
    },
    initialize : function(){
        console.log("just initialzed user traits")
        this.on("change:firstPriority", function(model){
            
            var prevAdj = $('#adjective_1').html(),
                prevClass = prevAdj + "-accent",
                newAdj = this.get('firstPriority').get('name'),
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

        this.on("change:secondPriority", function(model){
            
            var prevAdj = $('#adjective_2').html(),
                prevClass = prevAdj + "-accent",
                newAdj = this.get('secondPriority').get('name'),
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

        this.on("change:thirdPriority", function(model){
            
            var prevAdj = $('#adjective_3').html(),
                prevClass = prevAdj + "-accent",            
                newAdj = this.get('thirdPriority').get('name'),
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

var Trait = Backbone.RelationalModel.extend({
    relations : [{
        type : Backbone.HasMany,
        key : 'traitSpecifics',
        relatedModel : 'TraitSpecific',
        collectionType : 'TraitSpecifics',
        collectionOptions : function(m){
            return {
                parentTrait : m.get('name')
            }
        },
        // autoFetch : true,
        reverseRelation : {
            key : 'parentTrait',
            includeInJSON: 'id'
        }
    }]
})

var TraitSpecific = Backbone.RelationalModel.extend({
    relations : [{
        type : Backbone.HasMany,
        key : 'recommendedBehaviors',
        relatedModel : 'RecommendedBehavior',
        collectionType : 'RecommendedBehaviors',
        // autoFetch : true,
        reverseRelation : {
            key : 'parentSpecific',
            includeInJSON : 'id'
        }
    }],
    defaults : {
        info : undefined,
        activeRecommendedBehavior : undefined
    },
    initialize : function(){

    }
})

var RecommendedBehavior = Backbone.RelationalModel.extend({
    relations : [{
        type : Backbone.HasMany,
        key : 'actions',
        relatedModel : 'Action',
        collectionType : 'Actions',
        // autoFetch : true,
        reverseRelation : {
            key : 'parentBehavior',
            includeInJSON : 'id'
        }
    },
    {
        type : Backbone.HasMany,
        key : 'currentStatus',
        relatedModel : 'CurrentStatus',
        collectionType : 'CurrentStatuses',
        // autoFetch : true,
        reverseRelation : {
            key : 'parentBehavior',
            includeInJSON : 'id'
        }
    }],
    defaults : {
        // dataTypes: undefined,
        // triggers : [] 
    },
    initialize : function(){

    }
})

var CurrentStatus = Backbone.RelationalModel.extend({
    defaults : {

    }, 
    initialize : function(){
        console.log("initializing an action")
    }
})

var Action = Backbone.RelationalModel.extend({
    defaults : {
        pizza : undefined
    },
    initialize : function(){
        console.log("initializing an action")
    }
})

// collections
var Traits = Backbone.Collection.extend({
    model : Trait,
    initialize : function() {
        console.log("initializing trait")
    }
})

var TraitSpecifics = Backbone.Collection.extend({
    model : TraitSpecific,
    url : function(){
        return '/v1/ref/traits/traitSpecifics?for_trait=' + this.parentTrait.get('name')
    }
})

var RecommendedBehaviors = Backbone.Collection.extend({
    model : RecommendedBehavior,
    url : function(){
        console.log("the parent's name is ", this.parentSpecific.get('trait_specific'))
        return '/v1/ref/traits/traitSpecifics/recommendedHabit?for_trait_specific=' + this.parentSpecific.get('trait_specific')
    },
    initialize : function() {
        // console.log("initializing recommendedBehaviors")
    }
})

var Actions = Backbone.Collection.extend({
    model : Action,
    url : function(){
        console.log("fetching with parent behavior ", this.parentBehavior.get('rec_habit_key'))
        return '/v1/ref/traits/traitSpecifics/recommendedHabit/actionsToTake?for_rec_habit_key=' + this.parentBehavior.get('rec_habit_key')
    },
    initialize : function() {
        console.log("initializing actions to take")
    }
})

var CurrentStatuses = Backbone.Collection.extend({
    model : CurrentStatus,
    url : function(){
        console.log("fetching with parent behavior ", this.parentBehavior.get('rec_habit_key'))
        return '/v1/ref/traits/traitSpecifics/recommendedHabit/currentStatus?for_rec_habit_key=' + this.parentBehavior.get('rec_habit_key')
    },
    initialize : function() {
        console.log("initializing current statuses")
    }
})

