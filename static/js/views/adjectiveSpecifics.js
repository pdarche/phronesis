var app = app || {};

app.AdjectiveSpecifics = Backbone.View.extend({

    state : 1,

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/adjectiveSpecifics.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
            })

        } else {

            console.log("gots the template")    

        }

    },

    render : function() {
        var data = []
        _.each(this.collection.models, function( model ){
            var as_heading = model.attributes.as_heading,
                trait_specific = model.attributes.trait_specific
            data.push( { "as_heading" : as_heading, "trait_specific" : trait_specific })
        })  

        var source = $(this.template).html()
        var template = Handlebars.compile( source );
        this.$el.html( template( { "attributes" : data } ) )

       $('#adjective_specifics').delay(500).css({ 
            "opacity" : 1,
            "z-index" : 2
        })

    },

    events : {
        "click .adjective-attribute" : "advanceAttributes"
    },

    advanceAttributes : function( ev ){

    }

})