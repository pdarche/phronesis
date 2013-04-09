var app = app || {};

app.ProfileView = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/profile.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
            })

        } else {

            self.render()

        }

    },

    render : function() {

        var source = $(this.template).html()
        var template = Handlebars.compile( source );
        this.$el.html( template )

        $('div').css('opacity', 1)

    }

})