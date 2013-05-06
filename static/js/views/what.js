var app = app || {};

app.WhatView = Backbone.View.extend({

    index : undefined,
    highlighedtTrait : undefined,

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

        "click .adjective" : "toggleAdjective",
        "mouseover .chosen-adj" : "showSpecifics",
        "click #adjective_container" : "removeSpecifics",
        "mouseover .trait-specific" : "highlightTrait",
        "mouseout .trait-specific" : "removeHighlight",
        "click .trait-specific" : "toggleTraitSpecific"
        // "mouseout .chosen-adj" : "removeSpecifics"

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

    },

    showSpecifics : function( ev ){

        var self = this
        var traits = user.get('traits').toJSON(),
            traitName = $(ev.target).attr('id'),
            specifics

        for ( key in traits ){
            if ( traits[key].attributes !== undefined ){
                traits[key].get('name') === traitName ? specifics = traits[key].get('traitSpecifics') : null
            }
        }

        if ( !($.isFunction(this.specificsTemplate)) ){

            $.get('/static/js/templates/traitSpecificsPopup.handlebars', function(tmpl){
                self.specificsTemplate = tmpl
                self.renderSpecifics( tmpl, specifics, ev.target )
            })

        } else {

            console.log("gots the template")

        }

        this.highlighedtTrait = traitName

    },

    renderSpecifics : function( tmpl, specifics, el ){

        var top = $(el).parent().position().top,
            left = $(el).parent().position().left,
            offset = $(el).parent().width(),
            data = []

        _.each(specifics.models, function(model){
            var heading = model.get('as_heading'),
                trait_specific = model.get('trait_specific'),
                datum = { heading : heading, trait_specific : trait_specific }

            data.push(datum)
        })

        console.log("the outgoing data are", data)

        var source = $(tmpl).html();
        var template = Handlebars.compile( source )

        if ( $('#trait_specifics_container').length === 0 ){
            $('#adjective_container').append( template( { "specifics" : data } ) );
            
            if ( left < 500){ 
                $('#trait_specifics_container').css({ position: 'absolute', top : top, left : (left + offset + 20) })
            } else {
                $('#trait_specifics_container').css({ position: 'absolute', top : top, left : (left - 380) })
            }
        }

    },

    removeSpecifics : function( ev ){
        
        $('#trait_specifics_container').remove()

    },

    highlightTrait : function( ev ){

        console.log("the highlighted trait is", this.highlighedtTrait)

        var accentClass = this.highlighedtTrait + "-accent"
        $(ev.target).addClass(accentClass)

    },

    highlightTrait : function( ev ){

        var accentClass = this.highlighedtTrait + "-accent"
        $(ev.target).removeClass(accentClass)

    },

    toggleTraitSpecific : function( ev ) {

        console.log("the event id is", ev.target)

    }

})