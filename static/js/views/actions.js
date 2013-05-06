var app = app || {};

app.ActionsView = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/howPartial.handlebars', function(tmpl){
                self.template = tmpl
                self.render()

                var accentClass = $('.active-adj').html() + "-accent"
                $('#vaff').addClass(accentClass + " chosen-action")

            })

        } else {

            console.log("gots the template")

        }

    },

    render : function() {

        this.$el.empty()

        var dataz = []
        _.each( this.collection.get('recommendedBehaviors').models, function(model){
            var rec_habit_key = model.attributes.rec_habit_key,
                rec_habit = model.attributes.rec_habit,
                datum = { "rec_habit" : rec_habit, "rec_habit_key" : rec_habit_key }

            dataz.push(datum)
        })

        var source = $(this.template).html();
        var template = Handlebars.compile( source );
        this.$el.append( template( { "habits" : dataz } ) );
        $('#action_list').hide().fadeIn()

    }

    // events : {

        // "click .nav-adjective" : "toggleActions"

    // }

    // toggleActions : function( ev ){

    //     var newAdj = $(ev.target).attr('class')

    // }

})