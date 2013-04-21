var app = app || {};

app.ActionsView = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/howPartial.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
                var accentClass = $('.active-adj').html() + "-accent"
                $('.action').eq(0).addClass(accentClass + ' chosen-action')

            })

        } else {

            console.log("gots the template")

        }

    },

    render : function() {

        this.$el.empty()


        var source = $(this.template).html();
        var template = Handlebars.compile( source );
        this.$el.append( template();
        $('#action_list').hide().fadeIn()

    }

    // events : {

        // "click .nav-adjective" : "toggleActions"

    // }

    // toggleActions : function( ev ){

    //     var newAdj = $(ev.target).attr('class')

    // }

})