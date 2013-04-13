var app = app || {};

app.CardioView = Backbone.View.extend({

    index : undefined,

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/health/cardiovascular-health.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
            })

        } else {

            console.log("gots the template")

        }

    },

    render : function() {

        console.log("the model is", this.model)

        var source = $(this.template).html();
        var template = Handlebars.compile( source );
        this.$el.html( template( { "actions" : this.model.actions } ) );

    },

})