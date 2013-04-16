var app = app || {};

app.HowView = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/how.handlebars', function(tmpl){
                self.template = tmpl
                self.render()

                var activeAdj = $('#adjective_1').html(),
                    actions = new app.ActionsView({ 
                        el : $('#action_list'),
                        model : adj[activeAdj]
                    })
                $('#action_container, .how-rect, .action-wrap').css('opacity', 1)
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

        "click .action" : "toggleAction"

    },

    toggleAdjective : function( ev ){

        console.log("being clicked")
        var selectedAdj = $('active-adj').html()
        console.log(selectedAdj)

    },

    toggleAction : function(){

        console.log("clicking action")

    }

})