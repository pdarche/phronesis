var app = app || {};

app.WhatView = Backbone.View.extend({

    index : undefined,

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

        var source = $(this.template).html();
        var template = Handlebars.compile( source );
        this.$el.html( template( { "adjectives" : adjectives } ) );

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
            var selector = '#' + $(this).html(),
                accentClass = $(this).html() + "-accent"
            $(selector).parent().addClass('chosen-adj').children().addClass(accentClass)
        })

    },

    events : {

        "click .adjective" : "toggleAdjective"

    },

    toggleAdjective : function( ev ){

        var self = this

        if ( $('.chosen-adj').length < 3 ){
            
            console.log("fewer than three")

            if ( $(ev.target).parent().hasClass('chosen-adj') ){

                $(ev.target).parent().removeClass('chosen-adj')
                var adj = $(ev.target).html(),
                    selector = '.' + adj,
                    accentClass = adj + " " + "-accent",
                    newPriority = {}
                
                self.index = $(selector).index()
                newPriority[priorities[self.index]] = undefined
                user.get('adjectives').set(newPriority)
                               

            } else {

                $(ev.target).parent().addClass('chosen-adj')
                var adj = $(ev.target).html(),
                    selector = '.' + adj,
                    newPriority = {}

                self.index = $(selector).index()
                newPriority[priorities[self.index]] = adj
                user.get('adjectives').set( newPriority )

            }

        } else {
                console.log("three or more")
                
                $(ev.target).parent().removeClass('chosen-adj')
                var adj = $(ev.target).html(),
                    selector = '.' + adj,
                    newPriority = {}
                
                self.index = $(selector).index()
                newPriority[priorities[self.index]] = undefined
                user.get('adjectives').set(newPriority)

        }

    }

})