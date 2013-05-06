var app = app || {};

app.ActionsToTakeView = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){
                
            $.when( $.get('/static/js/templates/actions.handlebars') )
             .done(
                function( tmpl ){
                    self.template = tmpl
                    self.render( self.model.pluck('action') )                      
                }
             )
                    
            var accentClass = $('.active-adj').html() + "-accent"

        } else {

            console.log("gots the template")

        }

    },

    render : function( data ) {

        console.log("incoming data is", data)

        var source = $(this.template).html();
        var template = Handlebars.compile( source );
        this.$el.html( template({ "actions" : data }) );

    },

    events : {

        // "click .nav-adjective" : "toggleActions"

    }
})