var app = app || {};

app.ActionsView = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/howPartial.handlebars', function(tmpl){
                self.template = tmpl
                self.render()                
            })

        } else {

            console.log("gots the template")

        }

    },

    render : function() {

        console.log("the model is", this.model.actions )

        var source = $(this.template).html();
        var template = Handlebars.compile( source );
        this.$el.html( template( { "actions" : this.model.actions }) );

    }

    // events : {

        // "click .nav-adjective" : "toggleActions"

    // }

    // toggleActions : function( ev ){

    //     var newAdj = $(ev.target).attr('class')

    // }

})