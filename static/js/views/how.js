var app = app || {};

app.HowView = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/how.handlebars', function(tmpl){
                self.template = tmpl
                self.render()

                var activeAdj = $('#adjective_1').html(),
                    activeSpecific = user.get('traits').get('firstPriorityActiveSpecific'),
                    activeHabitKey = $('.chosen-action').attr('id'),
                    activeSpecificCollection,
                    activeHabitCollection

                _.each( user.get('traits').get('firstPriority').get('traitSpecifics').models, function( model ){
                    model.attributes.trait_specific === activeSpecific ? activeSpecificCollection = model : null
                    _.each( model.get('recommendedBehaviors').models, function( recHabit ){
                        recHabit.attributes.rec_habit_key === "vaff" ? activeHabitCollection = recHabit : null
                    })
                })

                console.log("active specific model is", activeHabitCollection)

                var actions = new app.ActionsView({ 
                        el : $('#action_list'),
                        collection : activeSpecificCollection
                    })

                var currentStatus = new app.CurrentStatusView({ 
                        el : $('#current_status_content'),
                        model : activeHabitCollection.get('currentStatus')
                    })

                var triggers = new app.TriggersView({ 
                        el : $('#triggers_content')
                    })

                var actions = new app.ActionsToTakeView({
                        el : $('#actions_content'),
                        model : activeHabitCollection.get('actions')
                })

                $('#action_container, .how-rect, .action-wrap').css('opacity', 1)
                //this should change with global heading
                $('#adjective_1').addClass('active-adj')
                 
            })

        } else {

            console.log("gots the template")

        }

    },

    render : function() {

        var source = $(this.template).html();
        var template = Handlebars.compile( source );
        this.$el.html( template );

    },

    events : {

        "click .action" : "toggleAction",
        "click #triggers_heading" : "toggleTriggers"

    },

    toggleAdjective : function( ev ){
        
        var selectedAdj = $('active-adj').html()
        console.log(selectedAdj)

    },

    toggleAction : function( ev ){

        var accentClass = $('.active-adj').html() + "-accent"
        $('.chosen-action').removeClass(accentClass).removeClass('chosen-action')
        $(ev.target).addClass(accentClass + ' chosen-action')

        var recHabitKey = $(ev.target).attr('id'),
            activeHabitCollection

        _.each( user.get('traits').get('firstPriority').get('traitSpecifics').models, function( model ){
            _.each( model.get('recommendedBehaviors').models, function( recHabit ){
                recHabit.attributes.rec_habit_key === recHabitKey ? activeHabitCollection = recHabit : null
            })
        })

        var currentStatus = new app.CurrentStatusView({ 
            el : $('#current_status_content'),
            model : activeHabitCollection.get('currentStatus')
        })

        var triggers = new app.TriggersView({ 
            el : $('#triggers_content')
        })

        var actions = new app.ActionsToTakeView({
                el : $('#actions_content'),
                model : activeHabitCollection.get('actions')
        })        

    },

    toggleTriggers : function(){

        if ( $('.col-2').hasClass('grid-6') ){

            $('.col-2').removeClass('grid-6').addClass('grid-3')
            $('.col-3').removeClass('grid-3').addClass('grid-6')
            $('svg').hide() 
            $('#count_container').css('width', '265px')

        } else {

            $('.col-2').addClass('grid-6').removeClass('grid-3')
            $('.col-3').addClass('grid-3').removeClass('grid-6')
            $('svg').fadeIn()
            $('#count_container').css('width', '30%')

        }

                                              

    }

})