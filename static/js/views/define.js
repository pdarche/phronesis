var app = app || {};

app.DefineView = Backbone.View.extend({
    state : 0,
    priorities : [  
        [ "firstPriority", "firstPriorityActiveSpecific" ],
        [ "secondPriority", "secondPriorityActiveSpecific" ],
        [ "thirdPriority", "thirdPriorityActiveSpecific" ]
    ],

    initialize : function() {

        var username = $('#phro_username').html()
        // username === "" ? window.location = 'http://localhost:8000' : null
        console.log("username is", username)

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/defineView.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
                self.transitionIn()
            })

        } else {

            self.render()

        }

    },

    render : function() {

        var source = $(this.template).html()
        var template = Handlebars.compile( source );
        this.$el.html( template( { "adjectives" : adjectives } ) )

        $('#adjective_container').isotope({
            // itemSelector : '.adjective-wrap',
            layoutMode: 'masonryHorizontal',
            masonryHorizontal: {
                rowHeight: 40
            },
            resizesContainer: false,
            gutterWidth: 20
        })

    },

    transitionIn : function(){

        $('#instructions').removeClass('hidden-top')
        $('.adjective-wrap').removeClass('hidden-left')
        $('.top-adj').removeClass('hidden-left')

    },

    events : {

        "click .adjective-wrap" : "toggleAdjective",
        "click .adjective-attribute" : "toggleSpecifics",
        "mouseover .adjective-attribute" : "addAccent",
        "mouseout .adjective-attribute" : "removeAccent"

    },

    toggleAdjective : function(ev){
        var self = this,
            traitName = $(ev.target).html(),
            accentClass = $(ev.target).html() + '-accent'

        if ( $(ev.target).parent().hasClass('chosen-adj') ){
        
            $(ev.target).parent().removeClass('chosen-adj')
        
        } else {

            if ( user.get('traits').get('firstPriority') === undefined ){

                user.get('traits').set({ firstPriority : new Trait({ name : traitName }) })                
                user.get('traits').get('firstPriority').get('traitSpecifics').fetch().then(
                    function(){
                        _.each( user.get('traits').get('firstPriority').get('traitSpecifics').models, function( model ){
                            model.get('recommendedBehaviors').fetch().then(
                                function(){
                                    _.each( model.get('recommendedBehaviors').models, function( subModel ){
                                        console.log("the subModel is", subModel)
                                    })
                                }
                            )
                        })
                    }
                )     

            } else if ( user.get('traits').get('secondPriority') === undefined ){

                user.get('traits').set({ secondPriority : new Trait({ name : traitName }) })
                user.get('traits').get('secondPriority').get('traitSpecifics').fetch()

            } else if ( user.get('traits').get('thirdPriority') === undefined ){

                user.get('traits').set({ thirdPriority : new Trait({ name : traitName }) })
                user.get('traits').get('thirdPriority').get('traitSpecifics').fetch()       

            }

            $(ev.target).parent().addClass('chosen-adj').children().addClass(accentClass);

        }

        if ( $('.chosen-adj').length === 3 ){

            $('#adjective_specifics').fadeIn()

            $('#adjective_container').isotope({
                    layoutMode : 'straightDown',
                    filter : '.chosen-adj',
                    columnWidth : 240,
                    gutterWidth : 20
                })

            $('.chosen-adj').each(function(i){
                var newClass = 'chosen-adj-' + i 
                $(this).addClass(newClass)
            })

            self.expandChosen()
        
        }

    },

    expandChosen : function(){

        this.$el.undelegate('.adjective-wrap', 'click')
        $('.adjective-wrap').not('.chosen-adj').remove()
        $('#instructions p').html("These are <span id='three'>big</span> categories. More <span>precisely...</span>")
        //unbind adjective choice
        this.toggleSpecifics()

    },

    toggleSpecifics : function( ev ){

        var self = this,
            activeAdj = '.chosen-adj-'+ this.state,
            adjName = $(activeAdj).find('div').html(),
            collection = undefined
            priority = this.priorities[this.state]
            
        $('.inactive').parent().removeClass('no-shadow')
        $('.inactive').removeClass('inactive')
        $('.chosen-adj').not(activeAdj).addClass('no-shadow')
        $('.chosen-adj').not(activeAdj).find('.adjective').addClass('inactive')

        if ( ev !== undefined ){
            var newPriorityName = this.priorities[this.state-1][1]
            var traitSpecific = $(ev.target).attr('id')
            var newPriority = {}
            newPriority[newPriorityName] = traitSpecific
            user.get('traits').set(newPriority)

            // set new trait specific priority
            // fetch models for that trait specific
        }

        if (this.state !== 3) {

            collection = user.get('traits').get(priority[0]).get('traitSpecifics')            

            var specific = new app.AdjectiveSpecifics({ 
                el : $('#adjective_specifics'),
                collection : collection
            })

        }

        this.state++

        if (this.state === 4){
            setTimeout( self.showTrackers, 500)
        }

    },

    addAccent : function( ev ){

        var accentClass = $('.adjective').not('.inactive').attr('class').split(" ")[1]
        $(ev.target).addClass(accentClass).css({"padding-left" : "40px"})

        $('#attribute_details').empty()
        $.when( $.get('/static/js/templates/tempCVDinfo.handlebars') )
         .done( function(data){
            var source = $(data).html()
            var template = Handlebars.compile( source );
            $('#attribute_details').append(template)
         })

    },

    removeAccent : function( ev ){
        
        // console.log(ev.target)
        var toRemoveClass = $(ev.target).attr('class').split(" ")[1]
        $('.adjective-attribute').removeClass(toRemoveClass).css({"padding-left" : "10px"})

    },

    showGrid : function(){
        $('#heading').fadeIn()
        window.location.hash = 'grid'
    },

    showProfile : function(){
        $('#heading').fadeIn()
        window.location.hash = 'profile'
    },

    showTrackers : function(){
        window.location.hash = 'addTrackers'
    }

})