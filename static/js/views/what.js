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
            var selector = '#' + $(this).html()
            $(selector).parent().addClass('chosen-adj')
        })

    },

    events : {

        "click .adjective" : "toggleAdjective"

    },

    toggleAdjective : function( ev ){

        var self = this

        if ( $('.chosen-adj').length < 3 ){

            if ( $(ev.target).parent().hasClass('chosen-adj') ){

                $(ev.target).parent().removeClass('chosen-adj')
                var adj = $(ev.target).html(),
                    selector = '.' + adj

                self.index = $(selector).index()
                console.log("the index is", self.index)
                $(selector).html("")
                $(selector).removeClass(adj)                

            } else {

                $(ev.target).parent().addClass('chosen-adj')
                var adj = $(ev.target).html(),
                    selector = '.' + adj

                console.log(self.index)
                $('.nav-adjective').eq(self.index).addClass(adj)
                $('.nav-adjective').eq(self.index).html(adj)
                self.index++

            }

        } else {

                $(ev.target).parent().removeClass('chosen-adj')
                var adj = $(ev.target).html(),
                    selector = '.' + adj

                self.index = $(selector).index()
                console.log("the index is", self.index)
                $(selector).html("")
                $(selector).removeClass(adj)

        }

    }

})