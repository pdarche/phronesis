var app = app || {};

app.AddTrackers = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/addTrackers.handlebars', function(tmpl){
                self.template = tmpl
                self.render() 
                $('#instructions').removeClass('hidden-top')
            })

        } else {

            console.log("gots the template")

        }

    },

    render : function() {

        var source = $(this.template).html()
        var template = Handlebars.compile( source );
        this.$el.html( template( { "tracker" : trackers } ) )

        $('#tracker_container').isotope({
            layoutMode: 'masonryHorizontal',
            masonryHorizontal: {
                rowHeight: 40
            },
            resizesContainer: false,
            gutterWidth: 20
        })

    },

    events : {

        "click .tracker-wrap" : "highlightTracker",
        "click #done" : "showProfile"

    },

    highlightTracker : function( ev ){

        $(ev.target).addClass('chosen-tracker')

    },

    showProfile : function( ev ){

        $('#heading').fadeIn()
        window.location.hash = 'profile'

    }

})