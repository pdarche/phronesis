var app = app || {};

app.WhatView = Backbone.View.extend({

    index : undefined,
    highlighedtTrait : undefined,
    cachedTranslate : undefined,
    priorityList : [ "firstPriority", "secondPriority", "thirdPriority" ],
    activeTraitName : undefined,
    activeTraitSpecifics : undefined,
    activeSpecificName : undefined,

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

        $('.nav-adjective').each(function(i){
            var selector = '#' + $(this).html(),
                accentClass = $(this).html() + "-accent",
                priorityClass = "priority-" + (i + 1) 

            $(selector).parent().addClass('chosen-adj').children().addClass(accentClass + ' ' + priorityClass)
        })

    },

    events : {

        "click .adjective" : "toggleAdjective",
        "click #adjective_container" : "removeSpecifics",
        "mouseover .adjective-wrap, .more-info" : "showInfo",
        "mouseout .more-info" : "hideInfo",
        "click .more-info" : "expandTrait",
        "dblclick .adjective-wrap" : "contractTrait",
        "click .expanded-trait-specific" : "toggleExpandedTraitSpecificInfo"

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

    showInfo : function( ev ){

        var target = $(ev.target),
            more = target.next(),
            expanded = $('.expanded-trait')

        expanded.length === 0 ? more.css({ display : "block" }) : null
        
    },

    hideInfo : function( ev ){
        
        console.log("hiding")
        $('.more-info').css({ display : "none"})

    },

    expandTrait : function( ev ){    

        var target = $(ev.target).prev(),
            targetParent = target.parent(),
            targetClass = target.attr('class'),
            traitName = target.html(),
            activeSpecificNameSelector,
            activeSpecificAccent = traitName + '-specific-accent',
            more = target.next()

        if ( targetParent.hasClass('chosen-adj') && 
            !(targetParent.hasClass('expanded-trait'))) {

            $('#instructions, .more-info').hide()
            $('#adjective_container, .expanded-trait').css({ "height" : '100%' })
            console.log("this goddam thing should be 100%")
            $('.expanded-trait').css({ "background-color" : "#eee", "height" : '100%' })

            this.activeTraitName = traitName
            this.activeTraitSpecifics = this.returnTraitObject( targetClass )[0]
            this.activeSpecificName = this.returnTraitObject( targetClass )[1]
            activeSpecificNameSelector = '#' + user.get('traits').get(this.activeSpecificName)
            this.cachedTranslate = targetParent.css('-webkit-transform')
            $('.adjective-wrap').not(targetParent).hide()
            targetParent.addClass('expanded-trait')
                        .css({ '-webkit-transform' : 'translate3d(0px,0px,0px)'})

            this.addTraitSpecifics( activeSpecificNameSelector, activeSpecificAccent )    

        }

    },

    contractTrait : function(){

        var expandedTrait = $('.expanded-trait')
        
        $('#adjective_container').css({ height : '400px' })
        $('#instructions').show()
        
        expandedTrait.removeClass('expanded-trait')
                     .css({"-webkit-transform" : this.cachedTranslate})
        
        $('.adjective-wrap').fadeIn()

    },

    addTraitSpecifics : function( activeSpecificNameSelector, activeSpecificAccent ){

        var self = this
        $.when( $.get('/static/js/templates/defineTraitSpecifics.handlebars') )
         .done( function(tmpl) {
            self.renderTraitSpecifics( tmpl, self )
            $(activeSpecificNameSelector).addClass(activeSpecificAccent)
            // $('.expanded-trait').css({ height : '1'})
         })

    },

    renderTraitSpecifics : function( tmpl, self ){

        var source = $(tmpl).html(),
            template = Handlebars.compile( source ),
            specifics = _.zip( self.activeTraitSpecifics.get('traitSpecifics').pluck('as_heading'), 
                               self.activeTraitSpecifics.get('traitSpecifics').pluck('trait_specific'))
            $('.expanded-trait').append( template( { "specifics" : specifics } ) )
            self.addTraitSpecificInfo( self )
    },

    addTraitSpecificInfo : function( self ){

        $.when( $.get('/static/js/templates/tempCVDInfo.handlebars') )
         .done( function(tmpl){
            self.renderTraitSpcificInfo( tmpl )
         })

    },

    renderTraitSpcificInfo : function( tmpl ){

        var source = $(tmpl).html(),
            template = Handlebars.compile( source )
        
        $('#trait_specific_info_conatiner').append( template )

    },

    returnTraitObject : function( targetClass ){

        var classes = targetClass.split(" "),
            priorityClass = classes[classes.length - 1],
            priorityIndex = Number(priorityClass.split("-")[1]) - 1,
            priorityString = this.priorityList[priorityIndex],
            prioritySpecificString = priorityString + 'ActiveSpecific',
            priorityObject = user.get('traits').get(priorityString)

        return [ priorityObject, prioritySpecificString ]
    },

    highlightTrait : function( ev ){

        console.log("the highlighted trait is", this.highlighedtTrait)

        var accentClass = this.highlighedtTrait + "-accent"
        $(ev.target).addClass(accentClass)

    },

    toggleTraitSpecific : function( ev ) {

        console.log("the event id is", ev.target)

    },

    toggleExpandedTraitSpecificInfo : function( ev ){
        var activeTraitSpecificAccent = this.activeTraitName + '-specific-accent',
            activeTraitSepcificAccentSelector = '.' + activeTraitSpecificAccent
        
        console.log("attempting to toggle", activeTraitSepcificAccentSelector)
        $(activeTraitSepcificAccentSelector).removeClass(activeTraitSpecificAccent)
        $(ev.target).addClass(activeTraitSpecificAccent)

        $('#trait_specific_info_conatiner').empty()


    }

})