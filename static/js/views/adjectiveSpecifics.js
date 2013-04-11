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

        var source = $(this.template).html()
        var template = Handlebars.compile( source );
        this.$el.html( template( this.model ) )

    },

    events : {
        "click .adjective-attribute" : "advanceAttributes"
    },

    advanceAttributes : function( ev ){

        console.log("advancing")
        $('.active-adj').removeClass('active-adj')
        $('.chosen-adj').eq(this.state).find('.adjective').addClass('active-adj')
        this.state++

    }

})