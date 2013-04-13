var app = app || {};

app.WhatView = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/what.handlebars', function(tmpl){
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
        this.$el.html( template( { "adjectives" : adjectives } ) )

        $('#adjective_container').isotope({
            layoutMode: 'masonryHorizontal',
            masonryHorizontal: {
                rowHeight: 40
            },
            resizesContainer: false,
            gutterWidth: 20
        })

        $('#instructions').removeClass('hidden-top')

        $('.nav-adjective').each(function(){
            var selector = '#' + $(this).html()
            $(selector).parent().addClass('chosen-adj')
        })

    },

    events : {

        "click .adjective" : "toggleAdjective"

    },

    toggleAdjective : function( ev ){

        if ( $('.chosen-adj').length < 3 ){

            $(ev.target).parent().hasClass('chosen-adj') ? $(ev.target).parent().removeClass('chosen-adj') :
                                                              $(ev.target).parent().addClass('chosen-adj')

            var selector = $(ev.target).html()

        } else {

            $(ev.target).parent().removeClass('chosen-adj')

        }

    }

})