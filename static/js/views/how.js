var app = app || {};

app.HowView = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/how.handlebars', function(tmpl){
                self.template = tmpl
                self.render()

                var activeAdj = $('#adjective_1').html()
                
                var actions = new app.ActionsView({ 
                        el : $('#action_list'),
                        model : adj[activeAdj]
                    })

                var currentStatus = new app.CurrentStatusView({ 
                        el : $('#current_status_content')
                    })

                var triggers = new app.TriggersView({ 
                        el : $('#triggers_content')
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

    },

    toggleTriggers : function(){

        console.log("toggling")

        $('.col-2').hasClass('grid-6') ? $('.col-2').removeClass('grid-6').addClass('grid-3') :
                                        $('.col-2').addClass('grid-6').removeClass('grid-3')


        $('.col-3').hasClass('grid-3') ? $('.col-3').removeClass('grid-3').addClass('grid-6') :
                                        $('.col-3').addClass('grid-3').removeClass('grid-6')                                        

    }

})